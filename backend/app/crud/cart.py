from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import Cart
from app.models.cart_item import CartItem
from sqlalchemy.orm import joinedload


# --- CART CRUD --- #

async def get_cart_by_user(db: AsyncSession, user_id: int):
    stmt = select(Cart).where(Cart.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_cart(db: AsyncSession, user_id: int):
    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.commit()
    await db.refresh(cart)
    return cart


# --- CART ITEMS CRUD --- #

async def get_cart_item(db: AsyncSession, cart_id: int, product_id: int):
    stmt = select(CartItem).where(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_cart_item(db: AsyncSession, cart_id: int, product_id: int, quantity: int):
    item = CartItem(
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update_cart_item_quantity(db: AsyncSession, item: CartItem, quantity: int):
    item.quantity = quantity
    await db.commit()
    await db.refresh(item)
    return item


async def get_all_cart_items(db: AsyncSession, cart_id: int):
    stmt = (
        select(CartItem)
        .where(CartItem.cart_id == cart_id)
        .options(joinedload(CartItem.product))  # <-- IMPORTANT
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def remove_cart_item(db: AsyncSession, item: CartItem):
    await db.delete(item)
    await db.commit()


async def clear_cart_items(db: AsyncSession, cart_id: int):
    stmt = select(CartItem).where(CartItem.cart_id == cart_id)
    result = await db.execute(stmt)
    items = result.scalars().all()

    for item in items:
        await db.delete(item)

    await db.commit()
