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
"""Standardized HTTP response model for API implementations."""

from typing import Generic, TypeVar, Optional, Any, Union
from pydantic import BaseModel, model_serializer
from src.main.app.common.enums.base_error_code import BaseErrorCode
from src.main.app.enums.biz_error_code import BusinessErrorCode

# Define generic type variables for response data
DataType = TypeVar("DataType")
T = TypeVar("T")

# Default response codes and messages
DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_FAIL_CODE: int = -1
DEFAULT_SUCCESS_MSG: str = "success"


class HttpResponse(BaseModel, Generic[T]):
    """Standardized API response model with success/failure constructors.

    Attributes:
        code: Numeric status code (HTTP status or business code)
        msg: Readable status message
        data: Optional typed response payload (default: None)
    """

    code: int = DEFAULT_SUCCESS_CODE
    msg: str = DEFAULT_SUCCESS_MSG
    data: Optional[T] = None

    @model_serializer
    def serialize_model(self) -> dict:
        """Custom serializer that conditionally excludes None data field."""

        if self.data is None:
            return {"code": self.code, "msg": self.msg}
        return {"code": self.code, "msg": self.msg, "data": self.data}

    @staticmethod
    def success(
        code: int = DEFAULT_SUCCESS_CODE, msg: str = DEFAULT_SUCCESS_MSG, data: Optional[T] = None
    ) -> "HttpResponse[T]":
        """Constructs a standardized success response.

        Args:
            code: Numeric status code (default: DEFAULT_SUCCESS_CODE)
            msg: Readable success message (default: DEFAULT_SUCCESS_MSG)
            data: Optional response payload data (default: None)

        Returns:
            HttpResponse[T]: Constructed success response instance

        Example:
            >>> HttpResponse.success(code=200, data={"id": 123})
            HttpResponse(code=200, msg='success', data={'id': 123})
        """
        return HttpResponse[T](code=code, msg=msg, data=data)

    @staticmethod
    def fail(msg: str = str, code: int = DEFAULT_FAIL_CODE, data: Optional[Any] = None) -> "HttpResponse[Any]":
        """Constructs a standardized error response.

        Args:
            msg: Error description message. If default str type is passed,
                will convert to string representation (default: str)
            code: Numeric error code (default: DEFAULT_FAIL_CODE)
            data: Optional additional error details (default: None)

        Returns:
            HttpResponse[Any]: Constructed error response instance

        Example:
            >>> HttpResponse.fail(msg="Not found", code=404)
            HttpResponse(code=404, msg='Not found', data=None)
        """
        return HttpResponse[Any](code=code, msg=msg, data=data)

    @staticmethod
    def fail_with_error(
        error: Union[BaseErrorCode, tuple[int, str]],  # Supports multiple error types
        extra_msg: Optional[str] = None,
    ) -> "HttpResponse[Any]":
        """Constructs an error response from various error type inputs.

        Provides a unified interface to create error responses from different error
        representations while maintaining consistent response format.

        Args:
            error: Error representation, which can be:
                - BaseErrorCode enum member
                - ErrorInfo object
                - Tuple of (error_code, error_message)
            extra_msg: Optional supplementary message to append to the error
                      message (default: None)

        Returns:
            HttpResponse[Any]: Constructed error response with the provided
                            error information.

        Examples:
            >>> HttpResponse.fail_with_error(BusinessErrorCode.VALIDATION_ERROR)
        """
        if isinstance(error, tuple) and len(error) == 2:
            code, msg = error
        elif hasattr(error, "code") and hasattr(error, "msg"):
            code, msg = error.code, error.msg
        else:
            code, msg = DEFAULT_FAIL_CODE, str(error)

        if extra_msg:
            msg = f"{msg}: {extra_msg}"

        return HttpResponse[Any](code=code, msg=msg)
