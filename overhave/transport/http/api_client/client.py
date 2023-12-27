from typing import Any, Mapping

import httpx

from overhave.transport.http import BaseHttpClient, BearerAuth
from overhave.transport.http.api_client.settings import OverhaveApiClientSettings
from overhave.transport.http.base_client import HttpMethod


class OverhaveApiClient(BaseHttpClient[OverhaveApiClientSettings]):
    def __init__(self, settings: OverhaveApiClientSettings):
        super().__init__(settings=settings)

    def _get(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            raise_for_status: bool = True,
    ):
        self._make_request(
            method=HttpMethod.GET,
            url=url,
            params=params,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token)
        )

    def _post(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
            data: str | bytes | Mapping[Any, Any] | None = None,
            raise_for_status: bool = True,
    ):
        self._make_request(
            method=HttpMethod.GET,
            url=url,
            params=params,
            json=json,
            data=data,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token)
        )

    def _put(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            json: dict[str, Any] | None = None,
            data: str | bytes | Mapping[Any, Any] | None = None,
            raise_for_status: bool = True,
    ):
        self._make_request(
            method=HttpMethod.PUT,
            url=url,
            params=params,
            json=json,
            data=data,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token)
        )

    def _delete(
            self,
            url: httpx.URL,
            params: dict[str, Any] | None = None,
            raise_for_status: bool = True,
    ):
        self._make_request(
            method=HttpMethod.DELETE,
            url=url,
            params=params,
            raise_for_status=raise_for_status,
            auth=BearerAuth(self._settings.auth_token)
        )
