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
"""Meta table data model"""

from datetime import datetime
from typing import Optional

from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    DateTime,
    String
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class TableBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    database_id: Optional[int] = Field(
        sa_column=Column(
            BigInteger, index=True, nullable=False, comment="数据库id"
        )
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="表名称")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )
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


class MetaTableModel(TableBase, table=True):
    __tablename__ = "db_meta_tables"
    __table_args__ = ({"comment": "表结构信息"},)
