"""Meta Table domain service interface"""

from abc import ABC, abstractmethod
from typing import Tuple, List

from src.main.app.schema.meta_table_schema import TableQuery, TableGenerate
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.meta_table_model import MetaTableModel


class MetaTableService(BaseService[MetaTableModel], ABC):
    @abstractmethod
    async def list_tables(
        self, data: TableQuery
    ) -> Tuple[
        List[MetaTableModel],
        int,
    ]:
        pass

    @abstractmethod
    async def generate_table(self, table_generate: TableGenerate) -> None: ...
