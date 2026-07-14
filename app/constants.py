from decouple import config

__all__ = ()

MAX_DESCRIPTION_LENGTH = 200

DEBUG = config("DEBUG", False, cast = bool)

CONFIG_PATH = config("CONFIG_PATH", "./config.toml")
MAL_USERNAME = config("MAL_USERNAME", "thegoldenpro")

SOURCE_CODE_URL = config("SOURCE_CODE_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz")
CHANGE_LOG_URL = config("CHANGE_LOG_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz/releases")
LICENSE_URL = config("LICENSE_URL", "https://github.com/THEGOLDENPRO/devgoldy.xyz/blob/master/LICENSE")

BLOG_CDN_URL = config("BLOG_CDN_URL", "https://cdn.devgoldy.xyz/goldy-exe")
BLOG_API_URL = config("BLOG_API_URL", "https://api.devgoldy.xyz/goldy-exe/v1")

DEFAULT_HOME_MODE = config("DEFAULT_HOME_MODE", "stable")