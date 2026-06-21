import requests
from tenacity import (
    retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type, before_sleep_log
)
from scraper.observability.logger import get_logger

logger = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": "MyScraperBot/1.0 (+https://github.com/yourname/scraper)"
}
DEFAULT_TIMEOUT = 10
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class TransientHTTPError(requests.RequestException):
    """Custom exception for transient HTTP errors."""
    pass


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=30),
    retry=retry_if_exception_type(
        (TransientHTTPError, requests.RequestException,
         requests.ConnectionError, requests.Timeout)
    ),
    before_sleep=before_sleep_log(logger, log_level="WARNING"),
    reraise=True
)
def fetch_html(url: str, *, timeout: int = DEFAULT_TIMEOUT) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    if response.status_code in RETRYABLE_STATUS:
        raise TransientHTTPError(
            f"Transient HTTP error: {response.status_code} for URL: {url}")

    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text
