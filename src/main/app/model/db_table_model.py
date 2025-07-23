"""Table data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
)
from src.main.app.model.model_base import ModelBase, ModelExt


class TableBase(SQLModel):
    database_id: Optional[int] = Field(
        sa_column=Column(
            BigInteger, index=True, nullable=False, comment="数据库id"
        )
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="表名称")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class TableDO(ModelExt, TableBase, ModelBase, table=True):
    __tablename__ = "db_table"
    __table_args__ = ({"comment": "表结构信息"},)
