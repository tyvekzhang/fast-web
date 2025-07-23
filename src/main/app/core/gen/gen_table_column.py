class GenTableColumn:
    def __init__(
        self,
        column_id=None,
        table_id=None,
        column_name="",
        column_comment="",
        column_type="",
        java_type="",
        java_field="",
        is_pk="0",
        is_increment="0",
        is_required="0",
        is_insert="0",
        is_edit="0",
        is_list="0",
        is_query="0",
        query_type="",
        html_type="",
        dict_type="",
        sort=0,
    ):
        """
        Initializes the GenTableColumn with default values.

        Args:
            column_id (int): Column ID
            table_id (int): Table ID
            column_name (str): Column name
            column_comment (str): Column comment
            column_type (str): Column type
            java_type (str): Java type
            java_field (str): Java field
            is_pk (str): Is primary key (1 is yes)
            is_increment (str): Is auto-increment (1 is yes)
            is_required (str): Is required (1 is yes)
            is_insert (str): Is insert field (1 is yes)
            is_edit (str): Is edit field (1 is yes)
            is_list (str): Is list field (1 is yes)
            is_query (str): Is query field (1 is yes)
            query_type (str): Query type
            html_type (str): HTML type
            dict_type (str): Dictionary type
            sort (int): Sort order
        """
        self.column_id = column_id
        self.table_id = table_id
        self.column_name = column_name
        self.column_comment = column_comment
        self.column_type = column_type
        self.java_type = java_type
        self.java_field = java_field
        self.is_pk = is_pk
        self.is_increment = is_increment
        self.is_required = is_required
        self.is_insert = is_insert
        self.is_edit = is_edit
        self.is_list = is_list
        self.is_query = is_query
        self.query_type = query_type
        self.html_type = html_type
        self.dict_type = dict_type
        self.sort = sort

    def is_pk(self):
        return self.is_pk == "1"

    def is_increment(self):
        return self.is_increment == "1"

    def is_required(self):
        return self.is_required == "1"

    def is_insert(self):
        return self.is_insert == "1"

    def is_edit(self):
        return self.is_edit == "1"

    def is_list(self):
        return self.is_list == "1"

    def is_query(self):
        return self.is_query == "1"

    def get_cap_java_field(self):
        return self.java_field.capitalize()

    def is_super_column(self):
        return self.java_field.lower() in {
            "createBy",
            "createTime",
            "updateBy",
            "updateTime",
            "remark",
            "parentName",
            "parentId",
            "orderNum",
            "ancestors",
        }

    def is_usable_column(self):
        # Check if the column is usable based on a whitelist
        return self.java_field.lower() in {"parentId", "orderNum", "remark"}

    def read_converter_exp(self):
        # Assuming the column comment is in a format that contains remarks between parentheses
        import re

        remarks = re.search(r"（(.*?)）", self.column_comment)
        if remarks:
            remarks_text = remarks.group(1)
            parts = remarks_text.split(" ")
            return ",".join(f"{part[0]}={part[1:]}" for part in parts if part)
        return self.column_comment

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
