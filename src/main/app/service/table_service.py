"""Table domain service interface"""

from abc import ABC, abstractmethod
from typing import Tuple, List

from src.main.app.schema.table_schema import TableQuery, TableGenerate
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.db_table_model import TableDO


class TableService(BaseService[TableDO], ABC):
    @abstractmethod
    async def list_tables(
        self, data: TableQuery
    ) -> Tuple[
        List[TableDO],
        int,
    ]:
        pass

    @abstractmethod
    async def generate_table(self, table_generate: TableGenerate) -> None: ...
