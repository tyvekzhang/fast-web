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
"""Base exception class for the application."""

from typing import Optional, Any

from src.main.app.core.enums import CustomExceptionCode


class CustomException(Exception):
    """Base exception class for all custom exception in the application.

    Attributes:
        code: The code enum member from BaseErrorCode or its subclasses.
        msg: Optional additional msg about the error.
    """

    def __init__(
        self,
        code: CustomExceptionCode,
        msg: Optional[Any] = None,
    ):
        self.code = code.code
        self.msg = msg or code.msg
        super().__init__(self.msg)

    def __str__(self) -> str:
        """Returns string representation of the error."""
        return f"{self.code}: {self.msg}"

    def to_dict(self) -> dict:
        """Converts the exception to a dictionary for API responses.

        Returns:
            A dictionary containing error code, message, and msg (if any).
        """
        result = {
            "code": self.code,
            "msg": self.msg,
        }
        return result
