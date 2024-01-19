import httpx
from pydantic import StrictStr

from overhave.base_settings import OVERHAVE_ENV_PREFIX
from overhave.transport.http.base_client import BaseHttpClientSettings


class OverhaveApiAuthenticatorSettings(BaseHttpClientSettings):
    """Settings for :class:`OverhaveApiAuthenticator`."""

    auth_token_path: str = "token"

    class Config:
        env_prefix = OVERHAVE_ENV_PREFIX + "API_AUTH_"

    @property
    def get_auth_token_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.auth_token_path}")


class OverhaveApiClientSettings(BaseHttpClientSettings):
    """Settings for :class:`OverhaveApiClient`."""

    auth_token: str
    feature_path: StrictStr = StrictStr("feature/")
    feature_tags_item_path: StrictStr = StrictStr("feature/tags/item")
    feature_tags_list_path: StrictStr = StrictStr("feature/tags/list")
    feature_types_list_path: StrictStr = StrictStr("feature/types/list")

    test_run_path: StrictStr = StrictStr("test_run")
    test_run_create_path: StrictStr = StrictStr("test_run/create/")

    emulation_run_list_path: StrictStr = StrictStr("emulation/run/list")

    test_user_path: StrictStr = StrictStr("test_user/")
    test_user_list_path: StrictStr = StrictStr("test_user/list")

    @property
    def get_feature_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.feature_path}")

    @property
    def get_feature_tags_item_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.feature_tags_item_path}")

    @property
    def get_feature_tags_list_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.feature_tags_list_path}")

    @property
    def get_feature_types_list_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.feature_types_list_path}")

    @property
    def get_test_run_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.test_run_path}")

    @property
    def get_test_run_create_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.test_run_create_path}")

    @property
    def get_emulation_run_list_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.emulation_run_list_path}")

    @property
    def get_test_user_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.test_user_path}")

    @property
    def get_test_user_list_url(self) -> httpx.URL:
        return httpx.URL(f"{self.url}/{self.test_user_list_path}")

    def get_test_user_id_url(self, user_id: int) -> httpx.URL:
        return httpx.URL(f"{self.url}/test_user/{user_id}")

    def get_test_user_id_spec_url(self, user_id: int) -> httpx.URL:
        return httpx.URL(f"{self.url}/test_user/{user_id}/specification")

    class Config:
        env_prefix = "OVERHAVE_API_CLIENT_"
