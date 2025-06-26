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
"""RoleMenu Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.model.sys_role_menu_model import RoleMenuModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_role_menu_schema import (
    RoleMenuQuery,
    RoleMenuDetail,
    RoleMenuCreate,
)
from src.main.app.core.service.base_service import BaseService


class RoleMenuService(BaseService[RoleMenuModel], ABC):
    @abstractmethod
    async def get_role_menu_by_page(
        self, *, role_menu_query: RoleMenuQuery, current_user: CurrentUser
    ) -> PageResult: ...

    @abstractmethod
    async def get_role_menu_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[RoleMenuDetail]: ...

    @abstractmethod
    async def export_role_menu_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def create_role_menu(
        self, *, role_menu_create: RoleMenuCreate, current_user: CurrentUser
    ) -> RoleMenuModel: ...

    @abstractmethod
    async def batch_create_role_menu(
        self,
        *,
        role_menu_create_list: List[RoleMenuCreate],
        current_user: CurrentUser,
    ) -> List[int]: ...

    @abstractmethod
    async def import_role_menu(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> List[RoleMenuCreate]: ...
