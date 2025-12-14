from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.services.vector_index import search_similar
from app.crud.persona import receive_persona

from app.models.product import Product
from sqlalchemy import select, desc

from app.schemas.product import ProductOut


router = APIRouter()


def clean_products(products):
    cleaned = []
    for p in products:
        if p.currency not in ("INR", "USD", "EUR"):
            p.currency = "INR"
        cleaned.append(ProductOut.model_validate(p, from_attributes=True))
    return cleaned


@router.post("/recommend")
async def recommend_products(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    persona = await receive_persona(db, user)

    # ---------------- FALLBACK: NO PERSONA ----------------
    if not persona or not persona.embedding:
        result = await db.execute(
            select(Product).order_by(desc(Product.created_at)).limit(10)
        )
        fallback_products = result.scalars().all()
        return clean_products(fallback_products)

    # ---------------- FAISS SEARCH ----------------
    try:
        top_ids = search_similar(persona.embedding, top_k=10)
    except:
        top_ids = []

    if not top_ids:
        result = await db.execute(
            select(Product).order_by(desc(Product.created_at)).limit(10)
        )
        fallback_products = result.scalars().all()
        return clean_products(fallback_products)

    # ---------------- GET PRODUCTS FROM DB ----------------
    result = await db.execute(
        select(Product).where(Product.id.in_(top_ids))
    )
    products = result.scalars().all()

    if not products:
        result = await db.execute(
            select(Product).order_by(desc(Product.created_at)).limit(10)
        )
        fallback_products = result.scalars().all()
        return clean_products(fallback_products)

    # ---------------- SORT + CLEAN ----------------
    ordered = sorted(products, key=lambda p: top_ids.index(p.id))
    return clean_products(ordered)
