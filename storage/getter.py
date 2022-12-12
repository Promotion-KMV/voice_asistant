from functools import cache

from storage.chat.base import AbstractChatStorage
from storage.chat.ch import ClickHouse
from storage.core import AbstractStorage
from storage.impl.redis.storage import RedisStorage


@cache
def get_storage() -> AbstractStorage:
    return RedisStorage()


@cache
def get_chat_storage() -> AbstractChatStorage:
    return ClickHouse()
