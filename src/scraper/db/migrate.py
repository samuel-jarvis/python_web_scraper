from pathlib import Path

from scraper.db.database import get_connection, DB_PATH
from scraper.observability.logger import get_logger

logger = get_logger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def ensure_migrations_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
      version     INTEGER PRIMARY KEY,
      name        TEXT NOT NULL,
      applied_at  DATETIME CURRENT_TIMESTAMP
    )
  """)


def get_applied_versions(conn) -> set[int]:
    rows = conn.execute("SELECT version from SCHEMA_MIGRATIONS").fetchall()
    print(rows)
    return {row["version"] for row in rows}


def discover_migrations() -> list[tuple[int, Path]]:
    migrations = []
    for path in sorted(MIGRATIONS_DIR.glob("[0-9]*.sql")):
        version = int(path.name.split("_")[0])
        migrations.append((version, path))
    return migrations


def apply_migration(conn, version: int, path: Path):
    sql = path.read_text(encoding="utf-8")
    # handles multi-statement files
    conn.executescript(sql)
    conn.execute(
        "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
        (version, path.name),
    )


def run_migrations(db_path: Path = DB_PATH):
    logger.info("Starting database migration")
    with get_connection(db_path) as conn:
        ensure_migrations_table(conn)
        applied_versions = get_applied_versions(conn)
        migrations = discover_migrations()

    for version, path in migrations:
        if version not in applied_versions:
            logger.info(f"Applying migration {version}: {path.name}")
            apply_migration(conn, version, path)
    logger.info("Database migration completed")
