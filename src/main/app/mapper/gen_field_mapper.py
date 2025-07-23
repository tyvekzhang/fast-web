"""GenField mapper"""

from typing import Union, List
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.gen_field_model import GenFieldDO


class GenFieldMapper(SqlModelMapper[GenFieldDO]):
    async def select_by_db_field_ids(
        self, *, ids: List[int], db_session: Union[AsyncSession, None] = None
    ) -> List[GenFieldDO]:
        db_session = db_session or self.db.session
        stmt = select(GenFieldDO).where(self.model.db_field_id.in_(ids))
        exec_result = await db_session.exec(stmt)
        return exec_result.all()

    async def batch_delete_by_field_ids(
        self,
        *,
        field_ids: List[int],
        db_session: Union[AsyncSession, None] = None,
    ) -> None:
        db_session = db_session or self.db.session
        stmt = delete(GenFieldDO).where(self.model.db_field_id.in_(field_ids))
        await db_session.exec(stmt)


genFieldMapper = GenFieldMapper(GenFieldDO)
