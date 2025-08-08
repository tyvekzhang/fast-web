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
"""Table domain service impl"""

import io
import json
import zipfile
from collections import OrderedDict
from typing import List

from loguru import logger

from src.main.app.core.constant import FilterOperators
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.utils.gen_util import GenUtils
from src.main.app.core.utils.jinja2_util import Jinja2Utils
from src.main.app.core.utils.template_util import load_template_file
from src.main.app.enums.biz_error_code import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.codegen.connection_mapper import connectionMapper
from src.main.app.mapper.codegen.database_mapper import databaseMapper
from src.main.app.mapper.codegen.field_mapper import fieldMapper
from src.main.app.mapper.codegen.index_mapper import indexMapper
from src.main.app.mapper.codegen.meta_field_mapper import metaFieldMapper
from src.main.app.mapper.codegen.meta_table_mapper import metaTableMapper
from src.main.app.mapper.codegen.table_mapper import TableMapper
from src.main.app.model.codegen.field_model import FieldModel
from src.main.app.model.codegen.meta_field_model import MetaFieldModel
from src.main.app.model.codegen.meta_table_model import MetaTableModel
from src.main.app.model.codegen.table_model import TableModel
from src.main.app.schema.codegen.field_schema import GenField
from src.main.app.schema.codegen.table_schema import (
    Table,
    TableDetail,
    ListTablesRequest,
    ImportTable,
    GenContext, UpdateTable, UpdateTableOption, RelationTable,
)
from src.main.app.service.codegen.table_service import TableService


