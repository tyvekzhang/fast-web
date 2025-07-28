"""GenTable mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.codegen.table_model import TableModel


class GenTableMapper(SqlModelMapper[TableModel]):
    pass


genTableMapper = GenTableMapper(TableModel)
