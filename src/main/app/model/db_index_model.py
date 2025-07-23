"""Index data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
)
from src.main.app.model.model_base import ModelBase, ModelExt


class IndexBase(SQLModel):
    table_id: int = Field(
        sa_column=Column(BigInteger, nullable=False, comment="表id")
    )
    name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="索引名称")
    )
    field: str = Field(
        sa_column=Column(String(64), nullable=False, comment="索引字段")
    )
    type: str = Field(
        sa_column=Column(String(16), nullable=False, comment="索引类型")
    )
    remark: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class IndexDO(ModelExt, IndexBase, ModelBase, table=True):
    __tablename__ = "db_index"
    __table_args__ = ({"comment": "索引信息表"},)
