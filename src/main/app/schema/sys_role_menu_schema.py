"""RoleMenu schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.core.schema import BasePage


class RoleMenuPage(BaseModel):
    """
    角色和菜单关联分页信息
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建时间
    create_time: Optional[datetime] = None


class RoleMenuQuery(BasePage):
    """
    角色和菜单关联查询参数
    """

    # 自增编号
    id: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    sort: Optional[str] = None


class RoleMenuCreate(BaseModel):
    """
    角色和菜单关联新增
    """

    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class RoleMenuModify(BaseModel):
    """
    角色和菜单关联更新
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int


class RoleMenuBatchModify(BaseModel):
    """
    角色和菜单关联批量更新
    """

    ids: List[int]
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int


class RoleMenuDetail(BaseModel):
    """
    角色和菜单关联详情
    """

    # 自增编号
    id: int
    # 角色ID
    role_id: int
    # 菜单ID
    menu_id: int
    # 创建时间
    create_time: Optional[datetime] = None
