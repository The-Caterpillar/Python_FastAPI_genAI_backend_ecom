from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class UserRole(enum.Enum):
    customer = "customer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    # NEW FIELDS (safe defaults so old users don't break)
    name = Column(String, nullable=False, server_default="")
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    dob = Column(Date, nullable=True)

    role = Column(
        SqlEnum(UserRole, name="user_role_enum"),
        nullable=False,
        server_default="customer"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # reviews = relationship("ProductReview", back_populates="user", cascade="all, delete-orphan")
