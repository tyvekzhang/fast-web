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
from src.main.app.mapper.system.role_mapper import roleMapper
from src.main.app.model.system.role_model import RoleModel
from src.main.app.schema.system.role_schema import (
    ListRolesRequest,
    Role,
    CreateRoleRequest,
    RoleDetail,
    UpdateRoleRequest,
    BatchDeleteRolesRequest,
    BatchUpdateRolesRequest,
    BatchUpdateRolesResponse,
    BatchCreateRolesRequest,
    BatchCreateRolesResponse,
    ExportRolesRequest,
    ImportRolesResponse,
    BatchGetRolesResponse,
    ImportRolesRequest,
    ImportRole,
    BatchPatchRolesRequest,
)
from src.main.app.service.impl.system.role_service_impl import RoleServiceImpl
from src.main.app.service.system.role_service import RoleService

role_router = APIRouter()
role_service: RoleService = RoleServiceImpl(mapper=roleMapper)


@role_router.get("/roles/{id}")
async def get_role(id: int) -> RoleDetail:
    """
    Retrieve role details.

    Args:

        id: Unique ID of the role resource.

    Returns:

        RoleDetail: The role object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested role does not exist.
    """
    role_record: RoleModel = await role_service.get_role(id=id)
    return RoleDetail(**role_record.model_dump())


@role_router.get("/roles")
async def list_roles(
    req: Annotated[ListRolesRequest, Query()],
) -> ListResult[Role]:
    """
    List roles with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of roles and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    role_records, total = await role_service.list_roles(req=req)
    role_records_with_children: list[Role] = await role_service.get_children_recursively(
        parent_data=role_records, schema_class=Role
    )
    return ListResult(records=role_records_with_children, total=total)


@role_router.post("/roles")
async def creat_role(
    req: CreateRoleRequest,
) -> Role:
    """
    Create a new role.

    Args:

        req: Request object containing role creation data.

    Returns:

         Role: The role object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    role: RoleModel = await role_service.create_role(req=req)
    return Role(**role.model_dump())


@role_router.put("/roles")
async def update_role(
    req: UpdateRoleRequest,
) -> Role:
    """
    Update an existing role.

    Args:

        req: Request object containing role update data.

    Returns:

        Role: The updated role object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the role to update doesn't exist.
    """
    role: RoleModel = await role_service.update_role(req=req)
    return Role(**role.model_dump())


@role_router.delete("/roles/{id}")
async def delete_role(
    id: int,
) -> None:
    """
    Delete role by ID.

    Args:

        id: The ID of the role to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the role with given ID doesn't exist.
    """
    await role_service.delete_role(id=id)


@role_router.get("/roles:batchGet")
async def batch_get_roles(
    ids: list[int] = Query(..., description="List of role IDs to retrieve"),
) -> BatchGetRolesResponse:
    """
    Retrieves multiple roles by their IDs.

    Args:

        ids (list[int]): A list of role resource IDs.

    Returns:

        list[RoleDetail]: A list of role objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested roles does not exist.
    """
    role_records: list[RoleModel] = await role_service.batch_get_roles(ids)
    role_detail_list: list[RoleDetail] = [
        RoleDetail(**role_record.model_dump()) for role_record in role_records
    ]
    return BatchGetRolesResponse(roles=role_detail_list)


@role_router.post("/roles:batchCreate")
async def batch_create_roles(
    req: BatchCreateRolesRequest,
) -> BatchCreateRolesResponse:
    """
    Batch create roles.

    Args:

        req (BatchCreateRolesRequest): Request body containing a list of role creation items.

    Returns:

        BatchCreateRolesResponse: Response containing the list of created roles.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any role creation data already exists.
    """

    role_records = await role_service.batch_create_roles(req=req)
    role_list: list[Role] = [Role(**role_record.model_dump()) for role_record in role_records]
    return BatchCreateRolesResponse(roles=role_list)


@role_router.post("/roles:batchUpdate")
async def batch_update_roles(
    req: BatchUpdateRolesRequest,
) -> BatchUpdateRolesResponse:
    """
    Batch update multiple roles with the same changes.

    Args:

        req (BatchUpdateRolesRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated roles.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify roles
        HTTPException 404 (Not Found): If any specified role ID doesn't exist
    """
    role_records: list[RoleModel] = await role_service.batch_update_roles(req=req)
    role_list: list[Role] = [Role(**role.model_dump()) for role in role_records]
    return BatchUpdateRolesResponse(roles=role_list)


@role_router.post("/roles:batchPatch")
async def batch_patch_roles(
    req: BatchPatchRolesRequest,
) -> BatchUpdateRolesResponse:
    """
    Batch update multiple roles with individual changes.

    Args:

        req (BatchPatchRolesRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated roles.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify roles
        HTTPException 404 (Not Found): If any specified role ID doesn't exist
    """
    role_records: list[RoleModel] = await role_service.batch_patch_roles(req=req)
    role_list: list[Role] = [Role(**role.model_dump()) for role in role_records]
    return BatchUpdateRolesResponse(roles=role_list)


@role_router.post("/roles:batchDelete")
async def batch_delete_roles(
    req: BatchDeleteRolesRequest,
) -> None:
    """
    Batch delete roles.

    Args:
        req (BatchDeleteRolesRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the roles do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await role_service.batch_delete_roles(req=req)


@role_router.get("/roles:exportTemplate")
async def export_roles_template() -> StreamingResponse:
    """
    Export the Excel template for role import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await role_service.export_roles_template()


@role_router.get("/roles:export")
async def export_roles(
    req: ExportRolesRequest = Query(...),
) -> StreamingResponse:
    """
    Export role data based on the provided role IDs.

    Args:
        req (ExportRolesRequest): Query parameters specifying the roles to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching roles are found.
    """
    return await role_service.export_roles(
        req=req,
    )


@role_router.post("/roles:import")
async def import_roles(
    req: ImportRolesRequest = Form(...),
) -> ImportRolesResponse:
    """
    Import roles from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing role data to import.

    Returns:
        ImportRolesResponse: List of successfully parsed role data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_roles_resp: list[ImportRole] = await role_service.import_roles(req=req)
    return ImportRolesResponse(roles=import_roles_resp)
