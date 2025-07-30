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
from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class ListDatabasesRequest(PaginationRequest):
    connection_id: Optional[int] = None

class Database(BaseModel):
    id: int
    database_name: str


class CreateDatabase(BaseModel):
    connection_id: int
    database_name: str
    owner: Optional[str] = None
    template: Optional[str] = None
    encoding: Optional[str] = None
    collation_order: Optional[str] = None
    character_classification: Optional[str] = None
    tablespace: Optional[str] = None
    connection_limit: Optional[int] = None
    allow_connection: Optional[bool] = None
    is_template: Optional[bool] = None

# SQL templates for different databases
DB_CREATE_TEMPLATES = {
    "mysql": """
        CREATE DATABASE IF NOT EXISTS {database_name}
        CHARACTER SET {encoding}
        COLLATE {collation_order};
    """,
    "postgresql": """
        CREATE DATABASE {database_name}
        WITH ENCODING 'utf8'
        LC_COLLATE 'en_US.utf8'
        LC_CTYPE 'en_US.utf8';
    """,
    "sqlite": "-- SQLite does not need CREATE DATABASE",
}





class DatabaseQuery(PaginationRequest):
    connection_id: int


class DatabaseExport(BaseModel):
    pass


class DatabaseQueryForm(BaseModel):
    pass


class DatabaseModify(BaseModel):
    pass


class SQLSchema(BaseModel):
    connection_id: Optional[int] = None  # 数据库连接id
    database_name: str  # 数据库名称
    owner: Optional[str] = None  # 拥有者
    template: Optional[str] = None  # 使用模板
    encoding: Optional[str] = None  # 字符编码
    collation_order: Optional[str] = None  # 排序规则
    character_classification: Optional[str] = None  # 字符分类
    tablespace: Optional[str] = None  # 表空间名称
    connection_limit: Optional[int] = None  # 连接限制
    allow_connection: Optional[bool] = None  # 是否允许连接
    is_template: Optional[bool] = None  # 是否为模板数据库
