CREATE TABLE books (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    book_url    TEXT NOT NULL UNIQUE,
    price       TEXT NOT NULL CHECK (CAST(price AS REAL) > 0),
    description TEXT NOT NULL,
    information TEXT NOT NULL DEFAULT '{}',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);