import logging
from typing import Any, Mapping

import httpx

from overhave.transport.http import BaseHttpClient, BearerAuth
from overhave.transport.http.api_client.models import ApiFeatureResponse, ApiFeatureTypeResponse, ApiTagResponse, \
    ApiTestRunResponse, ApiEmulationRunResponse
from overhave.transport.http.api_client.settings import OverhaveApiClientSettings
from overhave.transport.http.base_client import HttpMethod

logger = logging.getLogger(__name__)


class OverhaveApiClient(BaseHttpClient[OverhaveApiClientSettings]):
    """Client for overhave api."""

    def __init__(self, settings: OverhaveApiClientSettings):
        super().__init__(settings=settings)

    def _get(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            raise_for_status: bool = True,
    ):
        return self._make_request(
            method=HttpMethod.GET,
            url=url,
            params=params,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token),
        )

    def _post(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
            data: str | bytes | Mapping[Any, Any] | None = None,
            raise_for_status: bool = True,
    ):
        return self._make_request(
            method=HttpMethod.POST,
            url=url,
            params=params,
            json=json,
            data=data,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token),
        )

    def _put(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
            data: str | bytes | Mapping[Any, Any] | None = None,
            raise_for_status: bool = True,
    ):
        return self._make_request(
            method=HttpMethod.PUT,
            url=url,
            params=params,
            json=json,
            data=data,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token),
        )

    def _delete(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            raise_for_status: bool = True,
    ):
        return self._make_request(
            method=HttpMethod.DELETE,
            url=url,
            params=params,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token),
        )

    def get_feature_tags_item(self, value: str) -> ApiTagResponse:
        logger.debug(f"Start get feature tags item with [value: {value}]")
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/tags/item"),
            params={"value": value}
        )
        logger.debug("Get tags item successfully")

        return ApiTagResponse.model_validate(response.json())

    def get_feature_tags_list(self, value: str) -> list[ApiTagResponse]:
        logger.debug(f"Start get feature tags list with [value: {value}]")
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/tags/list"),
            params={"value": value}
        )
        logger.debug("Get tags list successfully")

        return [ApiTagResponse.model_validate(data) for data in response.json()]

    def get_feature_types(self) -> list[ApiFeatureTypeResponse]:
        logger.debug(f"Start get feature types list")
        response = self._get(url=httpx.URL(f"{self._settings.url}/feature/types/list"))
        logger.debug("Get feature types successfully")

        return [ApiFeatureTypeResponse.model_validate(data) for data in response.json()]

    def get_features_by_tag_id(self, tag_id: int) -> list[ApiFeatureResponse]:
        logger.debug(f"Start get feature with [tag_id: {tag_id}]")
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/"),
            params={"tag_id": tag_id},
        )
        logger.debug("Get feature successfully")

        return [ApiFeatureResponse.model_validate(data) for data in response.json()]

    def get_features_by_tag_value(self, tag_value: str) -> list[ApiFeatureResponse]:
        logger.debug(f"Start get feature with [tag_value: {tag_value}]")
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/"),
            params={"tag_value": tag_value},
        )
        logger.debug("Get feature successfully")

        return [ApiFeatureResponse.model_validate(data) for data in response.json()]

    def get_test_run(self, test_run_id: int) -> ApiTestRunResponse:
        logger.debug(f"Start get test run with [test_run_id: {test_run_id}]")
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/test_run"),
            params={"test_run_id": test_run_id},
        )
        logger.debug("Get test run successfully")

        return ApiTestRunResponse.model_validate(response.json())

    def create_test_run(self, tag_value: str) -> list[str]:
        logger.debug(f"Start create test run with [tag_value: {tag_value}]")
        response = self._post(
            url=httpx.URL(f"{self._settings.url}/test_run/create/"),
            params={"tag_value": tag_value},
        )
        logger.debug("Create test run successfully")

        return response.json()

    def get_emulation_runs(self, test_user_id: int | None = None):
        logger.debug("Stat get list of EmulationRun")
        params = {'test_user_id': test_user_id} if test_user_id else {}
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/emulation/run/list"),
            params=params,
        )
        logger.debug("Get list of EmulationRun successfully")
        return [ApiEmulationRunResponse.model_validate(data) for data in response.json()]
