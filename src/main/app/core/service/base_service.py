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
"""Abstract service with common database operations."""

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Tuple, Dict

from sqlmodel import SQLModel

from src.main.app.core.schema import SortItem

T = TypeVar("T", bound=SQLModel)
IDType = TypeVar("IDType", int, str)


class BaseService(Generic[T], ABC):
    """Abstract base service providing common database operations."""

    @abstractmethod
    async def save(self, *, data: T) -> T:
        """Save a single data and return it."""
        ...

    @abstractmethod
    async def batch_save(self, *, data_list: List[T]) -> int:
        """Save multiple data and return the count saved."""
        ...

    @abstractmethod
    async def retrieve_by_id(self, *, id: IDType) -> T:
        """Return a record by its ID."""
        ...

    @abstractmethod
    async def retrieve_by_ids(self, *, ids: List[IDType]) -> List[T]:
        """Return multiple records by their IDs."""
        ...

    @abstractmethod
    async def retrieve_data(
        self, *, current: int, page_size: int, **kwargs
    ) -> Tuple[List[T], int]:
        """Return paginated data with optional filters and total count."""
        ...

    @abstractmethod
    async def retrieve_ordered_data(
        self,
        *,
        current: int,
        page_size: int,
        sort: List[SortItem] = None,
        **kwargs,
    ) -> Tuple[List[T], int]:
        """Return paginated and sorted record with total count."""
        ...

    @abstractmethod
    async def modify_by_id(self, *, data: T) -> None:
        """Update a record by ID."""
        ...

    @abstractmethod
    async def batch_modify_by_ids(
        self, *, ids: List[IDType], data: Dict
    ) -> None:
        """Update multiple records by their IDs."""
        ...

    @abstractmethod
    async def remove_by_id(self, *, id: IDType) -> None:
        """Delete a record by its ID."""
        ...

    @abstractmethod
    async def batch_remove_by_ids(self, *, ids: List[IDType]) -> None:
        """Delete multiple records by their IDs."""
        ...
