"""RoleMenu mapper"""

from typing import Union, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_role_menu_model import RoleMenuModel


class RoleMenuMapper(SqlModelMapper[RoleMenuModel]):
    async def select_by_role_ids(
        self,
        *,
        role_ids: List[int],
        db_session: Union[AsyncSession, None] = None,
    ) -> Union[RoleMenuModel, None]:
        db_session = db_session or self.db.session
        query = select(RoleMenuModel).where(RoleMenuModel.id.in_(role_ids))
        result = await db_session.exec(query)
        return result.all()


roleMenuMapper = RoleMenuMapper(RoleMenuModel)
