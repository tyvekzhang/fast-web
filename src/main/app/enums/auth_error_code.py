"""Authentication and authorization error codes (20000-29999)."""

from src.main.app.core.enums.base_error_code import CustomExceptionCode


class AuthErrorCode(CustomExceptionCode):
    """Authentication and authorization error codes."""

    AUTH_FAILED = (20001, "Username or password error")
    TOKEN_EXPIRED = (20002, "Token has expired")
    OPENAPI_FORBIDDEN = (20003, "OpenAPI is not ready")
    MISSING_TOKEN = (20004, "Authentication token is missing")
