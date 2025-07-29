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
"""Field domain schema"""

from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class FieldAdd(BaseModel):
    table_id: int
    name: str
    type: str
    default: Optional[int] = None
    length: Optional[int] = None
    decimals: Optional[int] = None
    not_null: Optional[bool] = None
    index_col: Optional[bool] = None
    remark: Optional[str] = None


class ListFieldRequest(PaginationRequest):
    table_id: int


class FieldExport(BaseModel):
    pass


class FieldQueryForm(BaseModel):
    pass


class FieldModify(BaseModel):
    pass


class FieldGenerate(BaseModel):
    name: str
    type: str
    modeltype: Optional[str] = None
    server_type: Optional[str] = None
    default: Optional[str] = None
    length: Optional[int] = None
    decimals: Optional[int] = None
    not_null: Optional[bool] = None
    index_col: Optional[bool] = None
    remark: Optional[str] = None


class AntTableColumn(BaseModel):
    title: str
    dataIndex: str
    key: str
    width: Optional[str] = None
    ellipsis: Optional[bool] = True
    sorter: Optional[bool] = False
    hidden: Optional[bool] = False
