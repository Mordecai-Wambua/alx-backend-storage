#!/usr/bin/env python3
"""Cache class."""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """System to count method calls."""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Make the actual counts then invoke called method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """System to get method parrameters and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        key = method.__qualname__
        inputs = key + ':inputs'
        outputs = key + ':outputs'

        self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
        """Display the history of calls of a particular function."""
        cache = method.__self__
        name = method.__qualname__
        print('{} was called {} times:'.format(name, cache.get(name)))

        inp_key = name + ':inputs'
        out_key = name + ':outputs'

        inp = [i.decode('utf-8') for i in cache._redis.lrange(inp_key, 0, -1)]
        out = [o.decode('utf-8') for o in cache._redis.lrange(out_key, 0, -1)]
        for i, o in zip(inp, out):
            print('{}(*{}) -> {}'.format(name, i, o))


class Cache:
    """class to interact with the redis server."""

    def __init__(self) -> None:
        """Instantiate the redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
