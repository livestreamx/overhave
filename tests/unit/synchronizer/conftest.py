from unittest.mock import MagicMock

import pytest

from overhave import OverhaveFileSettings
from overhave.entities import FeatureExtractor
from overhave.synchronization import OverhaveSynchronizer, SynchronizerStorageManager
from tests.objects import get_test_feature_extractor, get_test_file_settings


@pytest.fixture()
def mock_feature_model():
    return MagicMock()


@pytest.fixture()
def mock_info():
    return MagicMock()


@pytest.fixture()
def synchronizer_storage_manager():
    return MagicMock(spec=SynchronizerStorageManager)


@pytest.fixture()
def file_settings():
    return get_test_file_settings()


@pytest.fixture()
def feature_extractor():
    return get_test_feature_extractor()


@pytest.fixture()
def overhave_synchronizer(
    file_settings: OverhaveFileSettings,
    feature_extractor: FeatureExtractor,
    synchronizer_storage_manager: MagicMock,
) -> OverhaveSynchronizer:
    return OverhaveSynchronizer(
        file_settings=file_settings,
        scenario_parser=MagicMock(),
        feature_extractor=feature_extractor,
        git_initializer=MagicMock(),
        storage_manager=synchronizer_storage_manager,
    )
