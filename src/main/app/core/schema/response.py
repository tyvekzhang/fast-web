"""Standardized HTTP response model for API implementations."""

from typing import Generic, TypeVar, Optional, Any, Union
from pydantic import BaseModel, model_serializer

from src.main.app.core.enums import ExceptionCode

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
        message: Readable status message
        data: Optional typed response payload (default: None)
    """

    code: int = DEFAULT_SUCCESS_CODE
    message: str = DEFAULT_SUCCESS_MSG
    data: Optional[T] = None

    @model_serializer
    def serialize_model(self) -> dict:
        """Custom serializer that conditionally excludes None data field."""

        if self.data is None:
            return {"code": self.code, "message": self.message}
        return {"code": self.code, "message": self.message, "data": self.data}

    @staticmethod
    def success(
        data: Optional[T] = None,
        code: int = DEFAULT_SUCCESS_CODE,
        message: str = DEFAULT_SUCCESS_MSG,
    ) -> "HttpResponse[T]":
        """Constructs a standardized success response.

        Args:
            code: Numeric status code (default: DEFAULT_SUCCESS_CODE)
            message: Readable success message (default: DEFAULT_SUCCESS_MSG)
            data: Optional response payload data (default: None)

        Returns:
            HttpResponse[T]: Constructed success response instance
        """
        return HttpResponse[T](code=code, message=message, data=data)

    @staticmethod
    def fail(
        message: str = str,
        code: int = DEFAULT_FAIL_CODE,
        data: Optional[Any] = None,
    ) -> "HttpResponse[Any]":
        """Constructs a standardized error response.

        Args:
            message: Error description message. If default str type is passed,
                will convert to string representation (default: str)
            code: Numeric error code (default: DEFAULT_FAIL_CODE)
            data: Optional additional error details (default: None)

        Returns:
            HttpResponse[Any]: Constructed error response instance
        """
        return HttpResponse[Any](code=code, message=message, data=data)

    @staticmethod
    def fail_with_error(
        error: Union[ExceptionCode, tuple[int, str]],  # Supports multiple error types
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
        """
        if isinstance(error, tuple) and len(error) == 2:
            code, message = error
        elif hasattr(error, "code") and hasattr(error, "message"):
            code, message = error.code, error.message
        else:
            code, message = DEFAULT_FAIL_CODE, str(error)

        if extra_msg:
            message = f"{message}: {extra_msg}"

        return HttpResponse[Any](code=code, message=message)
