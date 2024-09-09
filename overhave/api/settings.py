from datetime import timedelta

from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from overhave.base_settings import OVERHAVE_ENV_PREFIX


class OverhaveUvicornApiSettings(BaseSettings):
    """Settings for Overhave API server, started with Uvicorn."""

    model_config = SettingsConfigDict(env_prefix=OVERHAVE_ENV_PREFIX + "UVICORN_")

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1


class OverhaveApiAuthSettings(BaseSettings):
    """Settings for Overhave API service auth_managers."""

    model_config = SettingsConfigDict(env_prefix=OVERHAVE_ENV_PREFIX + "API_AUTH_")

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def access_token_expire_timedelta(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)
