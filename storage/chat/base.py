from abc import ABC, abstractmethod
from uuid import UUID


class AbstractChatStorage(ABC):
    def __init__(self, name):
        self.name = name

    """Abstract class to for user chat."""

    @abstractmethod
    async def load(self, user_id: UUID) -> str | None:
        """Load user chat history."""

    @abstractmethod
    async def save(self, user_id: UUID, message: str) -> None:
        """Save user message."""
