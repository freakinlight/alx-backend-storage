#!/usr/bin/env python3
"""
Cache class for interacting with Redis and retrieving values.
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.
        The data can be of type str, bytes, int, or float.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis
        return key  # Return the key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis by key and apply the callable fn if provided.
        If the key does not exist, return None.
        """
        data = self._redis.get(key)  # Get data from Redis
        if data is None:
            return None  # If the key does not exist, return None
        if fn:
            return fn(data)  # Apply the conversion function if provided
        return data  # Return raw data if no conversion function is provided

    def get_str(self, key: str) -> Optional[str]:
        """Automatically convert the retrieved data to a UTF-8 string."""
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Automatically convert the retrieved data to an integer."""
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    # Test cases as per the example
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)  # Store each test case value
        assert cache.get(key, fn=fn) == value  # Assert the retrieved value matches

