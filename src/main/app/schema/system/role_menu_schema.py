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
"""RoleMenu schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListRoleMenusRequest(PaginationRequest):
    id: Optional[int] = None
    create_time: Optional[datetime] = None


class RoleMenu(BaseModel):
    id: int
    role_id: int
    menu_id: int
    create_time: Optional[datetime] = None


class RoleMenuDetail(BaseModel):
    id: int
    role_id: int
    menu_id: int
    create_time: Optional[datetime] = None


class CreateRoleMenu(BaseModel):
    role_id: int
    menu_id: int


class CreateRoleMenuRequest(BaseModel):
    role_menu: CreateRoleMenu = Field(alias="roleMenu")


class UpdateRoleMenu(BaseModel):
    id: int
    role_id: int
    menu_id: int


class UpdateRoleMenuRequest(BaseModel):
    role_menu: UpdateRoleMenu = Field(alias="roleMenu")


class BatchGetRoleMenusResponse(BaseModel):
    role_menus: list[RoleMenuDetail] = Field(default_factory=list, alias="roleMenus")


class BatchCreateRoleMenusRequest(BaseModel):
    role_menus: list[CreateRoleMenu] = Field(default_factory=list, alias="roleMenus")


class BatchCreateRoleMenusResponse(BaseModel):
    role_menus: list[RoleMenu] = Field(default_factory=list, alias="roleMenus")


class BatchUpdateRoleMenu(BaseModel):
    role_id: int
    menu_id: int


class BatchUpdateRoleMenusRequest(BaseModel):
    ids: list[int]
    role_menu: BatchUpdateRoleMenu = Field(alias="roleMenu")


class BatchPatchRoleMenusRequest(BaseModel):
    role_menus: list[UpdateRoleMenu] = Field(default_factory=list, alias="roleMenus")


class BatchUpdateRoleMenusResponse(BaseModel):
    role_menus: list[RoleMenu] = Field(default_factory=list, alias="roleMenus")


class BatchDeleteRoleMenusRequest(BaseModel):
    ids: list[int]


class ExportRoleMenu(RoleMenu):
    pass


class ExportRoleMenusRequest(BaseModel):
    ids: list[int]


class ImportRoleMenusRequest(BaseModel):
    file: UploadFile


class ImportRoleMenu(CreateRoleMenu):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportRoleMenusResponse(BaseModel):
    role_menus: list[ImportRoleMenu] = Field(default_factory=list, alias="roleMenus")
