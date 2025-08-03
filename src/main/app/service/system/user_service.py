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
"""Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.system.user_model import UserModel
from src.main.app.schema.system.user_schema import (
    ListUsersRequest,
    CreateUserRequest,
    User,
    UpdateUserRequest,
    BatchDeleteUsersRequest,
    ExportUsersRequest,
    BatchCreateUsersRequest,
    BatchUpdateUsersRequest,
    ImportUsersRequest,
    ImportUser,
    BatchPatchUsersRequest,
)


class UserService(BaseService[UserModel], ABC):
    @abstractmethod
    async def get_user(
        self,
        *,
        id: int,
    ) -> UserModel: ...

    @abstractmethod
    async def list_users(self, *, req: ListUsersRequest) -> tuple[list[UserModel], int]: ...

    @abstractmethod
    async def get_children_recursively(
        self, *, parent_data: list[UserModel], schema_class: Type[User]
    ) -> list[User]: ...

    @abstractmethod
    async def create_user(self, *, req: CreateUserRequest) -> UserModel: ...

    @abstractmethod
    async def update_user(self, req: UpdateUserRequest) -> UserModel: ...

    @abstractmethod
    async def delete_user(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_users(self, ids: list[int]) -> list[UserModel]: ...

    @abstractmethod
    async def batch_create_users(
        self,
        *,
        req: BatchCreateUsersRequest,
    ) -> list[UserModel]: ...

    @abstractmethod
    async def batch_update_users(self, req: BatchUpdateUsersRequest) -> list[UserModel]: ...

    @abstractmethod
    async def batch_patch_users(self, req: BatchPatchUsersRequest) -> list[UserModel]: ...

    @abstractmethod
    async def batch_delete_users(self, req: BatchDeleteUsersRequest): ...

    @abstractmethod
    async def export_users_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_users(self, req: ExportUsersRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_users(self, req: ImportUsersRequest) -> list[ImportUser]: ...
