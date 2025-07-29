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
"""Index data model"""

from datetime import datetime
from typing import Optional

from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    DateTime,
    String,
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class IndexBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    table_id: int = Field(
        sa_column=Column(BigInteger, nullable=False, comment="表id")
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="索引名称")
    )
    field: str = Field(
        sa_column=Column(String(64), nullable=False, comment="索引字段")
    )
    type: str = Field(
        sa_column=Column(String(16), nullable=False, comment="索引类型")
    )
    remark: Optional[str] = Field(
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


class IndexModel(IndexBase, table=True):
    __tablename__ = "db_indexes"
    __table_args__ = ({"comment": "索引信息表"},)
