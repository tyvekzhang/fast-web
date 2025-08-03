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
"""RoleMenu data model"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    DateTime,
    Integer,
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class RoleMenuBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "自增编号"},
    )
    role_id: int = Field(sa_column=Column(Integer, nullable=False, comment="角色ID"))
    menu_id: int = Field(sa_column=Column(Integer, nullable=False, comment="菜单ID"))
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


class RoleMenuModel(RoleMenuBase, table=True):
    __tablename__ = "role_menu"
    __table_args__ = ()
