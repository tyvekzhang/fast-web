"""Field domain service interface"""

from abc import ABC

from src.main.app.model.field_model import GenFieldDO
from src.main.app.core.service.base_service import BaseService


class FieldService(BaseService[GenFieldDO], ABC):
    pass
