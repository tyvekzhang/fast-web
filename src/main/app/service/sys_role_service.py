"""Role Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.model.sys_role_model import RoleModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_role_schema import (
    RoleQuery,
    RoleDetail,
    RoleCreate,
)
from src.main.app.core.service.base_service import BaseService


class RoleService(BaseService[RoleModel], ABC):
    @abstractmethod
    async def get_role_by_page(
        self, *, role_query: RoleQuery, current_user: CurrentUser
    ) -> PageResult: ...

    @abstractmethod
    async def get_role_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[RoleDetail]: ...

    @abstractmethod
    async def export_role_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def create_role(
        self, *, role_create: RoleCreate, current_user: CurrentUser
    ) -> RoleModel: ...

    @abstractmethod
    async def batch_create_role(
        self, *, role_create_list: List[RoleCreate], current_user: CurrentUser
    ) -> List[int]: ...

    @abstractmethod
    async def import_role(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> List[RoleCreate]: ...
