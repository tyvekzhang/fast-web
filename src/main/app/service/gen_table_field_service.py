"""GenTableField domain service interface"""

from abc import ABC

from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.core.service.base_service import BaseService


class GenTableFieldService(BaseService[GenFieldDO], ABC):
    pass
