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
"""Enumerations module. Contains commonly used enum types for the application."""

from enum import Enum

from src.main.app.core.enums import ExceptionCode


class SortEnum(str, Enum):
    """Enumeration for sorting directions."""

    ascending = "asc"
    descending = "desc"


class TokenTypeEnum(str, Enum):
    """Enumeration for token types in authentication."""

    access = "access"
    refresh = "refresh"
    bearer = "Bearer"


class DBTypeEnum(str, Enum):
    """Enumeration for supported database types."""

    PGSQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


class MediaTypeEnum(str, Enum):
    """Enumeration for media/content types."""

    JSON = ".json"


class CommonErrorCode:
    """Error codes for core domain."""

    INTERNAL_SERVER_ERROR = ExceptionCode(code=-1, message="Internal server exception")
