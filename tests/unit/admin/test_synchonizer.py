import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from overhave.synchronization.storage_manager import SynchronizerStorageManager
from overhave.synchronization.synchronizer import OverhaveSynchronizer


@pytest.fixture
def mock_feature_model():
    return MagicMock()


@pytest.fixture
def mock_info():
    return MagicMock()


@pytest.fixture
def synchronizer_storage_manager():
    return MagicMock(spec=SynchronizerStorageManager)


def test_update_feature(mock_feature_model, mock_info, synchronizer_storage_manager):
    synchronizer = OverhaveSynchronizer(
        file_settings=MagicMock(),
        scenario_parser=MagicMock(),
        feature_extractor=MagicMock(),
        git_initializer=MagicMock(),
        storage_manager=synchronizer_storage_manager,
    )

    feature_file_ts = datetime.now()

    with patch("overhave.synchronization.synchronizer.get_current_time", return_value=feature_file_ts):
        with patch("overhave.synchronization.synchronizer.db.create_session", return_value=MagicMock()):
            synchronizer._update_feature(mock_feature_model, mock_info, feature_file_ts)

    synchronizer_storage_manager.ensure_users_exist.assert_called_once()
    synchronizer_storage_manager.get_feature_tags.assert_called_once()
    synchronizer_storage_manager.update_db_feature.assert_called_once_with(model=mock_feature_model,
                                                                           scenario=mock_info.scenarios)
