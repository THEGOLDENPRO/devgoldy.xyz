from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import List, Tuple
    from typing_extensions import NotRequired

import toml
from pathlib import Path
from aiofiles import open
from datetime import datetime

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
    def __init__(self, local_config_path: str) -> None:
        self.local_config_path = Path(local_config_path)
        self.static_config_path = Path(__file__).parent.parent.joinpath("static_config.toml")

        self.config_data: Tuple[float, ConfigData] = (0.0, {})

    async def get_config(self) -> ConfigData:
        now = datetime.now().timestamp()

        if now > self.config_data[0] + 120:
            merged_config_data: ConfigData = None

            async with open(self.static_config_path, mode = "r", encoding = "utf+8") as file:
                merged_config_data = toml.loads(await file.read())["config"]

            async with open(self.local_config_path, mode = "r", encoding = "utf+8") as file:
                local_config_data = toml.loads(await file.read())["config"]
                merged_config_data.update(local_config_data)

            self.config_data = (now, merged_config_data)

        return self.config_data[1]