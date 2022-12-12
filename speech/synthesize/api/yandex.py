"""Module for yandex voice recognition API."""
from http import HTTPStatus
from io import BytesIO

from loguru import logger
from pydub import AudioSegment

from services.http_service import get_session
from speech.synthesize.api.base import BaseSynthesizeService
from speech.common.yandex.auth import IAMTokenIssuer


class YandexSynthesizeService(BaseSynthesizeService):
    """Class implements Yandex Speechkit API.

    It is a synchronous recognition API.
    """

    def __init__(self):
        super().__init__('yandex')
        self._session = get_session()
        self._iam_token_issuer = IAMTokenIssuer()

    async def synthesize(self, text: str, lang: str) -> bytes:
        """Return synthesize audio data."""
        data = {
            'text': text,
            'lang': lang,
            'voice': 'omazh',
            'emotion': 'evil',
            'format': 'lpcm',
            'sampleRateHertz': 48000,
        }
        iam_token = await self._iam_token_issuer.get_token()
        async with self._session.post(
            url=f'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
            data=data,
            headers={'Authorization': f'Bearer {iam_token}'},
        ) as response:
            logger.debug(f'Got response from yandex synthesize api.\n {response.status}')
            audio_data = BytesIO()
            async for chunk, _ in response.content.iter_chunks():
                audio_data.write(chunk)
            audio_data.seek(0)
            audio_segment = AudioSegment.from_raw(
                audio_data,
                sample_width=2,
                frame_rate=48000,
                channels=1,
            )
            out_put_audio_data = BytesIO()
            audio_segment.export(out_put_audio_data, format='wav')
        return out_put_audio_data.read()
