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
"""Meta Table domain service impl"""

from sqlalchemy import MetaData

from src.main.app.core.constant import FilterOperators
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.session.db_engine import get_cached_async_engine
from src.main.app.mapper.codegen.meta_table_mapper import MetaTableMapper
from src.main.app.mapper.codegen.table_mapper import tableMapper
from src.main.app.model.codegen.meta_table_model import MetaTableModel
from src.main.app.schema.codegen.meta_table_schema import ListMetaTablesRequest, CreateMetaTable
from src.main.app.service.codegen.meta_table_service import MetaTableService


class MetaTableServiceImpl(BaseServiceImpl[MetaTableMapper, MetaTableModel], MetaTableService):
    def __init__(self, mapper: MetaTableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_meta_tables(
        self, req: ListMetaTablesRequest
    ) -> tuple[list[MetaTableModel], int]:
        database_id = req.database_id
        engine = await get_cached_async_engine(database_id=database_id)
        async with engine.connect() as conn:
            metadata = MetaData()
            await conn.run_sync(metadata.reflect)
            table_info = []
            for table_name, table in metadata.tables.items():
                table_info.append((table_name, table.comment))
        new_add_tables = []
        need_delete_ids = []
        records: list[MetaTableModel] = await self.mapper.select_by_database_id(
            database_id=database_id
        )
        exist_table_names = set()
        if records is not None:
            exist_table_names = {record.name: record.id for record in records}
        for table_name, table_comment in table_info:
            if table_name not in exist_table_names:
                new_add_tables.append(
                    MetaTableModel(
                        **CreateMetaTable(
                            database_id=database_id,
                            name=table_name,
                            comment=table_comment,
                        ).model_dump()
                    )
                )
        table_names = [table_name for table_name, table_comment in table_info]
        for table_name in exist_table_names.keys():
            if table_name not in set(table_names):
                need_delete_ids.append(exist_table_names[table_name])
        if len(new_add_tables) > 0:
            await self.mapper.batch_insert(data_list=new_add_tables)
        filters = {
            FilterOperators.LIKE: {},
            FilterOperators.NE: {},
            FilterOperators.EQ: {"database_id": database_id},
        }
        if req.table_name:
            filters[FilterOperators.LIKE]["name"] = req.table_name
        if req.comment:
            filters[FilterOperators.LIKE]["comment"] = req.comment
        table_records = await tableMapper.select_by_database_ids(database_ids=[database_id])
        if table_records is not None:
            for record in table_records:
                filters[FilterOperators.NE]["name"] = record.table_name
        return await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            **filters,
        )
