import logging
from typing import cast

import flask
import werkzeug
from flask_admin import expose
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_login import current_user
from wtforms import Form, ValidationError

from overhave import db
from overhave.admin.views.base import ModelViewConfigured
from overhave.factory import get_admin_factory, get_test_execution_factory
from overhave.pytest_plugin import get_proxy_manager
from overhave.transport import TestRunData, TestRunTask

logger = logging.getLogger(__name__)


class TestRunView(ModelViewConfigured):
    """View for :class:`TestRun` table."""

    __test__ = False

    list_template = "test_run_list.html"
    details_template = "test_run_detail.html"
    can_create = False
    can_edit = True
    column_searchable_list = (
        "name",
        "executed_by",
    )
    column_list = (
        "id",
        "name",
        "start",
        "end",
        "executed_by",
        "status",
    )
    column_details_list = (
        "id",
        "name",
        "start",
        "end",
        "executed_by",
        "status",
        "report_status",
        "report",
        "traceback",
    )
    column_filters = (
        "name",
        "start",
        "executed_by",
        "status",
    )
    column_descriptions = {
        "name": "Feature name",
        "executed_by": "Initiator of scenarios set test run",
        "status": "Test run result",
    }

    def on_model_change(self, form: Form, model: db.TestRun, is_created: bool) -> None:
        if not is_created and current_user.role != db.Role.admin:
            raise ValidationError("Only administrator could change test run data!")

    def on_model_delete(self, model: db.TestRun) -> None:
        if not (current_user.login == model.executed_by or current_user.role == db.Role.admin):
            raise ValidationError("Only test run initiator could delete test run result!")

    @staticmethod
    def _run_test(rendered: werkzeug.Response) -> werkzeug.Response:
        current_scenario_id = int(get_mdict_item_or_list(flask.request.args, "id"))
        factory = get_admin_factory()
        test_run_id = factory.test_run_storage.create_testrun(
            scenario_id=current_scenario_id, executed_by=current_user.login
        )

        if not factory.context.admin_settings.consumer_based:
            proxy_manager = get_proxy_manager()
            test_execution_factory = get_test_execution_factory()
            proxy_manager.clear_factory()
            proxy_manager.set_factory(test_execution_factory)
            factory.threadpool.apply_async(get_test_execution_factory().test_executor.execute_test, args=(test_run_id,))
        if factory.context.admin_settings.consumer_based and not factory.redis_producer.add_task(
            TestRunTask(data=TestRunData(test_run_id=test_run_id))
        ):
            flask.flash("Problems with Redis service! TestRunTask has not been sent.", category="error")
            return rendered
        logger.debug("Redirect to TestRun details view with test_run_id='%s'...", test_run_id)
        return flask.redirect(flask.url_for("testrun.details_view", id=test_run_id))

    @expose("/details/", methods=("GET", "POST"))
    def details_view(self) -> werkzeug.Response:
        rendered: werkzeug.Response = super().details_view()

        if flask.request.method == "POST":
            return self._run_test(rendered)

        return cast(werkzeug.Response, super().details_view())
