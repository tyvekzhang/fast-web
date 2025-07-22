"""User Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Set

from fastapi import UploadFile
from starlette.responses import StreamingResponse

from src.main.app.core.schema import PageResult, Token, CurrentUser
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.role_model import RoleModel
from src.main.app.model.user_model import UserModel
from src.main.app.schema.menus_schema import Menu
from src.main.app.schema.users_schema import (
    UserQuery,
    UserDetail,
    CreateUserRequest,
    LoginForm,
    UserPage,
)


class UserService(BaseService[UserModel], ABC):
    @abstractmethod
    async def create_user(
        self, *, create_user: CreateUserRequest
    ) -> UserModel: ...

    @abstractmethod
    async def login(self, *, login_form: LoginForm) -> Token: ...

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

    @abstractmethod
    async def get_roles(self, id: int) -> tuple[Set[str], list[RoleModel]]: ...

    @abstractmethod
    async def get_menus(
        self, id: int, role_models: list[RoleModel]
    ) -> list[Menu]: ...
