import re
from datetime import datetime
from typing import Any

import allure
import httpx
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup

from overhave import db
from overhave.admin.views.formatters.helpers import (
    get_button_class_by_status,
    get_feature_link_markup,
    get_report_index_link,
    get_testrun_details_link,
)
from overhave.admin.views.formatters.safe_formatter import safe_formatter


@safe_formatter(
    type=datetime,
    supported_models=(
        db.UserRole,
        db.GroupRole,
        db.Feature,
        db.TestRun,
        db.Draft,
        db.TestUser,
        db.Emulation,
        db.EmulationRun,
        db.Tags,
    ),
)
def datetime_formatter(view: ModelView, context: Any, model: db.BaseTable, value: datetime) -> Markup:
    return Markup(value.strftime("%d-%m-%Y %H:%M:%S"))


@safe_formatter(type=list, supported_models=(db.Feature,))
def task_formatter(view: ModelView, context: Any, model: db.Feature, value: list[str]) -> Markup:
    task_tracker_url = getattr(view, "task_tracker_url")
    if not task_tracker_url:
        return Markup(", ".join(value))
    task_links = (f"<a href='{task_tracker_url}/{task}' target='blank'>{task}</a>" for task in value)
    return Markup(", ".join(task_links))


@safe_formatter(type=str, supported_models=(db.Feature,))
def file_path_formatter(view: ModelView, context: Any, model: db.Feature, value: str) -> Markup:
    if isinstance(model, db.Feature):
        value_without_suffix = re.sub(rf"({view.feature_suffix})", "", value)
        value_to_visualize = value_without_suffix.split("/")[-1]
        return Markup(f"<i>{value_to_visualize}</i>")
    raise NotImplementedError()


@safe_formatter(type=str, supported_models=(db.TestRun,))
def result_report_formatter(view: ModelView, context: Any, model: db.TestRun, value: db.TestRunStatus) -> Markup:
    test_run_id = getattr(model, "id")
    if test_run_id is None:
        raise ValueError("test_run_id could not be None!")
    report = model.report
    if model.report_status.has_report and isinstance(report, str):
        return Markup(
            f"<form action='{get_report_index_link(report)}' method='POST' target='_blank'>"
            f"<input type='hidden' name='run_id' value='{test_run_id}' />"
            f"<fieldset title='Go to report'>"
            f"<button class='link-button {get_button_class_by_status(value)}' type='submit'>{value.upper()}</button>"
            "</fieldset>"
            "</form>"
        )
    return Markup(
        f"<form action='{get_testrun_details_link(test_run_id)}'>"
        f"<fieldset title='Show details'>"
        f"<button class='link-button {get_button_class_by_status(value)}'>{value.upper()}</button>"
        "</fieldset>"
        "</form>"
    )


@safe_formatter(type=dict, supported_models=(db.TestUser,))
def json_formatter(view: ModelView, context: Any, model: db.BaseTable, value: dict[str, str | None]) -> Markup:
    info = ""
    for k, v in list(filter(lambda x: x, value.items())):
        info += f"<b>{k}</b>:&nbsp;&nbsp;{v}<br>"
    return Markup("<form>" "<fieldset>" f"<div class='json-data'>{info}</div>" "</fieldset>" "</form>")


@safe_formatter(type=str, supported_models=(db.Feature, db.TestRun))
def feature_link_formatter(view: ModelView, context: Any, model: db.BaseTable, value: str) -> Markup:
    if isinstance(model, db.Feature):
        return get_feature_link_markup(feature_id=model.id, feature_name=value)
    if isinstance(model, db.TestRun):
        return get_feature_link_markup(feature_id=model.scenario.feature_id, feature_name=value)
    raise NotImplementedError()


def _get_severity_color(severity: str) -> str:
    match severity:
        case allure.severity_level.BLOCKER:
            return "brown"
        case allure.severity_level.CRITICAL:
            return "maroon"
        case allure.severity_level.MINOR:
            return "gray"
        case allure.severity_level.TRIVIAL:
            return "silver"
    return "black"


@safe_formatter(type=str, supported_models=(db.Feature,))
def feature_severity_formatter(view: ModelView, context: Any, model: db.BaseTable, value: str) -> Markup:
    color = _get_severity_color(severity=value)
    return Markup(f"<font color='{color}'>{value.upper()}</font>")


@safe_formatter(type=int, supported_models=(db.Draft,))
def draft_feature_formatter(view: ModelView, context: Any, model: db.Draft, value: str) -> Markup:
    return get_feature_link_markup(feature_id=value, feature_name=model.feature.name)


@safe_formatter(type=int, supported_models=(db.Draft,))
def draft_testrun_formatter(view: ModelView, context: Any, model: db.BaseTable, value: int) -> Markup:
    return Markup(f"<a {get_testrun_details_link(value)}>{value}</a>")


@safe_formatter(type=str, supported_models=(db.Draft,))
def draft_prurl_formatter(view: ModelView, context: Any, model: db.BaseTable, value: str) -> Markup:
    return Markup(f"<a href='{httpx.URL(value)}'>{value}</a>")
