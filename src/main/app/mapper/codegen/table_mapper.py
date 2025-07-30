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
"""Table mapper"""
from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.codegen.table_model import TableModel


class TableMapper(SqlModelMapper[TableModel]):
    async def select_by_database_ids(
        self, *, database_ids: int, db_session: Optional[AsyncSession] = None
    ) -> Optional[list[TableModel]]:
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.database_id.in_(database_ids))
        )
        return result.all()


tableMapper = TableMapper(TableModel)
