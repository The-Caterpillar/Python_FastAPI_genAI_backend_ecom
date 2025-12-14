from fastapi import HTTPException

from app.crud.cart import (
    get_cart_by_user,
    create_cart,
    get_cart_item,
    create_cart_item,
    update_cart_item_quantity,
    get_all_cart_items,
    remove_cart_item,
    clear_cart_items
)
from app.models.product import Product


async def add_product_to_cart(db, user_id: int, product_id: int, quantity: int):

    # 1. Validate product exists
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found.")

    # 2. Get or create cart
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        cart = await create_cart(db, user_id)

    # 3. Check if item already in cart
    existing_item = await get_cart_item(db, cart.id, product_id)

    if existing_item:
        new_qty = existing_item.quantity + quantity
        return await update_cart_item_quantity(db, existing_item, new_qty)

    # 4. Otherwise create new cart item
    return await create_cart_item(db, cart.id, product_id, quantity)


async def fetch_cart(db, user_id: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        return {"cart_id": None, "items": [], "cart_total": 0}

    items = await get_all_cart_items(db, cart.id)

    cart_total = 0
    item_list = []

    for item in items:
        product = item.product  # loaded by joinedload
        price = product.price
        total_for_item = price * item.quantity

        cart_total += total_for_item

        item_list.append({
            "item_id": item.id,
            "product_id": item.product_id,
            "product_name": product.name,
            "price": price,
            "quantity": item.quantity,
            "total": total_for_item,
            "added_at": str(item.added_at),
        })

    return {
        "cart_id": cart.id,
        "items": item_list,
        "cart_total": cart_total
    }


async def update_cart_product_quantity(db, user_id: int, product_id: int, quantity: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(404, "Cart not found.")

    item = await get_cart_item(db, cart.id, product_id)
    if not item:
        raise HTTPException(404, "Item not found in cart.")

    if quantity <= 0:
        await remove_cart_item(db, item)
        return {"message": "Item removed."}

    return await update_cart_item_quantity(db, item, quantity)


async def remove_product_from_cart(db, user_id: int, product_id: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        raise HTTPException(404, "Cart not found.")

    item = await get_cart_item(db, cart.id, product_id)
    if not item:
        raise HTTPException(404, "Item not found in cart.")

    await remove_cart_item(db, item)
    return {"message": "Item removed."}


async def clear_cart_service(db, user_id: int):
    cart = await get_cart_by_user(db, user_id)
    if not cart:
        return {"message": "Cart already empty."}

    await clear_cart_items(db, cart.id)
    return {"message": "Cart cleared."}
