import typing

import logging
from datetime import datetime, timedelta

from .http_client import HTTPClient

__all__ = ()

logger = logging.getLogger(__name__)

class AnimeAPI():
    def __init__(self, username: str) -> None:
        self.username = username

        self.__history_cache: tuple[float, dict[str, str]] = (0, {})
        self.__updates_cache: tuple[float, dict[str, str]] = (0, {})

        self.cache_expire = timedelta(minutes = 5)

    async def get_anime_status(self, http_client: HTTPClient) -> list[dict]:
        anime_list = []

        mal_history = await self.__get_history(http_client)
        mal_updates = await self.__get_updates(http_client)

        if not mal_updates == {}:

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

        if not mal_history == {}:
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

    async def __get_history(self, http_client: HTTPClient) -> dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__history_cache[0]:
            http_session = await http_client.get_http_session()

            async with http_session.get(f"https://api.jikan.moe/v4/users/{self.username}/history") as response:
                if not response.ok:
                    logger.error(f"Received unsuccessful response from jikan! Response: {response}")

                data = typing.cast(dict, val = await response.json() if response.ok else {})

            self.__history_cache = (
                current_timestamp + self.cache_expire.seconds, data
            )

        return self.__history_cache[1]

    async def __get_updates(self, http_client: HTTPClient) -> dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__updates_cache[0]:
            http_session = await http_client.get_http_session()

            async with http_session.get(f"https://api.jikan.moe/v4/users/{self.username}/userupdates") as response:
                if not response.ok:
                    logger.error(f"Received unsuccessful response from jikan! Response: {response}")

                data = typing.cast(dict, val = await response.json() if response.ok else {})

            self.__updates_cache = (
                current_timestamp + self.cache_expire.seconds, data
            )

        return self.__updates_cache[1]