from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from overhave import db, OverhaveAdminApp
from overhave.storage import SystemUserModel
from tests.db_utils import create_test_session


@pytest.mark.usefixtures("database")
class TestIndexView:
    """Tests for login view."""

    @pytest.mark.parametrize("test_user_role", [db.Role.user, db.Role.admin], indirect=True)
    def test_logout_user_without_auto_redirect(
            self,
            test_app: OverhaveAdminApp,
            test_client: FlaskClient,
            test_authorized_user: SystemUserModel
    ) -> None:
        with create_test_session():
            response = test_client.get("/logout")

        assert response.status_code == HTTPStatus.FOUND
        assert ('You should be redirected automatically to the target URL: <a href="/login">/login</a>' in
                response.data.decode("utf-8")), "Doesn't redirect to the index page"
