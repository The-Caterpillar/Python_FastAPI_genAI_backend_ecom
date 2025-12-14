from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import json

from app.models.persona import Persona
from app.models.product import Product
from app.utils.gemini_client import ask_gemini


async def generate_product_recommendations(db: AsyncSession, user):
    # 1. Fetch user persona
    stmt = select(Persona).where(Persona.user_id == user.id)
    result = await db.execute(stmt)
    persona = result.scalar_one_or_none()

    if not persona:
        raise HTTPException(400, "Persona not found for this user.")

    # 2. Fetch all products
    stmt = select(Product)
    result = await db.execute(stmt)
    products = result.scalars().all()

    if not products:
        raise HTTPException(400, "No products available.")

    # Convert products to a simple JSON list
    products_list = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.long_description,
        }
        for p in products
    ]

    # 3. Build GenAI prompt
    prompt = f"""
    You are an expert ecommerce recommendation system.

    Your job:
    Analyze:
    1. The user's persona (psychology + shopping behavior)
    2. The available product list (name + description)

    And select the products most aligned with the user's:
    - shopping_style
    - spending_style
    - emotional_shopping_tendency
    - aesthetic_preferences
    - purchase_drivers
    - values_priority

    STRICT RULES:
    - ONLY return VALID JSON.
    - Provide a short explanation (max 15-20 words) for why each product is suggested.
    - Recommend all products that match the persona and give them a score(1-100).
    - Arrange the products from highest to lowest recommendation score
    - Do NOT add commentary outside JSON.

    JSON FORMAT:
    {{
        "recommendations": [
            {{
                "product_id": <int>,
                "reason": "short reason",
                "recommendation_score": "score"
            }}
        ]
    }}

    User Persona:
    {json.dumps(persona.persona_json, indent=2)}

    Product List:
    {json.dumps(products_list, indent=2)}
    """

    # 4. Query Gemini
    raw = ask_gemini(prompt).strip()

    # Cleanup fences
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    try:
        data = json.loads(raw)
    except:
        raise HTTPException(500, f"Gemini returned invalid JSON: {raw}")

    return data
