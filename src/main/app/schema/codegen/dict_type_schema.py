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
"""DictType schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListDictTypesRequest(PaginationRequest):
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    create_time: Optional[datetime] = None


class DictType(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class DictTypeDetail(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class CreateDictType(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    comment: Optional[str] = None


class CreateDictTypeRequest(BaseModel):
    dict_type: CreateDictType = Field(alias="dictType")


class UpdateDictType(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    comment: Optional[str] = None


class UpdateDictTypeRequest(BaseModel):
    dict_type: UpdateDictType = Field(alias="dictType")


class BatchGetDictTypesResponse(BaseModel):
    dict_types: list[DictTypeDetail] = Field(default_factory=list, alias="dictTypes")


class BatchCreateDictTypesRequest(BaseModel):
    dict_types: list[CreateDictType] = Field(default_factory=list, alias="dictTypes")


class BatchCreateDictTypesResponse(BaseModel):
    dict_types: list[DictType] = Field(default_factory=list, alias="dictTypes")


class BatchUpdateDictType(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    status: Optional[int] = None
    comment: Optional[str] = None


class BatchUpdateDictTypesRequest(BaseModel):
    ids: list[int]
    dict_type: BatchUpdateDictType = Field(alias="dictType")


class BatchPatchDictTypesRequest(BaseModel):
    dict_types: list[UpdateDictType] = Field(default_factory=list, alias="dictTypes")


class BatchUpdateDictTypesResponse(BaseModel):
    dict_types: list[DictType] = Field(default_factory=list, alias="dictTypes")


class BatchDeleteDictTypesRequest(BaseModel):
    ids: list[int]


class ExportDictType(DictType):
    pass


class ExportDictTypesRequest(BaseModel):
    ids: list[int]


class ImportDictTypesRequest(BaseModel):
    file: UploadFile


class ImportDictType(CreateDictType):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportDictTypesResponse(BaseModel):
    dict_types: list[ImportDictType] = Field(default_factory=list, alias="dictTypes")
