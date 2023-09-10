from fastapi import FastAPI
from openbb import obb

from bot import run_bot
from bot.config import settings as cfg
from utils.backend import pywry_backend

if getattr(cfg, "OPENBB_HUB_PAT"):
    obb.account.login(pat=getattr(cfg, "OPENBB_HUB_PAT"))

app = FastAPI(title="OpenBB Bots", docs_url=None, redoc_url=None)


app.include_router(run_bot.router)


@app.on_event("startup")
async def startup_event():
    pywry_backend().start(headless=True)
