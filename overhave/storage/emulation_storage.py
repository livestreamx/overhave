import abc
import logging
import socket
from typing import List, cast

import orjson
import sqlalchemy as sa
from redis import Redis

from overhave import db
from overhave.entities.settings import OverhaveEmulationSettings
from overhave.storage import EmulationRunModel
from overhave.utils import get_current_time

logger = logging.getLogger(__name__)


class EmulationStorageError(Exception):
    """Base Exception for :class:`EmulationStorage`."""


class AllPortsAreBusyError(EmulationStorageError):
    """Exception for situation when all ports are busy."""


class IEmulationStorage(abc.ABC):
    """Abstract class for emulation runs storage."""

    @staticmethod
    @abc.abstractmethod
    def create_emulation_run(emulation_id: int, initiated_by: str) -> int:
        pass

    @abc.abstractmethod
    def get_requested_emulation_run(self, emulation_run_id: int) -> EmulationRunModel:
        pass

    @abc.abstractmethod
    def set_emulation_run_status(self, emulation_run_id: int, status: db.EmulationStatus) -> None:
        pass

    @abc.abstractmethod
    def set_error_emulation_run(self, emulation_run_id: int, traceback: str) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_emulation_runs_by_test_user_id(test_user_id: int) -> list[EmulationRunModel]:
        pass

    @abc.abstractmethod
    def has_running_emulation_with_user(self, test_user_id: int) -> bool:
        pass


class EmulationStorage(IEmulationStorage):
    """Class for emulation runs storage."""

    def __init__(self, settings: OverhaveEmulationSettings, redis: Redis):
        self._redis = redis
        self._settings = settings
        self._redis.set(self._settings.redis_ports_key, orjson.dumps([]))
        self._emulation_ports_len = len(self._settings.emulation_ports)

    @staticmethod
    def create_emulation_run(emulation_id: int, initiated_by: str) -> int:
        with db.create_session() as session:
            emulation_run = db.EmulationRun(
                emulation_id=emulation_id, initiated_by=initiated_by, status=db.EmulationStatus.CREATED
            )
            session.add(emulation_run)
            session.flush()
            return emulation_run.id

    def _get_next_port(self) -> int:
        allocated_ports = self.get_allocated_ports()

        logger.debug("Allocated ports: %s", allocated_ports)
        not_allocated_ports = set(self._settings.emulation_ports).difference(allocated_ports)
        logger.debug("Not allocated ports: %s", not_allocated_ports)
        if not_allocated_ports:
            for port in not_allocated_ports:
                if self._is_port_in_use(port):
                    continue
                return port
            logger.debug("All not allocated ports are busy!")
        for port in allocated_ports:
            if self._is_port_in_use(port):
                continue
            return port
        raise AllPortsAreBusyError("All ports are busy - could not find free port!")

    def get_allocated_ports(self) -> List[int]:
        port_user_pairs = self.get_allocated_port_user_pairs()
        return [port for port, _ in port_user_pairs]

    def get_allocated_port_user_pairs(self) -> List[List[int]]:
        allocated_port_user_pairs = cast(bytes | None, self._redis.get(self._settings.redis_ports_key))
        logger.debug("allocated port user pairs: %s", allocated_port_user_pairs)
        if allocated_port_user_pairs is None:
            return []
        return cast(List[List[int]], orjson.loads(allocated_port_user_pairs))

    def allocate_port_for_user(self, port: int, test_user_id: int) -> None:
        new_allocated_ports = self.get_allocated_port_user_pairs()
        if [port, test_user_id] in new_allocated_ports:
            logger.debug("port %s for user %s already in redis: %s", port, test_user_id, new_allocated_ports)
            return
        new_allocated_ports.append([port, test_user_id])
        logger.debug("added port %s for user %s in redis: %s", port, test_user_id, new_allocated_ports)
        self._redis.set(self._settings.redis_ports_key, orjson.dumps(sorted(new_allocated_ports)))

    def _is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self._settings.emulation_bind_ip, port)) == 0

    def get_requested_emulation_run(self, emulation_run_id: int) -> EmulationRunModel:
        with db.create_session() as session:
            emulation_run = session.query(db.EmulationRun).filter(db.EmulationRun.id == emulation_run_id).one()
            emulation_run.status = db.EmulationStatus.REQUESTED
            emulation_run.port = self._get_next_port()
            self.allocate_port_for_user(emulation_run.port, emulation_run.emulation.test_user_id)
            emulation_run.changed_at = get_current_time()
            return EmulationRunModel.model_validate(emulation_run)

    def set_emulation_run_status(self, emulation_run_id: int, status: db.EmulationStatus) -> None:
        with db.create_session() as session:
            session.execute(
                sa.update(db.EmulationRun)
                .where(db.EmulationRun.id == emulation_run_id)
                .values(status=status, changed_at=get_current_time())
            )

    def set_error_emulation_run(self, emulation_run_id: int, traceback: str) -> None:
        with db.create_session() as session:
            session.execute(
                sa.update(db.EmulationRun)
                .where(db.EmulationRun.id == emulation_run_id)
                .values(status=db.EmulationStatus.ERROR, changed_at=get_current_time(), traceback=traceback)
            )

    @staticmethod
    def get_emulation_runs_by_test_user_id(test_user_id: int) -> list[EmulationRunModel]:
        with db.create_session() as session:
            emulation_ids_query = (
                session.query(db.Emulation)
                .with_entities(db.Emulation.id)
                .filter(db.Emulation.test_user_id == test_user_id)
                .scalar_subquery()
            )
            emulation_runs = (
                session.query(db.EmulationRun).where(db.EmulationRun.emulation_id.in_(emulation_ids_query)).all()
            )
            return [EmulationRunModel.model_validate(x) for x in emulation_runs]

    def has_running_emulation_with_user(self, test_user_id: int) -> bool:
        port_user_pairs = self.get_allocated_port_user_pairs()

        for port, user in port_user_pairs:
            if user == test_user_id and self._is_port_in_use(port):
                return True
        return False
