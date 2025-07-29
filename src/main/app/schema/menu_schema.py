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
"""Menu schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.main.app.core.schema import PaginationRequest


class ListMenusRequest(PaginationRequest):
    """
    系统菜单查询参数
    """

    # 主键
    id: Optional[int] = None
    # 名称
    name: Optional[str] = None
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[int] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = None
    # 父ID
    parent_id: Optional[int] = None
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None


class Menu(BaseModel):
    """
    Key info in menu
    """

    # 主键
    id: int
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[int] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = None
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = None
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    # 备注信息
    comment: Optional[str] = None
    # 子节点
    children: Optional[list[Menu]] = None


class MenuDetail(Menu):
    """
    系统菜单详情
    """

    pass


class CreateMenu(BaseModel):
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[int] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = None
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = None
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = None
    # 备注信息
    comment: Optional[str] = None


class CreateMenuRequest(BaseModel):
    """
    All information for creating the menu.
    """

    menu: CreateMenu


class UpdateMenu(BaseModel):
    # 主键
    id: int
    # 名称
    name: str
    # 图标
    icon: Optional[str] = None
    # 权限标识
    permission: Optional[str] = None
    # 排序
    sort: Optional[int] = None
    # 路由地址
    path: Optional[str] = None
    # 组件路径
    component: Optional[str] = None
    # 类型（1目录 2菜单 3按钮）
    type: Optional[int] = None
    # 是否缓存（1缓存 0不缓存）
    cacheable: Optional[int] = None
    # 是否显示（1显示 0隐藏）
    visible: Optional[int] = None
    # 父ID
    parent_id: Optional[int] = None
    # 状态（1正常 0停用）
    status: Optional[int] = None
    # 备注信息
    comment: Optional[str] = None


class UpdateMenuRequest(BaseModel):
    menu: UpdateMenu


class BatchGetMenusResponse(BaseModel):
    menus: list[MenuDetail]


class BatchCreateMenusRequest(BaseModel):
    menus: list[CreateMenu]


class BatchCreateMenusResponse(BaseModel):
    menus: list[Menu]


class BatchUpdateMenu(BaseModel):
    pass


class BatchUpdateMenusRequest(BaseModel):
    ids: list[int]
    menu: BatchUpdateMenu


class BatchPatchMenusRequest(BaseModel):
    menus: list[UpdateMenu]


class BatchUpdateMenusResponse(BaseModel):
    menus: list[Menu]


class BatchDeleteMenusRequest(BaseModel):
    ids: list[int]


class ExportMenu(Menu):
    pass


class ExportMenusRequest(BaseModel):
    ids: list[int]


class ImportMenusRequest(BaseModel):
    file: UploadFile


class ImportMenu(CreateMenu):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportMenusResponse(BaseModel):
    menus: list[ImportMenu]
