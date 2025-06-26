"""Redis cache implementation"""

from typing import Any

from src.main.app.core.cache.cache import Cache
import asyncio
from typing import Optional

import redis.asyncio as redis

from src.main.app.core.config.config_manager import load_config


class RedisCache(Cache):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def get(self, key: str) -> Any:
        """Retrieve a value by key from Redis."""
        return await self.redis_client.get(key)

    async def set(self, key: str, value: Any, timeout=None):
        """Set the value of a key in Redis with timeout."""
        if timeout:
            await self.redis_client.setex(key, timeout, value)
        else:
            await self.redis_client.set(key, value)

    async def delete(self, key: str):
        """Delete a key from Redis."""
        return await self.redis_client.delete(key)

    async def exists(self, key: str):
        """Check if a key exists in Redis."""
        return await self.redis_client.exists(key)


class RedisManager:
    _instance: Optional[redis.Redis] = None
    _connection_pool: Optional[redis.ConnectionPool] = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls) -> redis.Redis:
        """
        Get redis instance
        """
        if cls._instance is None:
            async with cls._lock:
                if cls._connection_pool is None:
                    database = load_config().database
                    cls._connection_pool = redis.ConnectionPool.from_url(
                        f"redis://:{database.cache_pass}@{database.cache_host}:{database.cache_port}/{database.db_num}",
                        decode_responses=True,
                    )
                if cls._instance is None:
                    cls._instance = await redis.Redis.from_pool(
                        cls._connection_pool
                    )
        return cls._instance
