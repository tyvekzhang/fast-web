"""Auth Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set


from src.main.app.core.schema import UserCredential
from src.main.app.model.role_model import RoleModel
from src.main.app.schema.menus_schema import Menu
from src.main.app.schema.users_schema import (
    SignInWithEmailAndPasswordRequest,
)


class AuthService(ABC):
    @abstractmethod
    async def signin_email_password(
        self, *, req: SignInWithEmailAndPasswordRequest
    ) -> UserCredential: ...

    @abstractmethod
    async def get_roles(self, id: int) -> tuple[Set[str], list[RoleModel]]: ...

    @abstractmethod
    async def get_menus(
        self, id: int, role_models: list[RoleModel]
    ) -> list[Menu]: ...
