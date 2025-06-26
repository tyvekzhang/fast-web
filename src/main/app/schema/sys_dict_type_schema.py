# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
"""DictType schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.core.schema import BasePage


class DictTypePage(BaseModel):
    """
    字典类型分页信息
    """

    # 主键
    id: int
    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None


class DictTypeQuery(BasePage):
    """
    字典类型查询参数
    """

    # 主键
    id: Optional[int] = None
    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    sort: Optional[str] = None


class DictTypeCreate(BaseModel):
    """
    字典类型新增
    """

    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class DictTypeModify(BaseModel):
    """
    字典类型更新
    """

    # 主键
    id: int
    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None


class DictTypeBatchModify(BaseModel):
    """
    字典类型批量更新
    """

    ids: List[int]
    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None


class DictTypeDetail(BaseModel):
    """
    字典类型详情
    """

    # 主键
    id: int
    # 字典名称
    name: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
