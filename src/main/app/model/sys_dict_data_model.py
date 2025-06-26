"""DictData data object"""

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


class DictDataBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
    sort: Optional[int] = Field(
        sa_column=Column(
            Integer, nullable=True, default=None, comment="字典排序"
        )
    )
    label: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="字典标签"
        )
    )
    value: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="字典键值"
        )
    )
    type: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="字典类型"
        )
    )
    echo_style: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="回显样式"
        )
    )
    ext_class: Optional[str] = Field(
        sa_column=Column(
            String(64), nullable=True, default=None, comment="扩展样式"
        )
    )
    is_default: Optional[int] = Field(
        sa_column=Column(
            Integer, nullable=True, default=None, comment="是否默认(1是 0否)"
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


class DictDataModel(DictDataBase, table=True):
    __tablename__ = "sys_dict_data"
    __table_args__ = {"comment": "字典数据表"}
