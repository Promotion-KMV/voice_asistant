import json
from .base import BaseSpeechRecognitionService
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from config import VOSK_MODEL_RU
from loguru import logger


class OfflineSR(BaseSpeechRecognitionService):
    """Class for offline text recognition.

    This class should be used as a backoff
    if all external APIs are unavailable.
    """

    def __init__(self):
        super().__init__('vosk')
        self._recognizer = sr.Recognizer()

    async def recognize(self, audio_segment: AudioSegment, lang: str) -> str:
        """Return recognized text.
        :param audio_segment: audio data.
        :param lang: recognition language
        :return: recognized text
        """
        model = Model(model_path=VOSK_MODEL_RU.as_posix())
        rec = KaldiRecognizer(model, audio_segment.frame_rate)
        rec.AcceptWaveform(audio_segment.raw_data)
        text = json.loads(rec.Result())['text']
        logger.debug(f'User says: "{text}"')
        return text
