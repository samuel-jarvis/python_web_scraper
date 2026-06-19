from pydantic import BaseModel, Field, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


class BookCreate(BaseModel):
    name: str
    book_url: HttpUrl
    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
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
            if not cleaned:
                raise ValueError("Price must be a valid number.")
        return cleaned


class Book(BookCreate):
    id: int
    created_at: datetime


class BookUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    book_url: Optional[HttpUrl] = None
    price: Optional[Decimal] = Field(
        default=None, gt=0, max_digits=10, decimal_places=2)
    description: Optional[str] = None
