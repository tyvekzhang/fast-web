"""Application Configuration."""

from src.main.app.core.config.database_config import DatabaseConfig
from src.main.app.core.config.security_config import SecurityConfig
from src.main.app.core.config.server_config import ServerConfig


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

    def __str__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            A string representation of the config instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
