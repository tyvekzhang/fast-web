"""Menu data object"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Index,
    BigInteger,
    Integer,
    DateTime,
    String,
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class MenuBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    name: str = Field(
        sa_column=Column(
            String(50), nullable=False, default=None, comment="名称"
        )
    )
    icon: Optional[str] = Field(
        sa_column=Column(
            String(100), nullable=True, default=None, comment="图标"
        )
    )
    permission: Optional[str] = Field(
        sa_column=Column(
            String(100), nullable=True, default=None, comment="权限标识"
        )
    )
    sort: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True, default=None, comment="排序")
    )
    path: Optional[str] = Field(
        sa_column=Column(
            String(200), nullable=True, default=None, comment="路由地址"
        )
    )
    component: Optional[str] = Field(
        sa_column=Column(
            String(255), nullable=True, default=None, comment="组件路径"
        )
    )
    type: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="类型（1目录 2菜单 3按钮）",
        )
    )
    cacheable: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="是否缓存（1缓存 0不缓存）",
        )
    )
    visible: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
            comment="是否显示（1显示 0隐藏）",
        )
    )
    parent_id: Optional[int] = Field(
        sa_column=Column(Integer, nullable=True, default=None, comment="父ID")
    )
    status: Optional[int] = Field(
        sa_column=Column(
            Integer, nullable=True, default=None, comment="状态（1正常 0停用）"
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
    comment: Optional[str] = Field(
        sa_column=Column(
            String(500), nullable=True, default=None, comment="备注信息"
        )
    )


class MenuModel(MenuBase, table=True):
    __tablename__ = "sys_menu"
    __table_args__ = (
        Index("idx_parent_id", "parent_id"),
        {"comment": "系统菜单表"},
    )
