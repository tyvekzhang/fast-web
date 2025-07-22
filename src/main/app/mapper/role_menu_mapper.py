"""RoleMenu mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.role_menu_model import RoleMenuModel


class RoleMenuMapper(SqlModelMapper[RoleMenuModel]):
    pass


roleMenuMapper = RoleMenuMapper(RoleMenuModel)
