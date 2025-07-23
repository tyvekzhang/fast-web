class GenConstants:
    """Constants for code generation."""

    # Template types
    TPL_CRUD = "crud"
    TPL_TREE = "tree"
    TPL_SUB = "sub"

    # Tree-related fields
    TREE_CODE = "treeCode"
    TREE_PARENT_CODE = "treeParentCode"
    TREE_NAME = "treeName"

    # Menu-related fields
    PARENT_MENU_ID = "parentMenuId"
    PARENT_MENU_NAME = "parentMenuName"

    # Database column types
    COLUMNTYPE_STR = ["char", "varchar", "nvarchar", "varchar2"]
    COLUMNTYPE_TEXT = ["tinytext", "text", "mediumtext", "longtext"]
    COLUMNTYPE_TIME = ["datetime", "time", "date", "timestamp"]
    COLUMNTYPE_NUMBER = [
        "tinyint",
        "smallint",
        "mediumint",
        "int",
        "number",
        "integer",
        "bit",
        "bigint",
        "float",
        "double",
        "decimal",
        "int2",
        "int4",
        "int8",
    ]

    # Page settings for fields
    COLUMNNAME_NOT_INSERT = [
        "id",
        "create_by",
        "create_time",
        "del_flag",
        "update_by",
        "update_time",
        "user_id",
        "tenant_id",
    ]
    COLUMNNAME_NOT_MODIFY = [
        "create_by",
        "create_time",
        "del_flag",
        "update_by",
        "update_time",
        "user_id",
        "tenant_id",
    ]
    COLUMNNAME_NOT_BATCH_MODIFY = [
        "id",
        "create_by",
        "create_time",
        "del_flag",
        "update_by",
        "update_time",
        "user_id",
        "tenant_id",
    ]
    COLUMNNAME_NOT_PAGE = [
        "create_by",
        "del_flag",
        "update_by",
        "update_time",
        "user_id",
        "tenant_id",
    ]
    COLUMNNAME_NOT_QUERY = [
        "create_by",
        "del_flag",
        "update_by",
        "update_time",
        "comment",
        "user_id",
        "tenant_id",
    ]

    # Base entity fields
    BASE_ENTITY = [
        "createBy",
        "createTime",
        "updateBy",
        "updateTime",
        "comment",
    ]
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors"]

    # HTML input types
    HTML_INPUT = "input"
    HTML_TEXTAREA = "textarea"
    HTML_SELECT = "select"
    HTML_RADIO = "radio"
    HTML_CHECKBOX = "checkbox"
    HTML_DATETIME = "datetime"
    HTML_DATEPICKER = "datepicker"
    HTML_IMAGE_UPLOAD = "imageUpload"
    HTML_FILE_UPLOAD = "fileUpload"
    HTML_MODIFYOR = "editor"

    # Data types
    TYPE_STRING = "String"
    TYPE_PY_STRING = "str"
    TYPE_JS_STRING = "string"
    TYPE_JS_NUMBER = "number"
    TYPE_JS_BIGINT = "bigint"
    TYPE_JS_BOOLEAN = "boolean"
    TYPE_INTEGER = "Integer"
    TYPE_PY_INTEGER = "int"
    TYPE_VECTOR = "vector"
    TYPE_LONG = "Long"
    TYPE_DOUBLE = "Double"
    TYPE_BIGDECIMAL = "BigDecimal"
    TYPE_PY_DECIMAL = "Decimal"
    TYPE_DATE = "Date"
    TYPE_LOCALDATETIME = "LocalDateTime"
    TYPE_PY_DATETIME = "datetime"

    # Query types
    QUERY_LIKE = "LIKE"
    QUERY_EQ = "EQ"

    # Requirement flag
    REQUIRE = "1"

    JAVA = "java"
    PYTHON = "python"
    MYBATIS = "mybatis"
