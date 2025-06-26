# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Exception handlers module for FastAPI application."""

import http
import textwrap
import traceback
from typing import Dict, Any, Optional

from pydantic_core._pydantic_core import ValidationError  # noqa

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, Response
from fastapi.utils import is_body_allowed_for_status_code
from loguru import logger
from src.main.app.core.config.config_manager import load_config
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.main.app.core.enums.enum import CommonErrorCode
from src.main.app.core.exception import CustomException

config = load_config()


async def extract_request_data(request: Request) -> Dict[str, Any]:
    """
    Extract request data based on content type.

    Args:
        request: The FastAPI request object

    Returns:
        Dictionary containing parsed request data
    """
    data = {}

    # Try to get request data based on content type
    content_type = request.headers.get("content-type", "")

    try:
        if "application/json" in content_type:
            data["json"] = await request.json()
        elif (
            "application/x-www-form-urlencoded" in content_type
            or "multipart/form-data" in content_type
        ):
            # Get form data but exclude files
            form = await request.form()
            form_data = {}
            for key, value in form.items():
                # Check if it's a file upload (UploadFile instance)
                if not hasattr(value, "filename"):  # Not a file
                    form_data[key] = value
                else:
                    # Record that a file was present but not included
                    form_data[key] = f"<file: {value.filename}>"

            if form_data:
                data["form"] = form_data
        else:
            # Get raw body
            body = await request.body()
            if body:
                # Try to decode as string, if fails save as binary indicator
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

    Args:
        request: The FastAPI request object

    Returns:
        Dictionary containing request metadata
    """
    return {
        "path": request.url.path,
        "method": request.method,
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
        "client": f"{request.client.host}:{request.client.port}"
        if request.client
        else None,
    }


def log_exception(exc: Exception, request_info: Dict[str, Any]) -> None:
    """
    Log exception with full context information.

    Args:
        exc: The exception that was raised
        request_info: Dictionary containing request information
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

    Args:
        exc: The exception that was raised
        request: The FastAPI request object
        status_code: HTTP status code for the response
        headers: Optional response headers

    Returns:
        JSONResponse with error details
    """
    # Check if response body is allowed for this status code
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)

    # Don't expose detailed error messages in production
    error_message = "Internal server error"
    if config.server.debug:
        error_message = str(exc)

    return JSONResponse(
        {
            "code": CommonErrorCode.INTERNAL_SERVER_ERROR.code,
            "msg": error_message,
        },
        status_code=status_code,
        headers=headers,
    )


async def global_exception_handler(
    request: Request, exc: Exception
) -> Response:
    """
    Handler for all uncaught exception.

    This handler captures all unhandled exception, logs them with request context,
    and returns a standardized error response to the client.

    Args:
        request: The FastAPI request object
        exc: The exception that was raised

    Returns:
        Response object with appropriate error information
    """
    # Collect request information
    request_info = collect_request_info(request)

    # Get request data
    try:
        request_data = await extract_request_data(request)
        if request_data:
            request_info["data"] = request_data
    except Exception as e:
        request_info["data_error"] = str(e)

    # Log the exception with context
    log_exception(exc, request_info)

    # Determine response status code and headers
    status_code = getattr(
        exc, "status_code", http.HTTPStatus.INTERNAL_SERVER_ERROR
    )
    headers = getattr(exc, "headers", None)

    # Build and return error response
    return build_error_response(exc, request, status_code, headers)


async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Asynchronous exception handler for validation exception.

    Args:
        request (Request): The request instance containing all request details.
        exc (ValidationError): The exception instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(status_code):
        return Response(status_code=status_code, headers=headers)
    return JSONResponse(
        {
            "code": CommonErrorCode.INTERNAL_SERVER_ERROR.code,
            "msg": str(exc).split("For further")[0],
        },
        status_code=status_code,
    )


def is_auth_errors_code(exc: CustomException) -> bool:
    if str(exc.code).startswith("20"):
        return True
    return False


async def custom_exception_handler(request: Request, exc: CustomException):
    """
    Asynchronous handler for CustomException.
    """
    if is_auth_errors_code(exc):
        return JSONResponse(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            content={"code": exc.code, "msg": exc.msg},
        )
    return JSONResponse(
        {"code": exc.code, "msg": exc.msg},
    )


async def custom_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    """
    Asynchronous handler for StarletteHTTPException.

    Args:
        request (Request): The request instance containing all request details.
        exc (StarletteHTTPException): The StarletteHTTPException instance.

    Returns:
        Response: A Response object which could be a basic Response or a JSONResponse,
                  depending on whether a response body is allowed for the given status code.
    """
    return await http_exception_handler(request, exc)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Asynchronous handler for RequestValidationError.

    Args:
        request (Request): The request instance containing all request details.
        exc (RequestValidationError): The RequestValidationError instance.

    Returns:
        Response: A JSONResponse object which contain code and msg,
    """
    return JSONResponse(
        {
            "code": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            "msg": str(exc.errors()),
        },
    )


async def jwt_exception_handler() -> JSONResponse:
    """
    Asynchronous handler for JWT-related exception.

    Returns:
        JSONResponse: A JSON response with an error code and message.
    """
    return JSONResponse(
        status_code=http.HTTPStatus.UNAUTHORIZED,
        content={
            "code": http.HTTPStatus.UNAUTHORIZED,
            "msg": "Your token has expired. Please log in again.",
        },
    )
