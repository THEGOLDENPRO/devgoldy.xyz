from __future__ import annotations

import io
from datetime import datetime
from colorthief import ColorThief

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from aiohttp import ClientSession

from ..context_builder import PageContextBuilder
from ..constants import BLOG_API_URL, BLOG_CDN_URL, MAX_DESCRIPTION_LENGTH

router = APIRouter()

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

    context = PageContextBuilder(
        request, 
        name = "Home", 
        description = "Where you can read my articles, tutorials and rants on technology.", 
        image_url = "https://devgoldy.xyz/image.png",
        site_name = "Goldy.exe",
        theme_colour = "#090b11"
    )

    return templates.TemplateResponse(
        "blogs/home.html", {
            "top_post": None if posts == [] else posts[0],
            "posts": posts,

            **context.data
        }
    )

@router.get("/post/{id}", response_class = HTMLResponse)
async def read_post(request: Request, id: int):
    post = {}

    async with http_client.request("GET", BLOG_API_URL + f"/post/{id}") as r:
        if not r.ok:
            raise HTTPException(404, "Hey what you doing here, there's no such post! Stop lurking, smh")

        post = await r.json()

    content = post["content"]
    description = content.split("<p>", 2)[1].split("</p>", 1)[0]

    if len(description) >= MAX_DESCRIPTION_LENGTH:
        description[:MAX_DESCRIPTION_LENGTH] += "..."

    thumbnail_url = BLOG_CDN_URL + post["thumbnail"]
    thumbnail_rgb = (9, 11, 17)

    async with http_client.request("GET", thumbnail_url) as r:

        if r.ok:
            file = await r.read()
            thumbnail_rgb = ColorThief(io.BytesIO(file)).get_color(200)

    context = PageContextBuilder(
        request, 
        name = post["name"], 
        description = description, 
        image_url = thumbnail_url,
        site_name = "Goldy.exe"
    )

    return templates.TemplateResponse(
        "blogs/post.html", {
            "id": id, 
            "name": post["name"],
            "short_description": description,
            "date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y"),
            "content": content,
            "rgb_colour": f"{thumbnail_rgb[0]}, {thumbnail_rgb[1]}, {thumbnail_rgb[2]}", # TODO: get rgb colour from thumbnail image.
            "thumbnail_url": thumbnail_url,

            **context.data
        }
    )