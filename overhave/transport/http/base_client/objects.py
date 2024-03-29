import enum


class HttpMethod(enum.StrEnum):
    """HTTP methods enum."""

    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
