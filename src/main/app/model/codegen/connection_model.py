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
"""Connection data model"""

from datetime import datetime
from typing import Optional

from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    Integer,
    DateTime,
    String,
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class ConnectionBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )

    connection_name: str = Field(sa_column=Column(String(32), nullable=False, comment="连接名称"))
    database_type: str = Field(sa_column=Column(String(16), nullable=False, comment="数据库类型"))
    connection_database: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="连接数据库名称")
    )
    host: Optional[str] = Field(default=None, sa_column=Column(String(16), comment="主机"))
    port: Optional[int] = Field(default=None, sa_column=Column(Integer, comment="端口号"))
    username: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="用户名"))
    password: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="密码"))
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,  # 使用 `datetime.utcnow` 在更新时自动更新时间
            "comment": "更新时间",
        },
    )


class ConnectionModel(ConnectionBase, table=True):
    __tablename__ = "db_connections"
    __table_args__ = ({"comment": "连接信息表"},)
