"""Menu mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_menu_model import MenuModel


class MenuMapper(SqlModelMapper[MenuModel]):
    pass


menuMapper = MenuMapper(MenuModel)
