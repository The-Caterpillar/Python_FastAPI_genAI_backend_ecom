from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import acquire_db_session as get_async_session
from app.api.dependencies import admin_required

from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud.product import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product,
)

router = APIRouter()


# -------------------------------
# CREATE PRODUCT (ADMIN ONLY)
# -------------------------------
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(admin_required),
):
    return await create_product(db, payload)


# -------------------------------
# LIST PRODUCTS (PUBLIC)
# -------------------------------
@router.get("/", response_model=list[ProductOut])
async def list_products_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: AsyncSession = Depends(get_async_session),
):
    return await get_all_products(db, skip=skip, limit=limit)


# -------------------------------
# GET PRODUCT BY ID (PUBLIC)
# -------------------------------
@router.get("/{product_id}", response_model=ProductOut)
async def get_product_route(
    product_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


# -------------------------------
# UPDATE PRODUCT (ADMIN ONLY)
# -------------------------------
@router.patch("/{product_id}", response_model=ProductOut)
async def update_product_route(
    product_id: int,
    payload: ProductUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(admin_required),
):
    product = await update_product(db, product_id, payload)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


# -------------------------------
# DELETE PRODUCT (ADMIN ONLY)
# -------------------------------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(admin_required),
):
    ok = await delete_product(db, product_id)
    if not ok:
        raise HTTPException(404, "Product not found")
    return None
