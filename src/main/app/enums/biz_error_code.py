# -*- coding: utf-8 -*-
# Copyright (c) 2025 Fast web
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

"""Business-related error codes (30000-39999)."""

from src.main.app.core.enums.base_error_code import CustomExceptionCode


class BusinessErrorCode(CustomExceptionCode):
    """Business-related error codes."""

    USER_NAME_EXISTS = (30001, "Username already exists")

