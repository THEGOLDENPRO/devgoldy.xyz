from __future__ import annotations

from bs4 import BeautifulSoup
from datetime import datetime
from pyromark import Markdown, Options

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from ..blog_api import BlogAPI
from ..http_client import HTTPClient
from ..context_builder import PageContextBuilder
from ..constants import BLOG_API_URL, BLOG_CDN_URL, MAX_DESCRIPTION_LENGTH

__all__ = ()

router = APIRouter(prefix = "/blogs")

markdown = Markdown(
    options = Options.ENABLE_HEADING_ATTRIBUTES
    | Options.ENABLE_STRIKETHROUGH
    | Options.ENABLE_TABLES
)
goldy_exe_api = BlogAPI()
http_client = HTTPClient()
templates = Jinja2Templates(directory = "templates")

@router.get("")
@router.get("/")
async def index(request: Request):
    posts = await goldy_exe_api.get_blog_posts(http_client)

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
    post_data = {}
    content: str = ""

    http_session = await http_client.get_http_session()

    async with http_session.get(BLOG_API_URL + f"/post/{id}") as response:
        if not response.ok:
            raise HTTPException(
                status_code = 404,
                detail = "Hey what you doing here, there's no such post! Stop lurking, smh"
            )

        post_data = await response.json()

    content_url = BLOG_CDN_URL + f"/{id}/content.md"
    thumbnail_url = BLOG_CDN_URL + post_data["thumbnail"]

    async with http_session.get(content_url) as r:
        if not r.ok:
            raise HTTPException(404, "SHIT WE MESSED UP! HOW DID THIS HAPPEN!!!!!")

        data = await r.text("utf-8")
        content = markdown.html(data)

    first_paragraph_tag = BeautifulSoup(content, features="html.parser").find("p")

    description = first_paragraph_tag.get_text() if first_paragraph_tag is not None else ""

    # Redirects all html elements linking to root to the blog's cdn redirect.
    content = content.replace('src="./', f'src="./{id}/')

    if len(description) >= MAX_DESCRIPTION_LENGTH:
        description = description[:MAX_DESCRIPTION_LENGTH] + "..."

    context = PageContextBuilder(
        request,
        name = post_data["name"],
        description = description,
        image_url = thumbnail_url,
        site_name = None,
        divider = None,
        theme_colour = PageContextBuilder.convert_rgb_to_hex(
            # Adding fallback here as the old api doesn't have accent_colour.
            tuple([int(value) for value in post_data.get("accent_colour", "9, 11, 17").split(",")]) # ty:ignore[invalid-argument-type]
        )
    )

    return templates.TemplateResponse(
        "blogs/post.html", {
            "id": id, 
            "blog_name": post_data["name"], 
            "blog_date_added": datetime.fromisoformat(post_data["date_added"]).strftime("%b %d %Y"),
            "blog_content": content,
            "blog_thumbnail_url": thumbnail_url,

            **context.data
        }
    )

@router.get("/post/{id}/{filename}", response_class = RedirectResponse)
async def get_post_file(id: int, filename: str) -> RedirectResponse:
    return RedirectResponse(BLOG_CDN_URL + f"/{id}/{filename}")