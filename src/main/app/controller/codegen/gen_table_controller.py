"""GenTable operation controller"""

from io import BytesIO
from typing import Dict, Annotated, List

from fastapi import APIRouter, Query
from starlette.responses import StreamingResponse

from src.main.app.core import result
from src.main.app.core.result import HttpResponse
from src.main.app.core.utils.excel_util import export_excel
from src.main.app.core.utils.time_util import get_date_time
from src.main.app.mapper.field_mapper import fieldMapper
from src.main.app.mapper.gen_field_mapper import genFieldMapper
from src.main.app.mapper.gen_table_mapper import genTableMapper
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.db_table_model import TableDO
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.gen_table_schema import (
    GenTableAdd,
    GenTableExport,
    GenTableQueryForm,
    GenTableModify,
    GenTableQuery,
    TableImport,
    GenTableDetail,
    GenTableExecute,
)
from src.main.app.schema.table_schema import TableQuery
from src.main.app.schema.user_schema import Ids
from src.main.app.service import table_service, field_service
from src.main.app.service.field_service import FieldService
from src.main.app.service.gen_table_field_service import GenTableFieldService
from src.main.app.service.gen_table_service import GenTableService
from src.main.app.service.impl.field_service_impl import FieldServiceImpl
from src.main.app.service.impl.gen_table_field_service_impl import (
    GenTableFieldServiceImpl,
)
from src.main.app.service.impl.gen_table_service_impl import GenTableServiceImpl
from src.main.app.service.impl.table_service_impl import TableServiceImpl
from src.main.app.service.table_service import TableService

gen_table_router = APIRouter()
gen_table_service: GenTableService = GenTableServiceImpl(mapper=genTableMapper)
db_table_service: TableService = TableServiceImpl(mapper=tableMapper)
gen_table_column_service: GenTableFieldService = GenTableFieldServiceImpl(
    mapper=genFieldMapper
)
db_field_service: FieldService = FieldServiceImpl(mapper=fieldMapper)


@gen_table_router.post("/gen-table/execute")
async def execute_sql(
    gen_table_execute: GenTableExecute,
) -> Dict:
    gen_table_record = await gen_table_service.execute_sql(
        gen_table_execute=gen_table_execute
    )
    return result.success(data=gen_table_record)


@gen_table_router.get("/gen-table/detail/{id}")
async def get_gen_table_detail(
    id: int,
) -> HttpResponse[GenTableDetail]:
    response: GenTableDetail = await gen_table_service.get_gen_table_detail(
        id=id
    )
    return HttpResponse(data=response)


@gen_table_router.post("/gen-table/add")
async def add_gen_table(
    gen_table_add: GenTableAdd,
) -> HttpResponse[int]:
    """
    GenTable add.

    Args:
        gen_table_add: Data required for add.

    Returns:
        BaseResponse with new gen_table's ID.
    """
    gen_table: GenTableDO = await gen_table_service.save(
        data=GenTableDO(**gen_table_add.model_dump())
    )
    return HttpResponse(data=gen_table.id)


