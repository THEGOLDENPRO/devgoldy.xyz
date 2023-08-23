"""
Python script that is ran during deployment that creates the symbolic links for the aliases we specified.

WARNING: Will only work during building.
"""

import os
import tomllib
import pathlib

with open("./config.toml", mode="rb") as file:
    toml = tomllib.load(file)

    for page in toml["build"]["aliases"]:
        
        for alias in toml["build"]["aliases"][page]:
            path = pathlib.Path(f"./build/{alias}/")

            if not path.exists():
                path.mkdir()

            os.symlink(f"./build/{page}", f"./build/{alias}/")