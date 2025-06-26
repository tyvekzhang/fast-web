"""DictType mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_dict_type_model import DictTypeModel


class DictTypeMapper(SqlModelMapper[DictTypeModel]):
    pass


dictTypeMapper = DictTypeMapper(DictTypeModel)
