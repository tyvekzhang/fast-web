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
from src.main.app.mapper.system.role_menu_mapper import roleMenuMapper
from src.main.app.model.system.role_menu_model import RoleMenuModel
from src.main.app.schema.system.role_menu_schema import (
    ListRoleMenusRequest,
    RoleMenu,
    CreateRoleMenuRequest,
    RoleMenuDetail,
    UpdateRoleMenuRequest,
    BatchDeleteRoleMenusRequest,
    BatchUpdateRoleMenusRequest,
    BatchUpdateRoleMenusResponse,
    BatchCreateRoleMenusRequest,
    BatchCreateRoleMenusResponse,
    ExportRoleMenusRequest,
    ImportRoleMenusResponse,
    BatchGetRoleMenusResponse,
    ImportRoleMenusRequest,
    ImportRoleMenu,
    BatchPatchRoleMenusRequest,
)
from src.main.app.service.impl.system.role_menu_service_impl import RoleMenuServiceImpl
from src.main.app.service.system.role_menu_service import RoleMenuService

role_menu_router = APIRouter()
role_menu_service: RoleMenuService = RoleMenuServiceImpl(mapper=roleMenuMapper)


@role_menu_router.get("/roleMenus/{id}")
async def get_role_menu(id: int) -> RoleMenuDetail:
    """
    Retrieve role_menu details.

    Args:

        id: Unique ID of the role_menu resource.

    Returns:

        RoleMenuDetail: The role_menu object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested role_menu does not exist.
    """
    role_menu_record: RoleMenuModel = await role_menu_service.get_role_menu(id=id)
    return RoleMenuDetail(**role_menu_record.model_dump())


@role_menu_router.get("/roleMenus")
async def list_role_menus(
    req: Annotated[ListRoleMenusRequest, Query()],
) -> ListResult[RoleMenu]:
    """
    List role_menus with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of role_menus and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    role_menu_records, total = await role_menu_service.list_role_menus(req=req)
    role_menu_records_with_children: list[
        RoleMenu
    ] = await role_menu_service.get_children_recursively(
        parent_data=role_menu_records, schema_class=RoleMenu
    )
    return ListResult(records=role_menu_records_with_children, total=total)


@role_menu_router.post("/roleMenus")
async def creat_role_menu(
    req: CreateRoleMenuRequest,
) -> RoleMenu:
    """
    Create a new role_menu.

    Args:

        req: Request object containing role_menu creation data.

    Returns:

         RoleMenu: The role_menu object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    role_menu: RoleMenuModel = await role_menu_service.create_role_menu(req=req)
    return RoleMenu(**role_menu.model_dump())


@role_menu_router.put("/roleMenus")
async def update_role_menu(
    req: UpdateRoleMenuRequest,
) -> RoleMenu:
    """
    Update an existing role_menu.

    Args:

        req: Request object containing role_menu update data.

    Returns:

        RoleMenu: The updated role_menu object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the role_menu to update doesn't exist.
    """
    role_menu: RoleMenuModel = await role_menu_service.update_role_menu(req=req)
    return RoleMenu(**role_menu.model_dump())


@role_menu_router.delete("/roleMenus/{id}")
async def delete_role_menu(
    id: int,
) -> None:
    """
    Delete role_menu by ID.

    Args:

        id: The ID of the role_menu to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the role_menu with given ID doesn't exist.
    """
    await role_menu_service.delete_role_menu(id=id)


@role_menu_router.get("/roleMenus:batchGet")
async def batch_get_role_menus(
    ids: list[int] = Query(..., description="List of role_menu IDs to retrieve"),
) -> BatchGetRoleMenusResponse:
    """
    Retrieves multiple role_menus by their IDs.

    Args:

        ids (list[int]): A list of role_menu resource IDs.

    Returns:

        list[RoleMenuDetail]: A list of role_menu objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested role_menus does not exist.
    """
    role_menu_records: list[RoleMenuModel] = await role_menu_service.batch_get_role_menus(ids)
    role_menu_detail_list: list[RoleMenuDetail] = [
        RoleMenuDetail(**role_menu_record.model_dump()) for role_menu_record in role_menu_records
    ]
    return BatchGetRoleMenusResponse(role_menus=role_menu_detail_list)


