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
"""Table REST API"""

from typing import Annotated

from fastapi import APIRouter, Query

from src.main.app.core.schema import ListResult
from src.main.app.mapper.codegen.field_mapper import fieldMapper
from src.main.app.mapper.codegen.meta_field_mapper import metaFieldMapper
from src.main.app.mapper.codegen.meta_table_mapper import metaTableMapper
from src.main.app.mapper.codegen.table_mapper import tableMapper
from src.main.app.schema.codegen.table_schema import ListTablesRequest
from src.main.app.service.codegen.field_service import FieldService
from src.main.app.service.codegen.meta_field_service import MetaFieldService
from src.main.app.service.codegen.meta_table_service import MetaTableService
from src.main.app.service.codegen.table_service import TableService
from src.main.app.service.impl.codegen.field_service_impl import (
    FieldServiceImpl,
)
from src.main.app.service.impl.codegen.meta_field_service_impl import (
    MetaFieldServiceImpl,
)
from src.main.app.service.impl.codegen.meta_table_service_impl import (
    MetaTableServiceImpl,
)
from src.main.app.service.impl.codegen.table_service_impl import (
    TableServiceImpl,
)

table_router = APIRouter()
meta_table_service: MetaTableService = MetaTableServiceImpl(
    mapper=metaTableMapper
)
table_service: TableService = TableServiceImpl(mapper=tableMapper)
field_service: FieldService = FieldServiceImpl(mapper=fieldMapper)
meta_field_service: MetaFieldService = MetaFieldServiceImpl(
    mapper=metaFieldMapper
)


