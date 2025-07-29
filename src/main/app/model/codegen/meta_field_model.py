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
"""Meta Field data model"""

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
    SmallInteger
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class MetaFieldBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    table_id: int = Field(
        sa_column=Column(BigInteger, nullable=False, index=True, comment="表id")
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="字段名称")
    )
    type: str = Field(
        sa_column=Column(String(32), nullable=False, comment="字段类型")
    )
    length: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="总长度")
    )
    scale: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="小数长度")
    )
    default: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="默认值")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )
    nullable: Optional[int] = Field(
        default=None,
        sa_column=Column(SmallInteger, comment="允许为空(0否,1是)"),
    )
    primary_key: Optional[int] = Field(
        default=None, sa_column=Column(SmallInteger, comment="主键(0否,1是)")
    )
    autoincrement: Optional[int] = Field(
        default=None, sa_column=Column(SmallInteger, comment="自增(0否,1是)")
    )
    sort: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="排序")
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


class MetaFieldModel(MetaFieldBase, table=True):
    __tablename__ = "db_meta_fields"
    __table_args__ = ({"comment": "字段信息表"},)
