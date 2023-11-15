import socket
from unittest import mock

import pytest

from overhave.storage import (
    FeatureModel,
    FeatureStorage,
    FeatureTagStorage,
    FeatureTypeStorage,
    ScenarioModel,
    TestRunStorage,
)
from tests.db_utils import create_test_session


@pytest.fixture(scope="class")
def socket_mock() -> mock.MagicMock:
    with mock.patch("socket.socket", return_value=mock.create_autospec(socket.socket)) as mocked_socket:
        yield mocked_socket


@pytest.fixture(scope="class")
def test_tag_storage() -> FeatureTagStorage:
    return FeatureTagStorage()


@pytest.fixture(scope="class")
def test_feature_storage(test_tag_storage: FeatureTagStorage) -> FeatureStorage:
    return FeatureStorage()


@pytest.fixture()
def test_feature_type_storage() -> FeatureTypeStorage:
    return FeatureTypeStorage()


@pytest.fixture()
def test_second_created_test_run_id(
    test_run_storage: TestRunStorage, test_scenario: ScenarioModel, test_feature: FeatureModel
) -> int:
    with create_test_session():
        return test_run_storage.create_testrun(test_scenario.id, test_feature.author)
