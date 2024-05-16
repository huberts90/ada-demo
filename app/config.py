import os

# Move to config file
PLATFORM_URL = os.environ.get("GIT_PLATFORM_URL", "https://api.github.com")
CACHE_EXPIRATION = os.environ.get("CACHE_EXPIRATION_HOUR", 1)
PORT = os.environ.get("PORT", 8000)
