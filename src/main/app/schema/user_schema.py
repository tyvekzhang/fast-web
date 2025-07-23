"""User schema"""

from datetime import datetime
from typing import Optional, Set
from pydantic import BaseModel, Field
from src.main.app.core.schema import PaginationRequest
from src.main.app.schema.menus_schema import Menu


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


class UserQuery(PaginationRequest):
    """
    用户信息查询参数
    """

    # 主键
    id: Optional[int] = None
    # 用户名
    username: Optional[str] = None
    # 密码
    password: Optional[str] = None
    # 昵称
    nickname: Optional[str] = None
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None


class CreateUserRequest(BaseModel):
    """
    用户信息新增
    """

    # 用户名
    username: str
    # 密码
    password: str
    # 昵称
    nickname: str
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class UserModify(BaseModel):
    """
    用户信息更新
    """

    # 主键
    id: int
    # 用户名
    username: str
    # 密码
    password: str
    # 昵称
    nickname: str
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None


class UserBatchModify(BaseModel):
    """
    用户信息批量更新
    """

    ids: list[int]
    # 用户名
    username: str
    # 密码
    password: str
    # 昵称
    nickname: str
    # 头像地址
    avatar_url: Optional[str] = None
    # 状态(0:停用,1:待审核,2:正常,3:已注销)
    status: Optional[int] = None
    # 备注
    remark: Optional[str] = None


class UserDetail(BaseModel):
    """
    用户信息详情
    """

    # 主键
    id: int
    # 用户名
    username: str
    # 密码
    password: str
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


class Ids(BaseModel):
    """
    Ids schema
    """

    ids: list[int]
