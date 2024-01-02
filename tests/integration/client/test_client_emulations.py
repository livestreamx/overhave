import pytest
from faker import Faker

from overhave import db
from overhave.storage import EmulationRunModel, TestUserModel
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestEmulationsApiClient:
    """Integration tests for Overhave Emulation API Client."""

    def test_get_emulation_run_list_by_test_user_id_empty(self, api_client: OverhaveApiClient, faker: Faker) -> None:
        emulations = api_client.get_emulation_runs(test_user_id=faker.random_int())
        assert len(emulations) == 0

    def test_get_emulation_run_list_by_test_user_id(
        self,
        api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
        test_emulation_run: EmulationRunModel,
    ) -> None:
        emulations = api_client.get_emulation_runs(test_user_id=test_testuser.id)
        assert len(emulations) == 1
        assert emulations[0].model_dump() == test_emulation_run.model_dump()
