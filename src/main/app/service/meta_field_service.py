"""Meta field domain service interface"""

from abc import ABC, abstractmethod
from typing import List

from src.main.app.schema.field_schema import FieldQuery, AntTableColumn
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.meta_field_model import FieldDO

class MetaFieldService(BaseService[FieldDO], ABC):
    @abstractmethod
    async def list_fields(self, data: FieldQuery): ...

    @abstractmethod
    async def get_ant_table_fields(
        self, table_id: int
    ) -> List[AntTableColumn]: ...
