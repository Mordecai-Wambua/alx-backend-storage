#!/usr/bin/env python3
"""Cache class."""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """class to interact with the redis server."""

    def __init__(self) -> None:
        """Instantiate the redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Input data into redis using the generated a random key."""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """Convert data to desired format."""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieve string values."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve integer values."""
        return self.get(key, int)
