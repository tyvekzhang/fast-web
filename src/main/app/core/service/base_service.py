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
    async def retrieve_data_list(
        self, *, current: int, page_size: int, **kwargs
    ) -> Tuple[List[T], int]:
        """Return paginated records with optional filters and total count."""
        ...

    @abstractmethod
    async def retrieve_ordered_data_list(
        self,
        *,
        current: int,
        page_size: int,
        sort: List[SortItem] = None,
        **kwargs,
    ) -> Tuple[List[T], int]:
        """Return paginated and sorted records with total count."""
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
