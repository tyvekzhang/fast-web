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
"""Meta field mapper"""

from typing import Union, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.codegen.meta_field_model import MetaFieldModel


class MetaFieldMapper(SqlModelMapper[MetaFieldModel]):
    async def select_by_table_id(
        self, table_id: int, db_session: Union[AsyncSession, None] = None
    ) -> List[MetaFieldModel]:
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.table_id == table_id)
        exec_result = await db_session.exec(statement)
        return exec_result.all()


metaFieldMapper = MetaFieldMapper(MetaFieldModel)
