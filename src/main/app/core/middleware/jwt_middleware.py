"""JWT middleware for FastAPI authentication"""

import http

from fastapi import Request
from jose import JWTError
from loguru import logger
from starlette.responses import JSONResponse

from src.main.app.core import security, constant
from src.main.app.core.config import config_manager
from src.main.app.core.enums.enum import MediaTypeEnum
from src.main.app.enums.auth_error_code import AuthErrorCode

# Load configuration
server_config = config_manager.load_server_config()
security_config = config_manager.load_security_config()


async def jwt_middleware(request: Request, call_next):
    # Check if URL contains API version and is not JSON media type
    raw_url_path = request.url.path
    if not raw_url_path.__contains__(
        server_config.api_version
    ) or raw_url_path.__contains__(MediaTypeEnum.JSON.value):
        if security_config.enable_swagger:
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=http.HTTPStatus.FORBIDDEN,
                content={
                    "code": AuthErrorCode.OPENAPI_FORBIDDEN.code,
                    "msg": AuthErrorCode.OPENAPI_FORBIDDEN.msg,
                },
            )

    # Check if route is in whitelist
    white_list_routes = [
        router.strip()
        for router in security_config.white_list_routes.split(",")
    ]
    request_url_path = (
        server_config.api_version
        + raw_url_path.split(server_config.api_version)[1]
    )
    if request_url_path in white_list_routes:
        return await call_next(request)

    # Disable jwt parse
    if not security_config.enable:
        return await call_next(request)

    # Validate JWT token
    auth_header = request.headers.get(constant.AUTHORIZATION)
    if auth_header:
        try:
            token = auth_header.split(" ")[-1]
            security.validate_token(token)
            user_id = security.get_user_id(token)
            request.state.user_id = user_id
        except JWTError as e:
            logger.error(f"{e}")
            return JSONResponse(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                content={
                    "code": AuthErrorCode.TOKEN_EXPIRED.code,
                    "msg": AuthErrorCode.TOKEN_EXPIRED.msg,
                },
            )
    else:
        return JSONResponse(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            content={
                "code": AuthErrorCode.MISSING_TOKEN.code,
                "msg": AuthErrorCode.MISSING_TOKEN.msg,
            },
        )

    return await call_next(request)