@role_menu_router.post("/roleMenus:batchCreate")
async def batch_create_role_menus(
    req: BatchCreateRoleMenusRequest,
) -> BatchCreateRoleMenusResponse:
    """
    Batch create role_menus.

    Args:

        req (BatchCreateRoleMenusRequest): Request body containing a list of role_menu creation items.

    Returns:

        BatchCreateRoleMenusResponse: Response containing the list of created role_menus.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any role_menu creation data already exists.
    """

    role_menu_records = await role_menu_service.batch_create_role_menus(req=req)
    role_menu_list: list[RoleMenu] = [
        RoleMenu(**role_menu_record.model_dump()) for role_menu_record in role_menu_records
    ]
    return BatchCreateRoleMenusResponse(role_menus=role_menu_list)


@role_menu_router.post("/roleMenus:batchUpdate")
async def batch_update_role_menus(
    req: BatchUpdateRoleMenusRequest,
) -> BatchUpdateRoleMenusResponse:
    """
    Batch update multiple role_menus with the same changes.

    Args:

        req (BatchUpdateRoleMenusRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated role_menus.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify role_menus
        HTTPException 404 (Not Found): If any specified role_menu ID doesn't exist
    """
    role_menu_records: list[RoleMenuModel] = await role_menu_service.batch_update_role_menus(
        req=req
    )
    role_menu_list: list[RoleMenu] = [
        RoleMenu(**role_menu.model_dump()) for role_menu in role_menu_records
    ]
    return BatchUpdateRoleMenusResponse(role_menus=role_menu_list)


@role_menu_router.post("/roleMenus:batchPatch")
async def batch_patch_role_menus(
    req: BatchPatchRoleMenusRequest,
) -> BatchUpdateRoleMenusResponse:
    """
    Batch update multiple role_menus with individual changes.

    Args:

        req (BatchPatchRoleMenusRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated role_menus.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify role_menus
        HTTPException 404 (Not Found): If any specified role_menu ID doesn't exist
    """
    role_menu_records: list[RoleMenuModel] = await role_menu_service.batch_patch_role_menus(req=req)
    role_menu_list: list[RoleMenu] = [
        RoleMenu(**role_menu.model_dump()) for role_menu in role_menu_records
    ]
    return BatchUpdateRoleMenusResponse(role_menus=role_menu_list)


@role_menu_router.post("/roleMenus:batchDelete")
async def batch_delete_role_menus(
    req: BatchDeleteRoleMenusRequest,
) -> None:
    """
    Batch delete role_menus.

    Args:
        req (BatchDeleteRoleMenusRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the role_menus do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await role_menu_service.batch_delete_role_menus(req=req)


@role_menu_router.get("/roleMenus:exportTemplate")
async def export_role_menus_template() -> StreamingResponse:
    """
    Export the Excel template for role_menu import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await role_menu_service.export_role_menus_template()


@role_menu_router.get("/roleMenus:export")
async def export_role_menus(
    req: ExportRoleMenusRequest = Query(...),
) -> StreamingResponse:
    """
    Export role_menu data based on the provided role_menu IDs.

    Args:
        req (ExportRoleMenusRequest): Query parameters specifying the role_menus to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching role_menus are found.
    """
    return await role_menu_service.export_role_menus(
        req=req,
    )


@role_menu_router.post("/roleMenus:import")
async def import_role_menus(
    req: ImportRoleMenusRequest = Form(...),
) -> ImportRoleMenusResponse:
    """
    Import role_menus from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing role_menu data to import.

    Returns:
        ImportRoleMenusResponse: List of successfully parsed role_menu data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_role_menus_resp: list[ImportRoleMenu] = await role_menu_service.import_role_menus(
        req=req
    )
    return ImportRoleMenusResponse(role_menus=import_role_menus_resp)
