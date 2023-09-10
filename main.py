from fastapi import FastAPI
from openbb import obb

from bot import run_bot
from bot.config import settings as cfg
from utils.backend import pywry_backend

for api_key in ["fmp", "polygon", "fred", "benzinga"]:
    if getattr(cfg, f"{api_key.upper()}_API_KEY"):
        setattr(
            obb.user.credentials,
            f"{api_key}_api_key",
            getattr(cfg, f"{api_key.upper()}_API_KEY"),
        )


app = FastAPI(title="OpenBB Bots", docs_url=None, redoc_url=None)


app.include_router(run_bot.router)


@app.on_event("startup")
async def startup_event():
    pywry_backend().start(headless=True)
