import pytest
from faker import Faker

from overhave import db
from overhave.storage import EmulationRunModel, TestUserModel


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestEmulationsApiClient:
    """Integration tests for Overhave Emulation API Client."""

    def test_get_emulation_run_list_by_test_user_id_empty(self, overhave_api_client, faker: Faker) -> None:
        emulations = overhave_api_client.get_emulation_runs(test_user_id=faker.random_int())
        assert len(emulations) == 0

    def test_get_emulation_run_list_by_test_user_id(
        self,
        overhave_api_client,
        test_testuser: TestUserModel,
        test_emulation_run: EmulationRunModel,
    ) -> None:
        emulations = overhave_api_client.get_emulation_runs(test_user_id=test_testuser.id)
        assert len(emulations) == 1
        assert emulations[0].model_dump() == test_emulation_run.model_dump()