class TableServiceImpl(BaseServiceImpl[TableMapper, TableModel], TableService):
    def __init__(self, mapper: TableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def build_tables(self, tables: List[TableModel]) -> list[Table]:
        if not tables:
            return []

        # Obtain all relevant data
        table_ids = [record.db_table_id for record in tables]
        table_records = await metaTableMapper.select_by_ids(ids=table_ids)
        db_ids = [record.database_id for record in table_records]
        db_records = await databaseMapper.select_by_ids(ids=db_ids)
        conn_ids = [record.connection_id for record in db_records]
        conn_records = await connectionMapper.select_by_ids(ids=conn_ids)

        # Convert to dict
        table_map = {record.id: record for record in table_records}
        db_map = {record.id: record for record in db_records}
        conn_map = {record.id: record for record in conn_records}

        results = []
        for record in tables:
            table_info = table_map.get(record.db_table_id)
            if not table_info:
                logger.error(f"{BusinessErrorCode.PARAMETER_ERROR.message}: {record.db_table_id}")
                raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
            db_info = db_map.get(table_info.database_id)
            if not db_info:
                logger.error(
                    f"{BusinessErrorCode.PARAMETER_ERROR.message}: {table_info.database_id}"
                )
                raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
            conn_info = conn_map.get(db_info.connection_id)
            if not conn_info:
                logger.error(
                    f"{BusinessErrorCode.PARAMETER_ERROR.message}: {db_info.connection_id}"
                )
                raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
            results.append(
                Table(
                    id=record.id,
                    connection_name=conn_info.connection_name,
                    database_name=db_info.database_name,
                    table_id=record.db_table_id,
                    table_name=table_info.name,
                    entity=record.class_name,
                    comment=table_info.comment,
                    create_time=record.create_time,
                )
            )

        return results

    async def list_tables(self, req: ListTablesRequest) -> tuple[list[TableModel], int]:
        filters = {
            FilterOperators.LIKE: {},
            FilterOperators.EQ: {},
        }
        if req.database_id:
            filters[FilterOperators.EQ]["database_id"] = req.database_id
        if req.table_name is not None and req.table_name != "":
            filters[FilterOperators.LIKE]["table_name"] = req.table_name
        if req.comment is not None and req.comment != "":
            filters[FilterOperators.LIKE]["comment"] = req.comment
        return await self.mapper.select_by_ordered_page(
            current=req.current, page_size=req.page_size, **filters
        )

    async def import_tables(self, req: ImportTable):
        table_ids = req.table_ids
        table_records: List[MetaTableModel] = await metaTableMapper.select_by_ids(ids=table_ids)
        for table_record in table_records:
            table_name = table_record.name
            comment = table_record.comment
            if comment is None:
                comment = "[请填写功能名]"
            table_id = table_record.id
            backend = req.backend
            gen_table_record = TableModel(
                database_id=req.database_id,
                db_table_id=table_id,
                class_name=table_name,
                function_name=comment,
                comment=comment,
                table_name=table_record.name,
                backend=backend,
            )
            GenUtils.init_table(gen_table_record)
            await self.save(data=gen_table_record)
            field_records = await metaFieldMapper.select_by_table_id(table_id=table_id)
            for field_record in field_records:
                gen_field_record = FieldModel(
                    db_field_id=field_record.id,
                    db_table_id=field_record.table_id,
                    length=field_record.length,
                )
                GenUtils.init_field(gen_field_record, field_record, backend)
                await fieldMapper.insert(data=gen_field_record)

    async def preview_code(self, id: int) -> dict:
        data_map = OrderedDict()
        table_record, gen_context = await self.generator_code(id)
        index_metadata = await indexMapper.select_by_table_id(table_id=table_record.db_table_id)
        backend = table_record.backend
        data_map["backend"] = backend
        context = Jinja2Utils.prepare_context(gen_context, index_metadata)
        templates = Jinja2Utils.get_template_list(
            backend,
            table_record.tpl_backend_type,
            table_record.tpl_category,
            table_record.tpl_web_type,
        )
        for template in templates:
            try:
                template_j2 = load_template_file(template)
                rendered_template = template_j2.render(context)
                data_map[GenUtils.trim_jinja2_name(template)] = rendered_template
            except Exception as e:
                logger.error(f"Error rendering template {template}: {e}")
        return data_map

    def set_sub_table(self, *, table: TableModel):
        pass

    def set_pk_column(self, *, gen_table: TableModel, table_gen: Table):
        table_gen.pk_field = gen_table

    async def generator_code(self, table_id: int):
        # Get import table record
        table_record: TableModel = await self.mapper.select_by_id(id=table_id)
        if table_record is None:
            logger.error(f"Table not found: {table_id}")
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        self.set_sub_table(table=table_record)
        # Get field mete field
        meta_field_records = await metaFieldMapper.select_by_table_id(
            table_id=table_record.db_table_id
        )
        if meta_field_records is None or len(meta_field_records) == 0:
            logger.error(f"Meta table not found: {table_record.db_table_id}")
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        meta_field_ids = [field_record.id for field_record in meta_field_records]
        # Get field records by mete field ids
        field_records: List[FieldModel] = await fieldMapper.select_by_db_field_ids(
            ids=meta_field_ids
        )
        if field_records is None or len(field_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        meta_id_field_dict = {
            field_record.db_field_id: field_record for field_record in field_records
        }
        field_list = []
        primary_key = ""
        for meta_field in meta_field_records:
            mapped_field: FieldModel = meta_id_field_dict.get(meta_field.id)
            if mapped_field is None:
                continue
            if mapped_field.primary_key == 1:
                meta_field_record: FieldModel = await metaFieldMapper.select_by_id(
                    id=mapped_field.db_field_id
                )
                primary_key = meta_field_record.name
            field_data = GenField(meta_field=meta_field, field=mapped_field)
            field_list.append(field_data)
        gen_context: GenContext = GenContext(table=table_record, gen_fields=field_list)
        gen_context.pk_field = primary_key
        return table_record, gen_context

    async def download_code(self, table_ids: list[int]):
        """
        Generate and download code for multiple tables as a ZIP file
        """
        output_stream = io.BytesIO()

        with zipfile.ZipFile(output_stream, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for table_id in table_ids:
                try:
                    # Generate code for each table
                    table_record, gen_context = await self.generator_code(table_id)
                    index_metadata = await indexMapper.select_by_table_id(
                        table_id=table_record.db_table_id
                    )
                    context = Jinja2Utils.prepare_context(gen_context, index_metadata)
                    templates = Jinja2Utils.get_template_list(
                        table_record.backend,
                        table_record.tpl_backend_type,
                        table_record.tpl_category,
                        table_record.tpl_web_type,
                    )

                    # Add generated files to ZIP archive
                    for template in templates:
                        try:
                            template_j2 = load_template_file(template)
                            rendered_template = template_j2.render(context)
                            # Prefix files with table name to avoid conflicts
                            file_path = Jinja2Utils.get_file_name(template, gen_context)
                            zip_file.writestr(file_path, rendered_template)
                        except Exception as e:
                            logger.error(f"Template rendering failed for {template}: {e}")

                except Exception as e:
                    logger.error(f"Code generation failed for table_id {table_id}: {e}")
                    continue

        return output_stream.getvalue()

    async def get_table_detail(self, *, id: int) -> TableDetail:
        table_record: TableModel = await self.retrieve_by_id(id=id)
        meta_table_id = table_record.db_table_id

        # 获取数据库表信息
        meta_fields: List[MetaFieldModel] = await metaFieldMapper.select_by_table_id(
            table_id=meta_table_id
        )

        # 获取字段对应的生成字段信息
        field_ids = [db_field.id for db_field in meta_fields]
        fields = await fieldMapper.select_by_db_field_ids(ids=field_ids)

        # 返回最终详情
        return TableDetail(table=table_record, fields=fields)

    async def update_table(self, req: UpdateTable) -> None:
        table_option: UpdateTableOption = req.table
        update_table_data = TableModel(**table_option.model_dump())
        options = None
        if table_option.tpl_category == "2":
            relation_tables = table_option.relationTables
            options = json.dumps(
                [table.model_dump(exclude_none=True) for table in relation_tables],
                ensure_ascii=False
            )
        elif table_option.tpl_category == "3":
            options = table_option.treeTable.model_dump_json()
        update_table_data.options = options
        await self.mapper.update_by_id(data=update_table_data)
        gen_fields: List[FieldModel] = req.fields
        for gen_field in gen_fields:
            await fieldMapper.update_by_id(data=gen_field)

    async def delete_table(self, id: int) -> None:
        table_record: TableModel = await self.retrieve_by_id(id=id)

        await metaTableMapper.delete_by_id(id=table_record.db_table_id)
        meta_field_fields: list[MetaFieldModel] = await metaFieldMapper.select_by_table_id(
            table_id=table_record.db_table_id
        )
        field_ids = [field.id for field in meta_field_fields]
        await metaFieldMapper.batch_delete_by_ids(ids=field_ids)
        await fieldMapper.batch_delete_by_field_ids(field_ids=field_ids)
        await self.remove_by_id(id=id)
