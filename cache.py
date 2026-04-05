import json
import os
from datetime import datetime, timedelta

CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache.json")

# TTLs in hours. None = cache forever (historical data never changes)
TTL = {
    "driverStandings": 1,
    "constructorStandings": 1,
    "circuits": 24,
    "drivers": 24,
    "races": 24,
    "results": None,
    "qualifying": None,
    "laps": None,
    "pitstops": None,
    "sprint": None,
    "status": None,
}


def _load() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def _save(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def _ttl_for(endpoint: str) -> int | None:
    for key, ttl in TTL.items():
        if key in endpoint:
            return ttl
    return 1


def get(endpoint: str):
    cache = _load()
    entry = cache.get(endpoint)
    if not entry:
        return None

    ttl_hours = _ttl_for(endpoint)
    if ttl_hours is None:
        return entry["data"]

    cached_at = datetime.fromisoformat(entry["cached_at"])
    if datetime.now() - cached_at < timedelta(hours=ttl_hours):
        return entry["data"]

    return None


def set(endpoint: str, data):
    cache = _load()
    cache[endpoint] = {
        "data": data,
        "cached_at": datetime.now().isoformat(),
    }
    _save(cache)


def invalidate(endpoint: str = None):
    """Clear a specific endpoint or the entire cache."""
    if endpoint is None:
        _save({})
    else:
        cache = _load()
        cache.pop(endpoint, None)
        _save(cache)
