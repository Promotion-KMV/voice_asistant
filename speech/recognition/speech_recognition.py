"""Module for speech recognition."""
from functools import cache

from pydub import AudioSegment

from speech.exceptions import SpeechRecognitionException
from speech.recognition.api.base import BaseSpeechRecognitionService
from speech.recognition.api.offline import OfflineSR
from speech.recognition.api.yandex import YandexSR
from loguru import logger
from io import BytesIO

available_apis = {
    'yandex': YandexSR,
}


class SpeechRecognitionService:
    """This class provides an interface to speech recognition.

    It uses external speech recognition api by default. You can implement your own
    api and add it to available_apis and pass it to init as default. It uses offline
    speech recognition service if any of external services are unavailable.
    """

    def __init__(self, speech_recognition_service: str = None):
        self._recognition_api: BaseSpeechRecognitionService = available_apis.get(speech_recognition_service,
                                                                                 OfflineSR)()
        self._offline = OfflineSR()

    async def recognize(self, audio_data: bytes, lang: str = 'ru-RU') -> str:
        """Return recognized text."""
        audio_segment = self._create_audio_segment(audio_data)
        try:
            recognized_text = await self._recognition_api.recognize(audio_segment, lang)
        except SpeechRecognitionException as e:
            logger.error(f'Got error from {self._recognition_api.name} api: {e}. Using offline speech recognition.')
            recognized_text = await self._offline.recognize(audio_segment, lang)
        return recognized_text

    @staticmethod
    def _create_audio_segment(raw_audio_data: bytes) -> AudioSegment:
        """Create audio segment from incoming audio data.

        Create default audio object to work with across the application.
        """
        input_audio_data = BytesIO(raw_audio_data)
        output_audio_data = BytesIO()
        audio_segment = AudioSegment.from_file(input_audio_data)
        audio_segment.export(output_audio_data, format='wav',
                             parameters=["-ac", "1", "-ar", "44100"])
        return AudioSegment.from_wav(output_audio_data)


@cache
def get_speech_recognition_service():
    return SpeechRecognitionService()
