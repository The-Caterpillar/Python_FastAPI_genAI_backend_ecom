from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user
from app.services.review_service import add_review, fetch_product_reviews

router = APIRouter()


@router.post("/add")
async def post_review(
    product_id: int,
    rating: int = Query(..., ge=1, le=5, description="Rating (1-5)"),
    comment: str = Query("", example="Great!"),
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    return await add_review(db, user.id, product_id, rating, comment)


@router.get("/product/{product_id}")
async def get_reviews(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await fetch_product_reviews(db, product_id)
