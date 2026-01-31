from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config.config import config

db_engine = create_async_engine(
    config.RDS_URI,
    print("USING DATABASE:", config.RDS_URI),
    pool_size=1,
    max_overflow=0,
    pool_timeout=60,
    pool_pre_ping=True,
    echo=False,
    connect_args={
        "timeout": 60,
        "command_timeout": 60,
        "ssl": "require",
    },
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