@table_router.get("/tables")
async def list_tables(
    req: Annotated[ListTablesRequest, Query()],
) -> ListResult:
    """
    List tables with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of tables and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    table_records, total_count = await table_service.list_tables(req=req)
    results = await table_service.build_tables(tables=table_records)
    return ListResult(records=results, total=total_count)

#
# @table_router.post("/gen-table/execute")
# async def execute_sql(
#     gen_table_execute: Table,
# ) -> Dict:
#     gen_table_record = await table_service.execute_sql(
#         gen_table_execute=gen_table_execute
#     )
#     return result.success(data=gen_table_record)
#
#
# @table_router.get("/gen-table/detail/{id}")
# async def get_gen_table_detail(
#     id: int,
# ) -> HttpResponse[TableDetail]:
#     response: TableDetail = await table_service.get_gen_table_detail(id=id)
#     return HttpResponse(data=response)
#
#
# @table_router.post("/gen-table/add")
# async def add_gen_table(
#     gen_table_add: TableAdd,
# ) -> HttpResponse[int]:
#     """
#     Table add.
#
#     Args:
#         gen_table_add: Data required for add.
#
#     Returns:
#         BaseResponse with new gen_table's ID.
#     """
#     gen_table: TableModel = await table_service.save(
#         data=TableModel(**gen_table_add.model_dump())
#     )
#     return HttpResponse(data=gen_table.id)
#
#
# @table_router.get("/gen-table/export-template")
# async def export_template() -> StreamingResponse:
#     """
#     Export a template for gen_table information.
#
#     Returns:
#         StreamingResponse with gen_table field
#     """
#     return await export_excel(
#         schema=TableExport, file_name="gen_table_import_template"
#     )
#
#
# @table_router.post("/gen-table/import")
# async def import_gen_table(table_import: TableImport) -> Dict:
#     await table_service.import_gen_table(table_import=table_import)
#     return result.success()
#
#
# @table_router.get("/gen-table/preview/{gen_table_id}")
# async def preview_code(gen_table_id: int) -> Dict:
#     res = await table_service.preview_code(gen_table_id=gen_table_id)
#     return result.success(res)
#
#
# @table_router.get("/gen-table/data/{id}/{current}/{page_size}")
# async def table_data(id: int, current: int = 1, page_size: int = 10) -> Dict:
#     res = await table_service.get_table_data(
#         id=id, current=current, page_size=page_size
#     )
#     return result.success(res)
#
#
# @table_router.get("/gen-table/download/{table_id}")
# async def preview_code(table_id: int) -> StreamingResponse:
#     # 生成代码
#     data = await table_service.download_code(table_id)
#
#     gen_table_DO: TableModel = await table_service.retrieve_by_id(id=table_id)
#     table_name = str(gen_table_DO.table_name)
#
#     return StreamingResponse(
#         BytesIO(data),
#         media_type="application/zip",
#         headers={
#             "Content-Disposition": f"attachment; filename={table_name}_{get_date_time()}.zip"
#         },
#     )
#
#
# @table_router.get("/gen-table/export")
# async def export(
#     data: Annotated[TableQueryForm, Query()],
# ) -> StreamingResponse:
#     """
#     Export gen_table information based on provided parameters.
#
#     Args:
#         data: Filtering and format parameters for export.
#
#     Returns:
#         StreamingResponse with gen_table info
#     """
#     return await table_service.export_gen_table(params=data)
#
#
# @table_router.put("/gen-table/modify")
# async def modify_gen_table(
#     gen_table_detail: TableDetail,
# ) -> Dict:
#     """
#     Update gen_table information.
#
#     Args:
#         gen_table_detail: Command containing updated gen_table info.
#
#     Returns:
#         Success result message
#     """
#     await table_service.modify_gen_table(gen_table_detail=gen_table_detail)
#     return result.success()
#
#
# @table_router.put("/gen-table/batchmodify")
# async def batch_modify(ids: Ids, data: TableModify) -> Dict:
#     cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
#     if len(cleaned_data) == 0:
#         return result.fail("Please fill in the modify information")
#
#     await table_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
#     return result.success()
#
#
# async def remove_logic(id: int) -> None:
#     """
#     Shared logic to remove a gen_table by their ID.
#     """
#     gen_table: TableModel = await table_service.retrieve_by_id(id=id)
#     db_table_id = gen_table.db_table_id
#     await meta_table_service.remove_by_id(id=db_table_id)
#     fields: List[FieldModel] = await fieldMapper.select_by_table_id(
#         table_id=db_table_id
#     )
#     field_ids = [field.id for field in fields]
#     await meta_field_service.batch_remove_by_ids(ids=field_ids)
#     await fieldMapper.batch_delete_by_field_ids(field_ids=field_ids)
#     await table_service.remove_by_id(id=id)
#
#
# @table_router.delete("/gen-table/remove/{id}")
# async def remove(
#     id: int,
# ) -> Dict:
#     """
#     Remove a gen_table by their ID.
#
#     Args:
#         id: Table ID to remove.
#
#     Returns:
#         Success result message
#     """
#     await remove_logic(id)
#     return result.success()
#
#
# @table_router.post("/gen-table/sync/{id}")
# async def sync_table(
#     id: int,
# ) -> Dict:
#     gen_table_do: TableModel = await table_service.retrieve_by_id(id=id)
#     table_do: MetaTableModel = await meta_table_service.retrieve_by_id(
#         id=gen_table_do.db_table_id
#     )
#     await remove_logic(id)
#     table_query = TableQuery(
#         database_id=table_do.database_id, current=1, page_size=200
#     )
#     records, total = await meta_table_service.list_tables(data=table_query)
#     table_id: int = 0
#     for record in records:
#         if record.name == gen_table_do.table_name:
#             table_id = record.id
#             break
#     table_import = TableImport(
#         database_id=table_do.database_id,
#         table_ids=[table_id],
#         backend=gen_table_do.backend,
#     )
#     await table_service.import_gen_table(table_import=table_import)
#     records, total = await table_service.list_tables(
#         data=ListMenusRequest(current=1, page_size=200)
#     )
#     gen_table_id: int = 0
#     for record in records:
#         if record.table_name == gen_table_do.table_name:
#             gen_table_id = record.id
#             break
#     new_gen_table_do: TableModel = await table_service.retrieve_by_id(
#         id=gen_table_id
#     )
#     new_gen_table_do.id = gen_table_do.id
#     await table_service.remove_by_id(id=new_gen_table_do.id)
#     await table_service.save(data=new_gen_table_do)
#     return result.success()
#
#
# @table_router.delete("/gen-table/batchremove")
# async def batch_remove(
#     ids: List[int] = Query(...),
# ) -> Dict:
#     """
#     Delete gen_tables by a list of IDs.
#
#     Args:
#         ids: List of gen_table IDs to delete.
#
#     Returns:
#         Success result message
#     """
#     await table_service.batch_remove_by_ids(ids=ids)
#     return result.success()
