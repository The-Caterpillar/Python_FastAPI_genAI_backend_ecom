from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import hash_password


async def get_user_by_email(db: AsyncSession, email: str):
    """Fetch user by email asynchronously."""
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user):
    """Create a new user asynchronously."""
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return new_user
