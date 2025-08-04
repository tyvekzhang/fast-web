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
"""UserRole schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListUserRolesRequest(PaginationRequest):
    id: Optional[int] = None
    create_time: Optional[datetime] = None


class UserRole(BaseModel):
    id: int
    role_id: int
    create_time: Optional[datetime] = None


class UserRoleDetail(BaseModel):
    id: int
    role_id: int
    create_time: Optional[datetime] = None


class CreateUserRole(BaseModel):
    role_id: int


class CreateUserRoleRequest(BaseModel):
    user_role: CreateUserRole = Field(alias="userRole")


class UpdateUserRole(BaseModel):
    id: int
    role_id: int


class UpdateUserRoleRequest(BaseModel):
    user_role: UpdateUserRole = Field(alias="userRole")


class BatchGetUserRolesResponse(BaseModel):
    user_roles: list[UserRoleDetail] = Field(default_factory=list, alias="userRoles")


class BatchCreateUserRolesRequest(BaseModel):
    user_roles: list[CreateUserRole] = Field(default_factory=list, alias="userRoles")


class BatchCreateUserRolesResponse(BaseModel):
    user_roles: list[UserRole] = Field(default_factory=list, alias="userRoles")


class BatchUpdateUserRole(BaseModel):
    role_id: int


class BatchUpdateUserRolesRequest(BaseModel):
    ids: list[int]
    user_role: BatchUpdateUserRole = Field(alias="userRole")


class BatchPatchUserRolesRequest(BaseModel):
    user_roles: list[UpdateUserRole] = Field(default_factory=list, alias="userRoles")


class BatchUpdateUserRolesResponse(BaseModel):
    user_roles: list[UserRole] = Field(default_factory=list, alias="userRoles")


class BatchDeleteUserRolesRequest(BaseModel):
    ids: list[int]


class ExportUserRole(UserRole):
    pass


class ExportUserRolesRequest(BaseModel):
    ids: list[int]


class ImportUserRolesRequest(BaseModel):
    file: UploadFile


class ImportUserRole(CreateUserRole):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportUserRolesResponse(BaseModel):
    user_roles: list[ImportUserRole] = Field(default_factory=list, alias="userRoles")
