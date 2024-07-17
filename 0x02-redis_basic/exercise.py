#!/usr/bin/env python3
"""Module for  Redis NoSQL data storage."""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class."""
    @wraps(method)
    def method_caller(self, *args, **kwargs) -> Any:
        """
        Calls the given method after incrementing its call counter.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return method_caller


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class."""
    @wraps(method)
    def archive(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its inputs and output.
        """
        input = '{}:inputs'.format(method.__qualname__)
        output = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output, result)
        return result
    return archive


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method."""
    if fn is None or not hasattr(fn, '__self__'):
        return
    store = getattr(fn.__self__, '_redis', None)
    if not isinstance(store, redis.Redis):
        return
    method_name = fn.__qualname__
    key_input = '{}:inputs'.format(method_name)
    key_output = '{}:outputs'.format(method_name)
    call_count = 0
    if store.exists(method_name) != 0:
        call_count = int(store.get(method_name))
    print('{} was called {} times:'.format(method_name, call_count))
    input_fns = store.lrange(key_input, 0, -1)
    output_fns = store.lrange(key_output, 0, -1)
    for input_method, output_method in zip(input_fns, output_fns):
        print('{}(*{}) -> {}'.format(
            method_name,
            input_method.decode("utf-8"),
            output_method,
        ))


class Cache:
    """
    Represents an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in a Redis data storage & returns it's key.
        """
        item_key = str(uuid.uuid4())
        self._redis.set(item_key, data)
        return item_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves data from a Redis storage."""
        result = self._redis.get(key)
        return fn(result) if fn is not None else result

    def get_str(self, key: str) -> str:
        """Retrieves data in string format from a Redis storage."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves data in integer format from a Redis data storage."""
        return self.get(key, lambda x: int(x))