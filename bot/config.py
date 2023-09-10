from pathlib import Path

import disnake
import disnake.http
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Paths
    API_PATH = Path(__file__).parent.parent.resolve()
    BOTS_PATH = Path(__file__).parent.resolve()

    # Bot Settings
    DISCORD_BOT_TOKEN: str
    SLASH_TESTING_SERVERS: list[int] | None = None
    COLOR: disnake.Color = disnake.Color.from_rgb(130, 38, 97)
    AUTHOR_NAME: str = "OpenBB Bot"
    AUTHOR_URL: str = ""
    AUTHOR_ICON_URL: str = ""

    # Get OpenBB Hub PAT from https://my.openbb.co/app/sdk/pat
    OPENBB_HUB_PAT: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
