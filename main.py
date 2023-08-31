# pylint: disable=unused-argument

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from bot import run_bot
from utils.backend import pywry_backend

app = FastAPI(title="OpenBB Bots", docs_url=None, redoc_url=None)


@app.exception_handler(Exception)
async def api_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"exception": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(run_bot.router)


@app.on_event("startup")
async def startup_event():
    pywry_backend().start(headless=True)
