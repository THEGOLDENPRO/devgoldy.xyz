import sys; sys.path.insert(0, '.')

import os
import main

os.system(
    f"docker build -t devgoldy/devgoldy_xyz:{main.__version__} --build-arg ARCH=amd64 ."
)

os.system(
    "docker build -t devgoldy/devgoldy_xyz:latest --build-arg ARCH=amd64 ."
)