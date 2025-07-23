from typing import Generic, TypeVar, Optional, Dict, Any

from pydantic import BaseModel

# Define generic model variables
DataType = TypeVar("DataType")
T = TypeVar("T")

# Define default response codes and messages
DEFAULT_SUCCESS_CODE: int = 0
DEFAULT_FAIL_CODE: int = -1
DEFAULT_SUCCESS_MSG: str = "success"


class HttpResponse(BaseModel, Generic[T]):
    """
    Response base model for API responses.

    Attributes:
        msg: Response message
        code: Response status code
        data: Optional response data of generic model T
    """

    msg: str = DEFAULT_SUCCESS_MSG
    code: Optional[int] = DEFAULT_SUCCESS_CODE
    data: Optional[T] = None


# Example of a ResponseErrorEnum in Python
class ResponseErrorEnum:
    BAD_REQUEST = (400, "Bad Request")
    NOT_FOUND = (404, "Not Found")
    INTERNAL_ERROR = (500, "Internal Server Error")

    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg

    def get_code(self) -> int:
        return self._code

    def get_msg(self) -> str:
        return self._msg

    def __str__(self):
        return f"[{self._code}] {self._msg}"


def success(
    data: DataType = None,
    msg: Optional[str] = DEFAULT_SUCCESS_MSG,
    code: Optional[int] = DEFAULT_SUCCESS_CODE,
) -> Dict[str, Any]:
    """
    Generate a success response dictionary

    Args:
        data: Response data of generic model DataType
        msg: Success message
        code: Success status code

    Returns:
        Dict containing response data
    """
    response = {"code": code, "msg": msg}
    if data is not None:
        response["data"] = data
    return response


def fail(msg: str, code: int = DEFAULT_FAIL_CODE) -> Dict:
    """
    Generate a failure response dictionary

    Args:
        msg: Error message
        code: Error status code

    Returns:
        Dict containing error response
    """
    return {"code": code, "msg": msg}
