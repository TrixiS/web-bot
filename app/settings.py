from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):

    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
    ]
    APP_PORT: int = 80


settings = Settings()
