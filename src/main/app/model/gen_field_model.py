"""Gen table column data object"""

from typing import Optional

from sqlmodel import (
    Field,
    Column,
    String,
    SQLModel,
    BigInteger,
    Integer,
    SmallInteger,
)
from src.main.app.model.model_base import ModelBase, ModelExt


class GenFieldBase(SQLModel):
    db_table_id: int = Field(
        sa_column=Column(
            BigInteger, nullable=False, index=True, comment="数据库表ID"
        )
    )
    db_field_id: int = Field(
        sa_column=Column(
            BigInteger, nullable=False, index=True, comment="数据库字段ID"
        )
    )
    field_name: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="字段名称")
    )
    field_type: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="字段类型")
    )
    sql_model_type: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="模型类型")
    )
    length: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="字段长度")
    )
    scale: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="分数位")
    )
    js_type: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="JS类型")
    )
    sort: Optional[int] = Field(
        default=None, sa_column=Column(Integer, comment="排序")
    )
    default: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="默认值")
    )
    primary_key: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="是否主键(0否,1是)")
    )
    nullable: Optional[int] = Field(
        default=1, sa_column=Column(SmallInteger, comment="允许为空(0否,1是)")
    )
    creatable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="创建字段(0否,1是)")
    )
    queryable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="查询字段(0否,1是)")
    )
    pageable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="列表字段(0否,1是)")
    )
    detailable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="详情字段(0否,1是)")
    )
    modifiable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="修改字段(0否,1是)")
    )
    batch_modifiable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="批量修改(0否,1是)")
    )
    query_type: Optional[str] = Field(
        default=0,
        sa_column=Column(
            String(64), comment="查询方式（等于、不等于、大于、小于、范围）"
        ),
    )
    html_type: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String(64),
            comment="显示类型(文本框、文本域、下拉框、复选框、单选框、日期控件)",
        ),
    )
    dict_type: Optional[str] = Field(
        default=None, sa_column=Column(String(64), comment="字典类型")
    )
    comment: Optional[str] = Field(
        default=None, sa_column=Column(String(255), comment="备注")
    )


class GenFieldDO(ModelExt, GenFieldBase, ModelBase, table=True):
    __tablename__ = "gen_field"
    __table_args__ = ({"comment": "代码生成字段表"},)
