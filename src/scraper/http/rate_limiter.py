# scraper/http/rate_limiter.py
import asyncio
import time
from urllib.parse import urlparse


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._tokens = capacity
        self._updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._updated_at
        self._tokens = min(self.capacity, self._tokens +
                           elapsed * self.refill_rate)
        self._updated_at = now

    async def acquire(self, tokens: int = 1) -> float:
        async with self._lock:
            self._refill()
            self._tokens -= tokens
            if self._tokens >= 0:
                return 0.0
            wait = -self._tokens / self.refill_rate
        await asyncio.sleep(wait)        # sleep OUTSIDE the lock
        return wait


class RateLimiter:
    def __init__(self, capacity: float = 5, refill_rate: float = 1.0):
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._buckets: dict[str, TokenBucket] = {}
        self._lock = asyncio.Lock()

    async def _bucket_for(self, url: str) -> TokenBucket:
        domain = urlparse(url).netloc
        async with self._lock:
            if domain not in self._buckets:
                self._buckets[domain] = TokenBucket(
                    self._capacity, self._refill_rate)
            return self._buckets[domain]

    async def acquire(self, url: str, tokens: int = 1) -> float:
        bucket = await self._bucket_for(url)
        return await bucket.acquire(tokens)
