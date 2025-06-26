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
"""UserRole mapper"""

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_user_role_model import UserRoleModel


class UserRoleMapper(SqlModelMapper[UserRoleModel]):
    async def select_by_userid(
        self, *, user_id: int, db_session: Union[AsyncSession, None] = None
    ) -> Union[UserRoleModel, None]:
        db_session = db_session or self.db.session
        query = select(UserRoleModel).where(UserRoleModel.user_id == user_id)
        result = await db_session.exec(query)
        return result.all()


userRoleMapper = UserRoleMapper(UserRoleModel)
