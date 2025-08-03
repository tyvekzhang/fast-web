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
"""DictDatum data model"""

from __future__ import annotations

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


class DictDatumBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    sort: Optional[int] = Field(sa_column=Column(Integer, nullable=True, comment="字典排序"))
    label: Optional[str] = Field(sa_column=Column(String(64), nullable=True, comment="字典标签"))
    value: Optional[str] = Field(sa_column=Column(String(64), nullable=True, comment="字典键值"))
    type: Optional[str] = Field(sa_column=Column(String(64), nullable=True, comment="字典类型"))
    echo_style: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True, comment="回显样式")
    )
    ext_class: Optional[str] = Field(
        sa_column=Column(String(64), nullable=True, comment="扩展样式")
    )
    is_default: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True, comment="是否默认(1是 0否)")
    )
    status: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True, comment="状态(1正常 0停用)")
    )
    comment: Optional[str] = Field(sa_column=Column(String(255), nullable=True, comment="备注"))
    create_time: Optional[datetime] = Field(
        sa_type=DateTime, default_factory=datetime.utcnow, sa_column_kwargs={"comment": "创建时间"}
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,
            "comment": "更新时间",
        },
    )


class DictDatumModel(DictDatumBase, table=True):
    __tablename__ = "dict_data"
    __table_args__ = ()
