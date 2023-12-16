from __future__ import annotations

import os
from datetime import datetime
from aiohttp import ClientSession

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .anime import Anime
from .config import Config, ProjectData

from .routers import linkers
from . import constants, __version__

__all__ = ("app",)

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH")) # Like: /aghpb/v1


app = FastAPI(
    docs_url = None, 
    redoc_url = None,
    root_path = ROOT_PATH
)
app.include_router(linkers.router)

projects_placeholder: ProjectData = {
    "name": "Wait what",
    "description": "there seems to be nothing here :(",
    "git": "https://cdn.devgoldy.xyz/ricky.webm"
}

http_client = ClientSession()
config = Config(constants.CONFIG_PATH)
anime = Anime(constants.MAL_USERNAME, http_client)
templates = Jinja2Templates(directory = "./templates")

@app.get("/")
async def index(request: Request):
    blog_posts = []
    anime_list = []
    live_config = await config.get_config()

    async with http_client.request("GET", constants.BLOG_API_URL + "/posts") as r:
        if r.ok:
            blog_posts = [
                {
                    "id": post.get("id"),
                    "name": post.get("name"),
                    "date_added": datetime.fromisoformat(post.get("date_added")).strftime("%b %d %Y")
                } for post in await r.json()
            ]

    mal_history = await anime.get_history()
    mal_updates = await anime.get_updates()

    if mal_updates is not None:

        for anime_update in mal_updates["data"]["anime"]:
            action = ""

            status = anime_update["status"].lower()

            if status == "watching":
                continue

            elif status == "plan to watch":
                action = "Planned to watch"

            elif status == "completed":
                action = "Completed"

            anime_list.append(
                {
                    "action": action,
                    "url": anime_update["entry"]["url"],
                    "title": anime_update["entry"]["title"],
                    "date": datetime.fromisoformat(anime_update["date"]).strftime("%b %d %Y"),
                    "date_timestamp": datetime.fromisoformat(anime_update["date"]).timestamp()
                }
            )

    if mal_history is not None:
        anime_list += [
            {
                "action": f"Watched episode {anime['increment']} of",
                "url": anime["entry"]["url"],
                "title": anime["entry"]["name"],
                "date": datetime.fromisoformat(anime["date"]).strftime("%b %d %Y"),
                "date_timestamp": datetime.fromisoformat(anime["date"]).timestamp()
            } for anime in mal_history["data"][:20]
        ]

    anime_list.sort(key = lambda x: x["date_timestamp"], reverse = True)

    return templates.TemplateResponse(
        "home.html", {
            "request": request,
            "blog_posts": blog_posts,
            "anime_list": anime_list,
            "open_source_projects": live_config.get("projects", [projects_placeholder]),
            "version": __version__
        }
    )


app.mount("/", StaticFiles(directory = "web"))