# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Field data model"""

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
    SmallInteger
)

from src.main.app.core.utils.snowflake_util import snowflake_id


class GenFieldBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        sa_type=BigInteger,
        sa_column_kwargs={"comment": "主键"},
    )
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
    critical: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="列表字段(0否,1是)")
    )
    detailable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="详情字段(0否,1是)")
    )
    updatable: Optional[int] = Field(
        default=0, sa_column=Column(SmallInteger, comment="修改字段(0否,1是)")
    )
    batch_updatable: Optional[int] = Field(
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
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={"comment": "创建时间"},
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,  # 使用 `datetime.utcnow` 在更新时自动更新时间
            "comment": "更新时间",
        },
    )


class GenFieldDO(GenFieldBase, table=True):
    __tablename__ = "gen_fields"
    __table_args__ = ({"comment": "代码生成字段表"},)
