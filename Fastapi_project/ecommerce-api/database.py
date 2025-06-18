from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

DATABASE_URL = "sqlite+aiosqlite:///ecommerce.db"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create Session Factory
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
