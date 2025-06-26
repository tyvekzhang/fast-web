"""User mapper"""

from typing import Union

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.sys_user_model import UserModel


class UserMapper(SqlModelMapper[UserModel]):
    async def get_user_by_username(
        self, *, username: str, db_session: Union[AsyncSession, None] = None
    ) -> Union[UserModel, None]:
        """
        Retrieve a user record by username.
        """
        db_session = db_session or self.db.session
        user = await db_session.exec(
            select(UserModel).where(UserModel.username == username)
        )
        return user.one_or_none()


userMapper = UserMapper(UserModel)
