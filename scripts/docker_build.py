import sys
sys.path.insert(0, '.')

import os
from app import __version__

os.system(
    f"docker build -t devgoldy/devgoldy_xyz:{__version__} --build-arg ARCH=amd64 ."
)

os.system(
    "docker build -t devgoldy/devgoldy_xyz:latest --build-arg ARCH=amd64 ."
)