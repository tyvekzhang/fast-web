"""DictData mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_dict_data_model import DictDataModel


class DictDataMapper(SqlModelMapper[DictDataModel]):
    pass


dictDataMapper = DictDataMapper(DictDataModel)
