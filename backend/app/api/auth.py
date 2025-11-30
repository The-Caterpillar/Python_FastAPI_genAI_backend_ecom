from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin, UserOut
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.db.session import acquire_db_session

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(acquire_db_session)
):
    # Check if user already exists
    existing_user = await get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Create user (includes Name, Phone, Address, DOB)
    new_user = await create_user(db, data)

    return new_user


@router.post("/login")
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(acquire_db_session)
):
    # Fetch user
    user = await get_user_by_email(db, data.email)
    if not user :
        raise HTTPException(status_code=400, detail="Invalid credentials(username)")

    # Verify password
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password!!")

    # Create JWT token (subject *must be a string*)
    token = create_access_token({"sub": str(user.id)})

    return {
        "message" : "Welcome Cutie",
        "access_token": token,
        "token_type": "bearer"
    }
