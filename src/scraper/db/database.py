import sqlite3
from contextlib import contextmanager
from scraper.paths import DATA_DIR
from pathlib import Path

DB_PATH = DATA_DIR / "books.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    book_url    TEXT NOT NULL UNIQUE,
    price       TEXT NOT NULL CHECK (CAST(price AS REAL) > 0),
    description TEXT NOT NULL,
    information TEXT NOT NULL DEFAULT '{}',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection(DB_PATH) as conn:
        conn.execute(SCHEMA)
