import os
import time

_rate_backend = None


class MemoryRateLimitStorage:
    def __init__(self):
        self.data = {}

    def increment(self, key: str, window_seconds: int):
        now = int(time.time())
        item = self.data.get(key)

        if not item or item["reset_at"] <= now:
            item = {
                "count": 0,
                "reset_at": now + window_seconds,
            }

        item["count"] += 1
        self.data[key] = item
        return item["count"], item["reset_at"]


def get_rate_backend():
    global _rate_backend

    if _rate_backend is not None:
        return _rate_backend

    if os.getenv("RATE_LIMIT_USE_MEMORY") == "1":
        _rate_backend = MemoryRateLimitStorage()
        return _rate_backend

    import redis

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    _rate_backend = redis.Redis.from_url(redis_url, decode_responses=True)
    return _rate_backend


def reset_rate_backend():
    global _rate_backend
    _rate_backend = None


def check_fixed_window_limit(bucket_key: str, limit: int, window_seconds: int):
    backend = get_rate_backend()
    now = int(time.time())

    if isinstance(backend, MemoryRateLimitStorage):
        current, reset_at = backend.increment(bucket_key, window_seconds)
    else:
        current = backend.incr(bucket_key)
        ttl = backend.ttl(bucket_key)

        if ttl == -1:
            backend.expire(bucket_key, window_seconds)
            ttl = window_seconds

        reset_at = now + max(ttl, 0)

    remaining = limit - current

    return {
        "limit": limit,
        "remaining": max(0, remaining),
        "reset_at": reset_at,
        "blocked": current > limit,
    }
