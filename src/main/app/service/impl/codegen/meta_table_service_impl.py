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

import os.path
import subprocess
import sys
from typing import List, Tuple

from sqlmodel import MetaData, inspect

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.session.db_engine import get_cached_async_engine
from src.main.app.core.utils.field_type_mapping_util import (
    mysql_map2sqlmodel_type,
    mysql_map2server_type,
)
from src.main.app.core.utils.template_util import (
    load_template_file,
    resource_dir,
    render_template,
)
from src.main.app.core.utils.time_util import get_current_time
from src.main.app.mapper.codegen.meta_table_mapper import MetaTableMapper
from src.main.app.model.codegen.meta_table_model import MetaTableModel
from src.main.app.schema.codegen.meta_table_schema import (
    TableQuery,
    TableAdd,
    TableGenerate,
)
from src.main.app.service.codegen.meta_table_service import MetaTableService


class MetaTableServiceImpl(
    BaseServiceImpl[MetaTableMapper, MetaTableModel], MetaTableService
):
    def __init__(self, mapper: MetaTableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_tables(
        self, data: TableQuery
    ) -> Tuple[
        List[MetaTableModel],
        int,
    ]:
        database_id = data.database_id
        engine = await get_cached_async_engine(database_id=database_id)
        async with engine.connect() as conn:
            metadata = MetaData()
            await conn.run_sync(metadata.reflect)
            table_info = []
            for table_name, table in metadata.tables.items():
                table_info.append((table_name, table.comment))

        new_add_tables = []
        need_delete_ids = []
        records: List[MetaTableModel] = await self.mapper.select_by_database_id(
            database_id=database_id
        )

        # 使用字典推导式存储已存在的表名和对应ID
        exist_table_names = (
            {record.name: record.id for record in records} if records else {}
        )

        # 获取当前数据库中的所有表名集合（优化：提前转换为set）
        current_table_names = {table_name for table_name, _ in table_info}

        # 检查需要新增的表
        for table_name, table_comment in table_info:
            if table_name not in exist_table_names:
                new_add_tables.append(
                    MetaTableModel(
                        **TableAdd(
                            database_id=database_id,
                            name=table_name,
                            comment=table_comment,
                        ).model_dump()
                    )
                )

        # 检查需要删除的表（直接遍历字典的键）
        for table_name in exist_table_names:
            if table_name not in current_table_names:
                need_delete_ids.append(exist_table_names[table_name])

        # 批量处理新增和删除
        if new_add_tables:
            await self.mapper.batch_insert(data_list=new_add_tables)
        if need_delete_ids:
            pass  # 取消注释以启用删除功能
            # await self.mapper.batch_delete_by_ids(ids=need_delete_ids)

        # 返回分页查询结果
        return await self.mapper.select_by_ordered_page(
            current=data.current,
            page_size=data.page_size,
            EQ={"database_id": database_id},
        )

    async def generate_table(self, table_generate: TableGenerate) -> None:
        database_id = table_generate.database_id
        engine = await get_cached_async_engine(database_id=database_id)

        table_name = table_generate.table_name
        async with engine.connect() as conn:
            tables = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_names()
            )
            if table_name in tables:
                raise
        template = load_template_file(
            template_name="default/table_create.py.j2"
        )
        if table_generate.class_name is None:
            table_name_split = table_generate.table_name.split("_")
            if len(table_name_split) == 1:
                table_generate.class_name = table_name_split[0].title()
            else:
                table_generate.class_name = table_name_split[1].title()
        table_generate.field_metadata = list(
            map(
                lambda item: item.model_copy(
                    update={
                        "modeltype": mysql_map2sqlmodel_type(item.type),
                        "server_type": mysql_map2server_type(item.type),
                    }
                ),
                table_generate.field_metadata,
            )
        )
        rendered_content = render_template(
            template, **table_generate.model_dump()
        )
        dest_dir = os.path.join(resource_dir, "table_create_history")
        file_name = f"{get_current_time(fmt='%Y-%m-%d-%H-%M')}_{table_generate.table_name}.py"
        dest_path = os.path.join(dest_dir, file_name)
        with open(dest_path, "w", encoding="UTF-8") as f:
            f.write(rendered_content)
        try:
            subprocess.run(
                [sys.executable, dest_path],
                capture_output=True,
                text=True,
                check=True,
            )
        except:
            pass
