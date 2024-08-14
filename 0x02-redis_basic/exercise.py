#!/usr/bin/env python3
"""Cache class."""
import redis
import uuid


class Cache:
    """class to interact with the redis server."""

    def __init__(self) -> None:
        """Instantiate the redis client."""
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: any) -> str:
        """Input data into redis using the generated a random key."""
        key: str = str(uuid.uuid4())
        self.__redis.set(key, data)
        return key
