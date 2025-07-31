"""Sqlmodel impl that handle database operation"""

from typing import Generic, TypeVar, Type, Optional, Sequence, Dict, Any

from pydantic import BaseModel
from sqlmodel import SQLModel, select, insert, update, delete, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.constant import FilterOperators, constant
from src.main.app.core.enums import SortEnum
from src.main.app.core.mapper.base_mapper import BaseMapper
from src.main.app.core.middleware.db_session_middleware import db
from src.main.app.core.schema import SortItem

IDType = TypeVar("IDType", int, str)
ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class SqlModelMapper(BaseMapper, Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
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
        validated_data = self.model.model_validate(data)
        db_session.add(validated_data)
        return validated_data

    async def batch_insert(
        self,
        *,
        data_list: list[ModelType],
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """
        Insert data list into the database in a single operation..
        """
        db_session = db_session or self.db.session
        validated_data_list = [
            self.model.model_validate(data) for data in data_list
        ]
        statement = insert(self.model).values(
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
        statement = select(self.model).where(self.model.id == id)
        db_response = await db_session.exec(statement)
        return db_response.one_or_none()

    async def select_by_ids(
        self, *, ids: list[IDType], db_session: Optional[AsyncSession] = None
    ) -> list[ModelType]:
        """
        Select record list by their IDs.
        """
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.id.in_(ids))
        db_response = await db_session.exec(statement)
        return db_response.all()

    async def select_by_page(
        self,
        *,
        current: int = 1,
        page_size: int = 100,
        count: bool = True,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> tuple[list[ModelType], int]:
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
        query = select(self.model)

        # Apply filters
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.model, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.model, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.model, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.model, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.model, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.model, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(
                    getattr(self.model, column).between(start, end)
                )
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                safe_value = f"{str(value)}%"
                query = query.filter(getattr(self.model, column).like(safe_value))

        # Get total count if requested
        total_count = 0
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        # Apply pagination
        query = query.offset((current - 1) * page_size).limit(page_size)

        exec_response = await db_session.exec(query)
        record_list: list[ModelType] = exec_response.all()

        return record_list, total_count

    async def select_by_ordered_page(
        self,
        *,
        current: int = 1,
        page_size: int = 100,
        count: bool = True,
        sort_list: list[SortItem] = None,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> tuple[list[ModelType], int]:
        """
        Select a list of data_list, with optional filtering, pagination, and ordering.

        Parameters:
            current : The current page number to select (1-indexed)
            page_size : The number of data_list per page
            count : Whether to data the total row
            sort_list: List of SortItems for multi-column ordering (default: primary key desc)
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
        query = select(self.model)

        # Apply filters
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.model, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.model, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.model, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.model, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.model, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.model, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(
                    getattr(self.model, column).between(start, end)
                )
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                safe_value = f"{str(value)}%"
                query = query.filter(getattr(self.model, column).like(safe_value))

        # Get total count if requested
        total_count = 0
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]

        # Apply sorting
        if sort_list:
            for sort_item in sort_list:
                column = getattr(self.model, sort_item["field"])
                query = query.order_by(
                    column.asc()
                    if sort_item["order"] == SortEnum.ascending
                    else column.desc()
                )
        else:
            # Default to primary key descending
            query = query.order_by(self.model.id.desc())

        # Apply pagination
        query = query.offset((current - 1) * page_size).limit(page_size)

        exec_response = await db_session.exec(query)
        data_list: list[ModelType] = exec_response.all()

        return data_list, total_count

    async def select_by_parent_id(
        self,
        *,
        current: int = 1,
        page_size: int = constant.MAX_PAGE_SIZE,
        count: bool = True,
        sort_list: list[SortItem] = None,
        db_session: Optional[AsyncSession] = None,
        **kwargs,
    ) -> tuple[list[ModelType], int]:
        """
        Select record list with pagination and sorting by parent ID.

        Parameters:
            current : The current page number to select (1-indexed)
            page_size : The number of data_list per page
            count : Whether to data the total row
            sort_list: List of SortItems for multi-column ordering (default: primary key desc)
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
        query = select(self.model)

        # Apply filters
        if hasattr(self.model, constant.PARENT_ID) and (
            constant.PARENT_ID not in kwargs
            or kwargs[constant.PARENT_ID] is None
        ):
            query = query.filter(
                getattr(self.model, constant.PARENT_ID)
                == constant.ROOT_PARENT_ID
            )
        if FilterOperators.EQ in kwargs:
            for column, value in kwargs[FilterOperators.EQ].items():
                query = query.filter(getattr(self.model, column) == value)
        if FilterOperators.NE in kwargs:
            for column, value in kwargs[FilterOperators.NE].items():
                query = query.filter(getattr(self.model, column) != value)
        if FilterOperators.GT in kwargs:
            for column, value in kwargs[FilterOperators.GT].items():
                query = query.filter(getattr(self.model, column) > value)
        if FilterOperators.GE in kwargs:
            for column, value in kwargs[FilterOperators.GE].items():
                query = query.filter(getattr(self.model, column) >= value)
        if FilterOperators.LT in kwargs:
            for column, value in kwargs[FilterOperators.LT].items():
                query = query.filter(getattr(self.model, column) < value)
        if FilterOperators.LE in kwargs:
            for column, value in kwargs[FilterOperators.LE].items():
                query = query.filter(getattr(self.model, column) <= value)
        if FilterOperators.BETWEEN in kwargs:
            for column, (start, end) in kwargs[FilterOperators.BETWEEN].items():
                query = query.filter(
                    getattr(self.model, column).between(start, end)
                )
        if FilterOperators.LIKE in kwargs:
            for column, value in kwargs[FilterOperators.LIKE].items():
                safe_value = f"{str(value)}%"
                query = query.filter(getattr(self.model, column).like(safe_value))

        # Get total count if requested
        total_count = 0
        if count:
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await db_session.exec(count_query)
            total_count: int = total_count_result.all()[0]
            if total_count > constant.MAX_PAGE_SIZE:
                raise ValueError(
                    f"Total count exceeds {constant.MAX_PAGE_SIZE}"
                )

        # Apply sorting
        if sort_list:
            for sort_item in sort_list:
                column = getattr(self.model, sort_item["field"])
                query = query.order_by(
                    column.asc()
                    if sort_item["order"] == SortEnum.ascending
                    else column.desc()
                )
        else:
            # Default to primary key descending
            query = query.order_by(self.model.id.desc())

        # Apply pagination
        query = query.offset((current - 1) * page_size).limit(page_size)

        exec_response = await db_session.exec(query)
        data_list: list[ModelType] = exec_response.all()

        return data_list, total_count

    async def update_by_id(
        self, *, data: ModelType, db_session: Optional[AsyncSession] = None
    ) -> int:
        """
        Update a single data by its ID.
        """
        db_session = db_session or self.db.session
        update_statement = update(self.model).where(self.model.id == data.id)
        update_values = data.model_dump(exclude_unset=True)
        update_statement = update_statement.values(**update_values)
        exec_response = await db_session.exec(update_statement)
        return exec_response.rowcount

    async def batch_update(
        self,
        *,
        items: Sequence[Dict[str, Any]],
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """
        Update multiple records with possibly different values.
        Supports both single and composite primary keys.

        Example:
            items = [
                {"user_id": 1, "role_id": 2, "status": "active"},
                {"user_id": 3, "role_id": 4, "status": "disabled"},
            ]
        """
        db_session = db_session or self.db.session
        updated_count = 0

        # Extract primary key column names
        pk_fields = list(self.model.__table__.primary_key.columns.keys())

        for item in items:
            # Skip if any primary key is missing
            if not all(k in item for k in pk_fields):
                continue

            # Build WHERE clause for composite keys
            where_clause = and_(
                *[getattr(self.model, pk) == item[pk] for pk in pk_fields]
            )

            # Extract update gen_fields
            update_data = {k: v for k, v in item.items() if k not in pk_fields}
            if not update_data:
                continue

            # Execute update
            stmt = update(self.model).where(where_clause).values(**update_data)
            result = await db_session.exec(stmt)
            updated_count += result.rowcount

        return updated_count

    async def batch_update_by_ids(
        self,
        *,
        ids: list[IDType],
        data: dict,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        """
        Update multiple record by their IDs.
        """
        db_session = db_session or self.db.session
        statement = update(self.model).where(self.model.id.in_(ids))
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
        statement = delete(self.model).where(self.model.id == id)
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def batch_delete_by_ids(
        self, *, ids: list[IDType], db_session: Optional[AsyncSession] = None
    ) -> int:
        """
        Delete record list by their IDs.
        """
        db_session = db_session or self.db.session
        statement = delete(self.model).where(self.model.id.in_(ids))
        exec_response = await db_session.exec(statement)
        return exec_response.rowcount

    async def get_children_recursively(
        self,
        *,
        parent_data: list[SchemaType],
        schema_class: Type[SchemaType],
        level: int = 1,
        max_level: int = 5,
        db_session: Optional[AsyncSession] = None,
    ) -> list[SchemaType]:
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
        db_session = db_session or self.db.session
        if level > max_level or not parent_data or len(parent_data) == 0:
            return parent_data

        parent_ids = [item.id for item in parent_data]
        if not parent_ids:
            return parent_data

        # Query children for the current level
        stmt = select(self.model).where(self.model.parent_id.in_(parent_ids))
        result = await db_session.execute(stmt)
        children = result.scalars().all()

        # Convert ORM children to SchemaType instances
        children_schema = [
            schema_class(**child.model_dump()) for child in children
        ]  # 假设使用 Pydantic 的 from_orm

        # Group children by parent_id
        children_by_parent = {}
        for child in children_schema:
            children_by_parent.setdefault(child.parent_id, []).append(child)

        # Assign children and recursively fetch deeper children
        for parent in parent_data:
            children = children_by_parent.get(parent.id, [])
            nested_children = await self.get_children_recursively(
                parent_data=children,
                schema_class=schema_class,
                level=level + 1,
                max_level=max_level,
                db_session=db_session,
            )
            parent.children = nested_children if nested_children else None

        return parent_data
