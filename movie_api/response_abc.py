from services.http_service import get_session
from config import get_config
from loguru import logger
from aiohttp import ClientConnectorError

settings = get_config().mv


class ResponseABC:
    def __init__(self, url: str):
        self.url = url
        self.session = get_session()

    async def get_response(self) -> dict | str:
        try:
            async with self.session.get(self.url) as response:
                response_message = await response.json()
                return response_message
        except ClientConnectorError:
            return settings.not_connection
        except Exception as ex:
            logger.error(f"Непредвиденная ошибка - {ex}")
            raise Exception(f"Непредвиденная ошибка {ex}")
