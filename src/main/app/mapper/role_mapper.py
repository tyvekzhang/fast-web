"""Role mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.role_model import RoleModel


class RoleMapper(SqlModelMapper[RoleModel]):
    pass


roleMapper = RoleMapper(RoleModel)
