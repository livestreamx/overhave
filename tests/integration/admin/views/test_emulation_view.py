from http import HTTPStatus

import flask
import flask_admin.helpers
import pytest
from flask.testing import FlaskClient

from overhave import db
from overhave.storage import SystemUserModel, EmulationModel
from tests.db_utils import create_test_session


@pytest.mark.usefixtures("database")
class TestEmulationView:
    """Tests for emulation view."""

    @pytest.mark.parametrize("test_user_role", [db.Role.admin], indirect=True)
    def test_edit_redirect_to_emulation_index_view_if_no_emulate(self, test_client: FlaskClient,
                                                                 test_authorized_user: SystemUserModel) -> None:
        with create_test_session():
            response = test_client.get("/emulation/edit/")
        assert response.status_code == HTTPStatus.FOUND
        assert response.location == '/emulation/'

    @pytest.mark.parametrize("test_user_role", [db.Role.admin], indirect=True)
    def test_edit_redirect_to_emulation_index_view_if_emulate_and_no_emulation_id(self, test_client: FlaskClient,
                                                                                  test_authorized_user) -> None:
        with create_test_session():
            response = test_client.get("/emulation/edit/", data={"emulate": True})
        assert response.status_code == HTTPStatus.FOUND
        assert response.location == '/emulation/'

    @pytest.mark.parametrize("test_user_role", [db.Role.admin], indirect=True)
    def test_edit_creates_emulation_run(self, test_client: FlaskClient,
                                        test_authorized_user: SystemUserModel,
                                        test_emulation: EmulationModel) -> None:
        with create_test_session():
            response = test_client.post("/emulation/edit/",
                                        data={"emulate": True},
                                        query_string={"id": test_emulation.id})
        assert response.status_code == HTTPStatus.FOUND
        emulation_run_id = int(response.request.args.get('id'))
        assert response.location == flask_admin.helpers.get_url('emulationrun.details_view',
                                                                id=emulation_run_id)
        with create_test_session():
            response = test_client.get("/emulationrun/details/",
                                       query_string={"id": emulation_run_id})
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("test_user_role", [db.Role.admin], indirect=True)
    def test_edit_redirects_back_if_redis_producer_cant_add_task(self, test_client: FlaskClient,
                                                                 test_authorized_user: SystemUserModel,
                                                                 test_emulation: EmulationModel,
                                                                 patched_app_admin_factory) -> None:
        patched_app_admin_factory.redis_producer.add_task = lambda *_: False
        with create_test_session():
            response = test_client.post("/emulation/edit/",
                                        data={"emulate": True},
                                        query_string={"id": test_emulation.id})
        assert response.status_code == HTTPStatus.FOUND
        assert response.location == flask.url_for("emulation.edit_view", id=test_emulation.id)
