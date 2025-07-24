"""GenTable domain service impl"""

import io
import zipfile
from collections import OrderedDict
from typing import List, Dict
from sqlalchemy import text

from src.main.app.core.utils.gen_util import GenUtils
from src.main.app.core.utils.jinja2_util import Jinja2Utils
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.session.db_engine import get_cached_async_engine
from src.main.app.core.utils.sql_util import SqlUtil
from src.main.app.core.utils.template_util import load_template_file
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.mapper.field_mapper import fieldMapper
from src.main.app.mapper.gen_field_mapper import genFieldMapper
from src.main.app.mapper.gen_table_mapper import GenTableMapper
from src.main.app.mapper.index_mapper import indexMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.db_table_model import TableDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.field_schema import FieldQuery, AntTableColumn
from src.main.app.schema.gen_field_schema import FieldGen
from src.main.app.schema.gen_table_schema import (
    TableImport,
    TableGen,
    GenTableQuery,
    GenTableQueryResponse,
    GenTableDetail,
    GenTableExecute,
    GenTableRecord,
)
from src.main.app.service.gen_table_service import GenTableService


class GenTableServiceImpl(
    BaseServiceImpl[GenTableMapper, GenTableDO], GenTableService
):
    def __init__(self, mapper: GenTableMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def import_gen_table(self, table_import: TableImport):
        from src.main.app.service.field_service import FieldService
        from src.main.app.service.impl.field_service_impl import (
            FieldServiceImpl,
        )

        field_service: FieldService = FieldServiceImpl(mapper=fieldMapper)
        table_ids = table_import.table_ids
        for table_id in table_ids:
            await field_service.list_fields(FieldQuery(table_id=table_id))
        table_records: List[TableDO] = await tableMapper.select_by_ids(
            ids=table_ids
        )
        for table_record in table_records:
            table_name = table_record.name
            comment = table_record.comment
            if comment is None:
                comment = "[请填写功能名]"
            table_id = table_record.id
            backend = table_import.backend
            gen_table_record = GenTableDO(
                database_id=table_import.database_id,
                db_table_id=table_id,
                class_name=table_name,
                function_name=comment,
                comment=comment,
                table_name=table_record.name,
                backend=backend,
            )
            GenUtils.init_table(gen_table_record)
            await self.save(data=gen_table_record)
            field_records = await fieldMapper.select_by_table_id(
                table_id=table_id
            )
            for field_record in field_records:
                gen_field_record = GenFieldDO(
                    db_field_id=field_record.id,
                    db_table_id=field_record.table_id,
                    length=field_record.length,
                )
                GenUtils.init_field(gen_field_record, field_record, backend)
                await genFieldMapper.insert(data=gen_field_record)

    async def preview_code(self, gen_table_id: int) -> Dict:
        data_map = OrderedDict()
        # 查询导入的表信息
        gen_table, table_gen = await self.generator_code(gen_table_id)
        index_metadata = await indexMapper.select_by_table_id(
            table_id=gen_table.db_table_id
        )
        backend = gen_table.backend
        data_map["backend"] = backend
        context = Jinja2Utils.prepare_context(table_gen, index_metadata)
        templates = Jinja2Utils.get_template_list(
            backend,
            gen_table.tpl_backend_type,
            gen_table.tpl_category,
            gen_table.tpl_web_type,
        )
        for template in templates:
            try:
                template_j2 = load_template_file(template)
                rendered_template = template_j2.render(context)
                data_map[GenUtils.trim_jinja2_name(template)] = (
                    rendered_template
                )
            except Exception as e:
                print(f"这里出错啦{template} {e}")
        return data_map

    def set_sub_table(self, *, gen_table: GenTableDO):
        pass

    def set_pk_column(self, *, gen_table: GenTableDO, table_gen: TableGen):
        table_gen.pk_field = gen_table

    async def list_gen_tables(self, data: GenTableQuery):
        results, total_count = await self.mapper.select_by_ordered_page(
            current=data.current, page_size=data.page_size
        )
        if not results:
            return results, total_count

        # 获取所有相关数据
        table_ids = [record.db_table_id for record in results]
        table_records = await tableMapper.select_by_ids(ids=table_ids)
        db_ids = [record.database_id for record in table_records]
        db_records = await databaseMapper.select_by_ids(ids=db_ids)
        conn_ids = [record.connection_id for record in db_records]
        conn_records = await connectionMapper.select_by_ids(ids=conn_ids)

        # 建立映射关系
        table_map = {record.id: record for record in table_records}
        db_map = {record.id: record for record in db_records}
        conn_map = {record.id: record for record in conn_records}

        records = []
        for record in results:
            table_info = table_map.get(record.db_table_id)
            if table_info:
                db_info = db_map.get(table_info.database_id)
                if db_info:
                    conn_info = conn_map.get(db_info.connection_id)
                    if conn_info:
                        records.append(
                            GenTableQueryResponse(
                                id=record.id,
                                connection_name=conn_info.connection_name,
                                database_name=db_info.database_name,
                                table_id=record.db_table_id,
                                table_name=table_info.name,
                                entity=record.class_name,
                                table_comment=table_info.comment,
                                create_time=record.create_time,
                            )
                        )

        return records, total_count

    async def generator_code(self, gen_table_id: int):
        # 查询导入的表信息
        gen_table: GenTableDO = await self.retrieve_by_id(id=gen_table_id)
        if gen_table is None:
            raise
        self.set_sub_table(gen_table=gen_table)
        # 通过表id查询父字段信息
        field_records = await fieldMapper.select_by_table_id(
            table_id=gen_table.db_table_id
        )
        if field_records is None or len(field_records) == 0:
            raise
        field_list = [field_record.id for field_record in field_records]
        # 通过字段的id查询子字段的信息
        gen_field_records: List[
            GenFieldDO
        ] = await genFieldMapper.select_by_db_field_ids(ids=field_list)
        if gen_field_records is None or len(gen_field_records) == 0:
            raise
        id_field_dict = {
            gen_field_record.db_field_id: gen_field_record
            for gen_field_record in gen_field_records
        }
        field_list = []
        primary_key = ""
        for field_record in field_records:
            field = field_record
            gen_field: GenFieldDO = id_field_dict.get(field.id)
            if gen_field is None:
                continue
            if gen_field.primary_key == 1:
                field_record: FieldDO = await fieldMapper.select_by_id(
                    id=gen_field.db_field_id
                )
                primary_key = field_record.name
            field_gen = FieldGen(field=field, gen_field=gen_field)
            field_list.append(field_gen)
        table_gen: TableGen = TableGen(gen_table=gen_table, fields=field_list)
        table_gen.pk_field = primary_key
        return gen_table, table_gen

    async def download_code(self, table_id: int):
        gen_table, table_gen = await self.generator_code(table_id)
        index_metadata = await indexMapper.select_by_table_id(
            table_id=gen_table.db_table_id
        )
        context = Jinja2Utils.prepare_context(table_gen, index_metadata)
        templates = Jinja2Utils.get_template_list(
            gen_table.backend,
            gen_table.tpl_backend_type,
            gen_table.tpl_category,
            gen_table.tpl_web_type,
        )
        output_stream = io.BytesIO()
        with zipfile.ZipFile(
            output_stream, "w", zipfile.ZIP_DEFLATED
        ) as zip_file:
            for template in templates:
                try:
                    template_j2 = load_template_file(template)
                    rendered_template = template_j2.render(context)
                    zip_file.writestr(
                        Jinja2Utils.get_file_name(template, table_gen),
                        rendered_template,
                    )
                except Exception as e:
                    print(f"{template}: {e}")
        return output_stream.getvalue()

    @classmethod
    async def get_table_data(cls, *, id: int, current: int, pageSize: int):
        # 根据生成表关联的数据库表ID查询表信息
        table_do: TableDO = await tableMapper.select_by_id(id=id)

        # 获取数据库异步引擎
        engine = await get_cached_async_engine(database_id=table_do.database_id)

        # 获取表名
        table_name = table_do.name

        # 使用异步连接
        async with engine.connect() as conn:
            # 计算分页起始位置
            offset = (current - 1) * pageSize

            # 构建查询语句
            query = text(
                f"SELECT * FROM {table_name} LIMIT :pageSize OFFSET :offset"
            )

            # 执行查询
            result = await conn.execute(
                query, {"pageSize": pageSize, "offset": offset}
            )

            # 获取总记录数的查询
            count_query = text(f"SELECT COUNT(*) as total FROM {table_name}")
            count_result = await conn.execute(count_query)
            total = count_result.scalar()

            print(result)
            # 将结果转换为字典列表
            data = [row._asdict() for row in result]

            # 返回分页结果
            return {"records": data, "total": total}

    async def get_gen_table_detail(self, *, id: int) -> GenTableDetail:
        gen_table: GenTableDO = await self.retrieve_by_id(id=id)
        table_id = gen_table.db_table_id

        # 获取数据库表信息
        db_table: TableDO = await tableMapper.select_by_id(id=table_id)
        db_fields: List[FieldDO] = await fieldMapper.select_by_table_id(
            table_id=table_id
        )

        # 获取字段对应的生成字段信息
        field_ids = [db_field.id for db_field in db_fields]
        gen_fields = await genFieldMapper.select_by_db_field_ids(ids=field_ids)

        # 返回最终详情
        return GenTableDetail(gen_table=gen_table, gen_field=gen_fields)

    async def modify_gen_table(self, gen_table_detail: GenTableDetail) -> None:
        gen_table: GenTableDO = gen_table_detail.gen_table
        await self.mapper.update_by_id(record=gen_table)
        gen_fields: List[GenFieldDO] = gen_table_detail.gen_field
        for gen_field in gen_fields:
            await genFieldMapper.update_by_id(data=gen_field)

    async def execute_sql(
        self, gen_table_execute: GenTableExecute
    ) -> GenTableRecord:
        sql_statement = gen_table_execute.sql_statement
        SqlUtil.filter_keyword(sql_statement)
        engine = await get_cached_async_engine(
            database_id=gen_table_execute.database_id
        )
        async with engine.connect() as conn:
            statement = text(sql_statement)
            query_response = await conn.execute(statement)

            # 获取查询结果
            results = query_response.mappings().fetchall()
            if not results:
                # 如果结果为空，返回一个空的记录对象
                return GenTableRecord(fields=[], records=[])

            # 构造字段列表
            fields = [
                AntTableColumn(title=field, dataIndex=field, key=field)
                for field in results[0].keys()
            ]
            records = [dict(result) for result in results]

            # 返回结果
            return GenTableRecord(fields=fields, records=records)
