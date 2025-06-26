"""Provides a unified cache client based on configuration."""

from .cache_manager import get_cache_client

__all__ = [
    get_cache_client,
]
