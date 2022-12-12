"""Core module of the Voice Assistant.

This module assembles all components that are required to implement
voice assistant and provides interface to work with.
"""
import random
from functools import cache
from uuid import UUID

from pydantic import BaseModel
from pydub import AudioSegment

from movie_api.get_response import call_desire_api
from speech.recognition.speech_recognition import SpeechRecognitionService
from director.core import Director
from loguru import logger

from speech.synthesize.synthesize import SynthesizeService

cannot_recognize = [
    'Чё?',
    'Что ты промямлил?',
    'А? Повтори.',
    'Ну ты и чушь спросил, я даже отвечать не буду.',
    'Я прослушала, чё хотел?',
    'Спроси у своей Алисы.',
    'Слышь ты, Кожаный Мешок, я тебе, чёрт побери, не Алиса, чтобы прислуживать!',
]


class GretaResponse(BaseModel):
    user_text_message: str
    greta_text_message: str
    greta_audio_message: bytes


class Greta:
    """Voice Assistant."""

    def __init__(self):
        self._sr = SpeechRecognitionService('test')
        self._synthesize = SynthesizeService()
        self._director = Director()
        self._movie = call_desire_api

    async def process_user_audio_message(self, audio_data: bytes, user_id: UUID):
        recognized_text = await self._sr.recognize(audio_data)
        director_result = await self._director.action(user_id, recognized_text)
        logger.debug(f'{director_result=}, {type(director_result)}')
        if director_result:
            requested_info = await self._movie(director_result)
            logger.debug(f'{requested_info=}, {type(requested_info)}')
        else:
            requested_info = random.choice(cannot_recognize)
        synthesize_text = await self._synthesize.synthesize(requested_info)
        return GretaResponse(
            user_text_message=recognized_text,
            greta_text_message=requested_info,
            greta_audio_message=synthesize_text,
        )


@cache
def get_voice_assistant():
    return Greta()
