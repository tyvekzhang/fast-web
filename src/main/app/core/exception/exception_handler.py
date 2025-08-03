"""Exception handlers module for FastAPI application."""

import textwrap
import traceback
from http import HTTPStatus
from typing import Dict, Any, Optional

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.utils import is_body_allowed_for_status_code
from loguru import logger
from pydantic_core._pydantic_core import ValidationError  # noqa
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.main.app.core.config.config_manager import load_config
from src.main.app.core.enums.enum import CommonErrorCode
from src.main.app.core.exception import HTTPException

config = load_config()


async def extract_request_data(request: Request) -> Dict[str, Any]:
    """
    Extract request data based on content type.
    """
    data = {}
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            data["json"] = await request.json()
        elif (
            "application/x-www-form-urlencoded" in content_type
            or "multipart/form-data" in content_type
        ):
            form = await request.form()
            form_data = {}
            for key, value in form.items():
                if (
                    not hasattr(value, "filename")
                    and not hasattr(value, "file")
                    and not hasattr(value, "files")
                ):
                    form_data[key] = value
                else:
                    form_data[key] = f"<file: {value.filename}>"
            if form_data:
                data["form"] = form_data
        else:
            body = await request.body()
            if body:
                try:
                    data["body"] = body.decode("utf-8")
                except UnicodeDecodeError:
                    data["body"] = f"<binary: {len(body)} bytes>"
    except Exception as e:
        data["error"] = f"Failed to parse request data: {str(e)}"

    return data


def collect_request_info(request: Request) -> Dict[str, Any]:
    """
    Collect comprehensive request information for logging.
    """
    return {
        "path": request.url.path,
        "method": request.method,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": f"{request.client.host}:{request.client.port}" if request.client else None,
    }


def log_exception(exc: Exception, request_info: Dict[str, Any]) -> None:
    """
    Log exception with full context information.
    """
    logger.error(
        textwrap.dedent(f"""\
    Unhandled exception,
    exception_type: {type(exc).__name__},
    exception_message: {str(exc)},
    traceback: {traceback.format_exc()},
    request: {request_info},
    """)
    )


def build_error_response(
    exc: Exception,
    request: Request,
    status_code: int,
    headers: Optional[Dict[str, str]] = None,
) -> Response:
    """
    Build standardized error response.
    """
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)

    error_message = "Internal server error"
    if config.server.debug:
        error_message = str(exc)

    return JSONResponse(
        content={
            "error": {
                "code": CommonErrorCode.INTERNAL_SERVER_ERROR.code,
                "message": error_message,
            }
        }
    )


async def global_exception_handler(request: Request, exc: Exception) -> Response:
    """
    Handler for all uncaught exceptions.
    """
    request_info = collect_request_info(request)

    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 记录日志
    log_exception(exc, request_info)

    status_code = getattr(exc, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR)
    headers = getattr(exc, "headers", None)
    return build_error_response(exc, request, status_code, headers)


async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handler for pydantic ValidationError.
    """
    request_info = collect_request_info(request)
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 记录日志
    log_exception(exc, request_info)

    code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return JSONResponse(content={"error": {"code": code, "message": str(exc.errors())}})


def is_auth_errors_code(error_code: int):
    if error_code == HTTPStatus.UNAUTHORIZED.value:
        return True
    return False


async def custom_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for custom HTTPException.
    """
    request_info = collect_request_info(request)
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 记录日志
    log_exception(exc, request_info)
    error_info = exc.code
    error_code = error_info.code
    if is_auth_errors_code(error_code):
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            content={"code": exc.code, "message": exc.message},
        )

    return JSONResponse(
        content={
            "error": {
                "code": error_code,
                "message": exc.message,
            }
        }
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handler for RequestValidationError.
    """
    request_info = collect_request_info(request)
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 记录日志
    log_exception(exc, request_info)

    return JSONResponse(
        content={
            "error": {
                "code": HTTPStatus.UNPROCESSABLE_ENTITY.value,
                "message": str(exc.errors()),
            }
        }
    )


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for StarletteHTTPException.
    """
    request_info = collect_request_info(request)
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 记录日志
    log_exception(exc, request_info)

    return await http_exception_handler(request, exc)


# 修改为：
async def jwt_exception_handler(request: Request):
    """
    Handler for JWT-related exceptions.
    """
    request_info = collect_request_info(request)
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # ✅ 可以记录一个模拟异常
    class JWTException(Exception):
        pass

    log_exception(JWTException("JWT token expired or invalid"), request_info)

    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED.value,
        content={
            "code": HTTPStatus.UNAUTHORIZED.value,
            "message": "Your token has expired. Please log in again.",
        },
    )
