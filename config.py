"""Main configuration module of the app."""
import os
from functools import cache
from pathlib import Path
from loguru import logger
from pydantic import BaseModel, BaseSettings, Field

PROJECT_DIR = Path(__file__).parent
STATIC_FILES_DIR = PROJECT_DIR / 'static'
ENV_FILE_NAME = PROJECT_DIR / '.env'
ENV_EXAMPLE_FILE_NAME = PROJECT_DIR / '.env-example'
VOSK_MODEL_RU = PROJECT_DIR / 'speech' / 'recognition' / 'vosk-model-small-ru-0.22'

if VOSK_MODEL_RU.exists():
    pass
else:
    import requests, zipfile, io

    logger.info('Cannot find local model for speech recognition, downloading...')
    try:
        r = requests.get('https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip')
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(VOSK_MODEL_RU.parent)
        logger.info('SR model has been downloaded!')
    except:
        logger.error('Cannot download model for offline speech recognition.')
        pass


class ServiceConfig(BaseModel):
    """Common service settings."""

    host: str
    port: int

    @property
    def url(self):
        """Return http connection string."""
        return f'http://{self.host}:{self.port}'


class RedisConfig(ServiceConfig):
    """Redis config"""
    context_expires_seconds: int = 30


class MoviesConfig(ServiceConfig):
    """Movies service settings."""

    ...


class SpeechRecognitionSettings(BaseSettings):
    """Yandex Voice Recognition settings."""

    yandex_greta_service_pub_key: str = 'default'
    yandex_greta_service_private_key: str = 'default'
    yandex_greta_service_key_id: str
    yandex_greta_service_account_id: str
    yandex_greta_service_folder_id: str
    yandex_token_refresh_frequency: int = 60 * 60

    class Config:
        env_file = ENV_EXAMPLE_FILE_NAME, ENV_FILE_NAME
        env_nested_delimiter = '__'
        case_sensitive = False
        secrets_dir = PROJECT_DIR / 'secrets'


class MovieSettings(BaseSettings):
    url_film = f'http://fast_api:8001/api/v1/films/voiceassistant/search?query=%s'
    url_person = 'http://fast_api:8001/api/v1/persons/voiceassistant/search?query==%s'
    empty_message = "По вашему запросу нет данных"
    not_connection = "Ошибка подключения к базе фильмов"
    lst_genre = ['драма', 'комедия', 'вестерн', 'боевик', 'аниме']


class AppSettings(BaseSettings):
    """App settings."""

    movies: MoviesConfig
    redis: RedisConfig

    host: str
    port: int
    MAJOR_VERSION: int = 1
    MINOR_VERSION: int = 0
    PATCH_VERSION: int = 0
    ENV: str = 'production'

    sr = SpeechRecognitionSettings()
    mv = MovieSettings()

    @property
    def version(self):
        """Return version of the app."""
        return f'v{self.MAJOR_VERSION}.{self.MINOR_VERSION}.{self.PATCH_VERSION}'

    class Config:
        env_file = ENV_EXAMPLE_FILE_NAME, ENV_FILE_NAME
        env_nested_delimiter = '__'
        case_sensitive = False


@cache
def get_config():
    return AppSettings()
