from abc import ABC, abstractmethod
from pydub import AudioSegment


class BaseSpeechRecognitionService(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def recognize(self, audio_data: AudioSegment, lang: str) -> str:
        """Return recognized text.
        :param audio_data: audio data.
        :param lang: recognition language
        :return: recognized text
        """
        ...
