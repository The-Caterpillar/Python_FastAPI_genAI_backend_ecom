import numpy as np
import faiss
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


index = None
product_ids = []


async def build_faiss_index(db: AsyncSession):
    global index, product_ids

    # Fetch all products with embeddings
    result = await db.execute(
        select(Product.id, Product.embedding).where(Product.embedding.isnot(None))
    )
    rows = result.all()

    if not rows:
        print("No products with embeddings found.")
        return

    product_ids = [row[0] for row in rows]
    vectors = np.array([row[1] for row in rows], dtype="float32")

    dim = vectors.shape[1]   # embedding size

    # Build FAISS index
    index = faiss.IndexFlatL2(dim)  # L2 similarity
    index.add(vectors)

    print(f"FAISS index built: {len(product_ids)} vectors loaded.")


def search_similar(vector: list[float], top_k: int = 10):
    global index, product_ids

    if index is None:
        raise RuntimeError("FAISS index not built yet.")

    query = np.array([vector], dtype="float32")
    distances, indices = index.search(query, top_k)

    # Convert FAISS indices → actual product IDs
    result_ids = [product_ids[i] for i in indices[0]]

    return result_ids
