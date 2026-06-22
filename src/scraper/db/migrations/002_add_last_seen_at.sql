ALTER TABLE books ADD COLUMN last_seen_at TIMESTAMP;

-- INSERT INTO books (name, book_url, price, description, information, last_seen_at)
-- VALUES (:name, :book_url, :price, :description, :information, CURRENT_TIMESTAMP)
-- ON CONFLICT(book_url) DO UPDATE SET
--     name         = excluded.name,
--     price        = excluded.price,
--     description  = excluded.description,
--     information  = excluded.information,
--     last_seen_at = CURRENT_TIMESTAMP
-- RETURNING *