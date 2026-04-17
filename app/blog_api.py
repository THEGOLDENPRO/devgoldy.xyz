from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, List, Optional

from datetime import datetime

from .http_client import HTTPClient
from .constants import BLOG_CDN_URL, BLOG_API_URL

__all__ = ()

class BlogAPI():
    def __init__(self) -> None:
        self.blogs_data: Tuple[float, list] = (0.0, [])

    async def get_blog_posts(self, http_client: HTTPClient, limit: Optional[int] = None) -> List[dict]:
        params = {}

        if limit is not None:
            params["limit"] = limit

        now = datetime.now().timestamp()

        if now > self.blogs_data[0] + 60 * 60 * 12: # 12 hours
            http_session = await http_client.get_http_session()

            async with http_session.request("GET", BLOG_API_URL + "/posts", params = params) as r:
                if r.ok:
                    blog_posts = [
                        {
                            "id": post["id"],
                            "name": post["name"],
                            "thumbnail_url": BLOG_CDN_URL + post["thumbnail"] if post["thumbnail"] is not None else None,
                            "date_added": datetime.fromisoformat(post["date_added"]).strftime("%b %d %Y")
                        } for post in await r.json()
                    ]

            self.blogs_data = (now, blog_posts)

        return self.blogs_data[1]