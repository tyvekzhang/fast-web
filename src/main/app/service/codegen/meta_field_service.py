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
"""Meta field domain service interface"""

from abc import ABC, abstractmethod
from typing import List

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.codegen.field_model import FieldModel
from src.main.app.schema.codegen.meta_field_schema import (
    ListFieldsRequest,
    AntTableColumn,
)


class MetaFieldService(BaseService[FieldModel], ABC):
    @abstractmethod
    async def list_fields(self, *, req: ListFieldsRequest): ...

    @abstractmethod
    async def get_ant_table_fields(
        self, table_id: int
    ) -> List[AntTableColumn]: ...
