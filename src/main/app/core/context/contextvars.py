"""Context variable for storing current user info."""

from contextvars import ContextVar
from typing import Optional

current_user_id: ContextVar[Optional[int]] = ContextVar(
    "current_user_id",
    default=None
)
