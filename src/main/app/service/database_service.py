"""Database domain service interface"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Any

from src.main.app.schema.database_schema import DatabaseQuery
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.database_model import DbDatabaseModel


class DatabaseService(BaseService[DbDatabaseModel], ABC):
    @abstractmethod
    async def add(self, *, data: DbDatabaseModel) -> DbDatabaseModel: ...

    @abstractmethod
    async def list_databases(
        self, data: DatabaseQuery
    ) -> Tuple[List[Any], int]: ...
