from os import getenv


FAST_API_RELOAD = getenv("FAST_API_RELOAD", "1") == "1"
FAST_API_PORT = int(getenv("FAST_API_PORT", "8000"))
FAST_API_HOST = getenv("FAST_API_HOST", "0.0.0.0")
