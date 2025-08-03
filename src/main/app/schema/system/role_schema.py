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
"""Role schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListRolesRequest(PaginationRequest):
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    sort: Optional[int] = None
    data_scope: Optional[int] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None


class Role(BaseModel):
    id: int
    name: str
    code: str
    sort: int
    data_scope: Optional[int] = None
    data_scope_dept_ids: Optional[str] = None
    status: int
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class RoleDetail(BaseModel):
    id: int
    name: str
    code: str
    sort: int
    data_scope: Optional[int] = None
    data_scope_dept_ids: Optional[str] = None
    status: int
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class CreateRole(BaseModel):
    name: str
    code: str
    sort: int
    data_scope: Optional[int] = None
    data_scope_dept_ids: Optional[str] = None
    status: int
    comment: Optional[str] = None


class CreateRoleRequest(BaseModel):
    role: CreateRole = Field(alias="role")


class UpdateRole(BaseModel):
    id: int
    name: str
    code: str
    sort: int
    data_scope: Optional[int] = None
    data_scope_dept_ids: Optional[str] = None
    status: int
    comment: Optional[str] = None


class UpdateRoleRequest(BaseModel):
    role: UpdateRole = Field(alias="role")


class BatchGetRolesResponse(BaseModel):
    roles: list[RoleDetail] = Field(default_factory=list, alias="roles")


class BatchCreateRolesRequest(BaseModel):
    roles: list[CreateRole] = Field(default_factory=list, alias="roles")


class BatchCreateRolesResponse(BaseModel):
    roles: list[Role] = Field(default_factory=list, alias="roles")


class BatchUpdateRole(BaseModel):
    name: str
    code: str
    sort: int
    data_scope: Optional[int] = None
    data_scope_dept_ids: Optional[str] = None
    status: int
    comment: Optional[str] = None


class BatchUpdateRolesRequest(BaseModel):
    ids: list[int]
    role: BatchUpdateRole = Field(alias="role")


class BatchPatchRolesRequest(BaseModel):
    roles: list[UpdateRole] = Field(default_factory=list, alias="roles")


class BatchUpdateRolesResponse(BaseModel):
    roles: list[Role] = Field(default_factory=list, alias="roles")


class BatchDeleteRolesRequest(BaseModel):
    ids: list[int]


class ExportRole(Role):
    pass


class ExportRolesRequest(BaseModel):
    ids: list[int]


class ImportRolesRequest(BaseModel):
    file: UploadFile


class ImportRole(CreateRole):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportRolesResponse(BaseModel):
    roles: list[ImportRole] = Field(default_factory=list, alias="roles")
