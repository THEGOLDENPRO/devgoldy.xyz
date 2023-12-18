from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List
    from typing_extensions import NotRequired
    from xml.etree.ElementTree import Element

from pathlib import Path
from aiofiles import open
import defusedxml.ElementTree as ET

__all__ = ("Config",)

class ProjectData(TypedDict):
    name: str
    description: str
    git: str

class LinkerData(TypedDict):
    id: str
    title: str
    description: str
    site_name: str
    image_url: str
    colour: str
    url: str

class ConfigData(TypedDict):
    projects: NotRequired[List[ProjectData]]
    linkers: NotRequired[List[LinkerData]]

class Config():
    def __init__(self, config_path: str) -> None:
        self.config_path = Path(config_path)

    async def get_config(self) -> ConfigData:
        config_file = await open(str(self.config_path), mode = "r", encoding = "utf+8")

        text = await config_file.read()
        await config_file.close()

        return self.__tree_to_dict(ET.fromstring(text))

    def __tree_to_dict(self, tree: Element) -> ConfigData:
        documents = list(tree)

        return {
            "linkers": [
                {
                    "id": element[0].text,
                    "title": element[1].text,
                    "description": element[2].text,
                    "site_name": element[3].text,
                    "image_url": element[4].text,
                    "colour": element[5].text,
                    "url": element[6].text
                } for element in documents[0]
            ],
            "projects": [
                {
                    "name": element[0].text,
                    "description": element[1].text,
                    "git": element[2].text
                } for element in documents[1]
            ]
        }