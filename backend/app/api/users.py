from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserOut, UserCreate
from app.core.security import get_current_user
from app.db.session import acquire_db_session
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: UserCreate,
    db: AsyncSession = Depends(acquire_db_session),
    current_user: User = Depends(get_current_user)
):
    # Partial update: only update fields that are provided (UserCreate requires name/password though;
    # for demo simplicity we use same schema
    # Here we set them directly (safe for demo)
    current_user.name = payload.name
    current_user.phone = payload.phone
    current_user.address = payload.address
    current_user.dob = payload.dob

    db.add(current_user)
    await db.flush()
    await db.refresh(current_user)
    return current_user