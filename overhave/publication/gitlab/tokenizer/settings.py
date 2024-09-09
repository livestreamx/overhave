import httpx
from pydantic import ValidationInfo, field_validator
from pydantic_settings import SettingsConfigDict

from overhave.base_settings import OVERHAVE_ENV_PREFIX
from overhave.transport.http import BaseHttpClientSettings
from overhave.utils import make_url


class TokenizerClientSettings(BaseHttpClientSettings):
    """Important environments and settings for :class:`TokenizerClient`."""

    model_config = SettingsConfigDict(env_prefix=OVERHAVE_ENV_PREFIX + "GITLAB_TOKENIZER_")

    enabled: bool = False
    url: httpx.URL | None = None  # type: ignore
    initiator: str = "Overhave"
    remote_key: str | None = None
    remote_key_name: str | None = None

    @field_validator("url", mode="before")
    def make_url(cls, v: str | None) -> httpx.URL | None:
        return make_url(v)

    @field_validator("url", "remote_key", "remote_key_name", mode="after")
    def validate_remote_key_and_initiator(cls, v: str | None, values: ValidationInfo) -> str | None:
        if values.data.get("enabled") and not isinstance(v, str):
            raise ValueError("Please verify that url, remote_key and remote_key_name variables are not nullable!")
        return v
