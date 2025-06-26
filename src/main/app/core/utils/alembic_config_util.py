# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Alembic configuration parser"""

import configparser
import os.path
from typing import NamedTuple
from urllib.parse import urlparse

from src.main.app.core.enums.enum import DBTypeEnum
from src.main.app.core.utils import file_util
from src.main.app.core.utils.file_util import get_file_path


class DbConnectionInfo(NamedTuple):
    """Container for parsed database connection information.

    Attributes:
        driver: Database driver (e.g., 'postgresql', 'mysql').
        username: Database username.
        password: Database password.
        host: Database host address.
        port: Database port number.
        dbname: Database name.
        full_url: Original full connection URL (with password masked for safety).
    """

    driver: str
    username: str
    password: str
    host: str
    port: str
    dbname: str
    full_url: str


def get_alembic_db_info(
    config_path: str,
) -> DbConnectionInfo:
    """Extracts and parses the SQLAlchemy URL from alembic.ini.

    Args:
        config_path: Path to the alembic.ini file.

    Returns:
        DbConnectionInfo: Named tuple containing parsed connection details.

    Raises:
        FileNotFoundError: If the specified config file doesn't exist.
        KeyError: If the sqlalchemy.url key is missing in the config.
        ValueError: If the URL parsing fails.
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    if not config.has_option("alembic", "sqlalchemy.url"):
        raise KeyError("sqlalchemy.url not found in alembic.ini")

    raw_url = config.get("alembic", "sqlalchemy.url")
    parsed = urlparse(raw_url)

    if not all([parsed.scheme, parsed.path]):
        raise ValueError(f"Invalid database URL format: {raw_url}")

    # Extract components
    driver = parsed.scheme
    username = parsed.username or ""
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = str(parsed.port) if parsed.port else ""
    dbname = parsed.path.lstrip("/")

    return DbConnectionInfo(
        driver=driver,
        username=username,
        password=password,
        host=host,
        port=port,
        dbname=dbname,
        full_url=raw_url.strip(),
    )


def get_db_url() -> str:
    """Get the database connection URL from alembic.ini configuration."""
    return get_alembic_db_info(file_util.get_file_path("alembic.ini")).full_url


def get_sqlite_db_path() -> str:
    """Get the absolute filesystem path for a SQLite database from the configured DB URL."""
    db_url = get_db_url()
    if db_url.strip() == "":
        raise ValueError("Invalid database URL")
    db_name = db_url.split(os.sep)[-1]
    return get_file_path(db_name)


def get_db_dialect() -> str:
    """Get the database type from the configured SQLAlchemy URL in alembic.ini."""
    db_url = get_db_url()

    try:
        scheme = db_url.split("://")[0].split("+")[0].lower()
    except (IndexError, AttributeError):
        raise ValueError(f"Malformed database URL: {db_url}")

    supported_dbs = {
        DBTypeEnum.PGSQL.value,
        DBTypeEnum.MYSQL.value,
        DBTypeEnum.SQLITE.value,
    }

    if scheme not in supported_dbs:
        raise RuntimeError(
            f"Unsupported database type: {scheme}. Supported types: {sorted(supported_dbs)}"
        )

    return scheme
