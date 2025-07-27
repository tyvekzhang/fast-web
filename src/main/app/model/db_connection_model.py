"""Connection data object"""

from typing import Optional

from sqlmodel import Field, Column, String, SQLModel, Integer
from src.main.app.model.model_base import ModelBase, ModelExt


class ConnectionBase(SQLModel):
    connection_name: str = Field(
        sa_column=Column(String(32), nullable=False, comment="连接名称")
    )
    database_type: str = Field(
        sa_column=Column(String(16), nullable=False, comment="数据库类型")
    )
    connection_database: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="连接数据库名称")
    )
    host: Optional[str] = Field(
        default=None, sa_column=Column(String(16), comment="主机")
    )
    port: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="端口号")
    )
    username: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="用户名")
    )
    password: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="密码")
    )


class ConnectionDO(ModelExt, ConnectionBase, ModelBase, table=True):
    __tablename__ = "db_connections"
    __table_args__ = ({"comment": "连接信息表"},)
