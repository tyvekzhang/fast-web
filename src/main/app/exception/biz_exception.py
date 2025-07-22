"""Business exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import HTTPException
from src.main.app.enums.biz_error_code import BusinessErrorCode


class BusinessException(HTTPException):
    def __init__(
        self,
        code: BusinessErrorCode,
        msg: Optional[Any] = None,
    ):
        super().__init__(code=code, msg=msg)
