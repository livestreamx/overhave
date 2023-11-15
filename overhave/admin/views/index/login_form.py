import logging

import flask
from flask_wtf import FlaskForm as Form
from pydantic import SecretStr
from werkzeug import Response
from wtforms import PasswordField, StringField, validators

from overhave.admin.flask.login_manager import AdminPanelUser
from overhave.entities import IAdminAuthorizationManager

logger = logging.getLogger(__name__)

_INVALID_AUTH_MSG = "Specified username '{username}' and password pair is invalid!"


class LoginForm(Form):
    """Form for user auth_managers."""

    username: StringField = StringField(
        "Username",
        validators=[validators.input_required(message="Field required!")],
        render_kw={"placeholder": "Username", "icon": "glyphicon-user"},
    )
    password: PasswordField = PasswordField(
        "Password",
        render_kw={"placeholder": "Password", "icon": "glyphicon-certificate"},
    )

    def __init__(self, auth_manager: IAdminAuthorizationManager) -> None:
        super().__init__()
        self._auth_manager = auth_manager

    def get_user(self) -> AdminPanelUser:
        authorized_user = self._auth_manager.authorize_user(
            username=self.username.data, password=SecretStr(self.password.data)
        )
        if authorized_user is None:
            raise validators.ValidationError(_INVALID_AUTH_MSG.format(username=self.username.data))
        return AdminPanelUser(user_data=authorized_user)

    @staticmethod
    def flash_and_redirect(flash_msg: str) -> Response:
        flask.flash(flash_msg, category="error")
        return flask.redirect(flask.url_for("admin.login"))
