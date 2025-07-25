import os
import re
from typing import List

from src.main.app.core.config.config_manager import load_config
from src.main.app.core.gen.gen_constants import GenConstants
from src.main.app.core.utils.converter_util import ClassNameConverter
from src.main.app.core.utils.field_type_mapping_util import (
    sql_map2sqlmodel_type,
)
from src.main.app.core.utils.string_util import StringUtils, is_empty
from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO

config = load_config()
gen_config = config.gen


class GenUtils:
    @staticmethod
    def init_table(gen_table: GenTableDO):
        gen_table.class_name = GenUtils.convert_class_name(gen_table.class_name)
        gen_table.package_name = gen_config.package_name
        gen_table.module_name = GenUtils.get_module_name(
            gen_config.package_name
        )
        gen_table.business_name = GenUtils.get_business_name(
            gen_table.class_name
        )
        gen_table.function_name = GenUtils.replace_text(gen_table.function_name)
        gen_table.function_author = gen_config.author

    @staticmethod
    def init_field(gen_field: GenFieldDO, field_record: FieldDO, backend: str):
        """
        Initialize column attribute fields
        """
        # 不同的backend影响field_name和field_type
        data_type = field_record.type
        field_name = field_record.name
        field_length = field_record.length
        sort = field_record.sort
        default = field_record.default
        nullable = field_record.nullable
        scale = field_record.scale

        gen_field.length = field_length
        if backend == "python":
            gen_field.field_name = field_name
            gen_field.field_type = GenConstants.TYPE_PY_STRING
        elif backend == "java":
            gen_field.field_name = StringUtils.to_camel_case(field_name)
            gen_field.field_type = GenConstants.TYPE_STRING
        else:
            raise Exception(f"未支持的后端语言: {backend}")

        gen_field.sort = sort
        gen_field.default = default
        gen_field.nullable = nullable
        gen_field.scale = scale
        gen_field.js_type = GenConstants.TYPE_JS_STRING
        gen_field.query_type = GenConstants.QUERY_EQ
        gen_field.primary_key = field_record.primary_key
        gen_field.comment = field_record.comment

        if GenUtils.arrays_contains(
            GenConstants.COLUMNTYPE_STR, data_type
        ) or GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TEXT, data_type):
            html_type = (
                GenConstants.HTML_TEXTAREA
                if GenUtils.arrays_contains(
                    GenConstants.COLUMNTYPE_TEXT, data_type
                )
                or (field_length is not None and field_length >= 500)
                else GenConstants.HTML_INPUT
            )
            if field_name == "comment" or field_name == "remark":
                html_type = GenConstants.HTML_TEXTAREA
            gen_field.html_type = html_type
        elif GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TIME, data_type):
            if backend == "python":
                gen_field.field_type = GenConstants.TYPE_PY_DATETIME
            elif backend == "java":
                gen_field.field_type = GenConstants.TYPE_LOCALDATETIME
            else:
                raise Exception(f"未支持的后端语言: {backend}")

            gen_field.html_type = GenConstants.HTML_DATEPICKER
        elif data_type == GenConstants.TYPE_VECTOR:
            gen_field.field_type = GenConstants.TYPE_VECTOR
        elif GenUtils.arrays_contains(
            GenConstants.COLUMNTYPE_NUMBER, data_type
        ):
            gen_field.html_type = GenConstants.HTML_INPUT
            gen_field.js_type = GenConstants.TYPE_JS_NUMBER
            scale = field_record.scale
            length = field_record.length
            if scale is not None:
                if backend == "python":
                    gen_field.field_type = GenConstants.TYPE_PY_DECIMAL
                elif backend == "java":
                    gen_field.field_type = GenConstants.TYPE_BIGDECIMAL
                else:
                    raise Exception(f"未支持的后端语言: {backend}")
            elif (
                data_type == "int4"
                or data_type == "int2"
                or (length is not None and length <= 10)
            ):
                if backend == "python":
                    gen_field.field_type = GenConstants.TYPE_PY_INTEGER
                elif backend == "java":
                    gen_field.field_type = GenConstants.TYPE_INTEGER
                else:
                    raise Exception(f"未支持的后端语言: {backend}")
            else:
                if backend == "python":
                    gen_field.field_type = GenConstants.TYPE_PY_INTEGER
                elif backend == "java":
                    gen_field.field_type = GenConstants.TYPE_LONG
                else:
                    raise Exception(f"未支持的后端语言: {backend}")
        gen_field.sql_model_type = sql_map2sqlmodel_type(gen_field.field_type)

        # Insert field
        if not GenUtils.arrays_contains(
            GenConstants.COLUMNNAME_NOT_INSERT, field_name
        ):
            gen_field.creatable = GenConstants.REQUIRE

        # Modify field
        if not GenUtils.arrays_contains(
            GenConstants.COLUMNNAME_NOT_MODIFY, field_name
        ):
            gen_field.updatable = GenConstants.REQUIRE

        # BatchModify field
        if not GenUtils.arrays_contains(
            GenConstants.COLUMNNAME_NOT_BATCH_MODIFY, field_name
        ):
            gen_field.batch_updatable = GenConstants.REQUIRE

        # Page field
        if not GenUtils.arrays_contains(
            GenConstants.COLUMNNAME_NOT_PAGE, field_name
        ):
            gen_field.critical = GenConstants.REQUIRE

        # Detail field
        if (
            not GenUtils.arrays_contains(
                GenConstants.COLUMNNAME_NOT_PAGE, field_name
            )
            and field_name != field_record.primary_key
        ):
            gen_field.detailable = GenConstants.REQUIRE

        # Query field
        if not GenUtils.arrays_contains(
            GenConstants.COLUMNNAME_NOT_QUERY, field_name
        ) and not field_name.__contains__("_id"):
            gen_field.queryable = GenConstants.REQUIRE

        # Query field type
        if StringUtils.ends_with_ignore_case(field_name, "name"):
            gen_field.query_type = GenConstants.QUERY_LIKE

        # Set radio button for status fields
        if StringUtils.ends_with_ignore_case(field_name, "status"):
            gen_field.html_type = GenConstants.HTML_RADIO
        # Set dropdown for type and sex fields
        elif StringUtils.ends_with_ignore_case(
            field_name, "type"
        ) or StringUtils.ends_with_ignore_case(field_name, "sex"):
            gen_field.html_type = GenConstants.HTML_SELECT
        # Set image upload control for image fields
        elif StringUtils.ends_with_ignore_case(field_name, "image"):
            gen_field.html_type = GenConstants.HTML_IMAGE_UPLOAD
        # Set file upload control for file fields
        elif StringUtils.ends_with_ignore_case(field_name, "file"):
            gen_field.html_type = GenConstants.HTML_FILE_UPLOAD
        # Set rich text control for content fields
        elif StringUtils.ends_with_ignore_case(field_name, "content"):
            gen_field.html_type = GenConstants.HTML_MODIFYOR

    @staticmethod
    def arrays_contains(arr, target_value) -> bool:
        return target_value in arr

    @staticmethod
    def get_module_name(package_name: str) -> str:
        return package_name.split(".")[-1]

    @staticmethod
    def get_business_name(table_name) -> str:
        return table_name.split("_")[-1]

    @staticmethod
    def convert_class_name(table_name: str) -> str:
        auto_remove_pre = gen_config.auto_remove_pre
        table_prefix = gen_config.table_prefix
        if auto_remove_pre and StringUtils.is_not_empty(table_prefix):
            search_list = StringUtils.split(table_prefix, ",")
            table_name = GenUtils.replace_first(table_name, search_list)
        converter = ClassNameConverter()
        table_name = converter.to_singular(table_name)
        table_name = table_name.strip("_")
        return converter.to_snake(table_name)

    @staticmethod
    def replace_first(replacement: str, search_list: List[str]) -> str:
        for search_string in search_list:
            search_string = search_string.strip()
            if replacement.startswith(search_string):
                return replacement.replace(search_string, "", 1)
        return replacement

    @staticmethod
    def replace_text(text):
        return re.sub(r"表", "", text)

    @staticmethod
    def get_db_type(field_type):
        return field_type.split("(")[0] if "(" in field_type else field_type

    @staticmethod
    def get_field_length(field_type):
        if "(" in field_type:
            length = field_type.split("(")[1].split(")")[0]
            return int(length)
        else:
            return 0

    @staticmethod
    def trim_jinja2_name(name: str) -> str:
        if is_empty(name):
            return ""
            # Get the base name of the file (without directory)
        base_name = os.path.basename(name)

        # Split the base name and extension
        name_without_extension, _ = os.path.splitext(base_name)

        # Split again to remove the .j2 extension if present
        name_without_j2, _ = os.path.splitext(name_without_extension)

        return name_without_j2
