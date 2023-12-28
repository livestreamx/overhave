import logging
from typing import Any, Mapping, cast

import httpx

from overhave.transport.http import BaseHttpClient, BearerAuth
from overhave.transport.http.api_client.models import ApiFeatureResponse, ApiFeatureTypeResponse, ApiTagResponse
from overhave.transport.http.api_client.settings import OverhaveApiClientSettings
from overhave.transport.http.base_client import HttpClientValidationError, HttpMethod

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
            method=HttpMethod.GET,
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

    def get_feature_tags_item(self):
        response = self._get(url=httpx.URL(f"{self._settings.url}/feature/tags/item"))

        try:
            return cast(ApiTagResponse, self._parse_or_raise(response, ApiTagResponse))
        except HttpClientValidationError:
            logger.debug("Could not convert response to '%s'!", ApiTagResponse, exc_info=True)

        return None

    def get_feature_tags_list(self):
        response = self._get(url=httpx.URL(f"{self._settings.url}/feature/tags/list"))

        try:
            return cast(ApiTagResponse, self._parse_or_raise(response, ApiTagResponse))
        except HttpClientValidationError:
            logger.debug("Could not convert response to '%s'!", ApiTagResponse, exc_info=True)

        return None

    def get_emulation_run_list(self) -> None:
        pass  # response = self._get(url=httpx.URL(f"{self._settings.url}/emulation/run/list"))

    def get_test_run(self) -> None:
        pass  # response = self._get(url=httpx.URL(f"{self._settings.url}/test_run"))

    def create_test_run(self) -> None:
        pass  # response = self._post(url=httpx.URL(f"{self._settings.url}/test_run/create/"))

    def get_feature_types(self) -> list[ApiFeatureTypeResponse]:
        response = self._get(url=httpx.URL(f"{self._settings.url}/feature/types/list"))
        feature_types = [ApiFeatureTypeResponse.model_validate(data) for data in response.json()]
        return feature_types

    def get_features_by_tag_id(self, tag_id: int) -> list[ApiFeatureResponse]:
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/"),
            params={"tag_id": tag_id},
        )
        return [ApiFeatureResponse.model_validate(data) for data in response.json()]

    def get_features_by_tag_value(self, tag_value: str) -> list[ApiFeatureResponse]:
        response = self._get(
            url=httpx.URL(f"{self._settings.url}/feature/"),
            params={"tag_value": tag_value},
        )
        return [ApiFeatureResponse.model_validate(data) for data in response.json()]
