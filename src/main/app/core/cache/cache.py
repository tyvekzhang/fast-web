"""Abstract base class for Cache"""

from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        """Retrieve a value by key from the cache."""

        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: Any, timeout=None) -> None:
        """Set the value of a key in the cache with an optional timeout."""

        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a key from the cache."""

        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""

        raise NotImplementedError
