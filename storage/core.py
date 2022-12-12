from abc import ABC, abstractmethod
from uuid import UUID

from storage.models import Context


class AbstractStorage(ABC):
    """Describes local storage logic structure"""

    @abstractmethod
    async def get_context(self, user_id: UUID) -> Context | None:
        """Returns saved context from previous user request"""

    @abstractmethod
    async def set_context(self, user_id: UUID, context: Context) -> None:
        """Set or update user's request context"""
