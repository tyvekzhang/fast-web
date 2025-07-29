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
"""Field mapper"""

from typing import Union, List
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.codegen.field_model import FieldModel


class FieldMapper(SqlModelMapper[FieldModel]):
    async def select_by_db_field_ids(
        self, *, ids: List[int], db_session: Union[AsyncSession, None] = None
    ) -> List[FieldModel]:
        db_session = db_session or self.db.session
        stmt = select(FieldModel).where(self.model.db_field_id.in_(ids))
        exec_result = await db_session.exec(stmt)
        return exec_result.all()

    async def batch_delete_by_field_ids(
        self,
        *,
        field_ids: List[int],
        db_session: Union[AsyncSession, None] = None,
    ) -> None:
        db_session = db_session or self.db.session
        stmt = delete(FieldModel).where(self.model.db_field_id.in_(field_ids))
        await db_session.exec(stmt)


fieldMapper = FieldMapper(FieldModel)
