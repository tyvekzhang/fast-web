"""Connection domain service impl"""

from src.main.app.core.config.config_manager import (
    load_config,
)

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.mapper.connection_mapper import ConnectionMapper
from src.main.app.model.connection_model import ConnectionDO
from src.main.app.schema.connection_schema import (
    ConnectionQuery,
    ConnectionQueryResponse,
)
from src.main.app.service.connection_service import ConnectionService


class ConnectionServiceImpl(
    BaseServiceImpl[ConnectionMapper, ConnectionDO], ConnectionService
):
    """
    Implementation of the ConnectionService interface.
    """

    def __init__(self, mapper: ConnectionMapper):
        """
        Initialize the ConnectionServiceImpl instance.

        Args:
            mapper (ConnectionMapper): The ConnectionMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_connections(self, data: ConnectionQuery):
        records, total_count = await self.mapper.select_by_ordered_page(
            current=data.current,
            pageSize=data.pageSize,
        )
        if total_count == 0:
            database_config = load_config().database
            dialect = database_config.dialect
            url = database_config.url
            connection_do: ConnectionDO
            if dialect.lower() == "sqlite":
                db_path = url.split("///")[1]
                connection_do = ConnectionDO(
                    connection_name="默认",
                    database_type=dialect,
                    host="",
                    port=0,
                    username="",
                    password="",
                    database=db_path,
                )

            else:
                # driver://user:pass@localhost:port/dbname
                url = url.split("//")[1]
                user_pass_arr = url.split("@")[0].split(":")
                host_port_arr = url.split("@")[1].split("/")[0].split(":")
                host = host_port_arr[0]
                port = host_port_arr[1]
                username = user_pass_arr[0]
                password = user_pass_arr[1]
                connection_do = ConnectionDO(
                    connection_name="默认",
                    database_type=dialect,
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    database=url.split("@")[1].split("/")[1],
                )
            await self.mapper.insert(data=connection_do)
            return [connection_do], 1
        records = [
            ConnectionQueryResponse(**record.model_dump()) for record in records
        ]
        return records, total_count
