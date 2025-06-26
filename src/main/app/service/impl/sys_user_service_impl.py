"""User domain service impl"""

from __future__ import annotations

import io
import json
from datetime import timedelta, datetime
from typing import Optional, List, Set, Tuple
from typing import Union

import pandas as pd
from fastapi import UploadFile
from starlette.responses import StreamingResponse

from src.main.app.core import security
from src.main.app.core.config import config_manager
from src.main.app.core.constant import FilterOperators
from src.main.app.core.enums import TokenTypeEnum
from src.main.app.core.schema import PageResult, Token, CurrentUser
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.utils import excel_util
from src.main.app.core.utils.validate_util import ValidateService
from src.main.app.enums import AuthErrorCode
from src.main.app.exception import AuthException
from src.main.app.mapper.sys_menu_mapper import menuMapper
from src.main.app.mapper.sys_role_mapper import roleMapper
from src.main.app.mapper.sys_role_menu_mapper import roleMenuMapper
from src.main.app.mapper.sys_user_mapper import UserMapper
from src.main.app.mapper.sys_user_role_mapper import userRoleMapper
from src.main.app.model.sys_menu_model import MenuModel
from src.main.app.model.sys_role_menu_model import RoleMenuModel
from src.main.app.model.sys_role_model import RoleModel
from src.main.app.model.sys_user_model import UserModel
from src.main.app.model.sys_user_role_model import UserRoleModel
from src.main.app.schema.sys_menu_schema import MenuPage
from src.main.app.schema.sys_user_schema import (
    UserQuery,
    UserPage,
    UserDetail,
    UserCreate,
    LoginForm,
    UserInfo,
)
from src.main.app.service.sys_user_service import UserService


