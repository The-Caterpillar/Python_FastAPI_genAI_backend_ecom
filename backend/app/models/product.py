from sqlalchemy import (
    Column, Integer, String, Text, Boolean, JSON,
    Numeric, DateTime
)
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum
from sqlalchemy.types import Enum as SqlEnum
from sqlalchemy.orm import relationship


class CurrencyEnum(enum.Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    short_description = Column(String, nullable=True)
    long_description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    stock = Column(Integer, nullable=False, default=0)

    currency = Column(
        SqlEnum(CurrencyEnum, name="currency_enum", native_enum=False),
        nullable=False,
        server_default="INR"
    )

    in_stock = Column(Boolean, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")