"""Authentication and authorization error codes (20000-29999)."""

from http import HTTPStatus

from src.main.app.core.enums.base_error_code import ExceptionCode


class AuthErrorCode(ExceptionCode):
    """Authentication and authorization error codes."""

    AUTH_FAILED = (HTTPStatus.UNAUTHORIZED, "Username or password error")
    TOKEN_EXPIRED = (20002, "Token has expired")
    OPENAPI_FORBIDDEN = (20003, "OpenAPI is not ready")
    MISSING_TOKEN = (20004, "Authentication token is missing")
