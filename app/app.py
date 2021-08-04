from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .settings import settings
from .routers import config, bot, logs
from .web_config import WebConfig
from bot import root_path

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=str((root_path / "static").absolute())),
    name="static",
)
app.include_router(config.router, prefix="/api")
app.include_router(bot.router, prefix="/api/bot")
app.include_router(logs.router, prefix="/api/logs")

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(StarletteHTTPException)
async def handler_404(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return RedirectResponse("/static/index.html")

    return await http_exception_handler(request, exc)


@app.on_event("startup")
async def on_startup():
    WebConfig._instance = await WebConfig.load()


@app.on_event("shutdown")
async def on_shutdown():
    await WebConfig._instance.save()

    if bot.manager.thread is not None:
        bot.manager.thread.stop()
