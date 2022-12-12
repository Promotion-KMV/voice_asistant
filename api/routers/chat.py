"""Main router of the application."""
import uuid

from fastapi import APIRouter, Depends, WebSocket, Request, Query
from starlette.responses import HTMLResponse

from services.chat_manager import ChatManager, get_chat_manager
from config import STATIC_FILES_DIR
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory=STATIC_FILES_DIR)


@router.get("/chat", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.websocket("/ws")
async def chat(
    websocket: WebSocket,
    user_id: str | None = Query(default=None),
    chat_manager: ChatManager = Depends(get_chat_manager)
):
    """Open new websocket chat with user."""
    if user_id is None:
        user_id = uuid.uuid4()
    await chat_manager.start_chat(websocket, user_id)
