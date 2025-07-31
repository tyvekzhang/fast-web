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
"""Table domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.codegen.table_model import TableModel
from src.main.app.schema.codegen.table_schema import (
    Table,
    TableDetail, TableExecute, TableRecord, ListTablesRequest, ImportTable,
)


class TableService(BaseService[TableModel], ABC):
    @abstractmethod
    async def list_tables(self, req: ListTablesRequest): ...

    @abstractmethod
    async def build_tables(self, tables: list[TableModel]) -> list[Table]: ...

    @abstractmethod
    async def import_tables(self, req: ImportTable): ...

    @abstractmethod
    async def preview_code(self, id: int): ...

    @abstractmethod
    async def download_code(self, table_id: int): ...

    @abstractmethod
    async def get_table_data(self, *, id: int, current: int, page_size: int): ...

    @abstractmethod
    async def get_table_detail(self, *, id: int) -> TableDetail: ...

    @abstractmethod
    async def update_table(
        self, req: TableDetail
    ) -> None: ...

    @abstractmethod
    async def execute_sql(
        self, gen_table_execute: TableExecute
    ) -> TableRecord: ...
