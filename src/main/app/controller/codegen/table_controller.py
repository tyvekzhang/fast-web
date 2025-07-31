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

from io import BytesIO
from typing import Annotated, Union

from fastapi import APIRouter, Query
from starlette.responses import StreamingResponse

from src.main.app.core.schema import ListResult
from src.main.app.core.utils.time_util import get_date_time
from src.main.app.enums import BusinessErrorCode
from src.main.app.exception import BusinessException
from src.main.app.mapper.codegen.field_mapper import fieldMapper
from src.main.app.mapper.codegen.meta_field_mapper import metaFieldMapper
from src.main.app.mapper.codegen.meta_table_mapper import metaTableMapper
from src.main.app.mapper.codegen.table_mapper import tableMapper
from src.main.app.model.codegen.table_model import TableModel
from src.main.app.schema.codegen.meta_field_schema import ListFieldsRequest
from src.main.app.schema.codegen.meta_table_schema import ListMetaTablesRequest
from src.main.app.schema.codegen.table_schema import ListTablesRequest, ImportTable, TableDetail
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
meta_table_service: MetaTableService = MetaTableServiceImpl(mapper=metaTableMapper)
table_service: TableService = TableServiceImpl(mapper=tableMapper)
field_service: FieldService = FieldServiceImpl(mapper=fieldMapper)
meta_field_service: MetaFieldService = MetaFieldServiceImpl(mapper=metaFieldMapper)


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


@table_router.post("/tables:import")
async def import_tables(req: ImportTable) -> None:
    """
    Import tables from external source.

    Args:
        req: Import request containing table IDs to import.

    Returns:
        None

    Raises:
        BusinessException: If table_ids parameter is empty.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    table_ids = req.table_ids
    if not table_ids:
        raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
    for table_id in table_ids:
        await meta_field_service.list_fields(req=ListFieldsRequest(table_id=table_id))
    await table_service.import_tables(req=req)


@table_router.post("/tables:sync/{id}")
async def sync_table(
    id: int,
) -> None:
    table_record: TableModel = await table_service.retrieve_by_id(id=id)
    req = ListMetaTablesRequest(
        database_id=table_record.database_id, table_name=table_record.table_name
    )
    await table_service.delete_table(id)
    records, total = await meta_table_service.list_meta_tables(req=req)
    if not records:
        raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
    table_import = ImportTable(
        database_id=table_record.database_id,
        table_ids=[records[0].id],
        backend=table_record.backend,
    )
    await table_service.import_tables(req=table_import)
    req = ListTablesRequest(
        database_id=table_record.database_id, table_name=table_record.table_name
    )
    records, total = await table_service.list_tables(req=req)
    if not records:
        raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
    new_table_record: TableModel = await table_service.retrieve_by_id(id=records[0].id)
    await table_service.remove_by_id(id=new_table_record.id)
    new_table_record.id = table_record.id
    await table_service.save(data=new_table_record)


@table_router.get("/tables:preview/{id}")
async def preview_code(id: int) -> dict:
    """
    Preview generated code for a table.

    Args:
        id: Table ID to preview code.

    Returns:
        dict: Preview data containing code information.

    Raises:
        HTTPException(404 Not Found): If table with specified ID doesn't exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    result = await table_service.preview_code(id=id)
    return result


@table_router.get("/tables/{id}")
async def get_table_detail(
    id: int,
) -> TableDetail:
    """
    Get detailed information about a table.

    Args:
        id: Table ID to retrieve details.

    Returns:
        TableDetail: Complete table information.

    Raises:
        HTTPException(404 Not Found): If table with specified ID doesn't exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    result = await table_service.get_table_detail(id=id)
    return result


@table_router.put("/tables")
async def update_table(
    req: TableDetail,
) -> None:
    """
    Update table information.

    Args:
        req: Command containing updated table info.

    Returns:
        None

    Raises:
        HTTPException(404 Not Found): If table with specified ID doesn't exist.
        HTTPException(403 Forbidden): If user don't have access rights.
        HTTPException(400 Bad Request): If request data is invalid.
    """
    await table_service.update_table(req=req)


@table_router.delete("/tables/{id}")
async def delete_table(
    id: int,
) -> None:
    """
    Remove a table by their ID.

    Args:
        id: Table ID to remove.

    Raises:
        HTTPException(404 Not Found): If table with specified ID doesn't exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await table_service.delete_table(id=id)


@table_router.get("/tables:download")
async def download_code(table_id: Union[int, list[int]] = Query(...)) -> StreamingResponse:
    """
    Download generated code for one or multiple tables as ZIP archive.

    Args:
        table_id: Single table ID or list of table IDs to download code.

    Returns:
        StreamingResponse: ZIP file containing generated code.

    Raises:
        HTTPException(404 Not Found): If any table with specified ID doesn't exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    # Convert single ID to list for consistent processing
    table_ids = [table_id] if isinstance(table_id, int) else table_id

    code_data = await table_service.download_code(table_ids)

    # Generate filename
    if len(table_ids) == 1:
        table_record = await table_service.retrieve_by_id(id=table_ids[0])
        file_name = f"{table_record.table_name}_{get_date_time()}.zip"
    else:
        file_name = f"tables_bundle_{get_date_time()}.zip"

    return StreamingResponse(
        BytesIO(code_data),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
