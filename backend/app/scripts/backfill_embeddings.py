import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_maker
from app.models.product import Product
from app.services.embedding import get_embedding


async def backfill_embeddings():
    async with async_session_maker() as session:
        print("Fetching products without embeddings...")
        result = await session.execute(
            select(Product).where(Product.embedding.is_(None))
        )
        products = result.scalars().all()

        if not products:
            print("All products already have embeddings. Nothing to update.")
            return

        print(f"Found {len(products)} products without embeddings.")

        updated = 0
        for product in products:
            text = f"{product.name or ''} {product.short_description or ''} {product.long_description or ''}"
            embedding = get_embedding(text)
            product.embedding = embedding

            session.add(product)
            updated += 1

            # Commit every 20 products
            if updated % 20 == 0:
                await session.commit()
                print(f"Committed {updated} products so far...")

        # Final commit
        await session.commit()
        print(f"Backfill complete! Total updated: {updated}")


if __name__ == "__main__":
    asyncio.run(backfill_embeddings())
