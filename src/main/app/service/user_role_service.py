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
from src.main.app.model.user_role_model import UserRoleModel
from src.main.app.schema.user_role_schema import (
    ListUserRolesRequest,
    CreateUserRoleRequest,
    UserRole,
    UpdateUserRoleRequest,
    BatchDeleteUserRolesRequest,
    ExportUserRolesRequest,
    BatchCreateUserRolesRequest,
    BatchUpdateUserRolesRequest,
    ImportUserRolesRequest,
    ImportUserRole,
    BatchPatchUserRolesRequest,
)


class UserRoleService(BaseService[UserRoleModel], ABC):
    @abstractmethod
    async def get_user_role(
        self,
        *,
        id: int,
    ) -> UserRoleModel: ...

    @abstractmethod
    async def list_user_roles(
        self, *, req: ListUserRolesRequest
    ) -> tuple[list[UserRoleModel], int]: ...


    @abstractmethod
    async def create_user_role(self, *, req: CreateUserRoleRequest) -> UserRoleModel: ...

    @abstractmethod
    async def update_user_role(self, req: UpdateUserRoleRequest) -> UserRoleModel: ...

    @abstractmethod
    async def delete_user_role(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_user_roles(self, ids: list[int]) -> list[UserRoleModel]: ...

    @abstractmethod
    async def batch_create_user_roles(
        self,
        *,
        req: BatchCreateUserRolesRequest,
    ) -> list[UserRoleModel]: ...

    @abstractmethod
    async def batch_update_user_roles(
        self, req: BatchUpdateUserRolesRequest
    ) -> list[UserRoleModel]: ...

    @abstractmethod
    async def batch_patch_user_roles(
        self, req: BatchPatchUserRolesRequest
    ) -> list[UserRoleModel]: ...

    @abstractmethod
    async def batch_delete_user_roles(self, req: BatchDeleteUserRolesRequest): ...

    @abstractmethod
    async def export_user_roles_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_user_roles(self, req: ExportUserRolesRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_user_roles(self, req: ImportUserRolesRequest) -> list[ImportUserRole]: ...
