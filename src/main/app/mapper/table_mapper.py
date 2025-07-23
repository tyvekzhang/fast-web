"""Table mapper"""

from typing import Union, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.db_table_model import TableDO


class TableMapper(SqlModelMapper[TableDO]):
    async def select_by_database_id(
        self, database_id: int, db_session: Union[AsyncSession, None] = None
    ) -> List[TableDO]:
        db_session = db_session or self.db.session
        statement = select(self.model).where(
            self.model.database_id == database_id
        )
        exec_result = await db_session.exec(statement)
        return exec_result.all()


tableMapper = TableMapper(TableDO)
