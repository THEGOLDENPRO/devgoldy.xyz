from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

__all__ = ("app",)
__version__ = "1.0.0"

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH")) # Like: /aghpb/v1


app = FastAPI(
    docs_url = None, 
    redoc_url = None,
    root_path = ROOT_PATH
)

@app.get("/")
async def index():
    return FileResponse("./src/index.html")

@app.get("/mal")
@app.get("/anime")
async def anime():
    return FileResponse("./src/anime/index.html")

@app.get("/github")
async def github():
    return FileResponse("./src/github/index.html")

app.mount("/", StaticFiles(directory = "src"))