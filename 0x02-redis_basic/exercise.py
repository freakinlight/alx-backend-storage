#!/usr/bin/env python3
"""
Cache class for interacting with Redis.
"""
import redis
import uuid
from typing import Union


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


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"  # Example data
    key = cache.store(data)  # Store data in Redis and get the key
    print(key)

    local_redis = redis.Redis()  # Create a Redis client instance to fetch data
    print(local_redis.get(key))  # Retrieve the data using the key
