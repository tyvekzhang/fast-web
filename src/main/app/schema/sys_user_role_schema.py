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
"""UserRole schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.core.schema import BasePage


class UserRolePage(BaseModel):
    """
    用户和角色关联分页信息
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 创建时间
    create_time: Optional[datetime] = None


class UserRoleQuery(BasePage):
    """
    用户和角色关联查询参数
    """

    # 自增编号
    id: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    sort: Optional[str] = None


class UserRoleCreate(BaseModel):
    """
    用户和角色关联新增
    """

    # 角色ID
    role_id: int
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class UserRoleModify(BaseModel):
    """
    用户和角色关联更新
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int


class UserRoleBatchModify(BaseModel):
    """
    用户和角色关联批量更新
    """

    ids: List[int]
    # 角色ID
    role_id: int


class UserRoleDetail(BaseModel):
    """
    用户和角色关联详情
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 创建时间
    create_time: Optional[datetime] = None
