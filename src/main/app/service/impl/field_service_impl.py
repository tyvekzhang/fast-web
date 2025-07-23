"""Field domain service impl"""

from typing import List

from sqlmodel import inspect

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.session.db_engine import get_cached_async_engine
from src.main.app.core.utils.field_type_mapping_util import (
    sqlmodel_map_to_mysql_type,
    sqlmodel_map_to_pgsql_type,
)
from src.main.app.core.utils.string_util import parse_type_params
from src.main.app.mapper.connection_mapper import connectionMapper
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.mapper.field_mapper import FieldMapper
from src.main.app.mapper.index_mapper import indexMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.db_index_model import IndexDO
from src.main.app.model.db_table_model import TableDO
from src.main.app.schema.field_schema import FieldQuery, AntTableColumn
from src.main.app.service.field_service import FieldService


class FieldServiceImpl(BaseServiceImpl[FieldMapper, FieldDO], FieldService):
    def __init__(self, mapper: FieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_fields(self, data: FieldQuery):
        table_id = data.table_id
        # 查询表信息
        table_record: TableDO = await tableMapper.select_by_id(id=table_id)
        if table_record is None:
            raise
        database_record = await databaseMapper.select_by_id(
            id=table_record.database_id
        )
        if database_record is None:
            raise
        connection_record = await connectionMapper.select_by_id(
            id=database_record.connection_id
        )
        if connection_record is None:
            raise
        database_type = connection_record.database_type.lower()
        field_name_id_map = {}
        index_name_id_map = {}
        # 通过表id查询字段信息
        field_records = await self.mapper.select_by_table_id(table_id=table_id)
        if field_records:
            field_name_id_map = {
                field_record.name: field_record.id
                for field_record in field_records
            }
        # 通过数据库id获取引擎
        engine = await get_cached_async_engine(
            database_id=table_record.database_id
        )
        async with engine.connect() as conn:
            try:
                table_name = table_record.name
                columns = await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).get_columns(table_name)
                )
                indexes = await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).get_indexes(table_name)
                )
                pk_index = await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).get_pk_constraint(
                        table_name
                    )
                )
            except:
                columns = []
                indexes = []
                pk_index = []

        indexed_columns = set()
        for index in indexes:
            for col in index["column_names"]:
                indexed_columns.add(col)
                break
        pk_index_columns = set()
        if pk_index is not None:
            pk_index_columns.add(pk_index["constrained_columns"][0])

        # {'comment': '年龄', 'default': None, 'name': 'age', 'nullable': True, 'type': DECIMAL(precision=10, scale=2)}
        new_add_field_records = []
        column_name_set = set()
        for index, column in enumerate(columns):
            name = column["name"]
            column_name_set.add(name)
            if name in field_name_id_map:
                continue
            type_str = str(column["type"])
            type_name, params = parse_type_params(type_str)
            length = None
            scale = None
            if len(params) == 1:
                length = int(list(params)[0])
            elif len(params) == 2:
                length = int(list(params)[0])
                scale = int(list(params)[1])
            if database_type == "mysql" or database_type == "sqlite":
                type_name = sqlmodel_map_to_mysql_type(type_name)
            elif database_type == "postgresql" or database_type == "pgsql":
                if name.__contains__("vector") or name.__contains__(
                    "embedding"
                ):
                    type_name = "vector"
                    length = 2560
                type_name = sqlmodel_map_to_pgsql_type(type_name)
            else:
                raise
            nullable = column["nullable"]
            new_add_field_records.append(
                FieldDO(
                    table_id=table_id,
                    name=name,
                    type=type_name,
                    length=length,
                    scale=scale,
                    default=column.get("default", None),
                    comment=column.get("comment", None),
                    nullable=nullable,
                    primary_key=name in pk_index_columns,
                    autoincrement=column.get("autoincrement", False),
                    sort=index,
                )
            )
        if len(new_add_field_records) > 0:
            await self.mapper.batch_insert(data_list=new_add_field_records)
        need_delete_field_ids = []
        for filed_name in field_name_id_map.keys():
            if filed_name not in column_name_set:
                need_delete_field_ids.append(field_name_id_map[filed_name])
        if len(need_delete_field_ids) > 0:
            await self.mapper.batch_delete_by_ids(ids=need_delete_field_ids)

        index_records = await indexMapper.select_by_table_id(table_id=table_id)
        if index_records is not None:
            index_name_id_map = {
                index_record.name: index_record.id
                for index_record in index_records
            }
        # {'column_names': ['status', 'nickname'], 'name': 'idx_status_nickname', 'unique': False}
        new_add_index_records = []
        index_name_set = set()
        for index in indexes:
            name: str = index["name"]
            index_name_set.add(name)
            if name in index_name_id_map:
                continue
            index_do = IndexDO(
                table_id=table_id,
                name=name,
                field=str(index["column_names"])
                .replace("[", "")
                .replace("]", ""),
                type=str(index.get("type", "normal")).lower(),
                remark=index.get("comment", None),
            )
            new_add_index_records.append(index_do)
        if len(new_add_index_records) > 0:
            await indexMapper.batch_insert(data_list=new_add_index_records)
        need_delete_index_ids = []
        for index_name in index_name_id_map.keys():
            if index_name not in index_name_set:
                need_delete_index_ids.append(index_name_id_map[index_name])
        if len(need_delete_index_ids) > 0:
            await indexMapper.batch_delete_by_ids(ids=need_delete_index_ids)
        return await self.mapper.select_by_ordered_page(
            current=data.current,
            pageSize=data.pageSize,
            EQ={"table_id": table_id},
        )

    async def get_ant_table_fields(self, table_id: int) -> List[AntTableColumn]:
        field_records = await self.mapper.select_by_table_id(table_id=table_id)
        if field_records is None or len(field_records) == 0:
            await self.list_fields(
                FieldQuery(
                    table_id=table_id,
                )
            )
            field_records = await self.mapper.select_by_table_id(
                table_id=table_id
            )
        ant_columns = []
        for field in field_records:
            column = AntTableColumn(
                title=field.comment,
                dataIndex=field.name,
                key=field.name,
            )

            # Add additional properties based on field type
            if field.type.lower() in ["varchar", "char", "text"]:
                column.ellipsis = True
            if field.name.lower() == "id":
                column.hidden = True
            # Add sorter for sortable columns
            if field.type.lower() not in ["text", "blob", "json"]:
                # column.sorter = True
                pass

            ant_columns.append(column)

        return ant_columns
