import json
import os
import time

_cache_backend = None
_cache_stats = {
    "hits": 0,
    "misses": 0,
}


class MemoryCache:
    def __init__(self):
        self.data = {}

    def get(self, key: str):
        item = self.data.get(key)
        if not item:
            return None

        if item["expires_at"] <= time.time():
            self.data.pop(key, None)
            return None

        return item["value"]

    def setex(self, key: str, ttl: int, value: str):
        self.data[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }

    def delete(self, *keys):
        for key in keys:
            self.data.pop(key, None)

    def keys(self, pattern: str):
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return [key for key in list(self.data.keys()) if key.startswith(prefix)]

        if pattern in self.data:
            return [pattern]

        return []


def get_cache_backend():
    global _cache_backend

    if _cache_backend is not None:
        return _cache_backend

    if os.getenv("CACHE_USE_MEMORY") == "1":
        _cache_backend = MemoryCache()
        return _cache_backend

    import redis

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    _cache_backend = redis.Redis.from_url(redis_url, decode_responses=True)
    return _cache_backend


def reset_cache_backend():
    global _cache_backend
    _cache_backend = None
    _cache_stats["hits"] = 0
    _cache_stats["misses"] = 0


def cache_get_json(key: str):
    value = get_cache_backend().get(key)
    if value is None:
        _cache_stats["misses"] += 1
        return None

    _cache_stats["hits"] += 1
    return json.loads(value)


def cache_set_json(key: str, data, ttl: int):
    get_cache_backend().setex(key, ttl, json.dumps(data, ensure_ascii=False))


def cache_delete(key: str):
    get_cache_backend().delete(key)


def cache_delete_by_prefix(prefix: str):
    backend = get_cache_backend()
    keys = backend.keys(f"{prefix}*")
    if keys:
        backend.delete(*keys)


def get_cache_stats():
    return {
        "hits": _cache_stats["hits"],
        "misses": _cache_stats["misses"],
        "requests": _cache_stats["hits"] + _cache_stats["misses"],
    }
