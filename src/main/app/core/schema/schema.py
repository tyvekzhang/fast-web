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
"""Common schema with data validation."""

from typing import List, Any, Optional

from pydantic import BaseModel


class PageResult(BaseModel):
    """Paginated query result container.

    Attributes:
        records: List of items in current page (default: None)
        total: Total number of items across all pages (default: 0)
    """

    records: List[Any] = None
    total: int = 0


class Token(BaseModel):
    """Represents an authentication token with metadata.

    Attributes:
        access_token: JWT access token string.
        token_type: Type of token (e.g., 'Bearer').
        expired_at: Unix timestamp when token expires.
        refresh_token: Token used to refresh access.
        re_expired_at: Unix timestamp when refresh token expires.
    """

    access_token: str
    token_type: str
    expired_at: int
    refresh_token: str
    re_expired_at: int


class CurrentUser(BaseModel):
    """Minimal user identity information for authenticated requests.

    Attributes:
        user_id: Unique identifier of the authenticated user.
    """

    user_id: int


class SortItem(BaseModel):
    """Single field sorting specification.

    Attributes:
        field: Name of the field to sort by
        order: Sort direction ('asc' or 'desc')
    """

    field: str
    order: str


class BasePage(BaseModel):
    """Pagination parameters for API endpoints.

    Attributes:
        current: Current page number (1-based).
        page_size: Number of items per page.
        count: Flag to request total count of items.
    """

    current: int = 1
    page_size: int = 10
    count: bool = False
    sort_str: Optional[str] = None
