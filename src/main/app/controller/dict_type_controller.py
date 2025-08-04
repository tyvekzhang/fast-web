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
from src.main.app.mapper.dict_type_mapper import dictTypeMapper
from src.main.app.model.dict_type_model import DictTypeModel
from src.main.app.schema.dict_type_schema import (
    ListDictTypesRequest,
    DictType,
    CreateDictTypeRequest,
    DictTypeDetail,
    UpdateDictTypeRequest,
    BatchDeleteDictTypesRequest,
    BatchUpdateDictTypesRequest,
    BatchUpdateDictTypesResponse,
    BatchCreateDictTypesRequest,
    BatchCreateDictTypesResponse,
    ExportDictTypesRequest,
    ImportDictTypesResponse,
    BatchGetDictTypesResponse,
    ImportDictTypesRequest,
    ImportDictType,
    BatchPatchDictTypesRequest,
)
from src.main.app.service.impl.dict_type_service_impl import DictTypeServiceImpl
from src.main.app.service.dict_type_service import DictTypeService

dict_type_router = APIRouter()
dict_type_service: DictTypeService = DictTypeServiceImpl(mapper=dictTypeMapper)


@dict_type_router.get("/dictTypes/{id}")
async def get_dict_type(id: int) -> DictTypeDetail:
    """
    Retrieve dict_type details.

    Args:

        id: Unique ID of the dict_type resource.

    Returns:

        DictTypeDetail: The dict_type object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested dict_type does not exist.
    """
    dict_type_record: DictTypeModel = await dict_type_service.get_dict_type(id=id)
    return DictTypeDetail(**dict_type_record.model_dump())


@dict_type_router.get("/dictTypes")
async def list_dict_types(
    req: Annotated[ListDictTypesRequest, Query()],
) -> ListResult[DictType]:
    """
    List dict_types with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of dict_types and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    dict_type_records, total = await dict_type_service.list_dict_types(req=req)
    return ListResult(records=dict_type_records, total=total)


@dict_type_router.post("/dictTypes")
async def creat_dict_type(
    req: CreateDictTypeRequest,
) -> DictType:
    """
    Create a new dict_type.

    Args:

        req: Request object containing dict_type creation data.

    Returns:

         DictType: The dict_type object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    dict_type: DictTypeModel = await dict_type_service.create_dict_type(req=req)
    return DictType(**dict_type.model_dump())


@dict_type_router.put("/dictTypes")
async def update_dict_type(
    req: UpdateDictTypeRequest,
) -> DictType:
    """
    Update an existing dict_type.

    Args:

        req: Request object containing dict_type update data.

    Returns:

        DictType: The updated dict_type object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the dict_type to update doesn't exist.
    """
    dict_type: DictTypeModel = await dict_type_service.update_dict_type(req=req)
    return DictType(**dict_type.model_dump())


@dict_type_router.delete("/dictTypes/{id}")
async def delete_dict_type(
    id: int,
) -> None:
    """
    Delete dict_type by ID.

    Args:

        id: The ID of the dict_type to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the dict_type with given ID doesn't exist.
    """
    await dict_type_service.delete_dict_type(id=id)


@dict_type_router.get("/dictTypes:batchGet")
async def batch_get_dict_types(
    ids: list[int] = Query(..., description="List of dict_type IDs to retrieve"),
) -> BatchGetDictTypesResponse:
    """
    Retrieves multiple dict_types by their IDs.

    Args:

        ids (list[int]): A list of dict_type resource IDs.

    Returns:

        list[DictTypeDetail]: A list of dict_type objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested dict_types does not exist.
    """
    dict_type_records: list[DictTypeModel] = await dict_type_service.batch_get_dict_types(ids)
    dict_type_detail_list: list[DictTypeDetail] = [
        DictTypeDetail(**dict_type_record.model_dump()) for dict_type_record in dict_type_records
    ]
    return BatchGetDictTypesResponse(dict_types=dict_type_detail_list)


@dict_type_router.post("/dictTypes:batchCreate")
async def batch_create_dict_types(
    req: BatchCreateDictTypesRequest,
) -> BatchCreateDictTypesResponse:
    """
    Batch create dict_types.

    Args:

        req (BatchCreateDictTypesRequest): Request body containing a list of dict_type creation items.

    Returns:

        BatchCreateDictTypesResponse: Response containing the list of created dict_types.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any dict_type creation data already exists.
    """

    dict_type_records = await dict_type_service.batch_create_dict_types(req=req)
    dict_type_list: list[DictType] = [
        DictType(**dict_type_record.model_dump()) for dict_type_record in dict_type_records
    ]
    return BatchCreateDictTypesResponse(dict_types=dict_type_list)


@dict_type_router.post("/dictTypes:batchUpdate")
async def batch_update_dict_types(
    req: BatchUpdateDictTypesRequest,
) -> BatchUpdateDictTypesResponse:
    """
    Batch update multiple dict_types with the same changes.

    Args:

        req (BatchUpdateDictTypesRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated dict_types.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify dict_types
        HTTPException 404 (Not Found): If any specified dict_type ID doesn't exist
    """
    dict_type_records: list[DictTypeModel] = await dict_type_service.batch_update_dict_types(
        req=req
    )
    dict_type_list: list[DictType] = [
        DictType(**dict_type.model_dump()) for dict_type in dict_type_records
    ]
    return BatchUpdateDictTypesResponse(dict_types=dict_type_list)


@dict_type_router.post("/dictTypes:batchPatch")
async def batch_patch_dict_types(
    req: BatchPatchDictTypesRequest,
) -> BatchUpdateDictTypesResponse:
    """
    Batch update multiple dict_types with individual changes.

    Args:

        req (BatchPatchDictTypesRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated dict_types.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify dict_types
        HTTPException 404 (Not Found): If any specified dict_type ID doesn't exist
    """
    dict_type_records: list[DictTypeModel] = await dict_type_service.batch_patch_dict_types(req=req)
    dict_type_list: list[DictType] = [
        DictType(**dict_type.model_dump()) for dict_type in dict_type_records
    ]
    return BatchUpdateDictTypesResponse(dict_types=dict_type_list)


@dict_type_router.post("/dictTypes:batchDelete")
async def batch_delete_dict_types(
    req: BatchDeleteDictTypesRequest,
) -> None:
    """
    Batch delete dict_types.

    Args:
        req (BatchDeleteDictTypesRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the dict_types do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await dict_type_service.batch_delete_dict_types(req=req)


@dict_type_router.get("/dictTypes:exportTemplate")
async def export_dict_types_template() -> StreamingResponse:
    """
    Export the Excel template for dict_type import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await dict_type_service.export_dict_types_template()


@dict_type_router.get("/dictTypes:export")
async def export_dict_types(
    req: ExportDictTypesRequest = Query(...),
) -> StreamingResponse:
    """
    Export dict_type data based on the provided dict_type IDs.

    Args:
        req (ExportDictTypesRequest): Query parameters specifying the dict_types to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching dict_types are found.
    """
    return await dict_type_service.export_dict_types(
        req=req,
    )


@dict_type_router.post("/dictTypes:import")
async def import_dict_types(
    req: ImportDictTypesRequest = Form(...),
) -> ImportDictTypesResponse:
    """
    Import dict_types from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing dict_type data to import.

    Returns:
        ImportDictTypesResponse: List of successfully parsed dict_type data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_dict_types_resp: list[ImportDictType] = await dict_type_service.import_dict_types(
        req=req
    )
    return ImportDictTypesResponse(dict_types=import_dict_types_resp)
