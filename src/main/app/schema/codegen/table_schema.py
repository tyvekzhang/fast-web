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
"""Table Modelmain schema"""

from datetime import datetime
from typing import Optional, List, Union, Any

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest
from src.main.app.model.codegen.field_model import FieldModel
from src.main.app.model.codegen.table_model import TableModel
from src.main.app.schema.codegen.field_schema import Field
from src.main.app.schema.codegen.meta_field_schema import AntTableColumn



class ListMenusRequest(PaginationRequest):
    connection_name: Optional[str] = None
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    table_comment: Optional[str] = None


class Table(BaseModel):
    id: int
    connection_name: str
    database_name: str
    table_id: int
    table_name: str
    entity: str
    table_comment: Optional[str] = None
    create_time: datetime


class TableImport(BaseModel):
    database_id: int
    table_ids: List[int]
    backend: str


class Table(BaseModel):
    gen_table: Optional[TableModel]
    fields: Union[List[Field], None]
    sub_table: Optional[TableModel] = None
    pk_field: Optional[str] = None
    tree_code: Optional[str] = None
    tree_parent_code: Optional[str] = None
    tree_name: Optional[str] = None
    parent_menu_id: Optional[int] = None
    parent_menu_name: Optional[str] = None


class TableDetail(BaseModel):
    gen_table: TableModel
    gen_field: List[FieldModel]


class TableExecute(BaseModel):
    database_id: int
    sql_statement: str


class TableRecord(BaseModel):
    fields: List[AntTableColumn]
    records: List[Any]
