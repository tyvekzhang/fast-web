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
"""User data object"""

from datetime import datetime
from typing import Optional

from sqlmodel import (
    SQLModel,
    Field,
    Column,
    UniqueConstraint,
    BigInteger,
    Integer,
    String,
    DateTime,
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class UserBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    username: str = Field(
        sa_column=Column(
            String(32), nullable=False, default=None, comment="用户名"
        )
    )
    password: str = Field(
        sa_column=Column(
            String(64), nullable=False, default=None, comment="密码"
        )
    )
    nickname: str = Field(
        sa_column=Column(
            String(32), nullable=False, default=None, comment="昵称"
        )
    )
    avatar_url: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="头像地址"
        )
    )
    status: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="状态(0:停用,1:待审核,2:正常,3:已注销)",
        )
    )
    remark: Optional[str] = Field(
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


class UserModel(UserBase, table=True):
    __tablename__ = "sys_user"
    __table_args__ = (
        UniqueConstraint("username", name="ix_sys_user_username"),
        {"comment": "用户信息表"},
    )
