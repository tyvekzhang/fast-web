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
"""Common schema with data validation."""

from typing import Optional, TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")


class ListResult(BaseModel, Generic[T]):
    """Paginated query result container.

    Attributes:
        records: List of items in current page
        total: Total number of items across all pages
    """

    records: list[T] = Field(default_factory=list)
    total: int = 0


class UserCredential(BaseModel):
    """Represents an authentication user credential with metadata.

    Attributes:
        access_token: JWT access token string.
        expired_in: Access token expiration time, second.
        refresh_token: Token used to refresh access.
    """

    access_token: str
    expired_in: int = 7200
    refresh_token: str


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


class PaginationRequest(BaseModel):
    """
    Pagination parameters for API endpoints.

    Attributes:

        current: Current page number (1-based).
        page_size: Number of items per page.
        count: Flag to request total count of items.
    """

    current: int = Field(
        default=1, gt=0, description="Current page number (1-based)"
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Number of items per page (1-1000)",
    )
    count: bool = Field(
        default=True, description="Flag to request total count of items"
    )
    sort_str: Optional[str] = Field(
        default=None, description="Optional sorting string, eg:"
    )
