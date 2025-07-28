"""Index mapper"""

from typing import Union, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.index_model import IndexDO


class IndexMapper(SqlModelMapper[IndexDO]):
    async def select_by_table_id(
        self, table_id: int, db_session: Union[AsyncSession, None] = None
    ) -> List[IndexDO]:
        db_session = db_session or self.db.session
        statement = select(self.model).where(self.model.table_id == table_id)
        exec_result = await db_session.exec(statement)
        return exec_result.all()


indexMapper = IndexMapper(IndexDO)
