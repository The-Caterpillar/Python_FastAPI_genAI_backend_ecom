from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review

async def create_review(db: AsyncSession, user_id: int, product_id: int, rating: int, comment: str):
    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def get_reviews_for_product(db: AsyncSession, product_id: int):
    stmt = select(Review).where(Review.product_id == product_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_review_for_product(db: AsyncSession, user_id: int, product_id: int):
    stmt = select(Review).where(
        Review.user_id == user_id,
        Review.product_id == product_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
