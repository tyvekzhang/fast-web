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
"""REST Controller"""

from __future__ import annotations
from typing import Annotated

from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.core.schema import ListResult
from src.main.app.mapper.codegen.dict_datum_mapper import dictDatumMapper
from src.main.app.model.codegen.dict_datum_model import DictDatumModel
from src.main.app.schema.codegen.dict_datum_schema import (
    ListDictDataRequest,
    DictDatum,
    CreateDictDatumRequest,
    DictDatumDetail,
    UpdateDictDatumRequest,
    BatchDeleteDictDataRequest,
    BatchUpdateDictDataRequest,
    BatchUpdateDictDataResponse,
    BatchCreateDictDataRequest,
    BatchCreateDictDataResponse,
    ExportDictDataRequest,
    ImportDictDataResponse,
    BatchGetDictDataResponse,
    ImportDictDataRequest,
    ImportDictDatum,
    BatchPatchDictDataRequest,
)
from src.main.app.service.impl.codegen.dict_datum_service_impl import DictDatumServiceImpl
from src.main.app.service.codegen.dict_datum_service import DictDatumService

dict_datum_router = APIRouter()
dict_datum_service: DictDatumService = DictDatumServiceImpl(mapper=dictDatumMapper)


@dict_datum_router.get("/dictData/{id}")
async def get_dict_datum(id: int) -> DictDatumDetail:
    """
    Retrieve dict_datum details.

    Args:

        id: Unique ID of the dict_datum resource.

    Returns:

        DictDatumDetail: The dict_datum object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested dict_datum does not exist.
    """
    dict_datum_record: DictDatumModel = await dict_datum_service.get_dict_datum(id=id)
    return DictDatumDetail(**dict_datum_record.model_dump())


@dict_datum_router.get("/dictData")
async def list_dict_data(
    req: Annotated[ListDictDataRequest, Query()],
) -> ListResult[DictDatum]:
    """
    List dict_data with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of dict_data and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    dict_datum_records, total = await dict_datum_service.list_dict_data(req=req)
    return ListResult(records=dict_datum_records, total=total)


@dict_datum_router.post("/dictData")
async def creat_dict_datum(
    req: CreateDictDatumRequest,
) -> DictDatum:
    """
    Create a new dict_datum.

    Args:

        req: Request object containing dict_datum creation data.

    Returns:

         DictDatum: The dict_datum object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    dict_datum: DictDatumModel = await dict_datum_service.create_dict_datum(req=req)
    return DictDatum(**dict_datum.model_dump())


@dict_datum_router.put("/dictData")
async def update_dict_datum(
    req: UpdateDictDatumRequest,
) -> DictDatum:
    """
    Update an existing dict_datum.

    Args:

        req: Request object containing dict_datum update data.

    Returns:

        DictDatum: The updated dict_datum object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the dict_datum to update doesn't exist.
    """
    dict_datum: DictDatumModel = await dict_datum_service.update_dict_datum(req=req)
    return DictDatum(**dict_datum.model_dump())


@dict_datum_router.delete("/dictData/{id}")
async def delete_dict_datum(
    id: int,
) -> None:
    """
    Delete dict_datum by ID.

    Args:

        id: The ID of the dict_datum to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the dict_datum with given ID doesn't exist.
    """
    await dict_datum_service.delete_dict_datum(id=id)


@dict_datum_router.get("/dictData:batchGet")
async def batch_get_dict_data(
    ids: list[int] = Query(..., description="List of dict_datum IDs to retrieve"),
) -> BatchGetDictDataResponse:
    """
    Retrieves multiple dict_data by their IDs.

    Args:

        ids (list[int]): A list of dict_datum resource IDs.

    Returns:

        list[DictDatumDetail]: A list of dict_datum objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested dict_data does not exist.
    """
    dict_datum_records: list[DictDatumModel] = await dict_datum_service.batch_get_dict_data(ids)
    dict_datum_detail_list: list[DictDatumDetail] = [
        DictDatumDetail(**dict_datum_record.model_dump())
        for dict_datum_record in dict_datum_records
    ]
    return BatchGetDictDataResponse(dict_data=dict_datum_detail_list)


