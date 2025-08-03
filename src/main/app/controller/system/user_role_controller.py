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
from src.main.app.mapper.system.user_role_mapper import userRoleMapper
from src.main.app.model.system.user_role_model import UserRoleModel
from src.main.app.schema.system.user_role_schema import (
    ListUserRolesRequest,
    UserRole,
    CreateUserRoleRequest,
    UserRoleDetail,
    UpdateUserRoleRequest,
    BatchDeleteUserRolesRequest,
    BatchUpdateUserRolesRequest,
    BatchUpdateUserRolesResponse,
    BatchCreateUserRolesRequest,
    BatchCreateUserRolesResponse,
    ExportUserRolesRequest,
    ImportUserRolesResponse,
    BatchGetUserRolesResponse,
    ImportUserRolesRequest,
    ImportUserRole,
    BatchPatchUserRolesRequest,
)
from src.main.app.service.impl.system.user_role_service_impl import UserRoleServiceImpl
from src.main.app.service.system.user_role_service import UserRoleService

user_role_router = APIRouter()
user_role_service: UserRoleService = UserRoleServiceImpl(mapper=userRoleMapper)


@user_role_router.get("/userRoles/{id}")
async def get_user_role(id: int) -> UserRoleDetail:
    """
    Retrieve user_role details.

    Args:

        id: Unique ID of the user_role resource.

    Returns:

        UserRoleDetail: The user_role object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested user_role does not exist.
    """
    user_role_record: UserRoleModel = await user_role_service.get_user_role(id=id)
    return UserRoleDetail(**user_role_record.model_dump())


@user_role_router.get("/userRoles")
async def list_user_roles(
    req: Annotated[ListUserRolesRequest, Query()],
) -> ListResult[UserRole]:
    """
    List user_roles with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of user_roles and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    user_role_records, total = await user_role_service.list_user_roles(req=req)
    user_role_records_with_children: list[
        UserRole
    ] = await user_role_service.get_children_recursively(
        parent_data=user_role_records, schema_class=UserRole
    )
    return ListResult(records=user_role_records_with_children, total=total)


@user_role_router.post("/userRoles")
async def creat_user_role(
    req: CreateUserRoleRequest,
) -> UserRole:
    """
    Create a new user_role.

    Args:

        req: Request object containing user_role creation data.

    Returns:

         UserRole: The user_role object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    user_role: UserRoleModel = await user_role_service.create_user_role(req=req)
    return UserRole(**user_role.model_dump())


@user_role_router.put("/userRoles")
async def update_user_role(
    req: UpdateUserRoleRequest,
) -> UserRole:
    """
    Update an existing user_role.

    Args:

        req: Request object containing user_role update data.

    Returns:

        UserRole: The updated user_role object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the user_role to update doesn't exist.
    """
    user_role: UserRoleModel = await user_role_service.update_user_role(req=req)
    return UserRole(**user_role.model_dump())


@user_role_router.delete("/userRoles/{id}")
async def delete_user_role(
    id: int,
) -> None:
    """
    Delete user_role by ID.

    Args:

        id: The ID of the user_role to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the user_role with given ID doesn't exist.
    """
    await user_role_service.delete_user_role(id=id)


@user_role_router.get("/userRoles:batchGet")
async def batch_get_user_roles(
    ids: list[int] = Query(..., description="List of user_role IDs to retrieve"),
) -> BatchGetUserRolesResponse:
    """
    Retrieves multiple user_roles by their IDs.

    Args:

        ids (list[int]): A list of user_role resource IDs.

    Returns:

        list[UserRoleDetail]: A list of user_role objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested user_roles does not exist.
    """
    user_role_records: list[UserRoleModel] = await user_role_service.batch_get_user_roles(ids)
    user_role_detail_list: list[UserRoleDetail] = [
        UserRoleDetail(**user_role_record.model_dump()) for user_role_record in user_role_records
    ]
    return BatchGetUserRolesResponse(user_roles=user_role_detail_list)


@user_role_router.post("/userRoles:batchCreate")
async def batch_create_user_roles(
    req: BatchCreateUserRolesRequest,
) -> BatchCreateUserRolesResponse:
    """
    Batch create user_roles.

    Args:

        req (BatchCreateUserRolesRequest): Request body containing a list of user_role creation items.

    Returns:

        BatchCreateUserRolesResponse: Response containing the list of created user_roles.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any user_role creation data already exists.
    """

    user_role_records = await user_role_service.batch_create_user_roles(req=req)
    user_role_list: list[UserRole] = [
        UserRole(**user_role_record.model_dump()) for user_role_record in user_role_records
    ]
    return BatchCreateUserRolesResponse(user_roles=user_role_list)


@user_role_router.post("/userRoles:batchUpdate")
async def batch_update_user_roles(
    req: BatchUpdateUserRolesRequest,
) -> BatchUpdateUserRolesResponse:
    """
    Batch update multiple user_roles with the same changes.

    Args:

        req (BatchUpdateUserRolesRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated user_roles.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify user_roles
        HTTPException 404 (Not Found): If any specified user_role ID doesn't exist
    """
    user_role_records: list[UserRoleModel] = await user_role_service.batch_update_user_roles(
        req=req
    )
    user_role_list: list[UserRole] = [
        UserRole(**user_role.model_dump()) for user_role in user_role_records
    ]
    return BatchUpdateUserRolesResponse(user_roles=user_role_list)


@user_role_router.post("/userRoles:batchPatch")
async def batch_patch_user_roles(
    req: BatchPatchUserRolesRequest,
) -> BatchUpdateUserRolesResponse:
    """
    Batch update multiple user_roles with individual changes.

    Args:

        req (BatchPatchUserRolesRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated user_roles.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify user_roles
        HTTPException 404 (Not Found): If any specified user_role ID doesn't exist
    """
    user_role_records: list[UserRoleModel] = await user_role_service.batch_patch_user_roles(req=req)
    user_role_list: list[UserRole] = [
        UserRole(**user_role.model_dump()) for user_role in user_role_records
    ]
    return BatchUpdateUserRolesResponse(user_roles=user_role_list)


@user_role_router.post("/userRoles:batchDelete")
async def batch_delete_user_roles(
    req: BatchDeleteUserRolesRequest,
) -> None:
    """
    Batch delete user_roles.

    Args:
        req (BatchDeleteUserRolesRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the user_roles do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await user_role_service.batch_delete_user_roles(req=req)


@user_role_router.get("/userRoles:exportTemplate")
async def export_user_roles_template() -> StreamingResponse:
    """
    Export the Excel template for user_role import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await user_role_service.export_user_roles_template()


@user_role_router.get("/userRoles:export")
async def export_user_roles(
    req: ExportUserRolesRequest = Query(...),
) -> StreamingResponse:
    """
    Export user_role data based on the provided user_role IDs.

    Args:
        req (ExportUserRolesRequest): Query parameters specifying the user_roles to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching user_roles are found.
    """
    return await user_role_service.export_user_roles(
        req=req,
    )


@user_role_router.post("/userRoles:import")
async def import_user_roles(
    req: ImportUserRolesRequest = Form(...),
) -> ImportUserRolesResponse:
    """
    Import user_roles from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing user_role data to import.

    Returns:
        ImportUserRolesResponse: List of successfully parsed user_role data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_user_roles_resp: list[ImportUserRole] = await user_role_service.import_user_roles(
        req=req
    )
    return ImportUserRolesResponse(user_roles=import_user_roles_resp)
