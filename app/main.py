from __future__ import annotations
from typing import Literal

import os
from datetime import datetime
from markdown import Markdown
from fastapi_tailwind import tailwind
from contextlib import asynccontextmanager
from meow_inator_5000.woutews import nya_service

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from .anime import Anime
from .routers import blogs, linkers
from .config import Config, ProjectData
from .async_http_client import get_http_client
from .context_builder import PageContextBuilder
from .CAIPIRINHA_CAIPIRINHA_WHOOOO_YEEEAAAAHHH import CAIPIRINHA_CAIPIRINHA_WHOOOO_YEEEAAAAHHH_or_http_exception

from . import constants, __version__

__all__ = ("app",)

ROOT_PATH = os.environ.get("ROOT_PATH", "") # Like: /aghpb/v1

static_files = StaticFiles(directory = "static")

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Compile tailwind css.
    popen = tailwind.compile(
        output_stylesheet_path = static_files.directory + "/output.css",
        tailwind_stylesheet_path = "./input.css"
    )

    yield

    popen.terminate()

app = FastAPI(
    docs_url = None,
    redoc_url = None,
    root_path = ROOT_PATH,
    version = __version__,
    lifespan = lifespan
)
app.include_router(nya_service.router)

app.include_router(blogs.router)
app.include_router(linkers.router)

projects_placeholder: ProjectData = {
    "name": "Wait what",
    "description": "there seems to be nothing here :(",
    "git": "https://cdn.devgoldy.xyz/ricky.webm"
}

config = Config(constants.CONFIG_PATH)
anime = Anime(constants.MAL_USERNAME)
templates = Jinja2Templates(directory = "./templates")
basic_markdown = Markdown()

@app.get("/")
async def index(request: Request, mode: Literal["legacy", "stable"] = constants.DEFAULT_HOME_MODE):
    blog_posts = []
    config_data = await config.get_config()
    http_client = await get_http_client()

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
        image_url = "https://devgoldy.xyz/images/image.webp"
    )

    with open("./markdown/about_me.md") as file:
        about_me_content = basic_markdown.convert(file.read())

    status_msg = None

    status = config_data.get("status")

    if not status == "" and status is not None:
        status_msg = basic_markdown.convert(status)

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
            "anime_list": await anime.get_anime_status() if mode == "legacy" else [], 
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

@app.get("/mopping-girl")
@app.get("/give-mopping-girl-a-salary")
async def mopping_girl(request: Request):
    context = PageContextBuilder(
        request, 
        name = "Give mopping girl a salary!", 
        description = "It's unacceptable that mopping girl does not have a salary, click to find out how long she's been working. 💀", 
        image_url = "/images/mopping_girl.gif", 
        theme_colour = "#009e05"
    )

    return templates.TemplateResponse(
        "give_mg_salary.html", {
            **context.data
        }
    )

@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse("./images/rikka.png") # You saw it, didn't you...

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exception: HTTPException):
    return await CAIPIRINHA_CAIPIRINHA_WHOOOO_YEEEAAAAHHH_or_http_exception(request, exception)

app.mount("/", static_files)