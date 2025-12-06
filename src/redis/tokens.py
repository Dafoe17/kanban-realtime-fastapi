from src.core.config import settings

from .client import RedisTools


class TokenStorage:

    @classmethod
    async def add_token(cls, user_id: str, token: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.set(
            f"refresh:user:{user_id}",
            token,
            ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        )

    @classmethod
    async def delete_token(cls, user_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.delete(f"refresh:user:{user_id}")

    @classmethod
    async def get_token(cls, user_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        return redis.get(f"refresh:user:{user_id}")
