from unittest.mock import MagicMock

import pytest

from overhave import OverhaveFileSettings
from overhave.entities import FeatureExtractor, GitRepositoryInitializer
from overhave.scenario import ScenarioParser
from overhave.synchronization import OverhaveSynchronizer, SynchronizerStorageManager


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
def overhave_synchronizer(
    file_settings: OverhaveFileSettings,
    scenario_parser: ScenarioParser,
    feature_extractor: FeatureExtractor,
    git_initializer: GitRepositoryInitializer,
    storage_manager: SynchronizerStorageManager,
) -> OverhaveSynchronizer:
    return OverhaveSynchronizer(
        file_settings=file_settings,
        scenario_parser=scenario_parser,
        feature_extractor=feature_extractor,
        git_initializer=git_initializer,
        storage_manager=storage_manager,
    )


@pytest.fixture()
def mock_synchronizer(synchronizer_storage_manager: MagicMock) -> OverhaveSynchronizer:
    return OverhaveSynchronizer(
        file_settings=MagicMock(),
        scenario_parser=MagicMock(),
        feature_extractor=MagicMock(),
        git_initializer=MagicMock(),
        storage_manager=synchronizer_storage_manager,
    )
