# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
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
"""User Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile
from starlette.responses import StreamingResponse

from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.user_model import UserModel
from src.main.app.schema.user_schema import (
    UserQuery,
    UserDetail,
    CreateUserRequest,
    UserPage,
)


class UserService(BaseService[UserModel], ABC):
    @abstractmethod
    async def create_user(
        self, *, create_user: CreateUserRequest
    ) -> UserModel: ...

    @abstractmethod
    async def find_by_id(self, *, id: int) -> UserPage: ...

    @abstractmethod
    async def get_user_by_page(
        self, *, user_query: UserQuery, current_user: CurrentUser
    ) -> PageResult: ...

    @abstractmethod
    async def get_user_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[UserDetail]: ...

    @abstractmethod
    async def export_user_page(
        self, *, ids: list[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def batch_create_user(
        self,
        *,
        user_create_list: list[CreateUserRequest],
        current_user: CurrentUser,
    ) -> list[int]: ...

    @abstractmethod
    async def import_user(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> list[CreateUserRequest]: ...
