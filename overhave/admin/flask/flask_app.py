from flask import Flask
from pydantic import SecretStr


def get_flask_app(template_folder: str, secret_key: SecretStr) -> Flask:
    app = Flask("admin", template_folder=template_folder)
    app.secret_key = secret_key.get_secret_value()
    app.config.update({"FLASK_ADMIN_SWATCH": "united", "FLASK_ADMIN_FLUID_LAYOUT": True})
    return app
