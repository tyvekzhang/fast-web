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
"""Table domain schema"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class ListMetaTablesRequest(PaginationRequest):
    database_id: Optional[int] = None
    table_name: Optional[str] = None
    comment: Optional[str] = None


class MetaTable(BaseModel):
    id: Optional[int] = None
    database_id: int
    name: str
    comment: Optional[str] = None
    create_time: Optional[datetime] = None


class CreateMetaTable(BaseModel):
    database_id: int
    name: str
    comment: Optional[str] = None


# class TableQuery(PaginationRequest):
#     database_id: int
#
#
# class TableGenerate(BaseModel):
#     database_id: int
#     table_name: str
#     class_name: Optional[str] = None
#     comment: Optional[str] = None
#     field_metadata: List[FieldGenerate]
#     index_metadata: List[IndexGenerate]
#
#
# class TableExport(BaseModel):
#     pass
#
#
# class TableQueryForm(BaseModel):
#     pass
#
#
# class TableModify(BaseModel):
#     pass
