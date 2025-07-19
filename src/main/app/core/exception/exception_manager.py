"""Common module exception"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jwt import PyJWTError
from pydantic_core._pydantic_core import ValidationError  # noqa
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.main.app.core.exception import exception_handler
from src.main.app.core.exception.custom_exception import HttpException


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers to the FastAPI application"""

    # Register handlers using add_exception_handler method
    app.add_exception_handler(
        Exception, exception_handler.global_exception_handler
    )
    app.add_exception_handler(
        ValidationError, exception_handler.validation_exception_handler
    )

    app.add_exception_handler(
        HttpException, exception_handler.custom_exception_handler
    )

    app.add_exception_handler(
        StarletteHTTPException, exception_handler.custom_http_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError,
        exception_handler.request_validation_exception_handler,
    )
    app.add_exception_handler(
        PyJWTError, exception_handler.jwt_exception_handler
    )
