"""Business-related error codes (30000-39999)."""

from http import HTTPStatus

from src.main.app.core.enums.base_error_code import ExceptionCode


class BusinessErrorCode(ExceptionCode):
    """Business-related error codes."""

    USER_NAME_EXISTS = (HTTPStatus.CONFLICT, "Username already exists")
    MENU_NAME_EXISTS = (HTTPStatus.CONFLICT, "Menu name already exists")

    RESOURCE_NOT_FOUND = (HTTPStatus.NOT_FOUND, "Requested resource not found")

    PARAMETER_ERROR = (HTTPStatus.BAD_REQUEST, "Parameter can not be null")
