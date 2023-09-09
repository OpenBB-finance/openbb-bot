import asyncio
from pathlib import Path

import disnake
from disnake.ext import commands  # type: ignore
from fastapi import APIRouter

from bot.config import settings as cfg


class OBB_Bot(commands.InteractionBot):
    def __init__(self: "OBB_Bot", **kwargs) -> None:
        super().__init__(
            intents=disnake.Intents.default(),
            command_sync_flags=commands.CommandSyncFlags.default(),
            chunk_guilds_at_startup=False,
            test_guilds=cfg.SLASH_TESTING_SERVERS,
            **kwargs,
        )

    def load_all_extensions(self, folder: str) -> None:
        folder_path = Path(__file__).parent.joinpath(folder).resolve()

        for path in folder_path.glob("*.py"):
            self.load_extension(
                ".".join(path.relative_to(cfg.API_PATH).parts).removesuffix(".py")
            )


router = APIRouter(
    prefix="/v1/discord",
    responses={404: {"description": "Not found"}},
    include_in_schema=False,
)


openbb_bot = OBB_Bot()
openbb_bot.load_all_extensions("cmds")


@router.on_event("startup")
async def startup_event():
    try:
        asyncio.create_task(openbb_bot.start(cfg.DISCORD_BOT_TOKEN))
    except KeyboardInterrupt:
        await openbb_bot.logout()
