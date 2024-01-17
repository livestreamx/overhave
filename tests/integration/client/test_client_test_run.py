import allure
import pytest
from faker import Faker
from httpx import HTTPStatusError

from overhave import db
from overhave.storage import FeatureModel, TestRunModel
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestTestRunApiClient:
    """Integration tests for Overhave Test Run API Client."""

    @pytest.mark.parametrize("test_severity", [allure.severity_level.NORMAL], indirect=True)
    def test_get_test_run(
        self,
        overhave_api_client: OverhaveApiClient,
        test_test_run: TestRunModel,
    ) -> None:
        item = overhave_api_client.get_test_run(test_run_id=test_test_run.id)
        assert item.model_dump() == test_test_run.model_dump()

    @pytest.mark.parametrize("test_severity", [allure.severity_level.NORMAL], indirect=True)
    def test_get_test_run_with_unknown_id(
        self,
        overhave_api_client: OverhaveApiClient,
        test_test_run: TestRunModel,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_test_run(test_run_id=faker.random_int())

    @pytest.mark.parametrize("test_severity", [allure.severity_level.NORMAL], indirect=True)
    def test_create_test_run(
        self,
        overhave_api_client: OverhaveApiClient,
        test_feature_with_scenario: FeatureModel,
    ) -> None:
        values = overhave_api_client.create_test_run(tag_value=test_feature_with_scenario.feature_tags[0].value)
        assert len(values) > 0
