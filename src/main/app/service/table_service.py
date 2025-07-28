"""Table domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.model.codegen.table_model import TableModel
from src.main.app.schema.gen_table_schema import (
    Table,
    TableImport,
    ListMenusRequest,
    GenTableDetail,
    GenTableExecute,
    GenTableRecord,
)
from src.main.app.core.service.base_service import BaseService


class TableService(BaseService[TableModel], ABC):

    @abstractmethod
    async def list_tables(self, req: ListMenusRequest): ...

    @abstractmethod
    async def build_tables(self, tables: list[TableModel]) -> list[Table]: ...

    @abstractmethod
    async def import_gen_table(self, table_import: TableImport): ...

    @abstractmethod
    async def preview_code(self, gen_table_id: int): ...

    @abstractmethod
    async def download_code(self, table_id: int): ...

    @abstractmethod
    async def get_table_data(self, *, id: int, current: int, pageSize: int): ...

    @abstractmethod
    async def get_gen_table_detail(self, *, id: int) -> GenTableDetail: ...

    @abstractmethod
    async def modify_gen_table(self, gen_table_detail: GenTableDetail) -> None: ...

    @abstractmethod
    async def execute_sql(
        self, gen_table_execute: GenTableExecute
    ) -> GenTableRecord: ...
