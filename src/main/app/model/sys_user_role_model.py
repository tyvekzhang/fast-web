"""UserRole data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    Integer,
    DateTime,
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class UserRoleBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "自增编号"},
    )
    user_id: int = Field(
        sa_column=Column(
            Integer, nullable=False, default=None, comment="用户ID"
        )
    )
    role_id: int = Field(
        sa_column=Column(
            Integer, nullable=False, default=None, comment="角色ID"
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


class UserRoleModel(UserRoleBase, table=True):
    __tablename__ = "sys_user_role"
    __table_args__ = {"comment": "用户和角色关联表"}