class UserServiceImpl(BaseServiceImpl[UserMapper, UserModel], UserService):
    """
    Implementation of the UserService interface.
    """

    def __init__(self, mapper: UserMapper):
        """
        Initialize the UserServiceImpl instance.

        Args:
            mapper (UserMapper): The UserMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    @classmethod
    async def generate_tokens(cls, user_id: int) -> Token:
        security_config = config_manager.load_security_config()

        # generate access token
        access_token_expires = timedelta(
            minutes=security_config.access_token_expire_minutes
        )
        access_token = security.create_token(
            subject=user_id, token_type=TokenTypeEnum.access
        )

        # generate refresh token
        refresh_token_expires = timedelta(
            minutes=security_config.refresh_token_expire_minutes
        )
        refresh_token = security.create_token(
            subject=user_id,
            token_type=TokenTypeEnum.refresh,
            expires_delta=refresh_token_expires,
        )

        access_token_expires_at = int(
            (datetime.now() + access_token_expires).timestamp()
        )
        refresh_token_expires_at = int(
            (datetime.now() + refresh_token_expires).timestamp()
        )

        return Token(
            access_token=access_token,
            expired_time=access_token_expires_at,
            token_type=TokenTypeEnum.bearer,
            refresh_token=refresh_token,
            re_expired_time=refresh_token_expires_at,
        )

    async def login(self, *, login_form: LoginForm) -> Token:
        """
        Perform login and return an access token and refresh token.

        Args:
            login_form (LoginCmd): The login command containing username and password.

        Returns:
            Token: The access token and refresh token.
        """
        # verify username and password
        username: str = login_form.username

        user_record = await self.mapper.get_user_by_username(username=username)
        if user_record is None or not security.verify_password(
            login_form.password, user_record.password
        ):
            raise AuthException(AuthErrorCode.AUTH_FAILED)
        user_record.status
        return await self.generate_tokens(user_id=user_record.id)

    async def find_by_id(self, id: int) -> Optional[UserPage]:
        """
        Retrieve a user by ID.

        Args:
            id (int): The user ID to retrieve.

        Returns:
            Optional[UserQuery]: The user query object if found, None otherwise.
        """
        user_record = await self.mapper.select_by_id(id=id)
        return UserPage(**user_record.model_dump()) if user_record else None

    async def get_user_by_page(
        self, user_query: UserQuery, current_user: CurrentUser
    ) -> PageResult:
        sort_list = None
        sort_str = user_query.sort_str
        if sort_str is not None:
            sort_list = json.loads(sort_str)
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if user_query.id is not None and user_query.id != "":
            eq["id"] = user_query.id
        if user_query.username is not None and user_query.username != "":
            like["username"] = user_query.username
        if user_query.password is not None and user_query.password != "":
            eq["password"] = user_query.password
        if user_query.nickname is not None and user_query.nickname != "":
            like["nickname"] = user_query.nickname
        if user_query.avatar_url is not None and user_query.avatar_url != "":
            eq["avatar_url"] = user_query.avatar_url
        if user_query.status is not None and user_query.status != "":
            eq["status"] = user_query.status
        if user_query.remark is not None and user_query.remark != "":
            eq["remark"] = user_query.remark
        if user_query.create_time is not None and user_query.create_time != "":
            eq["create_time"] = user_query.create_time
        filters = {
            FilterOperators.EQ: eq,
            FilterOperators.NE: ne,
            FilterOperators.GT: gt,
            FilterOperators.GE: ge,
            FilterOperators.LT: lt,
            FilterOperators.LE: le,
            FilterOperators.BETWEEN: between,
            FilterOperators.LIKE: like,
        }
        records, total = await self.mapper.select_by_ordered_page(
            current=user_query.current,
            page_size=user_query.page_size,
            count=user_query.count,
            sort_list=sort_list,
            **filters,
        )
        if total == 0 and user_query.count:
            return PageResult(records=[], total=total)
        records = [UserPage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def get_user_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[UserDetail]:
        user_do: UserModel = await self.mapper.select_by_id(id=id)
        if user_do is None:
            return None
        return UserDetail(**user_do.model_dump())

    async def export_user_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        user_list: List[UserModel] = await self.retrieve_by_ids(ids=ids)
        if user_list is None or len(user_list) == 0:
            return None
        user_page_list = [UserPage(**user.model_dump()) for user in user_list]
        return await excel_util.export_excel(
            schema=UserPage,
            file_name="user_data_export",
            data_list=user_page_list,
        )

    async def create_user(
        self, user_create: UserCreate, current_user: CurrentUser
    ) -> UserModel:
        user: UserModel = UserModel(**user_create.model_dump())
        # user.user_id = request.state.user_id
        return await self.save(data=user)

    async def batch_create_user(
        self, *, user_create_list: List[UserCreate], current_user: CurrentUser
    ) -> List[int]:
        user_list: List[UserModel] = [
            UserModel(**user_create.model_dump())
            for user_create in user_create_list
        ]
        await self.batch_save(data_list=user_list)
        return [user.id for user in user_list]

    @staticmethod
    async def import_user(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[List[UserCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_records = import_df.to_dict(orient="records")
        if user_records is None or len(user_records) == 0:
            return None
        for record in user_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_create_list = []
        for user_record in user_records:
            try:
                user_create = UserCreate(**user_record)
                user_create_list.append(user_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in user_record.items()
                    if k in UserCreate.model_fields
                }
                user_create = UserCreate.model_construct(**valid_data)
                user_create.err_msg = ValidateService.get_validate_err_msg(e)
                user_create_list.append(user_create)
                return user_create_list

        return user_create_list

    async def get_roles(self, id: int) -> Tuple[Set[str], List[RoleModel]]:
        """
        Get user's roles by user ID.
        Returns a set of role names and a list of role models.
        """
        roles: Set[str] = set()
        role_models: List[RoleModel] = []

        # Admin gets automatic 'admin' role
        if UserInfo.is_admin(id):
            roles.add("admin")
        else:
            # Get roles from database for non-admin users
            user_roles: List[UserRoleModel] = userRoleMapper.select_by_userid(
                user_id=id
            )
            if not user_roles:
                return roles, role_models

            role_ids = [user_role.role_id for user_role in user_roles]
            role_models = roleMapper.select_by_role_ids(role_ids=role_ids)
            if not role_models:
                return roles, role_models

            # Extract role names from role models
            role_names = [role.name for role in role_models]
            roles.update(role_names)

        return roles, role_models

    async def get_menus(
        self, id: int, role_models: List[RoleModel] = None
    ) -> List[MenuPage]:
        """
        Get accessible menus for user based on their roles.
        Returns a list of menu pages.
        """
        menus: List[MenuPage] = []

        # Admin gets all menus
        if UserInfo.is_admin(id):
            menu_list, total_count = await menuMapper.select_by_parent_id()
            if total_count == 0:
                return menus
            menus = [MenuPage(**menu.model_dump()) for menu in menu_list]
            return menus

        # Return empty if no roles provided for non-admin
        if not role_models:
            return menus

        # Get menus associated with user's roles
        role_ids = [role_model.id for role_model in role_models]
        role_menu_records: List[RoleMenuModel] = (
            roleMenuMapper.select_by_role_ids(role_ids=role_ids)
        )
        if not role_menu_records:
            return menus

        # Convert menu models to menu pages
        menu_id_list = [
            role_menu_record.menu_id for role_menu_record in role_menu_records
        ]
        menu_list: List[MenuModel] = menuMapper.select_by_ids(ids=menu_id_list)
        menus = [MenuPage(**menu.model_dump()) for menu in menu_list]
        return menus
