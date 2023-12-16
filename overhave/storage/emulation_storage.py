import abc
import logging
import pickle
import socket
from typing import cast

import sqlalchemy as sa

from overhave import db
from overhave.entities.settings import OverhaveEmulationSettings
from overhave.storage import EmulationRunModel
from overhave.transport.redis.deps import make_redis, get_redis_settings
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


class EmulationStorage(IEmulationStorage):
    """Class for emulation runs storage."""

    def __init__(self, settings: OverhaveEmulationSettings):
        self._redis = redis = make_redis(get_redis_settings())
        self._redis.set('allocated_ports', pickle.dumps([]))
        self._settings = settings
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
            if self._is_port_in_use(cast(int, port)):
                continue
            return cast(int, port)
        raise AllPortsAreBusyError("All ports are busy - could not find free port!")

    def get_allocated_ports(self):
        return pickle.loads(self._redis.get('allocated_ports'))

    def allocate_port(self, port):
        new_allocated_ports = self.get_allocated_ports()
        new_allocated_ports.append(port)
        self._redis.set('allocated_ports', pickle.dumps(sorted(new_allocated_ports)))

    def _is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self._settings.emulation_bind_ip, port)) == 0

    def get_requested_emulation_run(self, emulation_run_id: int) -> EmulationRunModel:
        with db.create_session() as session:
            emulation_run = session.query(db.EmulationRun).filter(db.EmulationRun.id == emulation_run_id).one()
            emulation_run.status = db.EmulationStatus.REQUESTED
            emulation_run.port = self._get_next_port()
            self.allocate_port(emulation_run.port)
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
