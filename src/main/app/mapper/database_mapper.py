"""Database mapper"""

from typing import Union, List

from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.db_database_model import DatabaseDO


class DatabaseMapper(SqlModelMapper[DatabaseDO]):
    async def select_by_connection_id(
        self, connection_id: int, db_session: Union[AsyncSession, None] = None
    ) -> List[DatabaseDO]:
        db_session = db_session or self.db.session
        statement = select(self.model).where(
            self.model.connection_id == connection_id
        )
        exec_result = await db_session.exec(statement)
        return exec_result.all()

    async def delete_by_connection_id(
        self, connection_id: int, db_session: Union[AsyncSession, None] = None
    ) -> int:
        db_session = db_session or self.db.session
        statement = delete(self.model).where(
            self.model.connection_id == connection_id
        )
        exec_result = await db_session.exec(statement)
        return exec_result.rowcount


databaseMapper = DatabaseMapper(DatabaseDO)
