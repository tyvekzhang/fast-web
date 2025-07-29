# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Connection domain service impl"""

from src.main.app.core.config.config_manager import (
    load_config,
)
from src.main.app.core.constant import FilterOperators

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.mapper.codegen.connection_mapper import ConnectionMapper
from src.main.app.model.codegen.connection_model import ConnectionModel
from src.main.app.schema.codegen.connection_schema import (
    ListConnectionResponse, ListConnectionsRequest,
)
from src.main.app.service.codegen.connection_service import ConnectionService


class ConnectionServiceImpl(
    BaseServiceImpl[ConnectionMapper, ConnectionModel], ConnectionService
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

    async def list_connections(self, req: ListConnectionsRequest):
        filters = {
            FilterOperators.LIKE: {},
            FilterOperators.EQ: {},
        }
        if not req.connection_name:
            filters[FilterOperators.LIKE]["connection_name"] = req.connection_name
        records, total_count = await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            **filters,
        )
        if total_count == 0:
            database_config = load_config().database
            dialect = database_config.dialect
            url = database_config.url
            connection_do: ConnectionModel
            if dialect.lower() == "sqlite":
                db_path = url.split("///")[1]
                connection_do = ConnectionModel(
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
                connection_do = ConnectionModel(
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
            ListConnectionResponse(**record.model_dump()) for record in records
        ]
        return records, total_count
