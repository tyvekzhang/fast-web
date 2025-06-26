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
"""RoleMenu mapper"""

from typing import Union, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_role_menu_model import RoleMenuModel


class RoleMenuMapper(SqlModelMapper[RoleMenuModel]):
    async def select_by_role_ids(
        self,
        *,
        role_ids: List[int],
        db_session: Union[AsyncSession, None] = None,
    ) -> Union[RoleMenuModel, None]:
        db_session = db_session or self.db.session
        query = select(RoleMenuModel).where(RoleMenuModel.id.in_(role_ids))
        result = await db_session.exec(query)
        return result.all()


roleMenuMapper = RoleMenuMapper(RoleMenuModel)
