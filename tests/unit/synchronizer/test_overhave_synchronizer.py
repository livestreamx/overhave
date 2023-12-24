from datetime import datetime
from unittest import mock

import pytest
from pytz import UTC

from overhave.synchronization import OverhaveSynchronizer


class TestSynchronizer:
    """Unit tests for :class:`OverhaveSynchronizer`."""

    def test_pull_repository_when_synchronize(
        self, overhave_synchronizer_mocked: OverhaveSynchronizer, git_initializer_mock: mock.MagicMock
    ) -> None:
        overhave_synchronizer_mocked.synchronize(pull_repository=True)
        git_initializer_mock.pull.assert_called_once()

    def test_not_pull_repository_when_synchronize(
        self, overhave_synchronizer_mocked: OverhaveSynchronizer, git_initializer_mock: mock.MagicMock
    ) -> None:
        overhave_synchronizer_mocked.synchronize(pull_repository=False)
        git_initializer_mock.pull.assert_not_called()

    def test_not_create_future_with_no_id(
        self,
        overhave_synchronizer_mocked: OverhaveSynchronizer,
        one_file_with_no_id_flow: None,
        synchronizer_create_feature_mock: mock.MagicMock,
    ) -> None:
        overhave_synchronizer_mocked.synchronize()
        synchronizer_create_feature_mock.assert_not_called()

    def test_create_future_with_no_id(
        self,
        overhave_synchronizer_mocked: OverhaveSynchronizer,
        one_file_with_no_id_flow: None,
        synchronizer_create_feature_mock: mock.MagicMock,
    ) -> None:
        overhave_synchronizer_mocked.synchronize(create_db_features=True)
        synchronizer_create_feature_mock.assert_called_once()

    def test_not_update_future_with_unknown_id(
        self,
        overhave_synchronizer_mocked: OverhaveSynchronizer,
        one_file_with_unknown_id_flow: None,
        synchronizer_update_feature_mock: mock.MagicMock,
    ) -> None:
        overhave_synchronizer_mocked.synchronize()
        synchronizer_update_feature_mock.assert_not_called()

    @pytest.mark.parametrize("feature_file_last_edited", [UTC.localize(datetime(2023, 1, 1))])
    @pytest.mark.parametrize(
        "feature_model_last_edited", [UTC.localize(datetime(2023, 1, 1)), UTC.localize(datetime(2023, 1, 2))]
    )
    @pytest.mark.parametrize("feature_model_released", [True])
    def test_not_update_already_released_future(
        self,
        overhave_synchronizer_mocked: OverhaveSynchronizer,
        one_file_with_known_id_flow: None,
        synchronizer_update_feature_mock: mock.MagicMock,
        feature_file_last_edited: datetime,
        feature_model_last_edited: datetime,
        feature_model_released: bool,
    ) -> None:
        overhave_synchronizer_mocked.synchronize()
        synchronizer_update_feature_mock.assert_not_called()

    @pytest.mark.parametrize("feature_file_last_edited", [UTC.localize(datetime(2023, 1, 2))])
    @pytest.mark.parametrize("feature_model_last_edited", [UTC.localize(datetime(2023, 1, 1))])
    @pytest.mark.parametrize("feature_model_released", [False])
    def test_update_not_actual_future(
        self,
        overhave_synchronizer_mocked: OverhaveSynchronizer,
        one_file_with_known_id_flow: None,
        synchronizer_update_feature_mock: mock.MagicMock,
        feature_file_last_edited: datetime,
        feature_model_last_edited: datetime,
        feature_model_released: bool,
    ) -> None:
        overhave_synchronizer_mocked.synchronize()
        synchronizer_update_feature_mock.assert_called_once()
