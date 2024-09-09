from pydantic_settings import SettingsConfigDict

from overhave.transport.http import BaseHttpClientSettings
from overhave.transport.http.gitlab_client.objects import TokenType


class OverhaveGitlabClientSettings(BaseHttpClientSettings):
    """Settings for :class:`GitlabHttpClient`."""

    model_config = SettingsConfigDict(env_prefix="OVERHAVE_GITLAB_")

    auth_token: str | None = None
    token_type: TokenType = TokenType.OAUTH
