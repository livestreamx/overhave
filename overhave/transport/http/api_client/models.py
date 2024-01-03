import enum
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
    """Model for Feature Type response data."""

    id: int
    name: str


class ApiFeatureResponse(BaseModel):
    """Model for Feature response data."""

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
    """Model for TestRun response data."""

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


class ApiEmulationStatus(enum.StrEnum):
    """Enum for Emulation Status."""

    CREATED = "CREATED"
    REQUESTED = "REQUESTED"
    READY = "READY"
    ERROR = "ERROR"


class ApiTestUserResponse(BaseModel):
    """Model for TestUser response data."""

    id: int
    created_at: datetime
    key: str
    name: str
    created_by: str
    specification: dict[str, str | None]
    feature_type_id: int
    feature_type: ApiFeatureTypeResponse
    allow_update: bool
    changed_at: datetime


class ApiEmulationResponse(BaseModel):
    """Model for Emulation response data."""

    id: int
    command: str
    test_user: ApiTestUserResponse


class ApiEmulationRunResponse(BaseModel):
    """Model for EmulationRun response data."""

    id: int
    emulation_id: int
    changed_at: datetime
    status: ApiEmulationStatus
    port: int | None
    initiated_by: str
    emulation: ApiEmulationResponse
