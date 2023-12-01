from typing import cast

from flask_admin.form import JSONField
from flask_login import current_user
from pydantic import BaseModel
from wtforms import Form, ValidationError

from overhave import db
from overhave.admin.views.base import ModelViewConfigured
from overhave.factory import get_admin_factory
from overhave.storage import FeatureTypeName
from overhave.utils import get_current_time


def _make_dict_from_model(model: type[BaseModel]) -> dict[str, int | str]:
    return {key: value.annotation.__name__ for key, value in model.model_fields.items() if value.annotation is not None}


class TestUserView(ModelViewConfigured):
    """View for :class:`TestUser` table."""

    __test__ = False

    create_template = "test_user_create.html"
    edit_template = "test_user_edit.html"

    can_view_details = False
    column_list = ("id", "name", "feature_type", "specification", "allow_update", "created_by", "changed_at")
    column_searchable_list = ("id", "name", "created_by")
    column_filters = ("id", "name", "key", "created_by", "allow_update")
    form_excluded_columns = ("created_at", "emulations", "changed_at")
    form_overrides = dict(specification=JSONField)

    form_extra_fields = {"template": JSONField("Specification format")}
    form_widget_args = {"template": {"readonly": True}}

    column_labels = {
        "key": "Key",
        "name": "Name",
        "feature_type": "Feature type",
    }
    column_descriptions = {
        "key": "Test user key",
        "name": "Custom name for test user",
        "feature_type": "Type of scenarios set, where test user will be used",
        "specification": "Test user specification in JSON format placed below",
        "created_by": "Author of test user set",
        "allow_update": "Property of updating allowance through API",
    }

    _feature_type: FeatureTypeName | None = None

    def on_form_prefill(self, form: Form, id) -> None:  # type: ignore  # noqa: A002
        if not isinstance(form._obj, db.TestUser):
            return
        self._feature_type = cast(FeatureTypeName, form._obj.feature_type.name)

    def get_specification_template(self) -> dict[str, int | str] | None:
        factory = get_admin_factory()
        if self._feature_type is None:
            self._feature_type: FeatureTypeName = factory.feature_type_storage.default_feature_type_name
        parser = factory.context.project_settings.user_spec_template_mapping.get(self._feature_type)
        if parser is not None:
            return _make_dict_from_model(parser)
        return None

    @staticmethod
    def _validate_json(model: db.TestUser) -> None:
        if not isinstance(model.specification, dict):
            raise ValidationError("Could not convert specified data into correct JSON!")
        parser: type[BaseModel] | None = get_admin_factory().context.project_settings.user_spec_template_mapping.get(
            model.feature_type.name
        )
        if parser is not None:
            try:
                parser.model_validate(model.specification)
            except ValueError:
                raise ValidationError(f"Could not convert specified data into {parser.__name__} model!")

    def on_model_change(self, form: Form, model: db.TestUser, is_created: bool) -> None:
        self._feature_type = cast(FeatureTypeName, model.feature_type.name)
        self._validate_json(model)
        if is_created:
            model.created_by = current_user.login
        model.changed_at = get_current_time()

    def on_model_delete(self, model: db.TestUser) -> None:
        if not (current_user.login == model.created_by or current_user.role == db.Role.admin):
            raise ValidationError("Only test user creator or administrator could delete test user!")
