from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import acquire_db_session as get_db
from app.core.security import get_current_user

from app.services.cart_service import add_product_to_cart, fetch_cart, remove_cart_item, remove_product_from_cart, update_cart_item_quantity, clear_cart_service, update_cart_product_quantity

router = APIRouter()


@router.post("/add")
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await add_product_to_cart(db, user.id, product_id, quantity)


@router.get("/view")
async def view_cart(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await fetch_cart(db, user.id)

@router.patch("/update")
async def update_quantity(
    product_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await update_cart_product_quantity(db, user.id, product_id, quantity)


@router.delete("/remove")
async def remove_item(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await remove_product_from_cart(db, user.id, product_id)


@router.delete("/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await clear_cart_service(db, user.id)

