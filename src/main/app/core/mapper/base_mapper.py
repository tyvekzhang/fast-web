"""BaseMapper defines the database operations to be implemented"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar, Type

from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.schema import SortItem

ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
IDType = TypeVar("IDType", int, str)


class BaseMapper(ABC, Generic[ModelType]):
    @abstractmethod
    async def insert(
        self, *, data: ModelType, db_session: Optional[AsyncSession] = None
    ) -> ModelType:
        """Insert a single data into the database.

        Args:
            data: The data to insert
            db_session: Optional async database session. If None, will use default session.

        Returns:
            The inserted data with id
        """
        raise NotImplementedError

    @abstractmethod
    async def batch_insert(
        self,
        *,
        data_list: List[ModelType],
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """Insert data list into the database in a single operation.

        Args:
            data_list: List of data to insert
            db_session: Optional async database session

        Returns:
            Number of data list successfully inserted
        """
        raise NotImplementedError

    @abstractmethod
    async def select_by_id(
        self, *, id: IDType, db_session: Optional[AsyncSession] = None
    ) -> Optional[ModelType]:
        """Select a single record by its ID.

        Args:
            id: The ID of the record to select
            db_session: Optional async database session

        Returns:
            The selected record or None if not found
        """
        raise NotImplementedError

    @abstractmethod
    async def select_by_ids(
        self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None
    ) -> List[ModelType]:
        """Select record list by their IDs.

        Args:
            ids: List of IDs to select
            db_session: Optional async database session

        Returns:
            List of selected record
        """
        raise NotImplementedError

    @abstractmethod
    async def select_by_page(
        self,
        *,
        current: IDType,
        page_size: int,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], int]:
        """Select record list with pagination.

        Args:
            current: Current page number (1-based)
            page_size: Number of data_list per page
            db_session: Optional async database session
            **kwargs: Additional filter criteria

        Returns:
            Tuple of (list of record for current page_size, total data count)
        """
        raise NotImplementedError

    @abstractmethod
    async def select_by_ordered_page(
        self,
        *,
        current: IDType,
        page_size: int,
        sort: List[SortItem] = None,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], int]:
        """Select record list with pagination and sorting.

        Args:
            current: Current page number (1-based)
            page_size: Number of record list per page
            sort: Sorting specification in the format[{"field": "field1", "sort": "asc"}]
            db_session: Optional async database session
            **kwargs: Additional filter criteria

        Returns:
            Tuple of (list of record for current page_size, total data count)
        """
        raise NotImplementedError

    @abstractmethod
    async def select_by_parent_id(
        self,
        *,
        current: IDType,
        page_size: int,
        sort: List[SortItem] = None,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], int]:
        """Select record list with pagination and sorting by parent ID.

        Args:
            current: Current page number (1-based)
            page_size: Number of record list per page
            sort: Sorting specification in the format[{"field": "field1", "sort": "asc"}]
            db_session: Optional async database session
            **kwargs: Additional filter criteria

        Returns:
            Tuple of (list of record for current page_size, total data count)
        """
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(
        self, *, data: ModelType, db_session: Optional[AsyncSession] = None
    ) -> int:
        """Update a record by its ID.

        Args:
            data: The data to update (must contain ID)
            db_session: Optional async database session

        Returns:
            Number of data updated (0 or 1)
        """
        raise NotImplementedError

    @abstractmethod
    async def batch_update_by_ids(
        self,
        *,
        ids: List[IDType],
        data: Dict[str, Any],
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """Update record list by their IDs with the same values.

        Args:
            ids: List of IDs to update
            data: Dictionary of field-value pairs to update
            db_session: Optional async database session

        Returns:
            Number of record list updated
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(
        self, *, id: IDType, db_session: Optional[AsyncSession] = None
    ) -> int:
        """Delete a data by its ID.

        Args:
            id: ID of the data to delete
            db_session: Optional async database session

        Returns:
            Number of data_list deleted (0 or 1)
        """
        raise NotImplementedError

    @abstractmethod
    async def batch_delete_by_ids(
        self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None
    ) -> int:
        """Delete multiple data_list by their IDs.

        Args:
            ids: List of IDs to delete
            db_session: Optional async database session

        Returns:
            Number of data_list deleted
        """
        raise NotImplementedError

    @abstractmethod
    async def get_children_recursively(
        self,
        *,
        parent_data: List[SchemaType],
        schema_class: Type[SchemaType],
        level: int = 1,
        max_level: int = 5,
        db_session: Optional[AsyncSession] = None
    ) -> List[SchemaType]:
        """
        Recursively fetch children of given parent items up to 5 levels.

        Args:
            parent_data: A list of parent items with at least 'id' field
            schema_class: The Pydantic schema class used to serialize ORM objects
            level: Current recursion depth (starts from 1)
            max_level: Max recursion depth
            db_session: Optional async database session

        Returns:
            A list of parent items, each with a `children` attribute (list)
        """
        raise NotImplementedError
