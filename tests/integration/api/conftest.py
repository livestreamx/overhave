from unittest import mock

import httpx
import pytest
from faker import Faker


@pytest.fixture(scope="module")
def envs_for_mock() -> dict[str, str | None]:
    return {
        "OVERHAVE_API_AUTH_SECRET_KEY": "123",
        "OVERHAVE_FEATURES_DIR": "/features",
        "OVERHAVE_FIXTURES_DIR": "/fixtures",
        "OVERHAVE_STEPS_DIR": "/steps",
    }


@pytest.fixture(scope="module")
def mock_default_value() -> str:
    return ""


def validate_content_null(response: httpx.Response, statement: bool) -> None:
    assert (response.content.decode() == "null") is statement


@pytest.fixture()
def flask_urlfor_handler_mock(faker: Faker) -> mock.MagicMock:
    with mock.patch("flask.url_for") as flask_urlfor_handler:
        flask_urlfor_handler.return_value = f"/testrun/details/?id={faker.random_int()}"
        yield flask_urlfor_handler
