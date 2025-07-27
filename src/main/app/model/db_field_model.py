"""Field data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    Integer,
    SmallInteger,
    BigInteger,
)
from src.main.app.model.model_base import ModelBase, ModelExt


class FieldBase(SQLModel):
    table_id: int = Field(
        sa_column=Column(BigInteger, nullable=False, index=True, comment="表id")
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="字段名称")
    )
    type: str = Field(
        sa_column=Column(String(32), nullable=False, comment="字段类型")
    )
    length: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="总长度")
    )
    scale: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="小数长度")
    )
    default: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="默认值")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )
    nullable: Optional[int] = Field(
        default=None,
        sa_column=Column(SmallInteger, comment="允许为空(0否,1是)"),
    )
    primary_key: Optional[int] = Field(
        default=None, sa_column=Column(SmallInteger, comment="主键(0否,1是)")
    )
    autoincrement: Optional[int] = Field(
        default=None, sa_column=Column(SmallInteger, comment="自增(0否,1是)")
    )
    sort: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="排序")
    )


class FieldDO(ModelExt, FieldBase, ModelBase, table=True):
    __tablename__ = "db_meta_fields"
    __table_args__ = ({"comment": "字段信息表"},)
