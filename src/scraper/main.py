from pydantic import ValidationError
from scraper.db.database import initialize_database
from scraper.http.client import fetch_html
from scraper.parser.book_parser import parse_book_detail, parse_book_links
from scraper.repository.book_repository import BookRepository
from scraper.observability.logger import configure_logging, get_logger, new_run_id
BASE_URL = "http://books.toscrape.com"

logger = get_logger(__name__)


def main() -> None:
    new_run_id()
    configure_logging()
    initialize_database()
    repo = BookRepository()

    try:
        listing_html = fetch_html(BASE_URL)
    except Exception:
        logger.exception("failed to fetch the main page")
        return

    links = parse_book_links(listing_html, BASE_URL)
    logger.info("found %d book links", len(links))

    saved = skipped = 0

    for url in links:
        try:
            html = fetch_html(url)
            book = parse_book_detail(html, url)
        except ValidationError as exc:
            logger.warning("skipping %s — validation failed: %s", url, exc)
            skipped += 1
            continue
        except Exception:
            logger.exception("skipping %s - fetch/parse error", url)
            skipped += 1
            continue

        repo.upsert_book(book)
        saved += 1

    logger.info("done: %d saved, %d skipped", saved, skipped)


if __name__ == "__main__":
    main()
