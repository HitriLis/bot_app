import asyncio
import os


from fastapi import FastAPI, Request, HTTPException, status, File, Header, Form, UploadFile, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import httpagentparser

import models
import schemas
from services import messages_create
from bot import bot
from database import database

from settings import settings

app = FastAPI()
api_key = APIKeyHeader(name='Authorization')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await database.connect()
    await bot.declare()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# Статические файлы
if not os.path.exists(settings.media_root):
    os.makedirs(settings.media_root)


@app.post('/message')
async def message(request: Request):
    data = await request.json()
    client_id = data.get('client_id')
    message = data.get('body')
    bot_respons = await bot.get_start_script(
       client_id=client_id,
       message=message
    )
    await messages_create(
       client_id=client_id,
       body=message,
       bot_script='main'
    )
    # bot_respons = await bot.get_start_script(
    #    client_id=client_id,
    #    message=message
    # )

    return {'status': bot_respons}



# Для запуска отладчика и профайлера
if __name__ == '__main__':
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ['0.0.0.0:8000']
    config.use_reloader = True

    asyncio.run(serve(app, config))
