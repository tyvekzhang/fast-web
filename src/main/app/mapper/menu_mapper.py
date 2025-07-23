"""Menu mapper"""

from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.menu_model import MenuModel


class MenuMapper(SqlModelMapper[MenuModel]):
    async def select_by_name(
        self, *, name: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[MenuModel]:
        """
        Retrieve a menu record by name.
        """
        db_session = db_session or self.db.session
        user = await db_session.exec(
            select(self.model).where(self.model.name == name)
        )
        return user.one_or_none()

    async def select_by_names(
        self, *, names: list[str], db_session: Optional[AsyncSession] = None
    ) -> Optional[list[MenuModel]]:
        """
        Retrieve menu records by names.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.name.in_(names))
        )
        return result.all()


menuMapper = MenuMapper(MenuModel)
