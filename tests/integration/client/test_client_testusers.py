import pytest as pytest
from faker import Faker
from httpx import HTTPStatusError

from overhave import db
from overhave.storage import TestUserModel, TestUserSpecification
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestTestUserApiClient:
    """Integration tests for Overhave TestUser API Client."""

    def test_get_user_by_id_empty(
        self,
        overhave_api_client: OverhaveApiClient,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_test_user_by_user_id(user_id=faker.random_int())

    def test_get_user_by_id(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
    ) -> None:
        test_user = overhave_api_client.get_test_user_by_user_id(user_id=test_testuser.id)
        assert test_user.model_dump() == test_testuser.model_dump()

    def test_get_user_by_key_empty(
        self,
        overhave_api_client: OverhaveApiClient,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_test_user_by_user_key(user_key=faker.word())

    def test_get_user_by_key(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
    ) -> None:
        test_user = overhave_api_client.get_test_user_by_user_key(user_key=test_testuser.key)
        assert test_user.model_dump() == test_testuser.model_dump()

    def test_delete_user_by_id_empty(self, overhave_api_client: OverhaveApiClient, faker: Faker) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.delete_test_user(user_id=faker.random_int())

    def test_delete_user_by_id(self, overhave_api_client: OverhaveApiClient, test_testuser: TestUserModel) -> None:
        overhave_api_client.delete_test_user(user_id=test_testuser.id)

    @pytest.mark.parametrize("allow_update", [True, False])
    def test_get_test_user_list_feature_type_empty(
        self, overhave_api_client: OverhaveApiClient, faker: Faker, allow_update: bool
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_test_users(
                feature_type=faker.word(),
                allow_update=allow_update,
            )

    def test_get_test_user_list(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
    ) -> None:
        test_users = overhave_api_client.get_test_users(
            feature_type=test_testuser.feature_type.name,
            allow_update=test_testuser.allow_update,
        )
        assert len(test_users) == 1
        assert test_users[0].model_dump() == test_testuser.model_dump()

    def test_get_user_spec_empty(self, overhave_api_client: OverhaveApiClient, faker: Faker) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_test_user_specification(user_id=faker.random_int())

    def test_get_user_spec(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
    ) -> None:
        user_spec = overhave_api_client.get_test_user_specification(user_id=test_testuser.id)
        assert user_spec == test_testuser.specification

    def test_put_user_spec_no_body(
        self,
        overhave_api_client: OverhaveApiClient,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.update_test_user_specification(user_id=faker.random_int(), specification={})

    def test_put_user_spec_no_user(
        self,
        overhave_api_client: OverhaveApiClient,
        test_new_specification: TestUserSpecification,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.update_test_user_specification(
                user_id=faker.random_int(), specification=test_new_specification
            )

    @pytest.mark.parametrize("testuser_allow_update", [False], indirect=True)
    def test_put_user_spec_not_allowed(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
        test_new_specification: TestUserSpecification,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.update_test_user_specification(
                user_id=test_testuser.id, specification=test_new_specification
            )

    @pytest.mark.parametrize("testuser_allow_update", [True], indirect=True)
    def test_put_user_spec(
        self,
        overhave_api_client: OverhaveApiClient,
        test_testuser: TestUserModel,
        test_new_specification: TestUserSpecification,
    ) -> None:
        overhave_api_client.update_test_user_specification(
            user_id=test_testuser.id, specification=test_new_specification
        )
        updated_user_specification = overhave_api_client.get_test_user_specification(user_id=test_testuser.id)
        assert updated_user_specification == test_new_specification
