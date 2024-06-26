from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List
    from typing_extensions import NotRequired

import toml
from pathlib import Path
from aiofiles import open

__all__ = ("Config",)

class ProjectData(TypedDict):
    name: str
    description: str
    git: str
    image: NotRequired[str]

class LinkerData(TypedDict):
    id: str
    title: str
    description: str
    site_name: str
    image_url: str
    colour: str
    url: str

class ConfigData(TypedDict):
    status: str
    projects: NotRequired[List[ProjectData]]
    linkers: NotRequired[List[LinkerData]]

class Config():
    def __init__(self, config_path: str) -> None:
        self.config_path = Path(config_path)

    async def get_config(self) -> ConfigData:
        config_file = await open(str(self.config_path), mode = "r", encoding = "utf+8")

        text = await config_file.read()
        await config_file.close()

        return toml.loads(text)["config"]