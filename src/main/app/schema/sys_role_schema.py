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
"""Role schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.core.schema import BasePage


class RolePage(BaseModel):
    """
    角色信息分页信息
    """

    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 数据范围(指定部门数组)
    data_scope_dept_ids: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None


class RoleQuery(BasePage):
    """
    角色信息查询参数
    """

    # 角色ID
    id: Optional[int] = None
    # 角色名称
    name: Optional[str] = None
    # 角色权限字符串
    code: Optional[str] = None
    # 显示顺序
    sort: Optional[int] = None
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 角色状态（0正常 1停用）
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    sort: Optional[str] = None


class RoleCreate(BaseModel):
    """
    角色信息新增
    """

    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 数据范围(指定部门数组)
    data_scope_dept_ids: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class RoleModify(BaseModel):
    """
    角色信息更新
    """

    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 数据范围(指定部门数组)
    data_scope_dept_ids: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None


class RoleBatchModify(BaseModel):
    """
    角色信息批量更新
    """

    ids: List[int]
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 数据范围(指定部门数组)
    data_scope_dept_ids: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None


class RoleDetail(BaseModel):
    """
    角色信息详情
    """

    # 角色ID
    id: int
    # 角色名称
    name: str
    # 角色权限字符串
    code: str
    # 显示顺序
    sort: int
    # 数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）
    data_scope: Optional[int] = None
    # 数据范围(指定部门数组)
    data_scope_dept_ids: Optional[str] = None
    # 角色状态（0正常 1停用）
    status: int
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
