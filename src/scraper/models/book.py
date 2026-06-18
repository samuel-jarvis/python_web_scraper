from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class BookCreate(BaseModel):
    name: str
    book_url: str
    price: float = Field(
        gt=0,
        description="The price of the book must be greater than zero.",
    )
    description: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Name cannot be empty.")
        return value.strip()

    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, value: float) -> float:
        if isinstance(value, str):
            cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
            try:
                value = float(cleaned)
            except ValueError:
                raise ValueError("Price must be a valid number.")
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        return value


class Book(BookCreate):
    id: int
    created_at: datetime


class BookUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    book_url: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
