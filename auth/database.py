from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, select
from fastapi_users.db import SQLAlchemyUserDatabase

from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


class Base(DeclarativeBase):
    pass


class CustomUser(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    city = Column(String)

    is_active = True

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    def __init__(self, session, user_model):
        super().__init__(session, user_model)
        self.user_model = user_model

    async def get_by_email(self, email: str):
        result = await self.session.execute(
            select(self.user_model).where(self.user_model.email == email)
        )
        return result.scalars().first()

    async def get_by_login(self, login: str):
        result = await self.session.execute(
            select(self.user_model).where(self.user_model.login == login)
        )
        return result.scalars().first()


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomSQLAlchemyUserDatabase(session, CustomUser)