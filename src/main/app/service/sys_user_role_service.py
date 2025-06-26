"""UserRole Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.model.sys_user_role_model import UserRoleModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_user_role_schema import (
    UserRoleQuery,
    UserRoleDetail,
    UserRoleCreate,
)
from src.main.app.core.service.base_service import BaseService


class UserRoleService(BaseService[UserRoleModel], ABC):
    @abstractmethod
    async def get_user_role_by_page(
        self, *, user_role_query: UserRoleQuery, current_user: CurrentUser
    ) -> PageResult: ...

    @abstractmethod
    async def get_user_role_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[UserRoleDetail]: ...

    @abstractmethod
    async def export_user_role_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def create_user_role(
        self, *, user_role_create: UserRoleCreate, current_user: CurrentUser
    ) -> UserRoleModel: ...

    @abstractmethod
    async def batch_create_user_role(
        self,
        *,
        user_role_create_list: List[UserRoleCreate],
        current_user: CurrentUser,
    ) -> List[int]: ...

    @abstractmethod
    async def import_user_role(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> List[UserRoleCreate]: ...
