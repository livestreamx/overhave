from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from overhave import db, OverhaveAdminApp
from overhave.storage import SystemUserModel
from tests.db_utils import count_queries


@pytest.mark.usefixtures("database")
class TestIndexView:
    """Tests for login view."""

    @pytest.mark.parametrize("test_user_role", [db.Role.user, db.Role.admin], indirect=True)
    def test_logout_user_with_auto_redirect(
            self,
            test_app: OverhaveAdminApp,
            test_client: FlaskClient,
            test_authorized_user: SystemUserModel
    ) -> None:
        with count_queries(expected_count=2):
            response = test_client.get("/logout", follow_redirects=True)

        assert response.status_code == HTTPStatus.OK
