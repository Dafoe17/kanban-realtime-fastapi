import asyncio

from .client import RedisTools


class WSConnectionStorage:

    @classmethod
    async def add_connection(cls, user_id: str, board_id: str, connection_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.sadd(f"ws:user:{user_id}", connection_id)
        await redis.sadd(f"ws:board:{board_id}", connection_id)

    @classmethod
    async def remove_connection(cls, user_id: str, board_id: str, connection_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.srem(f"ws:user:{user_id}", connection_id)
        await redis.srem(f"ws:board:{board_id}", connection_id)

    @classmethod
    async def remove_from_board(cls, board_id: str, connection_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.srem(f"ws:board:{board_id}", connection_id)

    @classmethod
    async def get_board_connections(cls, board_id: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        return await redis.smembers(f"ws:board:{board_id}")


class RedisBroadcaster:

    def __init__(self):
        self.tasks = {}

    async def sub_board(self, board_id: str, callback):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"board:{board_id}")

        async def reader():
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    await callback(msg["data"])

        task = asyncio.create_task(reader())
        self.tasks[board_id] = task

    async def pub_board(self, board_id: str, message: str):
        redis = await RedisTools.ensure_initialized()
        assert redis is not None
        await redis.publish(f"board:{board_id}", message)
