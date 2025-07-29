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
"""Database mapper"""

from typing import Union, List

from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.codegen.database_model import DatabaseModel


class DatabaseMapper(SqlModelMapper[DatabaseModel]):
    async def select_by_connection_id(
        self, connection_id: int, db_session: Union[AsyncSession, None] = None
    ) -> List[DatabaseModel]:
        db_session = db_session or self.db.session
        statement = select(self.model).where(
            self.model.connection_id == connection_id
        )
        exec_result = await db_session.exec(statement)
        return exec_result.all()

    async def delete_by_connection_id(
        self, connection_id: int, db_session: Union[AsyncSession, None] = None
    ) -> int:
        db_session = db_session or self.db.session
        statement = delete(self.model).where(
            self.model.connection_id == connection_id
        )
        exec_result = await db_session.exec(statement)
        return exec_result.rowcount


databaseMapper = DatabaseMapper(DatabaseModel)
