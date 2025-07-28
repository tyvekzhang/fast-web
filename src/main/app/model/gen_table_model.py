"""Gen table data object"""

from typing import Optional

from sqlmodel import Field, Column, String, SQLModel, BigInteger

from src.main.app.model.model_base import ModelBase, ModelExt


class GenTableBase(SQLModel):
    database_id: Optional[int] = Field(
        sa_column=Column(
            BigInteger, index=True, nullable=False, comment="数据库ID"
        )
    )
    db_table_id: Optional[int] = Field(
        sa_column=Column(
            BigInteger, index=True, nullable=False, comment="数据库表ID"
        )
    )
    table_name: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="表名")
    )
    sub_table_name: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="关联子表的表名")
    )
    sub_table_fk_name: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="子表关联的外键名")
    )
    class_name: Optional[str] = Field(
        default="", sa_column=Column(String(64), comment="实体类名称")
    )
    backend: Optional[str] = Field(
        default=None, sa_column=Column(String(16), comment="后端语言")
    )
    tpl_category: Optional[str] = Field(
        default="crud",
        sa_column=Column(
            String(64), comment="使用的模板（crud单表操作 tree树表操作）"
        ),
    )
    tpl_web_type: Optional[str] = Field(
        default="", sa_column=Column(String(32), comment="前端模板类型")
    )
    tpl_backend_type: Optional[str] = Field(
        default="mp", sa_column=Column(String(32), comment="后端模板类型")
    )
    package_name: Optional[str] = Field(
        default=None, sa_column=Column(String(128), comment="生成包路径")
    )
    module_name: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="生成模块名")
    )
    business_name: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="生成业务名")
    )
    function_name: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="生成功能名")
    )
    function_author: Optional[str] = Field(
        default=None, sa_column=Column(String(32), comment="生成功能作者")
    )
    gen_type: str = Field(
        default="0",
        sa_column=Column(
            String(1), comment="生成代码方式（0zip压缩包 1自定义路径）"
        ),
    )
    gen_path: str = Field(
        default="/",
        sa_column=Column(String(255), comment="生成路径（不填默认项目路径）"),
    )
    options: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="其它生成选项")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="表描述")
    )


class GenTableDO(ModelExt, GenTableBase, ModelBase, table=True):
    __tablename__ = "gen_tables"
    __table_args__ = ({"comment": "代码生成业务表"},)
