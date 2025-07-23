"""Connection mapper"""

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.db_connection_model import ConnectionDO


class ConnectionMapper(SqlModelMapper[ConnectionDO]):
    pass


connectionMapper = ConnectionMapper(ConnectionDO)
