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

from starlette.responses import StreamingResponse

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.role_menu_model import RoleMenuModel
from src.main.app.schema.role_menu_schema import (
    ListRoleMenusRequest,
    CreateRoleMenuRequest,
    UpdateRoleMenuRequest,
    BatchDeleteRoleMenusRequest,
    ExportRoleMenusRequest,
    BatchCreateRoleMenusRequest,
    BatchUpdateRoleMenusRequest,
    ImportRoleMenusRequest,
    ImportRoleMenu,
    BatchPatchRoleMenusRequest,
)


class RoleMenuService(BaseService[RoleMenuModel], ABC):
    @abstractmethod
    async def get_role_menu(
        self,
        *,
        id: int,
    ) -> RoleMenuModel: ...

    @abstractmethod
    async def list_role_menus(
        self, *, req: ListRoleMenusRequest
    ) -> tuple[list[RoleMenuModel], int]: ...

    @abstractmethod
    async def create_role_menu(self, *, req: CreateRoleMenuRequest) -> RoleMenuModel: ...

    @abstractmethod
    async def update_role_menu(self, req: UpdateRoleMenuRequest) -> RoleMenuModel: ...

    @abstractmethod
    async def delete_role_menu(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_role_menus(self, ids: list[int]) -> list[RoleMenuModel]: ...

    @abstractmethod
    async def batch_create_role_menus(
        self,
        *,
        req: BatchCreateRoleMenusRequest,
    ) -> list[RoleMenuModel]: ...

    @abstractmethod
    async def batch_update_role_menus(
        self, req: BatchUpdateRoleMenusRequest
    ) -> list[RoleMenuModel]: ...

    @abstractmethod
    async def batch_patch_role_menus(
        self, req: BatchPatchRoleMenusRequest
    ) -> list[RoleMenuModel]: ...

    @abstractmethod
    async def batch_delete_role_menus(self, req: BatchDeleteRoleMenusRequest): ...

    @abstractmethod
    async def export_role_menus_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_role_menus(self, req: ExportRoleMenusRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_role_menus(self, req: ImportRoleMenusRequest) -> list[ImportRoleMenu]: ...
