# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
"""DictType data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    UniqueConstraint,
    BigInteger,
    Integer,
    DateTime,
    String,
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class DictTypeBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    name: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="字典名称"
        )
    )
    type: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="字典类型"
        )
    )
    status: Optional[int] = Field(
        sa_column=Column(
            Integer, nullable=True, default=None, comment="状态(1正常 0停用)"
        )
    )
    comment: Optional[str] = Field(
        sa_column=Column(
            String(255), nullable=True, default=None, comment="备注"
        )
    )
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.now,
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.now,
        sa_column_kwargs={
            "onupdate": datetime.now,
            "comment": "更新时间",
        },
    )


class DictTypeModel(DictTypeBase, table=True):
    __tablename__ = "sys_dict_type"
    __table_args__ = (
        UniqueConstraint("type", name="dict_type"),
        {"comment": "字典类型表"},
    )
