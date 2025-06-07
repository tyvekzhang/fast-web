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
"""Sqlmodel impl that handle database operation"""

from typing import Generic, TypeVar, List, Type, Tuple, Optional

from sqlmodel import SQLModel, select, insert, update, delete, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.constants import FilterOperators
from src.main.app.core.enums import SortEnum
from src.main.app.core.mapper.base_mapper import BaseMapper
from src.main.app.core.middleware.db_session_middleware import db
from src.main.app.core.schemas import SortItem

IDType = TypeVar("IDType", int, str)
ModelType = TypeVar("ModelType", bound=SQLModel)


class SqlModelMapper(BaseMapper, Generic[ModelType]):
    def __init__(self, entity: Type[ModelType]):
        self.entity = entity
        self.db = db

    async def insert(
        self,
        *,
        data: ModelType,
        db_session: Optional[AsyncSession] = None,
    ) -> ModelType:
        """
        Inserts a single data into the database.
        """

        db_session = db_session or self.db.session
        validated_data = self.entity.model_validate(data)
        db_session.add(validated_data)
        return validated_data

    async def batch_insert(
        self,
        *,
        data_list: List[ModelType],
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """
        Insert data list into the database in a single operation..
        """
        db_session = db_session or self.db.session
        validated_data_list = [
            self.entity.model_validate(data) for data in data_list
        ]
        statement = insert(self.entity).values(
            [data.model_dump() for data in validated_data_list]
        )
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def select_by_id(
        self, *, id: IDType, db_session: Optional[AsyncSession] = None
    ) -> Optional[ModelType]:
        """
        Select a single record by its ID.
        """
        db_session = db_session or self.db.session
        statement = select(self.entity).where(self.entity.id == id)
        db_response = await db_session.exec(statement)
        return db_response.one_or_none()

    async def select_by_ids(
        self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None
    ) -> List[ModelType]:
        """
        Select record list by their IDs.
        """
        db_session = db_session or self.db.session
        statement = select(self.entity).where(self.entity.id.in_(ids))
        db_response = await db_session.exec(statement)
        return db_response.all()

    async def select_by_page(
        self,
        *,
        current: int = 1,
        page_size: int = 200,
        count: bool = True,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], int]:
        """
        Select a list of record, with optional filtering, pagination, and ordering.

        Parameters:
            current : The current page number to select (1-indexed)
            page_size : The number of data_list per page
            count : Whether to data the total row
            db_session : The database session to use
            **kwargs: Additional filter criteria, including:
                - EQ: Equal to (e.g., {"column_name": value})
                - NE: Not equal to (e.g., {"column_name": value})
                - GT: Greater than (e.g., {"column_name": value})
                - GE: Greater than or equal to (e.g., {"column_name": value})
                - LT: Less than (e.g., {"column_name": value})
                - LE: Less than or equal to (e.g., {"column_name": value})
                - BETWEEN: Between two values (e.g., {"column_name": (start, end)})
                - LIKE: Fuzzy search (e.g., {"column_name": "%value%"})
        """
        db_session = db_session or self.db.session
        query = select(self.entity)

        # Apply filters
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.entity, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.entity, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.entity, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.entity, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.entity, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.entity, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(
                    getattr(self.entity, column).between(start, end)
                )
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                query = query.filter(getattr(self.entity, column).like(value))

        # Get total count if requested
        total_count = 0
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        # Apply pagination
        query = query.offset((current - 1) * page_size).limit(page_size)

        exec_response = await db_session.exec(query)
        record_list: List[ModelType] = exec_response.all()

        return record_list, total_count

    async def select_by_ordered_page(
        self,
        *,
        current: int = 1,
        page_size: int = 200,
        count: bool = True,
        sort: List[SortItem] = None,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> Tuple[List[ModelType], int]:
        """
        Select a list of data_list, with optional filtering, pagination, and ordering.

        Parameters:
            current : The current page number to select (1-indexed)
            page_size : The number of data_list per page
            count : Whether to data the total row
            sort: List of SortItems for multi-column ordering (default: primary key desc)
            db_session : The database session to use
            **kwargs: Additional filter criteria, including:
                - EQ: Equal to (e.g., {"column_name": value})
                - NE: Not equal to (e.g., {"column_name": value})
                - GT: Greater than (e.g., {"column_name": value})
                - GE: Greater than or equal to (e.g., {"column_name": value})
                - LT: Less than (e.g., {"column_name": value})
                - LE: Less than or equal to (e.g., {"column_name": value})
                - BETWEEN: Between two values (e.g., {"column_name": (start, end)})
                - LIKE: Fuzzy search (e.g., {"column_name": "%value%"})
        """
        db_session = db_session or self.db.session
        query = select(self.entity)

        # Apply filters
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.entity, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.entity, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.entity, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.entity, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.entity, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.entity, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(
                    getattr(self.entity, column).between(start, end)
                )
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                query = query.filter(getattr(self.entity, column).like(value))

        # Get total count if requested
        total_count = 0
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        # Apply sorting
        if sort:
            for sort_item in sort:
                column = getattr(self.entity, sort_item.field)
                query = query.order_by(
                    column.asc() if sort_item.order ==SortEnum.ascending  else column.desc()
                )
        else:
            # Default to primary key descending
            query = query.order_by(self.entity.id.desc())

        # Apply pagination
        query = query.offset((current - 1) * page_size).limit(page_size)

        exec_response = await db_session.exec(query)
        data_list: List[ModelType] = exec_response.all()

        return data_list, total_count

    async def update_by_id(
        self, *, data: ModelType, db_session: Optional[AsyncSession] = None
    ) -> int:
        """
        Update a single data by its ID.
        """
        db_session = db_session or self.db.session
        update_statement = update(self.entity).where(self.entity.id == data.id)
        update_values = data.model_dump(exclude_unset=True)
        update_statement = update_statement.values(**update_values)
        exec_response = await db_session.exec(update_statement)
        return exec_response.rowcount

    async def batch_update_by_ids(
        self,
        *,
        ids: List[IDType],
        data: dict,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """
        Update multiple record by their IDs.
        """
        db_session = db_session or self.db.session
        statement = update(self.entity).where(self.entity.id.in_(ids))
        for key, value in data.items():
            statement = statement.values({key: value})
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def delete_by_id(
        self, *, id: IDType, db_session: Optional[AsyncSession] = None
    ) -> int:
        """
        Delete a single data by its ID.
        """
        db_session = db_session or self.db.session
        statement = delete(self.entity).where(self.entity.id == id)
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def batch_delete_by_ids(
        self, *, ids: List[IDType], db_session: Optional[AsyncSession] = None
    ) -> int:
        """
        Delete record list by their IDs.
        """
        db_session = db_session or self.db.session
        statement = delete(self.entity).where(self.entity.id.in_(ids))
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount
