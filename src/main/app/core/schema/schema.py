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
