from abc import ABC, abstractmethod
from pydub import AudioSegment


class BaseSynthesizeService(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def synthesize(self, text: str, lang: str) -> str:
        """Return synthesize text."""
        ...
