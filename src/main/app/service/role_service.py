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
from src.main.app.model.role_model import RoleModel
from src.main.app.schema.role_schema import (
    ListRolesRequest,
    CreateRoleRequest,
    Role,
    UpdateRoleRequest,
    BatchDeleteRolesRequest,
    ExportRolesRequest,
    BatchCreateRolesRequest,
    BatchUpdateRolesRequest,
    ImportRolesRequest,
    ImportRole,
    BatchPatchRolesRequest,
)


class RoleService(BaseService[RoleModel], ABC):
    @abstractmethod
    async def get_role(
        self,
        *,
        id: int,
    ) -> RoleModel: ...

    @abstractmethod
    async def list_roles(self, *, req: ListRolesRequest) -> tuple[list[RoleModel], int]: ...

    @abstractmethod
    async def create_role(self, *, req: CreateRoleRequest) -> RoleModel: ...

    @abstractmethod
    async def update_role(self, req: UpdateRoleRequest) -> RoleModel: ...

    @abstractmethod
    async def delete_role(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_roles(self, ids: list[int]) -> list[RoleModel]: ...

    @abstractmethod
    async def batch_create_roles(
        self,
        *,
        req: BatchCreateRolesRequest,
    ) -> list[RoleModel]: ...

    @abstractmethod
    async def batch_update_roles(self, req: BatchUpdateRolesRequest) -> list[RoleModel]: ...

    @abstractmethod
    async def batch_patch_roles(self, req: BatchPatchRolesRequest) -> list[RoleModel]: ...

    @abstractmethod
    async def batch_delete_roles(self, req: BatchDeleteRolesRequest): ...

    @abstractmethod
    async def export_roles_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_roles(self, req: ExportRolesRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_roles(self, req: ImportRolesRequest) -> list[ImportRole]: ...
