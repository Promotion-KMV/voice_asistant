from speech.synthesize.api.yandex import YandexSynthesizeService


class SynthesizeService:
    def __init__(self):
        self._yandex = YandexSynthesizeService()

    async def synthesize(self, text: str, lang: str = 'ru-RU') -> bytes:
        """Return synthesized text."""
        audio = await self._yandex.synthesize(text, lang)
        return audio
