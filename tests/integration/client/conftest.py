from typing import Iterator
from unittest import mock

import httpx
import pytest
from fastapi.testclient import TestClient

from overhave.transport.http.api_client.client import OverhaveApiClient
from overhave.transport.http.api_client.settings import OverhaveApiClientSettings
from overhave.transport.http.base_client import BearerAuth


@pytest.fixture(scope="module")
def envs_for_mock() -> dict[str, str | None]:
    return {
        "OVERHAVE_API_AUTH_SECRET_KEY": "123",
        "OVERHAVE_FEATURES_DIR": "/features",
        "OVERHAVE_FIXTURES_DIR": "/fixtures",
        "OVERHAVE_STEPS_DIR": "/steps",
    }


@pytest.fixture()
def overhave_api_client_settings(
    test_api_client: TestClient, test_api_bearer_auth: BearerAuth
) -> OverhaveApiClientSettings:
    return OverhaveApiClientSettings(url=test_api_client.base_url, auth_token=test_api_bearer_auth.token)


@pytest.fixture()
def overhave_api_client(
    mock_envs, test_api_client: TestClient, overhave_api_client_settings: OverhaveApiClientSettings
) -> Iterator[OverhaveApiClient]:
    with mock.patch.object(httpx, "request", new_callable=lambda: test_api_client.request):
        yield OverhaveApiClient(settings=overhave_api_client_settings)
