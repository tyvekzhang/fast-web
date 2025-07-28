"""RoleMenu data model"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
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
            BigInteger, nullable=False, default=None, comment="角色ID"
        )
    )
    menu_id: int = Field(
        sa_column=Column(
            BigInteger, nullable=False, default=None, comment="菜单ID"
        )
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
            "onupdate": datetime.utcnow,
            "comment": "更新时间",
        },
    )


class RoleMenuModel(RoleMenuBase, table=True):
    __tablename__ = "role_menu"
    __table_args__ = {"comment": "角色和菜单关联表"}
