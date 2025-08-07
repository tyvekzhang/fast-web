from typing import List, Optional


class GenTable:
    def __init__(
        self,
        table_id: Optional[int] = None,
        table_name: str = "",
        table_comment: str = "",
        sub_table_name: Optional[str] = None,
        sub_table_fk_name: Optional[str] = None,
        class_name: str = "",
        tpl_category: Optional[str] = None,
        tpl_web_type: Optional[str] = None,
        package_name: str = "",
        module_name: str = "",
        business_name: str = "",
        function_name: str = "",
        function_author: str = "",
        gen_type: Optional[str] = None,
        gen_path: Optional[str] = None,
        pk_column: Optional["GenTableColumn"] = None,
        sub_table: Optional["GenTable"] = None,
        columns: Optional[List["GenTableColumn"]] = None,
        options: Optional[str] = None,
        tree_code: Optional[str] = None,
        tree_parent_code: Optional[str] = None,
        tree_name: Optional[str] = None,
        parent_menu_id: Optional[int] = None,
        parent_menu_name: Optional[str] = None,
    ):
        self.table_id = table_id
        self.table_name = table_name
        self.table_comment = table_comment
        self.sub_table_name = sub_table_name
        self.sub_table_fk_name = sub_table_fk_name
        self.class_name = class_name
        self.tpl_category = tpl_category
        self.tpl_web_type = tpl_web_type
        self.package_name = package_name
        self.module_name = module_name
        self.business_name = business_name
        self.function_name = function_name
        self.function_author = function_author
        self.gen_type = gen_type
        self.gen_path = gen_path
        self.pk_column = pk_column
        self.sub_table = sub_table
        self.columns = columns or []
        self.options = options
        self.tree_code = tree_code
        self.tree_parent_code = tree_parent_code
        self.tree_name = tree_name
        self.parent_menu_id = parent_menu_id
        self.parent_menu_name = parent_menu_name

    def is_sub(self) -> bool:
        return self.tpl_category == "2"

    def is_tree(self) -> bool:
        return self.tpl_category == "3"

    def is_crud(self) -> bool:
        return self.tpl_category == "1"

    def is_super_column(self, java_field: str) -> bool:
        base_entity_fields = {
            "createBy",
            "createTime",
            "updateBy",
            "updateTime",
            "remark",
        }
        tree_entity_fields = {"parentName", "parentId", "orderNum", "ancestors"}

        if self.is_tree():
            return java_field.lower() in (tree_entity_fields | base_entity_fields)
        return java_field.lower() in base_entity_fields

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
