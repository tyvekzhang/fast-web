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
"""MetaTable domain service interface"""

from abc import ABC

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.codegen.meta_table_model import MetaTableModel
from src.main.app.schema.codegen.meta_table_schema import (
    ListMetaTablesRequest,
)


class MetaTableService(BaseService[MetaTableModel], ABC):
    @staticmethod
    async def list_meta_tables(
        self, req: ListMetaTablesRequest
    ) -> tuple[list[MetaTableModel], int]: ...

    @staticmethod
    async def filter_exist_meta_tables(self, req: list[MetaTableModel]) -> list[MetaTableModel]: ...
