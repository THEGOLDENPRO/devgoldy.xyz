from decouple import config

__all__ = (
    "CONFIG_PATH",
    "MAL_USERNAME",
    "BLOG_API_URL"
)

CONFIG_PATH = config("CONFIG_PATH", "./config.xml")
MAL_USERNAME = config("MAL_USERNAME", "thegoldenpro")
BLOG_API_URL = config("BLOG_API_URL", "https://api.devgoldy.xyz/goldy-exe/v1")
SOURCE_CODE_URL = config("SOURCE_CODE_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz")
CHANGE_LOG_URL = config("CHANGE_LOG_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz/releases")
LICENSE_URL = config("LICENSE_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz/blob/master/LICENSE")