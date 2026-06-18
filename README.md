# scraper

A small web scraper that collects book data (name, price, description) from
[books.toscrape.com](http://books.toscrape.com) and persists it to a SQLite database.

## Layout

```
src/scraper/
├── main.py                 # entry point / scraping driver
├── book_details.py         # scrapes individual book detail pages
├── logger.py               # configured logger (writes to output/logger.log)
├── db/
│   └── database.py         # SQLite connection + schema initialization
├── http/
│   └── client.py           # HTTP client helpers
├── models/
│   └── book.py             # pydantic models for books
└── repository/
    └── book_repository.py  # CRUD persistence for books
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
scraper          # runs the console entry point (scraper.main:main)
```

## Development

```bash
ruff check src   # lint
mypy src         # type-check
pytest           # tests
```
