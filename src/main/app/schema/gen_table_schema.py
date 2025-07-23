"""GenTable domain schema"""

from datetime import datetime
from typing import Optional, List, Union, Any

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.field_schema import AntTableColumn
from src.main.app.schema.gen_field_schema import FieldGen


class GenTableAdd(BaseModel):
    pass


class GenTableQuery(PaginationRequest):
    pass


class GenTableQueryResponse(BaseModel):
    id: int
    connection_name: str
    database_name: str
    table_id: int
    table_name: str
    entity: str
    table_comment: Optional[str] = None
    create_time: datetime


class GenTableExport(BaseModel):
    pass


class GenTableQueryForm(BaseModel):
    pass


class GenTableModify(BaseModel):
    pass


class TableImport(BaseModel):
    database_id: int
    table_ids: List[int]
    backend: str


class TableGen(BaseModel):
    gen_table: Optional[GenTableDO]
    fields: Union[List[FieldGen], None]
    sub_table: Optional[GenTableDO] = None
    pk_field: Optional[str] = None
    tree_code: Optional[str] = None
    tree_parent_code: Optional[str] = None
    tree_name: Optional[str] = None
    parent_menu_id: Optional[int] = None
    parent_menu_name: Optional[str] = None


class GenTableDetail(BaseModel):
    gen_table: GenTableDO
    gen_field: List[GenFieldDO]


class GenTableExecute(BaseModel):
    database_id: int
    sql_statement: str


class GenTableRecord(BaseModel):
    fields: List[AntTableColumn]
    records: List[Any]
