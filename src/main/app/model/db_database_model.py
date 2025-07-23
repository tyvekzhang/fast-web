"""Database data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
    Boolean,
    Integer,
)
from src.main.app.model.model_base import ModelBase, ModelExt


class DatabaseBase(SQLModel):
    connection_id: int = Field(
        sa_column=Column(
            BigInteger, index=True, nullable=False, comment="数据库连接id"
        )
    )
    database_name: str = Field(
        sa_column=Column(String(64), nullable=False, comment="数据库名称")
    )
    owner: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="拥有者")
    )
    template: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="使用模板")
    )
    encoding: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="字符编码")
    )
    collation_order: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="排序规则")
    )
    character_classification: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="字符分类")
    )
    tablespace: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="表空间名称")
    )
    connection_limit: Optional[str] = Field(
        default=-1, sa_column=Column(Integer, comment="连接限制")
    )
    allow_connection: Optional[str] = Field(
        default=True, sa_column=Column(Boolean, comment="是否允许连接")
    )
    is_template: Optional[str] = Field(
        default=False, sa_column=Column(Boolean, comment="是否为模板数据库")
    )


class DatabaseDO(ModelExt, DatabaseBase, ModelBase, table=True):
    __tablename__ = "db_database"
    __table_args__ = ({"comment": "数据库信息表"},)
