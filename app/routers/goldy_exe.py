from __future__ import annotations

import io
from decouple import config
from datetime import datetime
from colorthief import ColorThief

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from aiohttp import ClientSession

from ..constants import SOURCE_CODE_URL, CHANGE_LOG_URL, LICENSE_URL

router = APIRouter(redirect_slashes = True)

MAX_DESCRIPTION_LENGTH = 200
BLOG_CDN_URL = config("BLOG_CDN_URL", "https://cdn.devgoldy.xyz/goldy-exe")
BLOG_API_URL = config("BLOG_API_URL", "https://api.devgoldy.xyz/goldy-exe/v1")

http_client = ClientSession()
templates = Jinja2Templates(directory = "templates")

@router.get("/")
async def index(request: Request):
    posts = []

    async with http_client.request("GET", BLOG_API_URL + "/posts") as r:
        if r.ok:
            posts = [
                {
                    "id": post.get("id"),
                    "name": post.get("name"),
                    "thumbnail_url": BLOG_CDN_URL + post.get("thumbnail") if post.get("thumbnail") is not None else None,
                    "date_added": datetime.fromisoformat(post.get("date_added")).strftime("%b %d %Y")
                } for post in await r.json()
            ]

    return templates.TemplateResponse(
        "blogs/home.html", {
            "request": request,
            "top_post": None if posts == [] else posts[0],
            "posts": posts,

            # Footer
            "privacy_policy_url": "../privacy",
            "source_code_url": SOURCE_CODE_URL,
            "change_log_url": CHANGE_LOG_URL
        }
    )

@router.get("/post/{id}", response_class = HTMLResponse)
async def read_post(request: Request, id: int):
    post = {}

    async with http_client.request("GET", BLOG_API_URL + f"/post/{id}") as r:
        if not r.ok:
            raise HTTPException(404, "Hey what you doing here, there's no such post! Stop lurking, smh")

        post = await r.json()

    content: str = post["content"]
    description = content.split("<p>", 2)[1].split("</p>", 1)[0]

    if len(description) >= MAX_DESCRIPTION_LENGTH:
        description[:MAX_DESCRIPTION_LENGTH] += "..."

    thumbnail_url = BLOG_CDN_URL + post["thumbnail"]
    thumbnail_rgb = (9, 11, 17)

    async with http_client.request("GET", thumbnail_url) as r:

        if r.ok:
            file = await r.read()
            thumbnail_rgb = ColorThief(io.BytesIO(file)).get_color(200)

    return templates.TemplateResponse(
        "blogs/post.html", {
            "request": request,
            "id": id, 
            "name": post["name"],
            "short_description": description,
            "date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y"),
            "content": content,
            "rgb_colour": f"{thumbnail_rgb[0]}, {thumbnail_rgb[1]}, {thumbnail_rgb[2]}", # TODO: get rgb colour from thumbnail image.
            "thumbnail_url": BLOG_CDN_URL + post["thumbnail"],

            # Footer
            "privacy_policy_url": "../../privacy",
            "source_code_url": SOURCE_CODE_URL,
            "change_log_url": CHANGE_LOG_URL
        }
    )