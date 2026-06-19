import sqlite3
from contextlib import contextmanager
import os
from scraper.paths import DATA_DIR
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    book_url    TEXT NOT NULL UNIQUE,
    price       TEXT NOT NULL CHECK (CAST(price AS REAL) > 0),
    description TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_connection(db_path: Path = DATA_DIR) -> sqlite3.Connection:
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


def initialize_database(db_path: Path = DATA_DIR) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection(db_path) as conn:
        conn.execute(SCHEMA)
