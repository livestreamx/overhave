from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OverhaveS3ManagerSettings(BaseSettings):
    """Settings for S3Client."""

    model_config = SettingsConfigDict(env_prefix="OVERHAVE_S3_")

    enabled: bool = False

    url: str | None = Field(default=None)
    region_name: str | None = Field(default=None)
    access_key: str | None = Field(default=None)
    secret_key: str | None = Field(default=None)
    verify: bool = True

    autocreate_buckets: bool = False

    @model_validator(mode="before")
    def validate_enabling(cls, values: dict[str, Any]) -> dict[str, Any]:
        enabled = values.get("enabled")
        if enabled and not all(
            (
                isinstance(values.get("url"), str),
                isinstance(values.get("access_key"), str),
                isinstance(values.get("secret_key"), str),
            )
        ):
            raise ValueError("Url, access key and secret key should be specified!")
        return values
