from pathlib import Path

import disnake
import disnake.http
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Paths
    API_PATH = Path(__file__).parent.parent.resolve()
    BOTS_PATH = Path(__file__).parent.resolve()

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PASS: str = None
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # FASTAPI Headers
    API_HEADER_KEY: str

    # Bot Settings
    BOT_VERSION: str = "1.0.0"
    DISCORD_BOT_TOKEN: str

    # Settings
    SLASH_TESTING_SERVERS: list[int] | None = None
    DATE_FORMAT: str = "%Y-%m-%d"
    COLOR: disnake.Color = disnake.Color.from_rgb(130, 38, 97)

    DEBUG: bool = False

    AUTHOR_NAME: str = "OpenBB Bot"
    AUTHOR_URL: str = ""
    AUTHOR_ICON_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# redis_conn = Redis(
#     host=settings.REDIS_HOST,
#     password=settings.REDIS_PASS,
#     port=settings.REDIS_PORT,
#     db=settings.REDIS_DB,
# )

# rq_que = Queue(connection=redis_conn)
