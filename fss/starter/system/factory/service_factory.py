"""Service factory to produces required services"""

from typing import Optional

from fss.starter.system.mapper.role_mapper import roleMapper
from fss.starter.system.mapper.user_mapper import userMapper
from fss.starter.system.mapper.user_role_mapper import userRoleMapper
from fss.starter.system.service.impl.role_service_impl import RoleServiceImpl
from fss.starter.system.service.impl.user_role_service_impl import UserRoleServiceImpl
from fss.starter.system.service.impl.user_service_impl import UserServiceImpl
from fss.starter.system.service.role_service import RoleService
from fss.starter.system.service.user_role_service import UserRoleService
from fss.starter.system.service.user_service import UserService

_singleton_user_service_instance: Optional[UserService] = None
_singleton_role_service_instance: Optional[RoleService] = None
_singleton_user_role_service_instance: Optional[UserRoleService] = None


def get_user_service(service_name: str = "default") -> UserService:
    """
    Return an instance of the UserService implementation.

    Returns:
        UserService: An instance of the UserServiceImpl class.
    """
    global _singleton_user_service_instance
    if service_name == "default":
        if _singleton_user_service_instance is None:
            _singleton_user_service_instance = UserServiceImpl(mapper=userMapper)
        return _singleton_user_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")


def get_role_service(service_name: str = "default") -> RoleService:
    """
    Return an instance of the RoleService implementation.

    Returns:
        RoleService: An instance of the RoleServiceImpl class.
    """
    global _singleton_role_service_instance
    if service_name == "default":
        if _singleton_role_service_instance is None:
            _singleton_role_service_instance = RoleServiceImpl(mapper=roleMapper)
        return _singleton_role_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")


def get_user_role_service(service_name: str = "default") -> UserRoleService:
    """
    Return an instance of the UserRoleService implementation.

    Returns:
        UserRoleService: An instance of the UserRoleServiceImpl class.
    """
    global _singleton_user_role_service_instance
    if service_name == "default":
        if _singleton_user_role_service_instance is None:
            _singleton_user_role_service_instance = UserRoleServiceImpl(
                mapper=userRoleMapper
            )
        return _singleton_user_role_service_instance
    else:
        raise ValueError(f"Unknown service name: {service_name}")
