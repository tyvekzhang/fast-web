from datetime import datetime
from typing import Optional, Set

from pydantic import BaseModel

from src.main.app.schema.menu_schema import Menu


class SignInWithEmailAndPasswordRequest(BaseModel):
    username: str
    password: str


class UserPage(BaseModel):
    """
    用户信息分页信息
    """

    # 主键
    id: int
    # 用户名
    username: str
    # 昵称
    nickname: str
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None


class UserInfo(BaseModel):
    """
    用户信息
    """

    # 主键
    id: int
    # 用户名
    username: str
    # 昵称
    nickname: str
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
    # 角色集合
    roles: Optional[Set[str]] = None
    # 权限集合
    permissions: Optional[list[str]] = None
    # 菜单集合
    menus: Optional[list[Menu]] = None

    @staticmethod
    def is_admin(user_id: int) -> bool:
        if user_id is not None and user_id == 9:
            return True
        return False
