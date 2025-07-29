# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
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
