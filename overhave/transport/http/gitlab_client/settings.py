from overhave.transport.http import BaseHttpClientSettings
from overhave.transport.http.gitlab_client.objects import TokenType


class OverhaveGitlabClientSettings(BaseHttpClientSettings):
    """Settings for :class:`GitlabHttpClient`."""

    auth_token: str | None = None
    token_type: TokenType = TokenType.OAUTH

    class Config:
        env_prefix = "OVERHAVE_GITLAB_"
