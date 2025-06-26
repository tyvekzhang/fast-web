"""UserRole mapper"""

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_user_role_model import UserRoleModel


class UserRoleMapper(SqlModelMapper[UserRoleModel]):
    async def select_by_userid(
        self, *, user_id: int, db_session: Union[AsyncSession, None] = None
    ) -> Union[UserRoleModel, None]:
        db_session = db_session or self.db.session
        query = select(UserRoleModel).where(UserRoleModel.user_id == user_id)
        result = await db_session.exec(query)
        return result.all()


userRoleMapper = UserRoleMapper(UserRoleModel)
