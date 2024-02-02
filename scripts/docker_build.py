import sys
sys.path.insert(0, '.')

import os
from app import __version__

os.system(
    f"docker buildx build -t devgoldy/devgoldy-xyz:{__version__} --build-arg ARCH=amd64 ."
)

os.system(
    "docker buildx build -t devgoldy/devgoldy-xyz:latest --build-arg ARCH=amd64 ."
)