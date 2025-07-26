"""Table operation controller"""

import subprocess
import sys
from typing import Dict, Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form
from src.main.app.core import result
from src.main.app.core.result import HttpResponse
from src.main.app.core.utils.excel_util import export_excel
from src.main.app.mapper.table_mapper import tableMapper
from src.main.app.model.db_table_model import TableDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.table_schema import (
    TableAdd,
    TableExport,
    TableQueryForm,
    TableModify,
    TableQuery,
    TableGenerate,
)
from src.main.app.schema.user_schema import Ids
from src.main.app.service.table_service import TableService
from src.main.app.service.impl.table_service_impl import TableServiceImpl
from starlette.responses import StreamingResponse

table_router = APIRouter()
table_service: TableService = TableServiceImpl(mapper=tableMapper)


@table_router.post("/table/add")
async def add_table(
    data: TableAdd,
) -> Dict:
    """
    Table add.

    Args:
        data: Data required for add.

    Returns:
        BaseResponse with new table's ID.
    """
    table: TableDO = await table_service.save(data=TableDO(**data.model_dump()))
    return result.success(data=table.id)


@table_router.get("/table/tables")
async def list_tables(
    table_query: Annotated[TableQuery, Query()],
) -> HttpResponse[PageResult]:
    """
    Filter tables with pagination.

    Args:
        table_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    table_list, total_count = await table_service.list_tables(data=table_query)

    return HttpResponse(
        data=PageResult(records=table_list, total_count=total_count)
    )


@table_router.post("/table/generate")
async def generate_table(table_generate: TableGenerate) -> Dict:
    await table_service.generate_table(table_generate)
    return result.success()


@table_router.post("/table/run_script")
async def run_script(script_path: str):
    try:
        # 使用 subprocess 执行 Python 脚本
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True,
        )
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "stdout": e.stdout, "stderr": e.stderr}


@table_router.post("/table/recover")
async def recover(
    data: TableDO,
) -> Dict:
    """
    Table recover that be deleted.

    Args:
        data: Table recover data

    Returns:
        BaseResponse with table's ID.
    """
    table: TableDO = await table_service.save(data=data)
    return result.success(data=table.id)


@table_router.get("/table/exporttemplate")
async def export_template() -> StreamingResponse:
    """
    Export a template for table information.

    Returns:
        StreamingResponse with table field
    """
    return await export_excel(
        schema=TableExport, file_name="table_import_template"
    )


@table_router.post("/table/import")
async def import_table(
    file: UploadFile = Form(),
) -> Dict:
    """
    Import table information from a file.

    Args:
        file: The file containing table information to import.

    Returns:
        Success result message
    """
    success_count = await table_service.import_table(file=file)
    return result.success(data=f"Success import count: {success_count}")


@table_router.get("/table/export")
async def export(
    data: Annotated[TableQueryForm, Query()],
) -> StreamingResponse:
    """
    Export table information based on provided parameters.

    Args:
        data: Filtering and format parameters for export.

    Returns:
        StreamingResponse with table info
    """
    return await table_service.export_table(params=data)


@table_router.put("/table/modify")
async def modify(
    data: TableModify,
) -> Dict:
    """
    Update table information.

    Args:
        data: Command containing updated table info.

    Returns:
        Success result message
    """
    await table_service.modify_by_id(
        data=TableDO(**data.model_dump(exclude_unset=True))
    )
    return result.success()


@table_router.put("/table/batchmodify")
async def batch_modify(ids: Ids, data: TableModify) -> Dict:
    cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if len(cleaned_data) == 0:
        return result.fail("Please fill in the modify information")

    await table_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
    return result.success()


@table_router.delete("/table/remove/{id}")
async def remove(
    id: int,
) -> Dict:
    """
    Remove a table by their ID.

    Args:
        id: Table ID to remove.

    Returns:
        Success result message
    """
    await table_service.remove_by_id(id=id)
    return result.success()


@table_router.delete("/table/batchremove")
async def batch_remove(
    ids: List[int] = Query(...),
) -> Dict:
    """
    Delete tables by a list of IDs.

    Args:
        ids: List of table IDs to delete.

    Returns:
        Success result message
    """
    await table_service.batch_remove_by_ids(ids=ids)
    return result.success()
