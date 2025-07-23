from typing import Optional

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase

# SQL templates for different databases
DB_CREATE_TEMPLATES = {
    "mysql": """
        CREATE DATABASE IF NOT EXISTS {database_name}
        CHARACTER SET {encoding}
        COLLATE {collation_order};
    """,
    "postgresql": """
        CREATE DATABASE {database_name}
        WITH ENCODING 'utf8'
        LC_COLLATE 'en_US.utf8'
        LC_CTYPE 'en_US.utf8';
    """,
    "sqlite": "-- SQLite does not need CREATE DATABASE",
}


class DatabaseAdd(BaseModel):
    connection_id: int  # 数据库连接id
    database_name: str  # 数据库名称
    owner: Optional[str] = None  # 拥有者
    template: Optional[str] = None  # 使用模板
    encoding: Optional[str] = None  # 字符编码
    collation_order: Optional[str] = None  # 排序规则
    character_classification: Optional[str] = None  # 字符分类
    tablespace: Optional[str] = None  # 表空间名称
    connection_limit: Optional[int] = None  # 连接限制
    allow_connection: Optional[bool] = None  # 是否允许连接
    is_template: Optional[bool] = None  # 是否为模板数据库


class DatabaseQuery(PageBase):
    connection_id: int


class DatabaseExport(BaseModel):
    pass


class DatabaseQueryForm(BaseModel):
    pass


class DatabaseModify(BaseModel):
    pass


class SQLSchema(BaseModel):
    connection_id: Optional[int] = None  # 数据库连接id
    database_name: str  # 数据库名称
    owner: Optional[str] = None  # 拥有者
    template: Optional[str] = None  # 使用模板
    encoding: Optional[str] = None  # 字符编码
    collation_order: Optional[str] = None  # 排序规则
    character_classification: Optional[str] = None  # 字符分类
    tablespace: Optional[str] = None  # 表空间名称
    connection_limit: Optional[int] = None  # 连接限制
    allow_connection: Optional[bool] = None  # 是否允许连接
    is_template: Optional[bool] = None  # 是否为模板数据库
