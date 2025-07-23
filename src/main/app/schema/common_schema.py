"""Common schema"""

from typing import Optional, Dict, Any, List

from pydantic import BaseModel


class Token(BaseModel):
    """
    Token schema
    """

    access_token: str
    token_type: str
    expired_at: int
    refresh_token: str
    re_expired_at: int


class CurrentUser(BaseModel):
    """
    CurrentUser schema
    """

    id: int


class PageBase(BaseModel):
    current: Optional[int] = 1
    pageSize: Optional[int] = 10
    sorter: Optional[str] = None


class FilterParams(PageBase):
    """
    FilterParams schema
    """

    filter_by: Optional[Dict[str, Any]] = None
    like: Optional[Dict[str, str]] = None


class ModelBaseParams(BaseModel):
    """
    ModelBaseParams for all data object
    """

    id: int
    create_time: int
    update_time: Optional[int] = None


class PageResult(BaseModel):
    records: List[Any] = None
    total: int = 0
