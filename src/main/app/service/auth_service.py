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
"""Auth Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set


from src.main.app.core.schema import UserCredential
from src.main.app.model.role_model import RoleModel
from src.main.app.schema.menu_schema import Menu
from src.main.app.schema.auth_schema import (
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
    async def get_menus(self, id: int, role_models: list[RoleModel]) -> list[Menu]: ...
