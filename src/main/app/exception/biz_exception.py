"""Business exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import HttpException
from src.main.app.enums.biz_error_code import BusinessErrorCode


class BusinessException(HttpException):
    def __init__(
        self,
        code: BusinessErrorCode,
        msg: Optional[Any] = None,
    ):
        super().__init__(code=code, msg=msg)
