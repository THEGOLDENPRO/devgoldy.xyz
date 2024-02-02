from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing import Optional
    from fastapi import Request
    from typing_extensions import NotRequired

from . import constants

__all__ = (
    "PageContextBuilder",
)

class PageContextData(TypedDict):
    request: Request
    site_name: NotRequired[str]
    title_divider: NotRequired[str]
    site_page_name: str
    site_description: str
    site_theme_colour: str
    site_image_url: NotRequired[str]
    privacy_policy_url: str
    source_code_url: str
    change_log_url: str

class PageContextBuilder():
    def __init__(
        self, 
        request: Request,
        name: str, 
        description: str, 
        image_url: Optional[str] = None, 
        site_name: Optional[str] = "Goldy", 
        divider: Optional[str] = " • ",
        theme_colour: str = "#fbc689"
    ) -> None:
        self.data = cast(
            PageContextData, {
                "request": request, 
                "site_page_name": name, 
                "site_description": description, 
                "site_theme_colour": theme_colour, 
                "privacy_policy_url": "/privacy", 
                "source_code_url": constants.SOURCE_CODE_URL, 
                "change_log_url": constants.CHANGE_LOG_URL
            }
        )

        if site_name is not None:
            self.data["site_name"] = site_name

        if divider is not None:
            self.data["title_divider"] = divider

        if image_url is not None:
            self.data["site_image_url"] = image_url