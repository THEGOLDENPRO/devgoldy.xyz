from __future__ import annotations
from typing import Literal

import os
from datetime import datetime
from markdown import Markdown
from aiohttp import ClientSession
from meow_inator_5000.woutews import nya_service

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from .anime import Anime
from .config import Config, ProjectData
from .context_builder import PageContextBuilder
from .routers import blogs, linkers
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
app.include_router(blogs.router)

projects_placeholder: ProjectData = {
    "name": "Wait what",
    "description": "there seems to be nothing here :(",
    "git": "https://cdn.devgoldy.xyz/ricky.webm"
}

http_client = ClientSession()
config = Config(constants.CONFIG_PATH)
anime = Anime(constants.MAL_USERNAME, http_client)
templates = Jinja2Templates(directory = "./templates")
basic_markdown = Markdown()

@app.get("/")
async def index(request: Request, mode: Literal["legacy", "new"] = constants.DEFAULT_HOME_MODE):
    blog_posts = []
    config_data = await config.get_config()

    async with http_client.request("GET", constants.BLOG_API_URL + "/posts", params = {"limit": "8"}) as r:
        if r.ok:
            blog_posts = [
                {
                    "id": post["id"], 
                    "name": post["name"], 
                    "thumbnail_url": constants.BLOG_CDN_URL + post["thumbnail"] if post["thumbnail"] is not None else None, 
                    "date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y")
                } for post in await r.json()
            ]

    context = PageContextBuilder(
        request, 
        name = "Home", 
        description = "My main website.", 
        image_url = "https://devgoldy.xyz/image.jpg"
    )

    with open("./markdown/about_me.md") as file:
        about_me_content = basic_markdown.convert(file.read())

    status_msg = None

    status = config_data.get("status")

    if not status == "" and status is not None:
        status_msg = basic_markdown.convert(status[:50])

    projects = config_data.get("projects", [projects_placeholder])

    for index, project in enumerate(projects):
        git_url = project["git"]

        project_image_url = projects[index].get("image")

        if project_image_url is None and "https://github.com" in git_url:
            split_git_url = git_url.split("/")

            git_user = split_git_url[-2]
            repo_name = split_git_url[-1]

            project_image_url = "https://opengraph.githubassets.com/d6e56308869b44ec6a37a53b7735b6d5bdd7131635f70cae050baf0197620f3a" \
                f"/{git_user}/{repo_name}"

        projects[index]["image"] = project_image_url

    return templates.TemplateResponse(
        "legacy_index.html" if mode == "legacy" else "index.html", {
            "status": status_msg, 
            "about_me_content": about_me_content, 
            "blog_posts": blog_posts, 
            "anime_list": await anime.get_anime_status(), 
            "open_source_projects": projects, 

            **context.data
        }
    )

@app.get("/privacy")
async def privacy(request: Request):
    with open("./markdown/privacy_policy.md") as file:
        privacy_policy_content = basic_markdown.convert(file.read())

    context = PageContextBuilder(
        request, 
        name = "Privacy Policy", 
        description = "Privacy policy for everything under devgoldy.xyz.", 
        theme_colour = "#ff6817"
    )

    edit_date = privacy_policy_content.split("<p>", 2)[1].split("</p>", 1)[0]
    content = privacy_policy_content.split("</blockquote>", 1)[1]

    return templates.TemplateResponse(
        "privacy_policy.html", {
            "edit_date": edit_date,
            "privacy_policy": content,

            **context.data
        }
    )

@app.get("/favicon.ico")
async def privacy():
    return RedirectResponse("./rikka.png") # You saw it, didn't you...

app.mount("/", StaticFiles(directory = "web"))