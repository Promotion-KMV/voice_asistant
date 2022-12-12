"""Module for ClickHouse database."""
from uuid import UUID

from storage.chat.base import AbstractChatStorage


class ClickHouse(AbstractChatStorage):
    def __init__(self):
        super().__init__('clickhouse')

    async def load(self, user_id: UUID) -> str | None:
        pass

    async def save(self, user_id: UUID, message: str) -> None:
        pass
