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
"""User schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListUsersRequest(PaginationRequest):
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None
    create_time: Optional[datetime] = None


class User(BaseModel):
    id: int
    username: str
    password: str
    nickname: str
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None
    create_time: Optional[datetime] = None


class UserDetail(BaseModel):
    id: int
    username: str
    password: str
    nickname: str
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None
    create_time: Optional[datetime] = None


class CreateUser(BaseModel):
    username: str
    password: str
    nickname: str
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None


class CreateUserRequest(BaseModel):
    user: CreateUser = Field(alias="user")


class UpdateUser(BaseModel):
    id: int
    username: str
    password: str
    nickname: str
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None


class UpdateUserRequest(BaseModel):
    user: UpdateUser = Field(alias="user")


class BatchGetUsersResponse(BaseModel):
    users: list[UserDetail] = Field(default_factory=list, alias="users")


class BatchCreateUsersRequest(BaseModel):
    users: list[CreateUser] = Field(default_factory=list, alias="users")


class BatchCreateUsersResponse(BaseModel):
    users: list[User] = Field(default_factory=list, alias="users")


class BatchUpdateUser(BaseModel):
    username: str
    password: str
    nickname: str
    avatar_url: Optional[str] = None
    status: Optional[int] = None
    remark: Optional[str] = None


class BatchUpdateUsersRequest(BaseModel):
    ids: list[int]
    user: BatchUpdateUser = Field(alias="user")


class BatchPatchUsersRequest(BaseModel):
    users: list[UpdateUser] = Field(default_factory=list, alias="users")


class BatchUpdateUsersResponse(BaseModel):
    users: list[User] = Field(default_factory=list, alias="users")


class BatchDeleteUsersRequest(BaseModel):
    ids: list[int]


class ExportUser(User):
    pass


class ExportUsersRequest(BaseModel):
    ids: list[int]


class ImportUsersRequest(BaseModel):
    file: UploadFile


class ImportUser(CreateUser):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportUsersResponse(BaseModel):
    users: list[ImportUser] = Field(default_factory=list, alias="users")
