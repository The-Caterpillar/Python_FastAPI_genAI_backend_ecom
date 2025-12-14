from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    user = relationship("User")
    product = relationship("Product")
