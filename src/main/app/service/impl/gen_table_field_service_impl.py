"""GenTableField domain service impl"""

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.mapper.gen_field_mapper import GenFieldMapper
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.service.gen_table_field_service import GenTableFieldService


class GenTableFieldServiceImpl(
    BaseServiceImpl[GenFieldMapper, GenFieldDO], GenTableFieldService
):
    def __init__(self, mapper: GenFieldMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper
