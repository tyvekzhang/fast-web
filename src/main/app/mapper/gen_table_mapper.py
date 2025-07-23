"""GenTable mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.gen_table_model import GenTableDO


class GenTableMapper(SqlModelMapper[GenTableDO]):
    pass


genTableMapper = GenTableMapper(GenTableDO)
