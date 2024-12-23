from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, List, Optional

from datetime import datetime

from . import constants
from .async_http_client import get_http_client

__all__ = ()

class GoldyEXEAPI():
    def __init__(self) -> None:
        self.blogs_data: Tuple[int, list] = (0.0, [])

    async def get_blog_posts(self, limit: Optional[int] = None) -> List[dict]:
        params = {}

        if limit is not None:
            params["limit"] = limit

        now = datetime.now().timestamp()

        if now > self.blogs_data[0] + 60 * 60 * 12: # 12 hours
            http_client = await get_http_client()

            async with http_client.request("GET", constants.BLOG_API_URL + "/posts", params = params) as r:
                if r.ok:
                    blog_posts = [
                        {
                            "id": post["id"],
                            "name": post["name"],
                            "thumbnail_url": constants.BLOG_CDN_URL + post["thumbnail"] if post["thumbnail"] is not None else None,
                            "date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y")
                        } for post in await r.json()
                    ]

            self.blogs_data = (now, blog_posts)

        return self.blogs_data[1]