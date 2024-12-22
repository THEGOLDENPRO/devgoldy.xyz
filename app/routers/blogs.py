from __future__ import annotations

from datetime import datetime
from pyromark import Markdown, Options
from bs4 import BeautifulSoup

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from ..async_http_client import get_http_client
from ..context_builder import PageContextBuilder
from ..constants import BLOG_API_URL, BLOG_CDN_URL, MAX_DESCRIPTION_LENGTH

router = APIRouter(prefix = "/blogs")

markdown = Markdown(
    options = Options.ENABLE_HEADING_ATTRIBUTES
    | Options.ENABLE_STRIKETHROUGH
    | Options.ENABLE_TABLES
)
#markdown = Markdown(extensions = ["fenced_code", "sane_lists", "pymdownx.tilde"])
templates = Jinja2Templates(directory = "templates")

@router.get("")
@router.get("/")
async def index(request: Request):
    posts = []

    http_client = await get_http_client()

    async with http_client.get(BLOG_API_URL + "/posts") as r:
        if r.ok:
            posts = [
                {
                    "id": post["id"],
                    "name": post["name"],
                    "thumbnail_url": BLOG_CDN_URL + post.get("thumbnail") if post.get("thumbnail") is not None else None,
                    "date_added": datetime.fromisoformat(post.get("date_added")).strftime("%b %d %Y")
                } for post in await r.json()
            ]

    context = PageContextBuilder(
        request, 
        name = "Home", 
        description = "Where you can read my articles, tutorials and rants on technology.", 
        site_name = "Goldy.exe",
        theme_colour = "#090b11"
    )

    return templates.TemplateResponse(
        "blogs/index.html", {
            "top_post": None if posts == [] else posts[0],
            "posts": posts,

            **context.data
        }
    )

@router.get("/post/{id}", response_class = HTMLResponse)
async def read_post(request: Request, id: int):
    post = {}
    content: str = ""

    http_client = await get_http_client()

    async with http_client.get(BLOG_API_URL + f"/post/{id}") as r:
        if not r.ok:
            raise HTTPException(404, "Hey what you doing here, there's no such post! Stop lurking, smh")

        post = await r.json()

    content_url = BLOG_CDN_URL + f"/{id}/content.md"
    thumbnail_url = BLOG_CDN_URL + post["thumbnail"]

    async with http_client.get(content_url) as r:
        if not r.ok:
            raise HTTPException(404, "SHIT WE MESSED UP! HOW DID THIS HAPPEN!!!!!")

        data = await r.text("utf-8")
        content = markdown.html(data)

    description = BeautifulSoup(content).find("p").get_text()

    content = content.replace('src="./', f'src="./{id}/') # Redirects all html elements linking to root to the blog's cdn redirect.

    if len(description) >= MAX_DESCRIPTION_LENGTH:
        description = description[:MAX_DESCRIPTION_LENGTH] + "..."

    context = PageContextBuilder(
        request, 
        name = post["name"], 
        description = description, 
        image_url = thumbnail_url, 
        site_name = None, 
        divider = None, 
        theme_colour = PageContextBuilder.convert_rgb_to_hex(
            # Adding fallback here as the old api doesn't have accent_colour.
            tuple([int(value) for value in post.get("accent_colour", "9, 11, 17").split(",")])
        )
    )

    return templates.TemplateResponse(
        "blogs/post.html", {
            "id": id, 
            "blog_name": post["name"], 
            "blog_date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y"), 
            "blog_content": content, 
            "blog_thumbnail_url": thumbnail_url, 

            **context.data
        }
    )

@router.get("/post/{id}/{filename}", response_class = RedirectResponse)
async def get_post_file(id: int, filename: str) -> RedirectResponse:
    return RedirectResponse(BLOG_CDN_URL + f"/{id}/{filename}")