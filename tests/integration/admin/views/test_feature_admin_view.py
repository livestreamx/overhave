from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from overhave import db
from overhave.storage import SystemUserModel
from tests.db_utils import create_test_session


@pytest.mark.usefixtures("database")
class TestFeatureAdminView:
    """Tests for feature view."""

    @pytest.mark.parametrize("test_user_role", [db.Role.admin], indirect=True)
    def test_edit_redirects_to_feature_index_view_if_no_feature(self, test_client: FlaskClient,
                                                                  test_authorized_user: SystemUserModel) -> None:
        with create_test_session():
            response = test_client.get("/feature/edit/")
        assert response.status_code == HTTPStatus.FOUND
        assert response.location == '/feature/'