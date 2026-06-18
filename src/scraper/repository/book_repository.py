from scraper.db.database import get_connection, initialize_database
from scraper.models.book import Book, BookCreate, BookUpdate


class BookRepository:
    def __init__(self):
        initialize_database()

    def create_book(self, book_create: BookCreate) -> Book:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (name, book_url, price, description)
                VALUES (?, ?, ?, ?)
            """, (book_create.name, book_create.book_url, book_create.price, book_create.description))
            book_id = cursor.lastrowid
        return self.get_book_by_id(book_id)

    def get_book_by_id(self, book_id: int) -> Book:
        with get_connection() as conn:
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

        updated_data = existing_book.dict()
        update_fields = book_update.dict(exclude_unset=True)
        updated_data.update(update_fields)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE books
                SET name = ?, book_url = ?, price = ?, description = ?
                WHERE id = ?
            """, (updated_data['name'], updated_data['book_url'], updated_data['price'], updated_data['description'], book_id))

        return self.get_book_by_id(book_id)

    def delete_book(self, book_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            return cursor.rowcount > 0

    def list_books(self) -> list[Book]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [Book(**row) for row in rows]
