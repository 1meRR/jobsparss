import time
import requests

from config import API_URL, CACHE_TIME, DEFAULT_BASE

_cache = {"rates": None, "base": None, "time": 0}


def load_rates(base=None):
    current_base = base or DEFAULT_BASE
    now = time.time()
    if (
        _cache["rates"]
        and _cache["base"] == current_base
        and now - _cache["time"] < CACHE_TIME
    ):
        return _cache["rates"]
    response = requests.get(API_URL, params={"base": current_base})
    data = response.json()
    rates = data.get("rates", {})
    if rates:
        _cache["rates"] = rates
        _cache["base"] = current_base
        _cache["time"] = now
    return rates


def convert_amount(amount, rate):
    return round(amount * rate, 2)


def normalize_currency(code):
    if not code:
        return None
    return code.strip().upper()
