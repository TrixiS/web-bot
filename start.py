import os
import platform

WINDOWS = platform.system() == "Windows"

if WINDOWS:
    deps_install_exit_code = os.system(
        "python -m pip install wheel -r requirements.txt --quiet"
    )
else:
    deps_install_exit_code = os.system(
        "python3 -m pip install -U wheel -r requirements.txt --quiet"
    )

if deps_install_exit_code != 0:
    if WINDOWS:
        os.system("pause")

    exit(deps_install_exit_code)

import logging
import webbrowser
import asyncio
import argparse

import uvicorn

from app.app import app, settings
from app.web_config import WebConfig
from bot.bot import Bot
from bot import root_path


async def start_app(loop: asyncio.AbstractEventLoop = None):
    app.add_event_handler("startup", lambda: webbrowser.open("http://localhost"))
    config = uvicorn.Config(
        app,
        port=settings.APP_PORT,
        loop=loop or asyncio.get_event_loop(),
        log_level="critical",
    )
    server = uvicorn.Server(config)
    await server.serve()


async def start_bot():
    logging.basicConfig(
        filename=root_path / "logs.log",
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    )

    config = await WebConfig.load()
    bot = Bot(config)
    await bot.start()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-app", action="store_true")

    args = parser.parse_args()

    if args.no_app:
        return await start_bot()

    await start_app()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
