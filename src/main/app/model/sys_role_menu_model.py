"""RoleMenu data object"""

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


class RoleMenuBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "自增编号"},
    )
    role_id: int = Field(
        sa_column=Column(
            Integer, nullable=False, default=None, comment="角色ID"
        )
    )
    menu_id: int = Field(
        sa_column=Column(
            Integer, nullable=False, default=None, comment="菜单ID"
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


class RoleMenuModel(RoleMenuBase, table=True):
    __tablename__ = "sys_role_menu"
    __table_args__ = {"comment": "角色和菜单关联表"}
