import asyncio

from pydantic import ValidationError
from scraper.db.database import initialize_database
from scraper.parser.book_parser import parse_book_detail, parse_book_links
from scraper.repository.book_repository import BookRepository
from scraper.observability.logger import configure_logging, get_logger, new_run_id
from scraper.db.migrate import run_migrations
from scraper.http.client import HttpClient
logger = get_logger(__name__)
BASE_URL = "http://books.toscrape.com"

# get single book details


async def scrape_book(client: HttpClient, url):
    try:
        html = await client.fetch_html(url)
        return parse_book_detail(html, url)
    except ValidationError as exc:
        logger.warning('skippint_invalid', extra={
                       'url': url, 'error': str(exc)})
    except Exception:
        logger.exception("fetch_parse_failed", extra={'url': url})
    return None


# get all the books
async def scraperr():
    async with HttpClient.create() as client:
        book_list = await client.fetch_html(BASE_URL)
        links = parse_book_links(book_list, BASE_URL)
        logger.info("links_found", extra={"count": len(links)})

        results = await asyncio.gather(
            *(scrape_book(client, url) for url in links)
        )

    return [book for book in results if book is not None]


def main() -> None:
    new_run_id()
    configure_logging()
    run_migrations()
    repo = BookRepository()

    books = asyncio.run(scraperr())
    for book in books:
        repo.upsert_book(book)

    logger.info("scrape_complete", extra={"saved": len(books)})


if __name__ == "__main__":
    main()
