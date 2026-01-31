from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config.config import config

db_engine = create_async_engine(
    config.RDS_URI,
    poolclass=NullPool,   # ← this disables SQLAlchemy pooling
    pool_pre_ping=True,
    echo=False
)
async_session_maker = async_sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def acquire_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_maker()
    try:
        yield session
    except Exception as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
 
 