"""Business-related error codes."""

from http import HTTPStatus

from src.main.app.core.enums.base_error_code import ExceptionCode


class BusinessErrorCode:
    """Business-related error codes."""

    USER_NAME_EXISTS = ExceptionCode(code=HTTPStatus.CONFLICT, message="Username already exists")
    MENU_NAME_EXISTS = ExceptionCode(code=HTTPStatus.CONFLICT, message="Menu name already exists")

    RESOURCE_NOT_FOUND = ExceptionCode(code=HTTPStatus.NOT_FOUND, message="Requested resource not found")

    PARAMETER_ERROR = ExceptionCode(code=HTTPStatus.BAD_REQUEST, message="Parameter error")