@dict_datum_router.post("/dictData:batchCreate")
async def batch_create_dict_data(
    req: BatchCreateDictDataRequest,
) -> BatchCreateDictDataResponse:
    """
    Batch create dict_data.

    Args:

        req (BatchCreateDictDataRequest): Request body containing a list of dict_datum creation items.

    Returns:

        BatchCreateDictDataResponse: Response containing the list of created dict_data.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any dict_datum creation data already exists.
    """

    dict_datum_records = await dict_datum_service.batch_create_dict_data(req=req)
    dict_datum_list: list[DictDatum] = [
        DictDatum(**dict_datum_record.model_dump()) for dict_datum_record in dict_datum_records
    ]
    return BatchCreateDictDataResponse(dict_data=dict_datum_list)


@dict_datum_router.post("/dictData:batchUpdate")
async def batch_update_dict_data(
    req: BatchUpdateDictDataRequest,
) -> BatchUpdateDictDataResponse:
    """
    Batch update multiple dict_data with the same changes.

    Args:

        req (BatchUpdateDictDataRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated dict_data.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify dict_data
        HTTPException 404 (Not Found): If any specified dict_datum ID doesn't exist
    """
    dict_datum_records: list[DictDatumModel] = await dict_datum_service.batch_update_dict_data(
        req=req
    )
    dict_datum_list: list[DictDatum] = [
        DictDatum(**dict_datum.model_dump()) for dict_datum in dict_datum_records
    ]
    return BatchUpdateDictDataResponse(dict_data=dict_datum_list)


@dict_datum_router.post("/dictData:batchPatch")
async def batch_patch_dict_data(
    req: BatchPatchDictDataRequest,
) -> BatchUpdateDictDataResponse:
    """
    Batch update multiple dict_data with individual changes.

    Args:

        req (BatchPatchDictDataRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated dict_data.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify dict_data
        HTTPException 404 (Not Found): If any specified dict_datum ID doesn't exist
    """
    dict_datum_records: list[DictDatumModel] = await dict_datum_service.batch_patch_dict_data(
        req=req
    )
    dict_datum_list: list[DictDatum] = [
        DictDatum(**dict_datum.model_dump()) for dict_datum in dict_datum_records
    ]
    return BatchUpdateDictDataResponse(dict_data=dict_datum_list)


@dict_datum_router.post("/dictData:batchDelete")
async def batch_delete_dict_data(
    req: BatchDeleteDictDataRequest,
) -> None:
    """
    Batch delete dict_data.

    Args:
        req (BatchDeleteDictDataRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the dict_data do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await dict_datum_service.batch_delete_dict_data(req=req)


@dict_datum_router.get("/dictData:exportTemplate")
async def export_dict_data_template() -> StreamingResponse:
    """
    Export the Excel template for dict_datum import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await dict_datum_service.export_dict_data_template()


@dict_datum_router.get("/dictData:export")
async def export_dict_data(
    req: ExportDictDataRequest = Query(...),
) -> StreamingResponse:
    """
    Export dict_datum data based on the provided dict_datum IDs.

    Args:
        req (ExportDictDataRequest): Query parameters specifying the dict_data to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching dict_data are found.
    """
    return await dict_datum_service.export_dict_data(
        req=req,
    )


@dict_datum_router.post("/dictData:import")
async def import_dict_data(
    req: ImportDictDataRequest = Form(...),
) -> ImportDictDataResponse:
    """
    Import dict_data from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing dict_datum data to import.

    Returns:
        ImportDictDataResponse: List of successfully parsed dict_datum data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_dict_data_resp: list[ImportDictDatum] = await dict_datum_service.import_dict_data(
        req=req
    )
    return ImportDictDataResponse(dict_data=import_dict_data_resp)
