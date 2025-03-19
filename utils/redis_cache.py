import json
from typing import Any, Optional
import redis.asyncio as redis


class RedisCacheFactory:
    def __init__(self, redis_url: str = "redis://localhost:6379", db: int = 0):
        """
        Initializes the Redis cache factory.

        :param redis_url: The URL of the Redis server (default: "redis://localhost:6379").
        :param db: The Redis database index (default: 0).
        """
        self.redis_url = redis_url
        self.db = db
        self._redis_client: Optional[redis.Redis] = None

    async def _get_client(self, decode_responses: bool = True) -> redis.Redis:
        """
        Lazily initializes and returns the Redis client.
        """
        if self._redis_client is None:
            self._redis_client = redis.from_url(
                self.redis_url, db=self.db, decode_responses=decode_responses
            )
        return self._redis_client

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Stores a value in Redis with an optional TTL.

        :param key: The cache key.
        :param value: The value to store.
        :param ttl: Time-to-live in seconds (default: 3600).
        """
        client = await self._get_client()
        try:
            dump_value = json.dumps(value)
            await client.set(key, dump_value, ex=ttl)
        except redis.RedisError as e:
            print(f"Redis set error: {e}")

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a value from Redis.

        :param key: The cache key.
        :return: The deserialized value, or None if the key does not exist.
        """
        client = await self._get_client()
        try:
            data = await client.get(key)
            return json.loads(data) if data else None
        except redis.RedisError as e:
            print(f"Redis get error: {e}")
            return None

    async def exists(self, key: str) -> bool:
        """
        Checks if a key exists in Redis.

        :param key: The key to check.
        :return: True if the key exists, otherwise False.
        """
        client = await self._get_client()
        try:
            return bool(await client.exists(key))
        except redis.RedisError as e:
            print(f"Redis exists error: {e}")
            return False

    async def delete(self, *keys: str) -> None:
        """
        Deletes specified keys from Redis.

        :param keys: The keys to delete.
        """
        if not keys:
            return  # Avoid unnecessary Redis calls if no keys are provided
        client = await self._get_client()
        try:
            await client.delete(*keys)
        except redis.RedisError as e:
            print(f"Redis delete error: {e}")

    async def close(self) -> None:
        """
        Closes the Redis connection.
        """
        if self._redis_client:
            await self._redis_client.aclose()
            self._redis_client = None
