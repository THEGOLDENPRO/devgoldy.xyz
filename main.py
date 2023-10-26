from __future__ import annotations

import os
from decouple import config
from datetime import datetime
from aiohttp import ClientSession
from jikan4snek import Jikan4SNEK

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


__all__ = ("app",)
__version__ = "1.1.5"

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH")) # Like: /aghpb/v1


app = FastAPI(
    docs_url = None, 
    redoc_url = None,
    root_path = ROOT_PATH
)

RAW_GIT_URL = config("RAW_GIT_URL", "https://raw.githubusercontent.com/THEGOLDENPRO/devgoldy.xyz/main")
BLOG_API_URL = config("BLOG_API_URL", "https://api.devgoldy.xyz/goldy-exe/v1")

jikan = Jikan4SNEK()
http_client = ClientSession()
templates = Jinja2Templates(directory = "./templates")

@app.get("/")
async def index(request: Request):
    blog_posts = []
    anime_list = []
    open_source_projects = []

    async with http_client.request("GET", BLOG_API_URL + "/posts") as r:
        if r.ok:
            blog_posts = [
                {
                    "id": post.get("id"),
                    "name": post.get("name"),
                    "date_added": datetime.fromisoformat(post.get("date_added")).strftime("%b %d %Y")
                } for post in await r.json()
            ]

    async with http_client.request("GET", RAW_GIT_URL + "/os_projects_to_preview.json") as r:
        if r.ok:
            open_source_projects = await r.json(content_type = None)

    mal_history = await jikan.get("thegoldenpro", "history").users()
    mal_updates = await jikan.get("thegoldenpro", "userupdates").users()

    if mal_updates is not None:

        for anime in mal_updates["data"]["anime"]:
            action = ""
            
            status = anime["status"].lower()

            if status == "watching":
                continue

            elif status == "plan to watch":
                action = "Planned to watch"

            elif status == "completed":
                action = "Completed"

            anime_list.append(
                {
                    "action": action,
                    "url": anime["entry"]["url"],
                    "title": anime["entry"]["title"],
                    "date": datetime.fromisoformat(anime["date"]).strftime("%b %d %Y"),
                    "date_timestamp": datetime.fromisoformat(anime["date"]).timestamp()
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
            "open_source_projects": open_source_projects
        }
    )

@app.get("/mal")
@app.get("/anime")
async def anime(request: Request):
    return templates.TemplateResponse(
        "linker.html", {
            "request": request,
            "title": "Goldy's Anime List",
            "description": "Check out my always up-to-date anime list!",
            "site_name": "MyAnimeList",
            "image_url": "https://devgoldy.xyz/mal_logo.png",
            "colour": "#3db8ff",
            "redirect_url": "https://myanimelist.net/animelist/thegoldenpro?status=7"
        }
    )

@app.get("/github")
async def github(request: Request):
    return templates.TemplateResponse(
        "linker.html", {
            "request": request,
            "title": "Goldy's GitHub",
            "description": "Check out my open-source work at GitHub!",
            "site_name": "GitHub",
            "image_url": "https://avatars.githubusercontent.com/u/66202304",
            "colour": "#ffe1b8",
            "redirect_url": "https://github.com/THEGOLDENPRO"
        }
    )

@app.get("/discord")
async def discord(request: Request):
    return templates.TemplateResponse(
        "linker.html", {
            "request": request,
            "title": "Goldy's Discord",
            "description": "Friend me on Discord to get in touch.",
            "site_name": "Discord",
            "image_url": "https://cdn.discordapp.com/avatars/332592361307897856/8014e2255d9236b5f5088b50957d32bc.webp?size=4096",
            "colour": "#5865F2",
            "redirect_url": "https://discordapp.com/users/332592361307897856"
        }
    )

app.mount("/", StaticFiles(directory = "src"))