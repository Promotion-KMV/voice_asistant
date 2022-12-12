"""Module for websocket chat."""
from functools import cache
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect
from core.greta import Greta
from storage.getter import get_chat_storage
from time import perf_counter
from loguru import logger


class ChatManager:
    """Class to handle chat."""

    def __init__(self):
        self._active_connections: list[WebSocket] = []
        self._greta = Greta()
        self._chat_storage = get_chat_storage()

    async def connect(self, websocket: WebSocket):
        """Connect user to the chat."""
        await websocket.accept()
        self._active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Disconnect user from the chat"""
        self._active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        """Send message to the chat."""
        await websocket.send_text(message)

    async def start_chat(self, websocket: WebSocket, user_id: UUID):
        """Start chat with user.

        This will open a new websocket connection for a user.
        Let's assume that user can send text messages and voice messages.
        When user sends us voice message we will recognize it and show it
        to user in a text form like user typed it himself.
        """
        await self.connect(websocket)

        try:
            while True:
                message = await websocket.receive_text()
                #  Перед тем как отправить голосовое сообщение, фронт должен
                #  предупредить нас специальным сообщением, после которого будет начата передача
                #  голосового сообщения
                await self._chat_storage.save(user_id, message)
                if message == '<BEGIN_VOICE_MESSAGE_TRANSMISSION>':
                    t1 = perf_counter()
                    audio_data = await websocket.receive_bytes()
                    greta_response = await self._greta.process_user_audio_message(audio_data, user_id)
                    await websocket.send_text(f'You: {greta_response.user_text_message}')
                    await websocket.send_text(f'Greta: {greta_response.greta_text_message}')
                    await websocket.send_text('<BEGIN_VOICE_MESSAGE_TRANSMISSION>')
                    await websocket.send_bytes(greta_response.greta_audio_message)
                    t2 = perf_counter()
                    logger.info(f'Time: {round(t2 - t1, 2)}')
                    await self._chat_storage.save(user_id, greta_response.user_text_message)
                    continue

                await websocket.send_text(f"Message text was: {message}")
        except WebSocketDisconnect:
            self.disconnect(websocket)


@cache
def get_chat_manager():
    return ChatManager()
