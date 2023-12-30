from datetime import datetime
from typing import Literal

import allure

from pydantic import BaseModel


class TokenRequestData(BaseModel):
    """Model for OAuth2 request data."""

    grant_type: Literal["password"] = "password"
    username: str
    password: str


class ApiTagResponse(BaseModel):
    """Model for Tag response data."""
    id: int
    value: str
    created_by: str


class ApiFeatureTypeResponse(BaseModel):
    id: int
    name: str


class ApiFeatureResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    author: str
    type_id: int
    last_edited_by: str
    last_edited_at: datetime
    task: list[str]
    file_path: str
    released: bool
    severity: allure.severity_level

    feature_type: ApiFeatureTypeResponse
    feature_tags: list[ApiTagResponse]


class ApiTestRunResponse(BaseModel):
    id: int
    created_at: datetime
    name: str
    executed_by: str
    start: datetime | None
    end: datetime | None
    status: str
    report_status: str
    report: str | None
    traceback: str | None
    scenario_id: int
