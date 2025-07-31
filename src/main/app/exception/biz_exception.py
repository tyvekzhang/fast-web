"""Business exception for the application."""
from dataclasses import dataclass
from typing import Optional, Any

from src.main.app.core.exception import HTTPException
from src.main.app.enums.biz_error_code import BusinessErrorCode


@dataclass
class BusinessException(HTTPException):
    code: BusinessErrorCode
    message: Optional[str] = None
    details: Optional[Any] = None
