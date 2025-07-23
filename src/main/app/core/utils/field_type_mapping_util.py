from typing import Dict

# Mysql field type mapping to python
# References: https://dev.mysql.com/doc/refman/8.0/en/numeric-types.html
MYSQL_TO_PYTHON_TYPE_MAP: Dict[str, str] = {
    "tinyint": "int",
    "smallint": "int",
    "mediumint": "int",
    "int": "int",
    "integer": "int",
    "bigint": "int",
    "float": "float",
    "double": "float",
    "decimal": "Decimal",
    "numeric": "Decimal",
    "bit": "bool",
    "year": "int",
    "date": "date",
    "time": "time",
    "datetime": "datetime",
    "timestamp": "datetime",
    "char": "str",
    "varchar": "str",
    "tinytext": "str",
    "text": "str",
    "mediumtext": "str",
    "longtext": "str",
    "tinyblob": "bytes",
    "blob": "bytes",
    "mediumblob": "bytes",
    "longblob": "bytes",
    "enum": "str",
    "set": "str",
    "json": "dict",
    "point": "Point",
    "linestring": "LineString",
    "polygon": "Polygon",
    "multipoint": "MultiPoint",
    "multilinestring": "MultiLineString",
    "multipolygon": "MultiPolygon",
    "geometrycollection": "GeometryCollection",
}


def mysql_map2server_type(field_type: str) -> str:
    return MYSQL_TO_PYTHON_TYPE_MAP.get(field_type.lower(), "Any")


# Mysql field type mapping to sqlmodel
# Reference: https://github.com/sqlalchemy/sqlalchemy/blob/main/lib/sqlalchemy/sql/sqltypes.py
MYSQL_TO_SQLMODEL_TYPE_MAP = {
    "tinyint": "Boolean",
    "smallint": "SmallInteger",
    "mediumint": "Integer",
    "int": "Integer",
    "integer": "Integer",
    "bigint": "BigInteger",
    "decimal": "Numeric",
    "numeric": "Numeric",
    "float": "Float",
    "double": "Double",
    "real": "Float",
    "char": "String",
    "varchar": "String",
    "tinytext": "String",
    "text": "String",
    "mediumtext": "String",
    "longtext": "String",
    "enum": "String",
    "set": "String",
    "date": "Date",
    "datetime": "DateTime",
    "timestamp": "DateTime",
    "time": "Time",
    "binary": "LargeBinary",
    "varbinary": "LargeBinary",
    "tinyblob": "LargeBinary",
    "blob": "LargeBinary",
    "mediumblob": "LargeBinary",
    "longblob": "LargeBinary",
    "json": "JSON",
    "year": "Integer",
}


def mysql_map2sqlmodel_type(field_type: str) -> str:
    field_type = field_type.lower()
    return MYSQL_TO_SQLMODEL_TYPE_MAP.get(field_type, "String")


# SQLModel field type mapping to MySQL
# Reference: https://github.com/sqlalchemy/sqlalchemy/blob/main/lib/sqlalchemy/sql/sqltypes.py
SQLMODEL_TO_MYSQL_TYPE_MAP = {
    "TINYINT": "tinyint",
    "BOOLEAN": "tinyint",
    "SMALLINTEGER": "smallint",
    "INTEGER": "int",
    "BIGINTEGER": "bigint",
    "BIGINT": "bigint",
    "NUMERIC": "decimal",
    "FLOAT": "float",
    "DOUBLE": "double",
    "STRING": "varchar",
    "DATE": "date",
    "DATETIME": "datetime",
    "TIME": "time",
    "LARGEBINARY": "blob",
    "JSON": "json",
}


def sqlmodel_map_to_mysql_type(sqlmodel_type: str) -> str:
    sqlmodel_type = sqlmodel_type.upper()
    return SQLMODEL_TO_MYSQL_TYPE_MAP.get(sqlmodel_type, "varchar")


SQLMODEL_TO_PGSQL_TYPE_MAP = {
    "BOOLEAN": "bool",
    "SMALLINTEGER": "int2",
    "SMALLINT": "int2",
    "INTEGER": "int4",
    "BIGINTEGER": "int8",
    "BIGINT": "int8",
    "NUMERIC": "numeric",
    "FLOAT": "float8",
    "DOUBLE": "float4",
    "STRING": "varchar",
    "TEXT": "text",
    "DATE": "date",
    "DATETIME": "timestamp",
    "TIMESTAMP": "timestamp",
    "TIME": "time",
    "LARGEBINARY": "bytea",
    "JSON": "jsonb",
    "VECTOR": "vector",
}


def sqlmodel_map_to_pgsql_type(sqlmodel_type: str) -> str:
    sqlmodel_type = sqlmodel_type.upper()
    return SQLMODEL_TO_PGSQL_TYPE_MAP.get(sqlmodel_type, "varchar")


SQL_TO_SQLMODEL_TYPE_MAP = {
    "tinyint": "Boolean",
    "smallint": "SmallInteger",
    "mediumint": "Integer",
    "int": "Integer",
    "integer": "Integer",
    "bigint": "BigInteger",
    "decimal": "Numeric",
    "numeric": "Numeric",
    "float": "Float",
    "double": "Double",
    "real": "Float",
    "char": "String",
    "varchar": "String",
    "tinytext": "String",
    "text": "String",
    "mediumtext": "String",
    "longtext": "String",
    "enum": "String",
    "set": "String",
    "date": "Date",
    "datetime": "DateTime",
    "timestamp": "DateTime",
    "time": "Time",
    "binary": "LargeBinary",
    "varbinary": "LargeBinary",
    "tinyblob": "LargeBinary",
    "blob": "LargeBinary",
    "mediumblob": "LargeBinary",
    "longblob": "LargeBinary",
    "json": "JSON",
    "year": "Integer",
    "bool": "BOOLEAN",
    "int2": "SMALLINTEGER",
    "int4": "INTEGER",
    "int8": "BIGINTEGER",
    "float8": "FLOAT",
    "float4": "DOUBLE",
    "bytea": "LARGEBINARY",
    "jsonb": "JSON",
    "vector": "Vector",
}


def sql_map2sqlmodel_type(field_type: str) -> str:
    field_type = field_type.lower()
    return SQL_TO_SQLMODEL_TYPE_MAP.get(field_type, "String")
