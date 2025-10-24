import os

API_URL = os.getenv("RATES_URL", "https://api.exchangerate.host/latest")
DEFAULT_BASE = os.getenv("BASE", "USD")
CACHE_TIME = int(os.getenv("CACHE_TIME", "300"))
