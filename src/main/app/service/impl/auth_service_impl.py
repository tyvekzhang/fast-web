"""Auth domain service impl"""

from __future__ import annotations

from datetime import timedelta
from typing import Set

from src.main.app.core import security
from src.main.app.core.config import config_manager
from src.main.app.core.enums import TokenTypeEnum
from src.main.app.core.schema import UserCredential
from src.main.app.enums import AuthErrorCode
from src.main.app.exception import AuthException
from src.main.app.mapper.menu_mapper import menuMapper
from src.main.app.mapper.role_mapper import roleMapper
from src.main.app.mapper.role_menu_mapper import roleMenuMapper
from src.main.app.mapper.user_mapper import userMapper
from src.main.app.mapper.user_role_mapper import userRoleMapper
from src.main.app.model.menus_model import MenuModel
from src.main.app.model.role_menu_model import RoleMenuModel
from src.main.app.model.role_model import RoleModel
from src.main.app.model.user_role_model import UserRoleModel
from src.main.app.schema.menus_schema import Menu
from src.main.app.schema.user_schema import (
    SignInWithEmailAndPasswordRequest,
    UserInfo,
)
from src.main.app.service.auth_service import AuthService


class AuthServiceImpl(AuthService):
    """
    Implementation of the AuthService interface.
    """

    @classmethod
    async def generate_tokens(cls, user_id: int) -> UserCredential:
        security_config = config_manager.load_security_config()

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

        return UserCredential(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def signin_email_password(
        self, *, req: SignInWithEmailAndPasswordRequest
    ) -> UserCredential:
        """
        Perform login and return an access token and refresh token.

        Args:
            req (LoginCmd): The login command containing username and password.

        Returns:
            UserCredential: The access token and refresh token.
        """
        # verify username and password
        username: str = req.username

        user_record = await userMapper.get_user_by_username(username=username)
        if user_record is None or not security.verify_password(
            req.password, user_record.password
        ):
            raise AuthException(AuthErrorCode.AUTH_FAILED)
        return await self.generate_tokens(user_id=user_record.id)

    async def get_roles(self, id: int) -> tuple[Set[str], list[RoleModel]]:
        """
        Get user's roles by user ID.
        Returns a set of role names and a list of role models.
        """
        roles: Set[str] = set()
        role_models: list[RoleModel] = []

        # Admin gets automatic 'admin' role
        if UserInfo.is_admin(id):
            roles.add("admin")
        else:
            # Get roles from database for non-admin users
            user_roles: list[
                UserRoleModel
            ] = await userRoleMapper.select_by_userid(user_id=id)
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
        self, id: int, role_models: list[RoleModel] = None
    ) -> list[Menu]:
        """
        Get accessible menus for user based on their roles.
        Returns a list of menu pages.
        """
        menus: list[Menu] = []

        # Admin gets all menus
        if UserInfo.is_admin(id):
            menu_list, total_count = await menuMapper.select_by_parent_id()
            if total_count == 0:
                return menus
            menus = [Menu(**menu.model_dump()) for menu in menu_list]
            return menus

        # Return empty if no roles provided for non-admin
        if not role_models:
            return menus

        # Get menus associated with user's roles
        role_ids = [role_model.id for role_model in role_models]
        role_menu_records: list[RoleMenuModel] = (
            roleMenuMapper.select_by_role_ids(role_ids=role_ids)
        )
        if not role_menu_records:
            return menus

        # Convert menu models to menu pages
        menu_id_list = [
            role_menu_record.menu_id for role_menu_record in role_menu_records
        ]
        menu_list: list[MenuModel] = menuMapper.select_by_ids(ids=menu_id_list)
        menus = [Menu(**menu.model_dump()) for menu in menu_list]
        return menus
