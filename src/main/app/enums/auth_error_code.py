# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
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
"""Authentication and authorization error codes (20000-29999)."""

from http import HTTPStatus

from src.main.app.core.enums.base_error_code import ExceptionCode


class AuthErrorCode:
    """Authentication and authorization error codes."""

    AUTH_FAILED = ExceptionCode(code=HTTPStatus.UNAUTHORIZED, message="Username or password error")
    TOKEN_EXPIRED = ExceptionCode(code=HTTPStatus.UNAUTHORIZED, message="Token has expired")
    OPENAPI_FORBIDDEN = ExceptionCode(code=HTTPStatus.FORBIDDEN, message="OpenAPI is not ready")
    MISSING_TOKEN = ExceptionCode(code=HTTPStatus.UNAUTHORIZED, message="Authentication token is missing")