@gen_table_router.get("/gen-table/list")
async def list_gen_tables(
    gen_table_query: Annotated[GenTableQuery, Query()],
) -> PageResult:
    """
    Filter gen_tables with pagination.

    Args:
        gen_table_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    records, total_count = await gen_table_service.list_gen_tables(
        data=gen_table_query
    )
    return PageResult(records=records, total=total_count)


@gen_table_router.get("/gen-table/export-template")
async def export_template() -> StreamingResponse:
    """
    Export a template for gen_table information.

    Returns:
        StreamingResponse with gen_table field
    """
    return await export_excel(
        schema=GenTableExport, file_name="gen_table_import_template"
    )


@gen_table_router.post("/gen-table/import")
async def import_gen_table(table_import: TableImport) -> Dict:
    await gen_table_service.import_gen_table(table_import=table_import)
    return result.success()


@gen_table_router.get("/gen-table/preview/{gen_table_id}")
async def preview_code(gen_table_id: int) -> Dict:
    res = await gen_table_service.preview_code(gen_table_id=gen_table_id)
    return result.success(res)


@gen_table_router.get("/gen-table/data/{id}/{current}/{pageSize}")
async def table_data(id: int, current: int = 1, pageSize: int = 10) -> Dict:
    res = await gen_table_service.get_table_data(
        id=id, current=current, pageSize=pageSize
    )
    return result.success(res)


@gen_table_router.get("/gen-table/download/{table_id}")
async def preview_code(table_id: int) -> StreamingResponse:
    # 生成代码
    data = await gen_table_service.download_code(table_id)

    gen_table_DO: GenTableDO = await gen_table_service.retrieve_by_id(
        id=table_id
    )
    table_name = str(gen_table_DO.table_name)

    return StreamingResponse(
        BytesIO(data),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={table_name}_{get_date_time()}.zip"
        },
    )


@gen_table_router.get("/gen-table/export")
async def export(
    data: Annotated[GenTableQueryForm, Query()],
) -> StreamingResponse:
    """
    Export gen_table information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with gen_table info
    """
    return await gen_table_service.export_gen_table(params=data)


@gen_table_router.put("/gen-table/modify")
async def modify_gen_table(
    gen_table_detail: GenTableDetail,
) -> Dict:
    """
    Update gen_table information.

    Args:
        gen_table_detail: Command containing updated gen_table info.

    Returns:
        Success result message
    """
    await gen_table_service.modify_gen_table(gen_table_detail=gen_table_detail)
    return result.success()


@gen_table_router.put("/gen-table/batchmodify")
async def batch_modify(ids: Ids, data: GenTableModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await gen_table_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
    return result.success()


async def remove_logic(id: int) -> None:
    """
    Shared logic to remove a gen_table by their ID.
    """
    gen_table: GenTableDO = await gen_table_service.retrieve_by_id(id=id)
    db_table_id = gen_table.db_table_id
    await db_table_service.remove_by_id(id=db_table_id)
    fields: List[FieldDO] = await fieldMapper.select_by_table_id(
        table_id=db_table_id
    )
    field_ids = [field.id for field in fields]
    await db_field_service.batch_remove_by_ids(ids=field_ids)
    await genFieldMapper.batch_delete_by_field_ids(field_ids=field_ids)
    await gen_table_service.remove_by_id(id=id)


@gen_table_router.delete("/gen-table/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a gen_table by their ID.

    Args:
        id: GenTable ID to remove.

    Returns:
        Success result message
    """
    await remove_logic(id)
    return result.success()


@gen_table_router.post("/gen-table/sync/{id}")
async def sync_table(
    id: int,
) -> Dict:
    gen_table_do: GenTableDO = await gen_table_service.retrieve_by_id(id=id)
    table_do: TableDO = await db_table_service.retrieve_by_id(
        id=gen_table_do.db_table_id
    )
    await remove_logic(id)
    table_query = TableQuery(
        database_id=table_do.database_id, current=1, pageSize=200
    )
    records, total = await db_table_service.list_tables(data=table_query)
    table_id: int = 0
    for record in records:
        if record.name == gen_table_do.table_name:
            table_id = record.id
            break
    table_import = TableImport(
        database_id=table_do.database_id,
        table_ids=[table_id],
        backend=gen_table_do.backend,
    )
    await gen_table_service.import_gen_table(table_import=table_import)
    records, total = await gen_table_service.list_gen_tables(
        data=GenTableQuery(current=1, pageSize=200)
    )
    gen_table_id: int = 0
    for record in records:
        if record.table_name == gen_table_do.table_name:
            gen_table_id = record.id
            break
    new_gen_table_do: GenTableDO = await gen_table_service.retrieve_by_id(
        id=gen_table_id
    )
    new_gen_table_do.id = gen_table_do.id
    await gen_table_service.remove_by_id(id=new_gen_table_do.id)
    await gen_table_service.save(data=new_gen_table_do)
    return result.success()


@gen_table_router.delete("/gen-table/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete gen_tables by a list of IDs.

    Args:
        ids: List of gen_table IDs to delete.

    Returns:
        Success result message
    """
    await gen_table_service.batch_remove_by_ids(ids=ids)
    return result.success()
