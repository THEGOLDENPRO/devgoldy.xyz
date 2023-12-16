from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Tuple, Optional

from aiohttp import ClientSession
from datetime import datetime, timedelta

__all__ = ("Anime",)

class Anime():
    def __init__(self, username: str, http_session: Optional[ClientSession] = None) -> None:
        self.username = username

        self._session = http_session
        self.__history_cache: Tuple[float, Dict[str, str]] = (0, {})
        self.__updates_cache: Tuple[float, Dict[str, str]] = (0, {})

    async def get_history(self) -> Dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__history_cache[0]:
            session = self.__get_session()
            r = await session.get(f"https://api.jikan.moe/v4/users/{self.username}/history")
            data = await r.json() if r.ok else {}

            self.__history_cache = (
                current_timestamp + timedelta(minutes = 2).seconds, data
            )

        return self.__history_cache[1]

    async def get_updates(self) -> Dict[str, str]:
        current_timestamp = datetime.now().timestamp()

        if current_timestamp > self.__updates_cache[0]:
            session = self.__get_session()
            r = await session.get(f"https://api.jikan.moe/v4/users/{self.username}/userupdates")
            data = await r.json() if r.ok else {}

            self.__updates_cache = (
                current_timestamp + timedelta(minutes = 2).seconds, data
            )

        return self.__updates_cache[1]

    def __get_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()

        return self._session