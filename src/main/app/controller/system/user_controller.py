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
from src.main.app.mapper.system.user_mapper import userMapper
from src.main.app.model.system.user_model import UserModel
from src.main.app.schema.system.user_schema import (
    ListUsersRequest,
    User,
    CreateUserRequest,
    UserDetail,
    UpdateUserRequest,
    BatchDeleteUsersRequest,
    BatchUpdateUsersRequest,
    BatchUpdateUsersResponse,
    BatchCreateUsersRequest,
    BatchCreateUsersResponse,
    ExportUsersRequest,
    ImportUsersResponse,
    BatchGetUsersResponse,
    ImportUsersRequest,
    ImportUser,
    BatchPatchUsersRequest,
)
from src.main.app.service.impl.system.user_service_impl import UserServiceImpl
from src.main.app.service.system.user_service import UserService

user_router = APIRouter()
user_service: UserService = UserServiceImpl(mapper=userMapper)


@user_router.get("/users/{id}")
async def get_user(id: int) -> UserDetail:
    """
    Retrieve user details.

    Args:

        id: Unique ID of the user resource.

    Returns:

        UserDetail: The user object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested user does not exist.
    """
    user_record: UserModel = await user_service.get_user(id=id)
    return UserDetail(**user_record.model_dump())


@user_router.get("/users")
async def list_users(
    req: Annotated[ListUsersRequest, Query()],
) -> ListResult[User]:
    """
    List users with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of users and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    user_records, total = await user_service.list_users(req=req)
    user_records_with_children: list[User] = await user_service.get_children_recursively(
        parent_data=user_records, schema_class=User
    )
    return ListResult(records=user_records_with_children, total=total)


@user_router.post("/users")
async def creat_user(
    req: CreateUserRequest,
) -> User:
    """
    Create a new user.

    Args:

        req: Request object containing user creation data.

    Returns:

         User: The user object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    user: UserModel = await user_service.create_user(req=req)
    return User(**user.model_dump())


@user_router.put("/users")
async def update_user(
    req: UpdateUserRequest,
) -> User:
    """
    Update an existing user.

    Args:

        req: Request object containing user update data.

    Returns:

        User: The updated user object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the user to update doesn't exist.
    """
    user: UserModel = await user_service.update_user(req=req)
    return User(**user.model_dump())


@user_router.delete("/users/{id}")
async def delete_user(
    id: int,
) -> None:
    """
    Delete user by ID.

    Args:

        id: The ID of the user to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the user with given ID doesn't exist.
    """
    await user_service.delete_user(id=id)


@user_router.get("/users:batchGet")
async def batch_get_users(
    ids: list[int] = Query(..., description="List of user IDs to retrieve"),
) -> BatchGetUsersResponse:
    """
    Retrieves multiple users by their IDs.

    Args:

        ids (list[int]): A list of user resource IDs.

    Returns:

        list[UserDetail]: A list of user objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested users does not exist.
    """
    user_records: list[UserModel] = await user_service.batch_get_users(ids)
    user_detail_list: list[UserDetail] = [
        UserDetail(**user_record.model_dump()) for user_record in user_records
    ]
    return BatchGetUsersResponse(users=user_detail_list)


@user_router.post("/users:batchCreate")
async def batch_create_users(
    req: BatchCreateUsersRequest,
) -> BatchCreateUsersResponse:
    """
    Batch create users.

    Args:

        req (BatchCreateUsersRequest): Request body containing a list of user creation items.

    Returns:

        BatchCreateUsersResponse: Response containing the list of created users.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any user creation data already exists.
    """

    user_records = await user_service.batch_create_users(req=req)
    user_list: list[User] = [User(**user_record.model_dump()) for user_record in user_records]
    return BatchCreateUsersResponse(users=user_list)


@user_router.post("/users:batchUpdate")
async def batch_update_users(
    req: BatchUpdateUsersRequest,
) -> BatchUpdateUsersResponse:
    """
    Batch update multiple users with the same changes.

    Args:

        req (BatchUpdateUsersRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated users.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify users
        HTTPException 404 (Not Found): If any specified user ID doesn't exist
    """
    user_records: list[UserModel] = await user_service.batch_update_users(req=req)
    user_list: list[User] = [User(**user.model_dump()) for user in user_records]
    return BatchUpdateUsersResponse(users=user_list)


@user_router.post("/users:batchPatch")
async def batch_patch_users(
    req: BatchPatchUsersRequest,
) -> BatchUpdateUsersResponse:
    """
    Batch update multiple users with individual changes.

    Args:

        req (BatchPatchUsersRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated users.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify users
        HTTPException 404 (Not Found): If any specified user ID doesn't exist
    """
    user_records: list[UserModel] = await user_service.batch_patch_users(req=req)
    user_list: list[User] = [User(**user.model_dump()) for user in user_records]
    return BatchUpdateUsersResponse(users=user_list)


@user_router.post("/users:batchDelete")
async def batch_delete_users(
    req: BatchDeleteUsersRequest,
) -> None:
    """
    Batch delete users.

    Args:
        req (BatchDeleteUsersRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the users do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await user_service.batch_delete_users(req=req)


@user_router.get("/users:exportTemplate")
async def export_users_template() -> StreamingResponse:
    """
    Export the Excel template for user import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await user_service.export_users_template()


@user_router.get("/users:export")
async def export_users(
    req: ExportUsersRequest = Query(...),
) -> StreamingResponse:
    """
    Export user data based on the provided user IDs.

    Args:
        req (ExportUsersRequest): Query parameters specifying the users to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching users are found.
    """
    return await user_service.export_users(
        req=req,
    )


@user_router.post("/users:import")
async def import_users(
    req: ImportUsersRequest = Form(...),
) -> ImportUsersResponse:
    """
    Import users from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing user data to import.

    Returns:
        ImportUsersResponse: List of successfully parsed user data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_users_resp: list[ImportUser] = await user_service.import_users(req=req)
    return ImportUsersResponse(users=import_users_resp)
