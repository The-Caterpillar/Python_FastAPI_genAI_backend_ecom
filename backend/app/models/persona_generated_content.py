from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class PersonaGeneratedContent(Base):
    __tablename__ = "persona_generated_content"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    persona_summary = Column(Text, nullable=True)
    personalized_description = Column(Text, nullable=True)
    personalized_review_summary = Column(Text, nullable=True)
    why_it_suits_you = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
