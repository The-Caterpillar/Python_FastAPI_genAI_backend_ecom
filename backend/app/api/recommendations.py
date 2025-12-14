from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.crud.recommendations import generate_product_recommendations


router = APIRouter()
# router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/products")
async def recommend_products(
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Generate product recommendations for the logged-in user
    based on:
        - user persona
        - product list in the database
    """
    recommendations = await generate_product_recommendations(db, user)
    return recommendations
