import json
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
    information: dict[str, str] = Field(default_factory=dict)

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
        return value

    @field_validator('information', mode='before')
    @classmethod
    def validate_information(cls, value: Optional[dict]) -> dict:
        if value is None:
            return {}
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError("Information must be valid JSON.") from exc
        if not isinstance(value, dict):
            raise ValueError("Information must be a dictionary.")
        return value


class Book(BookCreate):
    id: int
    created_at: datetime


class BookUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    book_url: Optional[HttpUrl] = None
    price: Optional[Decimal] = Field(
        default=None, gt=0, max_digits=10, decimal_places=2)
    description: Optional[str] = None
    information: Optional[dict[str, str]] = Field(default=None)
