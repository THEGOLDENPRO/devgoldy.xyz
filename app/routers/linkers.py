from __future__ import annotations

import random
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from .. import constants
from ..config import Config

router = APIRouter()
templates = Jinja2Templates(directory = "./templates")

config = Config(constants.CONFIG_PATH)

@router.get("/mal")
@router.get("/anime")
async def anime_(request: Request):
    return templates.TemplateResponse(
        "linker.html", {
            "request": request,
            "title": "Goldy's Anime List",
            "description": "Check out my always up-to-date anime list!",
            "site_name": "MyAnimeList",
            "image_url": "https://devgoldy.xyz/mal_logo.png",
            "colour": "#3db8ff",
            "redirect_url": "https://myanimelist.net/animelist/thegoldenpro?status=2"
        }
    )

@router.get("/github")
async def github(request: Request):
    return templates.TemplateResponse(
        "linker.html", {
            "request": request,
            "title": "Goldy's GitHub",
            "description": "Check out my open-source work at GitHub!",
            "site_name": "GitHub",
            "image_url": "https://avatars.githubusercontent.com/u/66202304",
            "colour": "#cb5242",
            "redirect_url": "https://github.com/THEGOLDENPRO"
        }
    )

@router.get("/discord")
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

@router.get("/link/{linker_id}")
async def custom_linkers(request: Request, linker_id: str):
    live_config = await config.get_config()

    for linker in live_config["linkers"]:

        if linker.get("id") == linker_id:

            return templates.TemplateResponse(
                "linker.html", {
                    "request": request,
                    "title": linker["title"],
                    "description": linker["description"],
                    "site_name": linker["site_name"],
                    "image_url": linker["image_url"],
                    "colour": linker["colour"],
                    "redirect_url": linker["url"]
                }
            )

    wait_what = "That link does not exist darling. Wait what, you had a 14.285714285714285% chance of getting this error message."

    raise HTTPException(
        404,
        detail = wait_what if random.randint(0, 6) == 0 else None
    )