# app/api/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import acquire_db_session
from app.models.user import User
from app.core.security import hash_password

router = APIRouter()

@router.post("/create")
async def create_admin(email: str, password: str, db: AsyncSession = Depends(acquire_db_session)):
    # check if any admin already exists
    result = await db.execute(select(User).where(User.role == "admin"))
    admin_exists = result.scalar_one_or_none()

    if admin_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already exists"
        )

    # create new admin
    new_admin = User(
        email=email,
        password_hash=hash_password(password),
        role="admin"
    )

    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)

    return {"message": "Admin created successfully", "admin_id": new_admin.id}
