from __future__ import annotations

import os
from datetime import datetime
from markdown import Markdown
from aiohttp import ClientSession
from meow_inator_5000.woutews import nya_service

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .anime import Anime
from .config import Config, ProjectData
from .context_builder import PageContextBuilder
from .routers import linkers, goldy_exe
from . import constants, __version__

__all__ = ("app",)

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH")) # Like: /aghpb/v1


app = FastAPI(
    docs_url = None, 
    redoc_url = None,
    root_path = ROOT_PATH,
    version = __version__
)
app.include_router(nya_service.router)

app.include_router(linkers.router)
app.include_router(goldy_exe.router, prefix = "/blogs")

projects_placeholder: ProjectData = {
    "name": "Wait what",
    "description": "there seems to be nothing here :(",
    "git": "https://cdn.devgoldy.xyz/ricky.webm"
}

http_client = ClientSession()
config = Config(constants.CONFIG_PATH)
anime = Anime(constants.MAL_USERNAME, http_client)
templates = Jinja2Templates(directory = "./templates")
markdown = Markdown(extensions = ["fenced_code", "sane_lists", "pymdownx.tilde"])

@app.get("/")
async def index(request: Request):
    blog_posts = []
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

    context = PageContextBuilder(
        request, 
        name = "Home", 
        description = "My main website.", 
        image_url = "https://devgoldy.xyz/image.png"
    )

    return templates.TemplateResponse(
        "home.html", {
            "blog_posts": blog_posts,
            "anime_list": await anime.get_anime_status(),
            "open_source_projects": live_config.get("projects", [projects_placeholder]),

            **context.data
        }
    )

@app.get("/privacy")
async def privacy(request: Request):
    with open("./privacy_policy.md") as file:
        privacy_policy_content = markdown.convert(file.read())

    context = PageContextBuilder(
        request, 
        name = "Privacy Policy", 
        description = "Privacy policy for everything under devgoldy.xyz.", 
        theme_colour = "#ff6817"
    )

    return templates.TemplateResponse(
        "privacy_policy.html", {
            "privacy_policy": privacy_policy_content,

            **context.data
        }
    )

app.mount("/", StaticFiles(directory = "web"))