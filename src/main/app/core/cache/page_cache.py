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
"""Simple in-memory page cache implementation"""

from typing import Any

import diskcache

from src.main.app.core.cache.cache import Cache


class PageCache(Cache):
    def __init__(self):
        self.cache = diskcache.Cache()

    async def get(self, key: str) -> Any:
        """Retrieve a value by key from the in-memory cache."""
        return self.cache.get(key)

    async def set(self, key: str, value: Any, timeout: int = None) -> None:
        """Set the value for a key in the in-memory cache."""
        if timeout:
            self.cache.set(key, value, timeout)
        else:
            self.cache.set(key, value)

    async def delete(self, key: str) -> None:
        """Delete a key from the in-memory cache."""
        if key in self.cache:
            self.cache.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the in-memory cache."""
        if key in self.cache:
            return True
        return False
