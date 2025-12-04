from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.models.questionnaire import UserQuestionnaire
from app.models.persona import Persona
from app.utils.gemini_client import ask_gemini

import json

load_dotenv()
router = APIRouter()


@router.post("/generate")
async def generate_persona(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    # 1. Fetch questionnaire answers
    stmt = select(UserQuestionnaire).where(UserQuestionnaire.user_id == user.id)
    result = await db.execute(stmt)
    questionnaire = result.scalar_one_or_none()

    if not questionnaire:
        raise HTTPException(400, "User has not completed the questionnaire.")

    # 2. Persona generation prompt for Gemini
    prompt = f"""
    You are an expert persona analyst.

    Based on the user's 5 questionnaire answers, generate a unique and creative persona.

    ONLY RETURN VALID JSON.

    JSON FORMAT:
    {{
      "persona_type": "short catchy archetype (1-3 words)",
      "details": {{
        "overview": "summary",
        "shopping_behavior": "text",
        "aesthetic_preferences": "text"
      }}
    }}

    User Questionnaire Answers:
    {json.dumps(questionnaire.answers, indent=2)}
    """

    # 3. Query Gemini
    raw = ask_gemini(prompt).strip()

    # Clean ```json fences if present
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    # 4. Parse JSON safely
    try:
        persona_data = json.loads(raw)
    except:
        raise HTTPException(500, f"Gemini returned invalid JSON: {raw}")

    # 5. Save or update Persona entry
    stmt2 = select(Persona).where(Persona.user_id == user.id)
    res2 = await db.execute(stmt2)
    existing = res2.scalar_one_or_none()

    if existing:
        existing.persona_type = persona_data["persona_type"]
        existing.persona_json = persona_data["details"]
    else:
        new_persona = Persona(
            user_id=user.id,
            persona_type=persona_data["persona_type"],
            persona_json=persona_data["details"]
        )
        db.add(new_persona)

    await db.commit()

    return {
        "status": "generated",
        "persona_type": persona_data["persona_type"],
        "details": persona_data["details"]
    }
