"""Menu schema"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.main.app.core.schema import BasePage


class GetMenuRequest(BaseModel):
    id: int = Field(gt=0)


class Menu(BaseModel):
    """
    系统菜单分页信息
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


class ListMenuRequest(BasePage):
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
    系统菜单新增
    """

    menu: CreateMenu


class UpdateMenu(BaseModel):
    """
    系统菜单更新
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
    # 备注信息
    comment: Optional[str] = None


class UpdateMenuRequest(BaseModel):
    """
    系统菜单更新请求
    """

    menu: UpdateMenu


class MenuBatchModify(BaseModel):
    """
    系统菜单批量更新
    """

    ids: list[int]
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


class MenuDetail(Menu):
    """
    系统菜单详情
    """

    pass


class BatchGetMenusResponse(BaseModel):
    menus: list[MenuDetail]


class BatchCreateMenuRequest(BaseModel):
    menus: list[CreateMenu]


class BatchCreateMenuResponse(BaseModel):
    menus: list[Menu]


class BatchUpdateMenusRequest(BaseModel):
    pass


class BatchUpdateMenusResponse(BaseModel):
    menus: list[UpdateMenu]


class BatchDeleteMenusRequest(BaseModel):
    ids: list[int] = Field(..., min_items=1)


class ExportMenusRequest(BaseModel):
    pass


class ImportMenusResponse(BaseModel):
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")
