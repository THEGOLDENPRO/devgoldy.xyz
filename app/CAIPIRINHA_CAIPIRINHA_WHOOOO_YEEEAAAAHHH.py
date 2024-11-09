from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.requests import Request

import re
from starlette.exceptions import HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.exception_handlers import http_exception_handler

__all__ = (
    "CAIPIRINHA_CAIPIRINHA_WHOOOO_YEEEAAAAHHH_or_http_exception",
)

async def CAIPIRINHA_CAIPIRINHA_WHOOOO_YEEEAAAAHHH_or_http_exception(request: Request, exception: HTTPException) -> FileResponse | Response:
    user_agent_string = request.headers.get("user-agent", "").lower()

    # yuuuuhhh, because I purposely wrote shit 
    # css you won't be able to enjoy it on mobile :)
    if exception.status_code == 404 and not is_mobile_device(user_agent_string):
        # I don't wanna redirect hence the use of file response.
        return FileResponse("./web/404.html")

    normal_http_exception = await http_exception_handler(request, exception)
    return normal_http_exception

def is_mobile_device(user_agent_string: str) -> bool:
    mobile_user_agent_regex_pattern = re.compile(
        r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", 
        re.I|re.M
    )

    match = mobile_user_agent_regex_pattern.search(user_agent_string)

    print(">><", match)

    return bool(match)