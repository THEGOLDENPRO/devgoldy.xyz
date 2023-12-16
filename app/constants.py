from decouple import config

__all__ = (
    "CONFIG_PATH",
    "MAL_USERNAME",
    "BLOG_API_URL"
)

CONFIG_PATH = config("CONFIG_PATH", "./config.xml")
MAL_USERNAME = config("MAL_USERNAME", "thegoldenpro")
BLOG_API_URL = config("BLOG_API_URL", "https://api.devgoldy.xyz/goldy-exe/v1")