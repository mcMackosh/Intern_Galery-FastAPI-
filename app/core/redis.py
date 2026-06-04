from typing import cast

from redis.asyncio import Redis
from app.core.config import settings

REFRESH_TTL = 60 * 60 * 48  # 2 дні в секундах

class RedisService:
    def __init__(self):
        self._client: Redis | None = None

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RuntimeError("Redis is not connected")
        return self._client

    async def connect(self):
        self._client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER or None,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
        )

    async def close(self):
        if self._client:
            await self._client.aclose()

    async def set_refresh_token(self, user_id: str, token: str) -> None:
        await self.client.setex(f"refresh:{user_id}", REFRESH_TTL, token)

    async def get_refresh_token(self, user_id: str) -> str | None:
        return cast(str | None, await self.client.get(f"refresh:{user_id}"))

    async def remove_refresh_token(self, user_id: str) -> bool:
        deleted = await self.client.delete(f"refresh:{user_id}")
        return bool(deleted)


redis_service = RedisService()