"""Main entrypoint module of the app."""

import uvicorn
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from fastapi.staticfiles import StaticFiles
from api.routers import chat
from common.serializer import orjson_session_dumps
from config import get_config, STATIC_FILES_DIR
from services import http_service

cfg = get_config()

app = FastAPI(
    title='VoiceAssistant',
    docs_url='/api',
    openapi_url='/docs.json',
    default_response_class=ORJSONResponse,
    version=cfg.version,
    description='Voice Assistant Service',
)

app.mount('/static', StaticFiles(directory=STATIC_FILES_DIR), name='static')


@app.on_event('startup')
async def startup():
    logger.info('Starting Voice Assistant Service...')
    http_service.session = ClientSession(
        json_serialize=orjson_session_dumps,
    )


@app.on_event('shutdown')
async def shutdown():
    logger.info('Shutting down Voice Assistant Service...')
    await http_service.session.close()


app.include_router(chat.router, prefix='/api', tags=['Voice'])

if __name__ == '__main__':
    logger.info('Running application with uvicorn.')
    uvicorn.run(
        'main:app',
        host=cfg.host,
        port=cfg.port,
        reload=True,
    )
