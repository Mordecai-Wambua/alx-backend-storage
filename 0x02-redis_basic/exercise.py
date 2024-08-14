#!/usr/bin/env python3
"""Cache class."""
import redis
import uuid
from typing import Union

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
