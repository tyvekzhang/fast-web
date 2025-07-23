"""Application Configuration."""

from src.main.app.core.config.database_config import DatabaseConfig
from src.main.app.core.config.security_config import SecurityConfig
from src.main.app.core.config.server_config import ServerConfig


class GenConfig:
    def __init__(
        self,
        author: str = "admin",
        package_name: str = "com.singularity.modules.reading",
        auto_remove_pre: bool = False,
        table_prefix: str = "read",
    ) -> None:
        """
        Initializes the generator configuration with default values.

        Args:
            author (str): The author of the generated code. Default is ''.
            package_name (str): The base package name for generated code. Default is ''.
            auto_remove_pre (bool): Whether to automatically remove table prefixes. Default is False.
            table_prefix (str): The prefix to remove from table names. Default is ''.
        """
        self.author = author
        self.package_name = package_name
        self.auto_remove_pre = auto_remove_pre
        self.table_prefix = table_prefix

    def __repr__(self) -> str:
        """
        Returns a string representation of the generator configuration.

        Returns:
            str: A string representation of the GenConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class Config:
    def __init__(self, config_dict=None):
        if "server" in config_dict:
            self.server = ServerConfig(**config_dict["server"])
        else:
            self.server = ServerConfig()
        if "database" in config_dict:
            self.database = DatabaseConfig(**config_dict["database"])
        else:
            self.database = DatabaseConfig()
        if "security" in config_dict:
            self.security = SecurityConfig(**config_dict["security"])
        else:
            self.security = SecurityConfig()
        if "gen" in config_dict:
            self.gen = GenConfig(**config_dict["gen"])
        else:
            self.gen = GenConfig()

    def __str__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            A string representation of the config instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
