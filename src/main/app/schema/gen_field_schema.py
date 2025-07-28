"""GenTableColumn domain schema"""

from pydantic import BaseModel

from src.main.app.model.meta_field_model import FieldDO
from src.main.app.model.field_model import GenFieldDO
from src.main.app.core.schema import PaginationRequest


class GenTableColumnAdd(BaseModel):
    pass


class GenTableColumnQuery(PaginationRequest):
    pass


class GenTableColumnQueryResponse(BaseModel):
    pass


class GenTableColumnExport(BaseModel):
    pass


class GenTableColumnQueryForm(BaseModel):
    pass


class GenTableColumnModify(BaseModel):
    pass


class FieldGen(BaseModel):
    #
    field: FieldDO
    gen_field: GenFieldDO


class GenFieldDb(BaseModel):
    gen_field: GenFieldDO
    db_field: FieldDO
