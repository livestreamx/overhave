from datetime import datetime
from unittest import mock

import pytest

from demo.settings import OverhaveDemoAppLanguage
from overhave import db
from overhave.storage import TestRunModel
from tests.db_utils import create_test_session


@pytest.mark.usefixtures("database")
@pytest.mark.parametrize("test_demo_language", [OverhaveDemoAppLanguage.RU], indirect=True)
class TestOverhaveTestExecution:
    """Sanity tests for application test run."""

    @pytest.mark.parametrize(
        ("run_test_process_return_code", "report_status"),
        [(0, db.TestReportStatus.GENERATED), (1, db.TestReportStatus.GENERATION_FAILED)],
        indirect=True,
    )
    def test_correct_run_executed(
        self, test_executed_testruntask_id: int, subprocess_run_mock: mock.MagicMock, report_status: db.TestReportStatus
    ) -> None:
        subprocess_run_mock.assert_called_once()
        with create_test_session() as session:
            db_test_run = session.query(db.TestRun).filter(db.TestRun.id == test_executed_testruntask_id).one()
            test_run = TestRunModel.model_validate(db_test_run)
        assert test_run.id == test_executed_testruntask_id
        assert isinstance(test_run.created_at, datetime)
        assert test_run.status is db.TestRunStatus.SUCCESS
        assert isinstance(test_run.start, datetime)
        assert isinstance(test_run.end, datetime)
        assert test_run.report_status is report_status
        assert test_run.traceback is None
