"""Module for yandex voice recognition API."""
from http import HTTPStatus
from io import BytesIO

from loguru import logger
from pydub import AudioSegment

from speech.exceptions import YandexSpeechRecognitionException
from services.http_service import get_session
from speech.recognition.api.base import BaseSpeechRecognitionService
from speech.common.yandex.auth import IAMTokenIssuer


class YandexSR(BaseSpeechRecognitionService):
    """Class implements Yandex Speechkit API.

    It is a synchronous recognition API.
    """

    def __init__(self):
        super().__init__('yandex')
        self._session = get_session()
        self._iam_token_issuer = IAMTokenIssuer()

    async def recognize(self, audio_segment: AudioSegment, lang: str) -> str:
        """Return recognized text.
        :param audio_segment: audio data.
        :param lang: recognition language
        :return: recognized text
        """
        audio_data_ogg = self._convert_to_ogg(audio_segment)
        iam_token = await self._iam_token_issuer.get_token()
        async with self._session.post(
            url=f'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize',
            data=audio_data_ogg,
            params={'topic': 'general', 'lang': lang},
            headers={'Authorization': f'Bearer {iam_token}'},
        ) as response:
            result: dict = await response.json()
            if response.status == HTTPStatus.OK:
                logger.debug('Got recognition result from yandex.')
                logger.debug(result)
                return result.get('result')
            raise YandexSpeechRecognitionException(
                result.get('error_message', 'Bad response from yandex recognize.'),
                response.status,
            )

    @staticmethod
    def _convert_to_ogg(audio_segment: AudioSegment) -> bytes:
        """Convert audio segment to ogg format.

        Convert audio to ogg format with opus codec and
        return raw data.
        """
        output_audio_data = BytesIO()
        audio_segment.export(output_audio_data, format='ogg', codec='opus', parameters=['-strict', '-2'])

        return output_audio_data.read()
