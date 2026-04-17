from typing import Optional

import logging
from aiohttp import ClientSession

__all__ = ()

logger = logging.getLogger(__name__)

class HTTPClient():
    def __init__(self):
        self.__http_session: Optional[ClientSession] = None

    async def get_http_session(self) -> ClientSession:
        if self.__http_session is None:
            logging.debug("Initializing aiohttp client session...")

            self.__http_session = ClientSession()

        return self.__http_session