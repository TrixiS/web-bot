import asyncio
import webbrowser

import uvicorn

from app.app import app as _app, settings
from app.web_config import WebConfig
from bot.bot import Bot


async def app(loop: asyncio.AbstractEventLoop = None):
    _app.add_event_handler("startup", lambda: webbrowser.open("http://localhost"))

    config = uvicorn.Config(
        _app,
        port=settings.APP_PORT,
        loop=loop or asyncio.get_event_loop(),
        log_level="critical",
    )

    server = uvicorn.Server(config)
    await server.serve()


async def bot():
    config = await WebConfig.load()
    bot = Bot(config)
    await bot.start()
