"""Role mapper"""

from typing import Union, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_role_model import RoleModel


class RoleMapper(SqlModelMapper[RoleModel]):
    async def select_by_user_ids(
        self,
        *,
        user_ids: List[int],
        db_session: Union[AsyncSession, None] = None,
    ) -> Union[RoleModel, None]:
        db_session = db_session or self.db.session
        query = select(RoleModel).where(RoleModel.id.in_(user_ids))
        result = await db_session.exec(query)
        return result.all()


roleMapper = RoleMapper(RoleModel)
