from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.persona import Persona
from app.models.questionnaire import UserQuestionnaire
from fastapi import HTTPException
import json
from app.utils.gemini_client import ask_gemini

from dotenv import load_dotenv
load_dotenv()

# create persona :
async def create_persona(db:AsyncSession, user):
    # 1. Fetch questionnaire answers
    stmt = select(UserQuestionnaire).where(UserQuestionnaire.user_id == user.id)
    result = await db.execute(stmt)
    questionnaire = result.scalar_one_or_none()

    if not questionnaire:
        raise HTTPException(400, "User has not completed the questionnaire.")

    # 2. Persona generation prompt for Gemini
    prompt = f"""
        You are an expert consumer-behavior analyst.
        Your task is to create a highly precise psychological + shopping persona based solely on the user’s questionnaire answers.

        Strict requirements:
        1. ONLY return VALID JSON. No commentary, no markdown.
        2. Every field must contain short phrases (maximum 4–5 words).
        3. Persona must feel unique, intuitive, and insight-driven.
        4. Avoid generic descriptions.

        JSON FORMAT:
        {{
        "persona_type": "short catchy archetype (1–3 words)",
        "details": {{
            "overview": "summary of personality",
            "shopping_style": "how they like to shop",
            "spending_style": "conservative, impulsive, balanced, etc.",
            "emotional_shopping_tendency": "likelihood of emotional buying",
            "brand_loyalty": "their loyalty tendencies",
            "deal_sensitivity": "how strongly they chase discounts",
            "risk_appetite": "risk behavior in purchases",
            "aesthetic_preferences": "design/style preferences",
            "decision_speed": "fast, slow, intuitive, etc.",
            "online_vs_offline_preference": "short phrase",
            "influence_factors": "what shapes their choices",
            "purchase_drivers": "key triggers for buying",
            "values_priority": "what they value most"
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

# get persona :
async def receive_persona(db:AsyncSession, user):
    # Fetch user persona:
    this_persona = select(Persona).where(Persona.user_id == user.id)
    result = await db.execute(this_persona)
    return result.scalar_one_or_none()