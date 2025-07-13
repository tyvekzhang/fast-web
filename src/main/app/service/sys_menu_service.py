"""Menu Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.model.sys_menu_model import MenuModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_menu_schema import (
    ListMenuRequest,
    MenuDetail,
    MenuCreate, Menu,
)
from src.main.app.core.service.base_service import BaseService


class MenuService(BaseService[MenuModel], ABC):
    @abstractmethod
    async def list_menus(
        self, *, req: ListMenuRequest
    ) -> PageResult[Menu]: ...

    @abstractmethod
    async def get_menu_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[MenuDetail]: ...

    @abstractmethod
    async def export_menu_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def create_menu(
        self, *, menu_create: MenuCreate, current_user: CurrentUser
    ) -> MenuModel: ...

    @abstractmethod
    async def batch_create_menu(
        self, *, menu_create_list: List[MenuCreate], current_user: CurrentUser
    ) -> List[int]: ...

    @abstractmethod
    async def import_menu(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> List[MenuCreate]: ...
