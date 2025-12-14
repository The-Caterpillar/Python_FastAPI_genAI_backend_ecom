from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional, Literal


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)

    short_description: Optional[str] = None
    long_description: Optional[str] = None

    price: Decimal
    stock: int

    currency: Literal["INR", "USD", "EUR"] = "INR"
    in_stock: Optional[bool] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    short_description: Optional[str] = None
    long_description: Optional[str] = None

    price: Optional[Decimal] = None
    stock: Optional[int] = None

    currency: Optional[Literal["INR", "USD", "EUR"]] = None
    in_stock: Optional[bool] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
        fields = {
            "embedding": {"exclude": True}
        }
