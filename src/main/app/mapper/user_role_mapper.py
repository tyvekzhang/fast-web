"""UserRole mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.user_role_model import UserRoleModel


class UserRoleMapper(SqlModelMapper[UserRoleModel]):
    pass


userRoleMapper = UserRoleMapper(UserRoleModel)
