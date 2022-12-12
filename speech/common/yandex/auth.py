import time
from http import HTTPStatus
from typing import Optional

import jwt
from loguru import logger

from services.http_service import get_session
from speech.exceptions import YandexIAMException
from config import get_config

sr_cfg = get_config().sr


class IAMTokenIssuer:
    def __init__(self):
        self._service_account_id = sr_cfg.yandex_greta_service_account_id
        self._key_id = sr_cfg.yandex_greta_service_key_id
        self._private_key = sr_cfg.yandex_greta_service_private_key
        self._session = get_session()
        self._iam_token: Optional[str] = None
        self._iam_token_iat: Optional[int] = None
        self._token_refresh_frequency = sr_cfg.yandex_token_refresh_frequency

    async def get_token(self) -> str:
        """Return IAM-token.

        It will check if it is the time to refresh IAM-token.
        If the time has come it will refresh IAM-token.
        """
        if not self._iam_token or self._time_to_refresh_token():
            jwt_token = self._get_jwt_token()
            self._iam_token = await self._get_iam_token(jwt_token)
            self._iam_token_iat = time.time()

        return self._iam_token

    def _time_to_refresh_token(self) -> bool:
        """Return True if it is time to refresh iam token."""
        return time.time() - self._iam_token_iat > self._token_refresh_frequency

    def _get_jwt_token(self) -> str:
        """Generate JWT token for further exchange for IAM-token."""
        now = int(time.time())
        payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': self._service_account_id,
            'iat': now,
            'exp': now + 360,
        }

        encoded_token = jwt.encode(
            payload=payload,
            key=self._private_key,
            algorithm='PS256',
            headers={'kid': self._key_id}
        )
        return encoded_token

    async def _get_iam_token(self, jwt_token: str) -> str:
        """Return IAM-token."""
        async with self._session.post(
            url='https://iam.api.cloud.yandex.net/iam/v1/tokens',
            json={'jwt': jwt_token},
        ) as response:
            logger.debug(str(response))
            if response.status == HTTPStatus.OK:
                logger.debug('Received IAM token from Yandex.')
                token = await response.json()
                return token.get('iamToken')

            raise YandexIAMException(
                'Cannot get IAM from Yandex.',
                response.status,
            )
