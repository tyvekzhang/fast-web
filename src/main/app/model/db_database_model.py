# Copyright (c) 2025 Admin and/or its affiliates. All rights reserved.
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
"""DbDatabase data model"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Index,
    BigInteger,
    String,
    DateTime,
    Integer,
    Boolean
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class DbDatabaseBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    connection_id: int = Field(sa_column=Column(BigInteger, index=True, nullable=False, comment="数据库连接id"))
    database_name: str = Field(sa_column=Column(String(64), nullable=False, comment="数据库名称"))
    owner: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="拥有者"))
    template: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="使用模板"))
    encoding: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="字符编码"))
    collation_order: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="排序规则"))
    character_classification: Optional[str] = Field(default=None, sa_column=Column(String(32), comment="字符分类"))
    tablespace: Optional[str] = Field(default=None, sa_column=Column(String(64), comment="表空间名称"))
    connection_limit: Optional[str] = Field(default=-1, sa_column=Column(Integer, comment="连接限制"))
    allow_connection: Optional[str] = Field(default=True, sa_column=Column(Boolean, comment="是否允许连接"))
    is_template: Optional[str] = Field(default=False, sa_column=Column(Boolean, comment="是否为模板数据库"))
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,
            "comment": "更新时间",
        },
    )


class DbDatabaseModel(DbDatabaseBase, table=True):
    __tablename__ = "db_databases"
    __table_args__ = (Index("ix_db_database_connection_id", "connection_id"),{"comment": "数据库信息表"})
