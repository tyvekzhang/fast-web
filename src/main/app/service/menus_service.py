"""Menu Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile
from starlette.responses import StreamingResponse

from src.main.app.core.schema import CurrentUser
from src.main.app.core.service.base_service import BaseService
from src.main.app.model.menus_model import MenuModel
from src.main.app.schema.menus_schema import (
    ListMenuRequest,
    CreateMenuRequest,
    Menu,
    UpdateMenuRequest,
    BatchDeleteMenusRequest,
    ImportMenusResponse,
    ExportMenusRequest,
    BatchCreateMenuRequest,
)


class MenuService(BaseService[MenuModel], ABC):
    @abstractmethod
    async def get_menu(
        self,
        *,
        id: int,
    ) -> MenuModel: ...

    @abstractmethod
    async def list_menus(
        self, *, req: ListMenuRequest
    ) -> tuple[list[MenuModel], int]: ...

    @abstractmethod
    async def get_children_recursively(
        self, *, parent_data: list[MenuModel], schema_class: Menu
    ) -> list[Menu]: ...

    @abstractmethod
    async def create_menu(self, *, req: CreateMenuRequest) -> MenuModel: ...

    @abstractmethod
    async def update_menu(self, req: UpdateMenuRequest) -> MenuModel: ...

    @abstractmethod
    async def delete_menu(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_menus(self, ids: list[int]) -> list[MenuModel]: ...

    @abstractmethod
    async def batch_create_menus(
        self,
        *,
        req: BatchCreateMenuRequest,
    ) -> list[MenuModel]: ...

    @abstractmethod
    async def export_menu_page(
        self, *, ids: list[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def batch_remove_menus(self, req: BatchDeleteMenusRequest): ...

    @abstractmethod
    async def import_menus(self, req: UploadFile) -> ImportMenusResponse: ...

    @abstractmethod
    async def export_menus_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_menus(
        self, req: ExportMenusRequest
    ) -> StreamingResponse: ...
