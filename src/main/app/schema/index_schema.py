"""Index domain schema"""

from typing import Optional

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase


class IndexAdd(BaseModel):
    pass


class IndexQuery(PageBase):
    table_id: int


class IndexExport(BaseModel):
    pass


class IndexQueryForm(BaseModel):
    pass


class IndexModify(BaseModel):
    pass


class IndexGenerate(BaseModel):
    name: str
    field: str
    type: Optional[str] = "normal"
    remark: Optional[str] = None
