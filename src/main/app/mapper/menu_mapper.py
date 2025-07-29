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
"""Menu mapper"""

from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.menu_model import MenuModel


class MenuMapper(SqlModelMapper[MenuModel]):
    async def select_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[MenuModel]:
        """
        Retrieve a menu record by name.
        """
        db_session = db_session or self.db.session
        user = await db_session.exec(
            select(self.model).where(self.model.name == name)
        )
        return user.one_or_none()

    async def select_by_names(
        self, *, names: list[str], db_session: Optional[AsyncSession] = None
    ) -> Optional[list[MenuModel]]:
        """
        Retrieve menu records by names.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.name.in_(names))
        )
        return result.all()


menuMapper = MenuMapper(MenuModel)
