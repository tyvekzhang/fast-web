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
"""DictDatum schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListDictDataRequest(PaginationRequest):
    label: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None


class DictDataOptionItem(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None


class DictDataOption(BaseModel):
    options: dict[str, list[DictDataOptionItem]]


class DictDatum(BaseModel):
    id: int
    sort: Optional[int] = None
    label: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    echo_style: Optional[str] = None
    ext_class: Optional[str] = None
    is_default: Optional[int] = None
    status: Optional[int] = None
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class DictDatumDetail(BaseModel):
    id: int
    sort: Optional[int] = None
    label: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    echo_style: Optional[str] = None
    ext_class: Optional[str] = None
    is_default: Optional[int] = None
    status: Optional[int] = None
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class CreateDictDatum(BaseModel):
    sort: Optional[int] = None
    label: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    echo_style: Optional[str] = None
    ext_class: Optional[str] = None
    is_default: Optional[int] = None
    status: Optional[int] = None
    comment: Optional[str] = None


class CreateDictDatumRequest(BaseModel):
    dict_datum: CreateDictDatum = Field(alias="dictDatum")


class UpdateDictDatum(BaseModel):
    id: int
    sort: Optional[int] = None
    label: Optional[str] = None
    value: Optional[str] = None
    type: Optional[str] = None
    echo_style: Optional[str] = None
    ext_class: Optional[str] = None
    is_default: Optional[int] = None
    status: Optional[int] = None
    comment: Optional[str] = None


class UpdateDictDatumRequest(BaseModel):
    dict_datum: UpdateDictDatum = Field(alias="dictDatum")


class BatchGetDictDataResponse(BaseModel):
    dict_data: list[DictDatumDetail] = Field(default_factory=list, alias="dictData")


class BatchCreateDictDataRequest(BaseModel):
    dict_data: list[CreateDictDatum] = Field(default_factory=list, alias="dictData")


class BatchCreateDictDataResponse(BaseModel):
    dict_data: list[DictDatum] = Field(default_factory=list, alias="dictData")


class BatchUpdateDictDatum(BaseModel):
    sort: Optional[int] = None
    echo_style: Optional[str] = None
    ext_class: Optional[str] = None


class BatchUpdateDictDataRequest(BaseModel):
    ids: list[int]
    dict_datum: BatchUpdateDictDatum = Field(alias="dictDatum")


class BatchPatchDictDataRequest(BaseModel):
    dict_data: list[UpdateDictDatum] = Field(default_factory=list, alias="dictData")


class BatchUpdateDictDataResponse(BaseModel):
    dict_data: list[DictDatum] = Field(default_factory=list, alias="dictData")


class BatchDeleteDictDataRequest(BaseModel):
    ids: list[int]


class ExportDictDatum(DictDatum):
    pass


class ExportDictDataRequest(BaseModel):
    ids: list[int]


class ImportDictDataRequest(BaseModel):
    file: UploadFile


class ImportDictDatum(CreateDictDatum):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportDictDataResponse(BaseModel):
    dict_data: list[ImportDictDatum] = Field(default_factory=list, alias="dictData")
