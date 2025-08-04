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
"""DictDatum mapper"""

from __future__ import annotations

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.dict_datum_model import DictDatumModel


class DictDatumMapper(SqlModelMapper[DictDatumModel]):
    async def select_by_types(self, data: list[str], db_session: Union[AsyncSession, None] = None) -> list[
        DictDatumModel]:
        db_session = db_session or self.db.session
        db_response = await db_session.exec(select(self.model).where(self.model.type.in_(data)))
        return db_response.all()


dictDatumMapper = DictDatumMapper(DictDatumModel)
