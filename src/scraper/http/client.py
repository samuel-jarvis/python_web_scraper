import asyncio
import logging
from contextlib import asynccontextmanager
import aiohttp
from tenacity import (
    retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type, before_sleep_log
)
from scraper.observability.logger import get_logger
from scraper.http.rate_limiter import RateLimiter

logger = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": "MyScraperBot/1.0 (+https://github.com/yourname/scraper)"}
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
DEFAULT_TIMEOUT = 10


class TransientHTTPError(Exception):
    """Custom exception for transient HTTP errors."""
    pass


class HttpClient:
    def __init__(self, session: aiohttp.ClientSession, rate_limiter: RateLimiter):
        self._session = session
        self._rate_limiter = rate_limiter

    @classmethod
    @asynccontextmanager
    async def create(cls, *, capacity: float = 5, refill_rate: float = 1.0,
                     max_connections: int = 10, timeout: float = 10.0):
        # factory pattern since we can't await inside __init__
        connector = aiohttp.TCPConnector(limit=max_connections)
        session = aiohttp.ClientSession(
            headers=DEFAULT_HEADERS,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=timeout)
        )
        try:
            yield cls(session, RateLimiter(capacity, refill_rate))
        finally:
            await session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(multiplier=1, max=30),
        retry=retry_if_exception_type(
            (TransientHTTPError, aiohttp.ClientConnectionError, asyncio.TimeoutError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    async def fetch_html(self, url: str, *, timeout: int = DEFAULT_TIMEOUT) -> str:
        await self._rate_limiter.acquire(url)

        async with self._session.get(url) as response:
            if response.status in RETRYABLE_STATUS:
                raise TransientHTTPError(
                    f"Transient HTTP error: {response.status} for URL: {url}")

            response.raise_for_status()
            return await response.text()
