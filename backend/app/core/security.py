from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import acquire_db_session
from app.models.user import User

from app.models.user import UserRole

# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "CHANGE_THIS_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# JWT TOKEN CREATION
# ============================================================

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# HTTP BEARER AUTH (Fixes Swagger Authorization)
# ============================================================

bearer_scheme = HTTPBearer(auto_error=True)


# ============================================================
# CURRENT USER EXTRACTION (ASYNC)
# ============================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(acquire_db_session)
):
    token = credentials.credentials  # <-- the raw JWT string

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")

        if user_id_raw is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user_id = int(user_id_raw)

    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Query DB
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ============================================================
# ADMIN ROLE CHECK
# ============================================================

async def admin_required(current_user: User = Depends(get_current_user)):
    print("ADMIN CHECK:", current_user.id, current_user.email, current_user.role)
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user