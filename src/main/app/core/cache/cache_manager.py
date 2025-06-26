"""Cache Client manager to instantiate the appropriate cache client"""

from src.main.app.core.cache.cache import Cache
from src.main.app.core.cache.redis_cache import RedisManager
from src.main.app.core.config.config_manager import load_config


async def get_cache_client() -> Cache:
    """Initialize and return the appropriate cache client based on configuration.

    Returns:
        Cache: Redis client if Redis is enabled in config, otherwise returns page cache.
    """

    config = load_config()
    if config.database.enable_redis:
        from src.main.app.core.cache.redis_cache import RedisCache

        redis_client = await RedisManager.get_instance()
        return RedisCache(redis_client)
    else:
        from src.main.app.core.cache.page_cache import PageCache

        return PageCache()
