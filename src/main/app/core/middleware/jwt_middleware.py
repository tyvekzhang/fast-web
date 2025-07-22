"""JWT middleware for FastAPI authentication"""

import http

from fastapi import Request
from jose import JWTError
from loguru import logger
from starlette.responses import JSONResponse

from src.main.app.core import security, constant
from src.main.app.core.config import config_manager
from src.main.app.core.context.contextvars import current_user_id
from src.main.app.core.enums.enum import MediaTypeEnum
from src.main.app.core.schema import UserCredential
from src.main.app.enums.auth_error_code import AuthErrorCode

# Load configuration
server_config = config_manager.load_server_config()
security_config = config_manager.load_security_config()


async def jwt_middleware(request: Request, call_next):
    ctx_token: UserCredential | None = None
    try:
        raw_url_path = request.url.path
        if not raw_url_path.__contains__(
            server_config.api_prefix
        ) or raw_url_path.__contains__(MediaTypeEnum.JSON.value):
            if security_config.enable_swagger:
                return await call_next(request)
            else:
                return JSONResponse(
                    status_code=http.HTTPStatus.FORBIDDEN,
                    content={
                        "code": AuthErrorCode.OPENAPI_FORBIDDEN.code,
                        "message": AuthErrorCode.OPENAPI_FORBIDDEN.message,
                    },
                )

        white_list_routes = [
            r.strip() for r in security_config.white_list_routes.split(",")
        ]
        request_url_path = (
            server_config.api_prefix
            + raw_url_path.split(server_config.api_prefix)[1]
        )
        if request_url_path in white_list_routes:
            return await call_next(request)

        if not security_config.enable:
            return await call_next(request)

        print(request.headers)
        auth_header = request.headers.get(constant.AUTHORIZATION)
        if auth_header:
            try:
                token = auth_header.split(" ")[-1]
                security.validate_token(token)
                user_id = security.get_user_id(token)

                ctx_token = current_user_id.set(user_id)

            except JWTError as e:
                logger.error(e)
                return JSONResponse(
                    status_code=http.HTTPStatus.UNAUTHORIZED,
                    content={
                        "code": AuthErrorCode.TOKEN_EXPIRED.code,
                        "message": AuthErrorCode.TOKEN_EXPIRED.message,
                    },
                )
        else:
            return JSONResponse(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                content={
                    "code": AuthErrorCode.MISSING_TOKEN.code,
                    "message": AuthErrorCode.MISSING_TOKEN.message,
                },
            )

        response = await call_next(request)
        return response

    finally:
        if ctx_token is not None:
            current_user_id.reset(ctx_token)
