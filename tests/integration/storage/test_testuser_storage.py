import pytest
from faker import Faker

from overhave import db
from overhave.storage import (
    TestUserDoesNotExistError,
    TestUserModel,
    TestUserSpecification,
    TestUserStorage,
    TestUserUpdatingNotAllowedError,
)
from tests.db_utils import count_queries, create_test_session


@pytest.mark.usefixtures("database")
class TestTestUserStorage:
    """Integration tests for :class:`TestUserStorage`."""

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    def test_get_test_user_by_id(self, test_user_storage: TestUserStorage, test_testuser: TestUserModel) -> None:
        with count_queries(2):
            test_user = test_user_storage.get_testuser_model_by_id(test_testuser.id)
        assert test_user is not None
        assert test_user == test_testuser

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    def test_get_user_by_key(self, test_user_storage: TestUserStorage, test_testuser: TestUserModel) -> None:
        with count_queries(2):
            test_user = test_user_storage.get_testuser_model_by_key(test_testuser.key)
        assert test_user is not None
        assert test_user == test_testuser

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    @pytest.mark.parametrize("feature_type_id", [1234])
    def test_get_user_list_empty(
        self, test_user_storage: TestUserStorage, test_testuser: TestUserModel, feature_type_id: int
    ) -> None:
        with count_queries(1):
            with db.create_session() as session:
                test_users = test_user_storage.get_test_users_by_feature_type_name(
                    session=session, feature_type_id=feature_type_id, allow_update=test_testuser.allow_update
                )
        assert not test_users

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    def test_get_user_list(self, test_user_storage: TestUserStorage, test_testuser: TestUserModel) -> None:
        with count_queries(2):
            with db.create_session() as session:
                test_users = test_user_storage.get_test_users_by_feature_type_name(
                    session=session,
                    feature_type_id=test_testuser.feature_type_id,
                    allow_update=test_testuser.allow_update,
                )
        assert len(test_users) == 1
        assert test_users[0] == test_testuser

    def test_update_test_user_specification_no_user(
        self,
        test_user_storage: TestUserStorage,
        faker: Faker,
    ) -> None:
        with count_queries(1):
            with pytest.raises(TestUserDoesNotExistError):
                test_user_storage.update_test_user_specification(
                    user_id=faker.random_int(), specification=TestUserSpecification({faker.word(): faker.word()})
                )

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    @pytest.mark.parametrize("new_specification", [{"kek": "lol", "overhave": "test"}, {}, {"test": "new_value"}])
    @pytest.mark.parametrize("testuser_allow_update", [False], indirect=True)
    def test_update_test_user_specification_not_allowed(
        self,
        test_user_storage: TestUserStorage,
        test_testuser: TestUserModel,
        test_specification: TestUserSpecification,
        new_specification: TestUserSpecification,
    ) -> None:
        assert test_testuser.specification == test_specification
        with count_queries(1):
            with pytest.raises(TestUserUpdatingNotAllowedError):
                test_user_storage.update_test_user_specification(test_testuser.id, new_specification)

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    @pytest.mark.parametrize("new_specification", [{"kek": "lol", "overhave": "test"}, {}, {"test": "new_value"}])
    @pytest.mark.parametrize("testuser_allow_update", [True], indirect=True)
    def test_update_test_user_specification(
        self,
        test_user_storage: TestUserStorage,
        test_testuser: TestUserModel,
        test_specification: TestUserSpecification,
        new_specification: TestUserSpecification,
    ) -> None:
        assert test_testuser.specification == test_specification
        with count_queries(2):
            test_user_storage.update_test_user_specification(test_testuser.id, new_specification)
        with create_test_session():
            test_user = test_user_storage.get_testuser_model_by_key(test_testuser.key)
        assert test_user is not None
        assert test_user.specification == new_specification

    def test_delete_test_user_by_id_empty(
        self, database: None, test_user_storage: TestUserStorage, faker: Faker
    ) -> None:
        with count_queries(1):
            with pytest.raises(TestUserDoesNotExistError):
                test_user_storage.delete_test_user(faker.random_int())

    @pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
    def test_delete_test_user_by_id(self, test_user_storage: TestUserStorage, test_testuser: TestUserModel) -> None:
        with count_queries(3):
            test_user_storage.delete_test_user(test_testuser.id)
        with count_queries(1):
            assert test_user_storage.get_testuser_model_by_id(test_testuser.id) is None
