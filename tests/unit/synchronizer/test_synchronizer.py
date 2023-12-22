from datetime import datetime
from unittest.mock import MagicMock, patch

from overhave.synchronization.synchronizer import OverhaveSynchronizer
from tests.unit.synchronizer.conftest import (
    mock_feature_model,
    mock_info,
    overhave_synchronizer,
    synchronizer_storage_manager,
)


class TestSynchronizer:
    def test_update_feature(
        self,
        mock_feature_model: MagicMock,
        mock_info: MagicMock,
        synchronizer_storage_manager: MagicMock,
        overhave_synchronizer: OverhaveSynchronizer,
    ):
        feature_file_ts = datetime.now()

        with patch("overhave.synchronization.synchronizer.get_current_time", return_value=feature_file_ts):
            with patch("overhave.synchronization.synchronizer.db.create_session", return_value=MagicMock()):
                overhave_synchronizer._update_feature(mock_feature_model, mock_info, feature_file_ts)

        synchronizer_storage_manager.ensure_users_exist.assert_called_once()
        synchronizer_storage_manager.get_feature_tags.assert_called_once()
        synchronizer_storage_manager.update_db_feature.assert_called_once_with(
            model=mock_feature_model, scenario=mock_info.scenarios
        )

    def test_synchronize(self, synchronizer_storage_manager: MagicMock, overhave_synchronizer: OverhaveSynchronizer):
        with patch.object(overhave_synchronizer, "_git_initializer"):
            with patch.object(overhave_synchronizer, "_extract_recursively", return_value=[]):
                with patch.object(overhave_synchronizer, "_storage_manager") as mock_storage_manager:
                    mock_feature_info = MagicMock()
                    mock_feature_info.id = 1
                    mock_storage_manager.get_feature.return_value = MagicMock(
                        released=True, last_edited_at=datetime.now()
                    )

                    with patch.object(overhave_synchronizer, "_update_feature") as mock_update_feature:
                        overhave_synchronizer.synchronize(create_db_features=True, pull_repository=True)
                        mock_update_feature.assert_not_called()
