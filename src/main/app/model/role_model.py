"""Roles data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    BigInteger,
    String,
    Integer,
    DateTime,
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class RoleBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "角色ID"},
    )
    name: str = Field(
        sa_column=Column(
            String(30), nullable=False, default=None, comment="角色名称"
        )
    )
    code: str = Field(
        sa_column=Column(
            String(100), nullable=False, default=None, comment="角色权限字符串"
        )
    )
    sort: int = Field(
        sa_column=Column(
            Integer, nullable=False, default=None, comment="显示顺序"
        )
    )
    data_scope: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）",
        )
    )
    data_scope_dept_ids: Optional[str] = Field(
        sa_column=Column(
            String(500),
            nullable=True,
            default=None,
            comment="数据范围(指定部门数组)",
        )
    )
    status: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=False,
            default=0,
            comment="角色状态（0正常 1停用）",
        )
    )
    comment: Optional[str] = Field(
        sa_column=Column(
            String(500), nullable=True, default=None, comment="备注"
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


class RoleModel(RoleBase, table=True):
    __tablename__ = "roles"
    __table_args__ = {"comment": "角色信息表"}
