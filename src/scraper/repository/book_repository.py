from scraper.db.database import DB_PATH, get_connection
from scraper.models.book import Book, BookCreate, BookUpdate
import json


class BookRepository:
    def __init__(self, db_path=None):
        self._db_path = db_path if db_path is not None else DB_PATH

    def create_book(self, book_create: BookCreate) -> Book:
        with get_connection(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (name, book_url, price, description, information)
                VALUES (?, ?, ?, ?, ?)
            """, (book_create.name, book_create.book_url, book_create.price, book_create.description, json.dumps(book_create.information, ensure_ascii=False)))
            book_id = cursor.lastrowid
        return self.get_book_by_id(book_id)

    def upsert_book(self, book_create: BookCreate) -> Book:
        data = book_create.model_dump(mode="json")
        data["information"] = json.dumps(
            data["information"], ensure_ascii=False)
        with get_connection(self._db_path) as conn:
            row = conn.execute(
                """
                    INSERT INTO books (name, book_url, price, description, information)
                    VALUES (:name, :book_url, :price, :description, :information)
                    ON CONFLICT(book_url) DO UPDATE SET
                        name = excluded.name,
                        price = excluded.price,
                        description = excluded.description,
                        information = excluded.information
                    RETURNING *
                    """, data
            ).fetchone()
        return Book(**row) if row else None

    def get_book_by_id(self, book_id: int) -> Book:
        with get_connection(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            row = cursor.fetchone()
            if row:
                return Book(**row)
        return None

    def update_book(self, book_id: int, book_update: BookUpdate) -> Book:
        existing_book = self.get_book_by_id(book_id)
        if not existing_book:
            return None

        # deprecated
        # updated_data = existing_book.dict()
        # update_fields = book_update.dict(exclude_unset=True)
        # updated_data.update(update_fields)

        merged = existing_book.model_dump(mode="json")
        merged.update(book_update.model_dump(exclude_unset=True, mode="json"))

        with get_connection(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books
                SET name = :name,
                    book_url = :book_url,
                    price = :price,
                    description = :description,
                    information = :information
                WHERE id = :id
            """, {**merged, "id": book_id})

        return self.get_book_by_id(book_id)

    def delete_book(self, book_id: int) -> bool:
        with get_connection(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = :id", {"id": book_id})
            return cursor.rowcount > 0

    def list_books(self) -> list[Book]:
        with get_connection(self._db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [Book(**row) for row in rows]
