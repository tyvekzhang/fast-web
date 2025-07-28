"""Connection domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.schema.connection_schema import ConnectionQuery
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.connection_model import ConnectionDO


class ConnectionService(BaseService[ConnectionDO], ABC):
    @abstractmethod
    async def list_connections(self, data: ConnectionQuery): ...
