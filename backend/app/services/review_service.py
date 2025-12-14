from fastapi import HTTPException
from app.crud.review import (
    create_review,
    get_reviews_for_product,
    get_user_review_for_product
)

from app.models.product import Product


async def add_review(db, user_id: int, product_id: int, rating: int, comment: str):

    if rating < 1 or rating > 5:
        raise HTTPException(400, "Rating must be between 1 and 5.")

    # ensure product exists
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found.")

    # prevent multiple reviews from same user for same product
    existing = await get_user_review_for_product(db, user_id, product_id)
    if existing:
        raise HTTPException(400, "You already reviewed this product.")

    review = await create_review(db, user_id, product_id, rating, comment)
    return review


async def fetch_product_reviews(db, product_id: int):
    reviews = await get_reviews_for_product(db, product_id)

    if not reviews:
        return {
            "product_id": product_id,
            "reviews": [],
            "average_rating": 0
        }

    avg_rating = sum(r.rating for r in reviews) / len(reviews)

    return {
        "product_id": product_id,
        "average_rating": round(avg_rating, 2),
        "reviews": [
            {
                "review_id": r.id,
                "user_id": r.user_id,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": str(r.created_at)
            }
            for r in reviews
        ]
    }
