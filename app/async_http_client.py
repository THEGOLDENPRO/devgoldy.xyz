from aiohttp import ClientSession

__all__ = ()

__client_session = None

async def get_http_client() -> ClientSession:
    global __client_session

    if __client_session is None:
        __client_session = ClientSession()

    return __client_session