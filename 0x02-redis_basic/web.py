#!/usr/bin/env python3
"""Module for request caching and tracking."""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""The module-level Redis instance."""


def create_cache(method: Callable) -> Callable:
    """Caches the output of fetched data."""
    @wraps(method)
    def initialize(url) -> str:
        """The wrapper function for caching the output."""
        redis_store.incr(f"count:{url}")
        response = redis_store.get(f"result:{url}")
        if response:
            return response.decode("utf-8")
        response = method(url)
        redis_store.setex(f"result:{url}", 10, response)
        return response
    return initialize


@create_cache
def get_page(url: str) -> str:
    """
    Returns the URL content after caching the response,
    and tracking the request.
    """
    return requests.get(url).text