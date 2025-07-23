"""Index domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.core.service.base_service import BaseService
from src.main.app.schema.index_schema import IndexQuery

from src.main.app.model.db_index_model import IndexDO


class IndexService(BaseService[IndexDO], ABC):
    @abstractmethod
    async def list_indexes(self, data: IndexQuery): ...
