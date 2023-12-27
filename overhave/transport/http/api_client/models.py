from typing import Literal

from pydantic import BaseModel


class TokenRequestData(BaseModel):
    """Model for OAuth2 request data."""

    grant_type: Literal["password"] = "password"
    username: str
    password: str


class ApiTagResponse(BaseModel):
    """resp."""

    id: int
    value: str
    created_by: str


class ApiTagsResponse(BaseModel):
    """resp."""

    items: list[ApiTagResponse]
