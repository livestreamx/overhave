import datetime
from pathlib import Path
from unittest import mock

import pytest

from overhave import OverhaveFileSettings
from overhave.entities import FeatureExtractor, GitRepositoryInitializer
from overhave.scenario import NullableFeatureIdError, ScenarioParser
from overhave.storage import FeatureModel
from overhave.synchronization import OverhaveSynchronizer, SynchronizerStorageManager


@pytest.fixture()
def feature_model_mock() -> FeatureModel:
    return mock.MagicMock()


@pytest.fixture()
def feature_file_mock() -> Path:
    return mock.MagicMock()


@pytest.fixture()
def file_settings_mock() -> OverhaveFileSettings:
    return mock.MagicMock()


@pytest.fixture()
def scenario_parser_mock() -> ScenarioParser:
    def set_strict_mode(mode):
        mocked.strict_mode = mode

    mocked = mock.MagicMock()
    mocked.set_strict_mode = set_strict_mode
    return mocked


@pytest.fixture()
def feature_extractor_mock() -> FeatureExtractor:
    return mock.MagicMock()


@pytest.fixture()
def git_initializer_mock() -> GitRepositoryInitializer:
    return mock.MagicMock()


@pytest.fixture()
def storage_manager_mock() -> SynchronizerStorageManager:
    return mock.MagicMock()


@pytest.fixture()
def synchronizer_extract_recursively_mock(feature_file_mock: Path) -> mock.MagicMock:
    with mock.patch(
        "overhave.entities.file_extractor.BaseFileExtractor._extract_recursively", return_value=[feature_file_mock]
    ) as mocked:
        yield mocked


@pytest.fixture()
def synchronizer_create_feature_mock() -> mock.MagicMock:
    with mock.patch("overhave.synchronization.synchronizer.OverhaveSynchronizer._create_feature") as mocked:
        yield mocked


@pytest.fixture()
def synchronizer_update_feature_mock() -> mock.MagicMock:
    with mock.patch("overhave.synchronization.synchronizer.OverhaveSynchronizer._update_feature") as mocked:
        yield mocked


@pytest.fixture()
def raise_nullable_feature_id_error_on_strict(scenario_parser_mock: ScenarioParser) -> None:
    def raise_nullable_feature_id_error(*args):
        if scenario_parser_mock.strict_mode:
            raise NullableFeatureIdError()

    scenario_parser_mock.parse.side_effect = raise_nullable_feature_id_error


@pytest.fixture()
def one_file_with_no_id_flow(synchronizer_extract_recursively_mock, raise_nullable_feature_id_error_on_strict) -> None:
    pass


@pytest.fixture()
def one_file_with_unknown_id_flow(
    storage_manager_mock: SynchronizerStorageManager, synchronizer_extract_recursively_mock
) -> None:
    storage_manager_mock.get_feature.return_value = None


@pytest.fixture()
def one_file_with_known_id_flow(
    storage_manager_mock: SynchronizerStorageManager,
    feature_model_mock: FeatureModel,
    feature_file_mock: Path,
    synchronizer_extract_recursively_mock,
    feature_file_last_edited: datetime.datetime,
    feature_model_last_edited: datetime.datetime,
    feature_model_released: bool,
) -> None:
    storage_manager_mock.get_feature.return_value = feature_model_mock
    storage_manager_mock.get_last_change_time.return_value = feature_model_last_edited

    stat_mocked = mock.MagicMock()
    stat_mocked.st_mtime = feature_file_last_edited.timestamp()
    feature_file_mock.stat.return_value = stat_mocked

    feature_model_mock.last_edited_at = feature_model_last_edited
    feature_model_mock.released = feature_model_released


@pytest.fixture()
def overhave_synchronizer_mocked(
    file_settings_mock: OverhaveFileSettings,
    scenario_parser_mock: ScenarioParser,
    feature_extractor_mock: FeatureExtractor,
    git_initializer_mock: GitRepositoryInitializer,
    storage_manager_mock: SynchronizerStorageManager,
) -> OverhaveSynchronizer:
    return OverhaveSynchronizer(
        file_settings=file_settings_mock,
        scenario_parser=scenario_parser_mock,
        feature_extractor=feature_extractor_mock,
        git_initializer=git_initializer_mock,
        storage_manager=storage_manager_mock,
    )
