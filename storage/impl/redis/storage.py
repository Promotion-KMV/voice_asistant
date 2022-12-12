from uuid import UUID

import aioredis as aioredis
import orjson
from aioredis import Redis

from config import get_config
from storage.core import AbstractStorage
from storage.models import Context

config = get_config()


class RedisStorage(AbstractStorage):
    async def get_context(self, user_id: UUID) -> Context | None:
        value = await self.connector.get(name=str(user_id))
        if value:
            return Context(**orjson.loads(value))

    async def set_context(self, user_id: UUID, context: Context) -> None:
        await self.connector.set(
            name=str(user_id),
            value=context.json(),
            ex=config.redis.context_expires_seconds
        )

    def __init__(self):
        self.connector: Redis = aioredis.Redis(
            host=config.redis.host,
            port=config.redis.port
        )

