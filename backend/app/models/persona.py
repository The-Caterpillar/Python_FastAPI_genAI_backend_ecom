from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Short archetype (1–3 words)
    persona_type = Column(String, nullable=True)

    # Persona structure JSON:
    # {
    #   "persona_type": "...",
    #   "details": {
    #       "overview": "...",
    #       "shopping_style": "...",
    #       "spending_style": "...",
    #       "emotional_shopping_tendency": "...",
    #       "brand_loyalty": "...",
    #       "deal_sensitivity": "...",
    #       "risk_appetite": "...",
    #       "aesthetic_preferences": "...",
    #       "decision_speed": "...",
    #       "online_vs_offline_preference": "...",
    #       "influence_factors": "...",
    #       "purchase_drivers": "...",
    #       "values_priority": "..."
    #   }
    # }
    persona_json = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
