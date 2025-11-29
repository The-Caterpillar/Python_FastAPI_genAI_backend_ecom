from sqlalchemy import (
    Column, Integer, String, Text, Boolean, JSON,
    Numeric, DateTime
)
from sqlalchemy.sql import func
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    slug = Column(String, unique=True, nullable=False, index=True)

    short_description = Column(String, nullable=True)
    long_description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String, nullable=True)
    in_stock = Column(Boolean, nullable=True)

    tags = Column(JSON, nullable=True)
    product_metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
