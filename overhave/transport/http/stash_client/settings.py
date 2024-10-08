import httpx
from pydantic_settings import SettingsConfigDict

from overhave.transport.http.base_client import BaseHttpClientSettings


class OverhaveStashClientSettings(BaseHttpClientSettings):
    """Settings for :class:`StashHttpClient`."""

    model_config = SettingsConfigDict(env_prefix="OVERHAVE_STASH_")

    pr_path: str = "rest/api/1.0/projects/{project_key}/repos/{repository_name}/pull-requests"
    auth_token: str

    def get_pr_url(self, project_key: str, repository_name: str) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.pr_path.format(project_key=project_key, repository_name=repository_name)}")
