from fastapi import FastAPI

from bot import run_bot
from utils.backend import pywry_backend

app = FastAPI(title="OpenBB Bots", docs_url=None, redoc_url=None)


app.include_router(run_bot.router)


@app.on_event("startup")
async def startup_event():
    pywry_backend().start(headless=True)
