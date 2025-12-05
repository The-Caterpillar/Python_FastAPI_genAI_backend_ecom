from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    product.currency = product.currency.value
    return product


async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return None

    for field, value in product_in.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    product.currency = product.currency.value
    return product


async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return False

    await db.delete(product)
    await db.commit()
    return True


async def get_all_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Product).offset(skip).limit(limit)
    )
    products = result.scalars().all()
    for p in products:
        if hasattr(p.currency, "value"):
            p.currency = p.currency.value
    return products



async def search_products(db:AsyncSession, name:str):
    stmt = select(Product).where(Product.name.like(f"%{name}%"))
    result = await db.execute(stmt)
    products = result.scalars().all()
    for p in products:
        if hasattr(p.currency,"value"):
            p.currency = p.currency.value
    return products
