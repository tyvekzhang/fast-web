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
"""Business exception for the application."""

from typing import Optional, Any

from src.main.app.common.exception.base_exception import BaseError
from src.main.app.enums.biz_error_code import BusinessErrorCode


class BusinessException(BaseError):
    def __init__(
            self,
            code: BusinessErrorCode,
            msg: Optional[Any] = None,
    ):
        super().__init__(code=code, msg=msg)