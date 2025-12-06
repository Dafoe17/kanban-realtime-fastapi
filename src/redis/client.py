from redis.asyncio import Redis
from src.core.config import settings


class RedisTools:
    redis_client: Redis | None = None

    @classmethod
    async def init_redis(cls):
        if cls.redis_client is None:
            cls.redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

    @classmethod
    async def ensure_initialized(cls):
        if cls.redis_client is None:
            await cls.init_redis()
        return cls.redis_client
