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
"""Index domain service impl"""

from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.mapper.codegen.index_mapper import IndexMapper
from src.main.app.model.codegen.index_model import IndexModel
from src.main.app.schema.codegen.index_schema import IndexQuery
from src.main.app.service.codegen.index_service import IndexService


class IndexServiceImpl(BaseServiceImpl[IndexMapper, IndexModel], IndexService):
    def __init__(self, mapper: IndexMapper):
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def list_indexes(self, data: IndexQuery):
        return await self.mapper.select_by_ordered_page(
            current=data.current,
            pageSize=data.pageSize,
            order_by=data.order_by,
            sort_order=data.sort_order,
            EQ={"table_id": data.table_id},
        )
