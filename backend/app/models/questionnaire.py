from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class UserQuestionnaire(Base):
    __tablename__ = "user_questionnaire"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    answers = Column(JSON, nullable=False)   # store full questionnaire JSON

    created_at = Column(DateTime(timezone=True), server_default=func.now())
