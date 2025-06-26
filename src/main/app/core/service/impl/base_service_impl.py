# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
"""Common service impl with frequently db operations"""

from typing import TypeVar, List, Generic, Tuple, Dict

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.core.model import BaseModel
from src.main.app.core.schema import SortItem
from src.main.app.core.service.base_service import BaseService

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=SqlModelMapper)
IDType = TypeVar("IDType", int, str)


class BaseServiceImpl(Generic[M, T], BaseService[T]):
    def __init__(self, mapper: M):
        self.mapper = mapper

    async def save(self, *, data: T) -> T:
        return await self.mapper.insert(data=data)

    async def batch_save(self, *, data_list: List[T]) -> int:
        return await self.mapper.batch_insert(data_list=data_list)

    async def retrieve_by_id(self, *, id: IDType) -> T:
        return await self.mapper.select_by_id(id=id)

    async def retrieve_by_ids(self, *, ids: List[IDType]) -> List[T]:
        return await self.mapper.select_by_ids(ids=ids)

    async def retrieve_data(
        self, *, current: int, page_size: int, **kwargs
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_by_page(
            current=current, page_size=page_size, **kwargs
        )

    async def retrieve_ordered_data(
        self,
        *,
        current: int,
        page_size: int,
        sort: List[SortItem] = None,
        **kwargs,
    ) -> Tuple[
        List[T],
        int,
    ]:
        return await self.mapper.select_by_ordered_page(
            current=current,
            page_size=page_size,
            sort=sort,
            **kwargs,
        )

    async def modify_by_id(self, *, data: T) -> None:
        affect_row: int = await self.mapper.update_by_id(data=data)
        if affect_row != 1:
            raise ValueError

    async def batch_modify_by_ids(
        self, *, ids: List[IDType], data: Dict
    ) -> None:
        affect_row: int = await self.mapper.batch_update_by_ids(
            ids=ids, data=data
        )
        if len(ids) != affect_row:
            raise ValueError

    async def remove_by_id(self, *, id: IDType) -> None:
        affect_row: int = await self.mapper.delete_by_id(id=id)
        if affect_row != 1:
            raise ValueError

    async def batch_remove_by_ids(self, *, ids: List[IDType]) -> None:
        affect_row: int = await self.mapper.batch_delete_by_ids(ids=ids)
        if len(ids) != affect_row:
            raise ValueError
