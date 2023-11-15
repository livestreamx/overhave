import enum
import logging
import socket
from logging.config import DictConfigurator
from typing import Any

import sqlalchemy as sa
import sqlalchemy.exc
from pydantic import field_validator
from pydantic_settings import BaseSettings
from sqlalchemy.pool import Pool, SingletonThreadPool

OVERHAVE_ENV_PREFIX = "OVERHAVE_"


class BaseOverhavePrefix(BaseSettings):
    """Possibility to change Overhave default settings from environment."""

    class Config:
        env_prefix = OVERHAVE_ENV_PREFIX


def _as_alchemy_url(db_url: str) -> sa.URL:
    try:
        return sa.make_url(db_url)
    except sqlalchemy.exc.ArgumentError as e:
        raise ValueError from e


class DataBaseSettings(BaseOverhavePrefix):
    """Overhave database settings."""

    db_url: str = "postgresql://postgres:postgres@localhost/overhave"
    db_pool_recycle: int = 500
    db_pool_size: int = 6
    db_echo: bool = False
    db_application_name: str = socket.gethostname()
    db_connect_timeout: int = 30
    db_poolclass: type[Pool] = SingletonThreadPool

    def _create_engine(self) -> sa.Engine:
        return sa.engine_from_config(
            {
                "url": _as_alchemy_url(self.db_url),
                "pool_recycle": self.db_pool_recycle,
                "pool_pre_ping": True,
                "pool_size": self.db_pool_size,
                "poolclass": self.db_poolclass,
                "connect_args": {
                    "connect_timeout": self.db_connect_timeout,
                    "application_name": self.db_application_name,
                },
            },
            prefix="",
        )

    def setup_engine(self) -> None:
        from overhave.db.base import current_session, metadata

        metadata.set_engine(engine=self._create_engine())
        current_session.configure(bind=metadata.engine)


class LoggingSettings(BaseOverhavePrefix):
    """Overhave logging settings."""

    log_level: str = logging.getLevelName(logging.INFO)
    log_config: dict[str, Any] = {}

    @field_validator("log_config", check_fields=True)
    def dict_config_validator(cls, v: dict[str, Any]) -> DictConfigurator | None:
        if not v:
            return None
        return DictConfigurator(v)

    def setup_logging(self) -> None:
        if isinstance(self.log_config, DictConfigurator):
            self.log_config.configure()
        else:
            logging.basicConfig(level=self.log_level)


class AuthorizationStrategy(enum.StrEnum):
    """
    Authorization strategies Enum.

    Simple - strategy without real auth_managers. Each user could use preferred name. This name will be used for user
    authority. Each user is unique. Password not required.
    Default - strategy with real auth_managers. Each user could use only registered credentials.
    LDAP - strategy with auth_managers using remote LDAP server. Each user should use his LDAP credentials. LDAP
    server returns user groups. If user in default 'admin' group or his groups list contains admin group - user
    will be authorized. If user already placed in database - user will be authorized too. No one password stores.
    """

    SIMPLE = "simple"
    DEFAULT = "default"
    LDAP = "ldap"


class OverhaveAuthorizationSettings(BaseOverhavePrefix):
    """Settings for Overhave auth_managers in components interface.

    Supports 3 strategies: SIMPLE, DEFAULT and LDAP.
    LDAP auth_managers uses group politics with administration group `admin_group`.
    SIMPLE and DEFAULT strategies use admin user that would be dynamically created at startup.
    """

    auth_strategy: AuthorizationStrategy = AuthorizationStrategy.SIMPLE
