from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Tuple, List

from datetime import datetime, timedelta

from .async_http_client import get_http_client

__all__ = ("Anime",)

class Anime():
    def __init__(self, username: str) -> None:
        self.username = username

        self.__history_cache: Tuple[float, Dict[str, str]] = (0, {})
        self.__updates_cache: Tuple[float, Dict[str, str]] = (0, {})

        self.cache_expire = timedelta(minutes = 5)

    async def get_anime_status(self) -> List[dict]:
        anime_list = []

        mal_history = await self.__get_history()
        mal_updates = await self.__get_updates()

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

        return anime_list

    async def __get_history(self) -> Dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__history_cache[0]:
            session = await get_http_client()
            r = await session.get(f"https://api.jikan.moe/v4/users/{self.username}/history")
            data = await r.json() if r.ok else {}

            self.__history_cache = (
                current_timestamp + self.cache_expire.seconds, data
            )

        return self.__history_cache[1]

    async def __get_updates(self) -> Dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__updates_cache[0]:
            session = await get_http_client()
            r = await session.get(f"https://api.jikan.moe/v4/users/{self.username}/userupdates")
            data = await r.json() if r.ok else {}

            self.__updates_cache = (
                current_timestamp + self.cache_expire.seconds, data
            )

        return self.__updates_cache[1]