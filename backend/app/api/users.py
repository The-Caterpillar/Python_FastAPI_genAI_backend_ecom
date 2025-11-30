from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.core.security import get_current_user
from app.db.session import acquire_db_session
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: UserUpdate,
    db: AsyncSession = Depends(acquire_db_session),
    current_user: User = Depends(get_current_user)
):
    # Convert provided fields only (exclude None and missing)
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(400, detail="No fields provided to update")

    # Apply updates
    for field, value in updates.items():
        setattr(current_user, field, value)

    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)

    return current_user