from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config import Config
from backend.infrustructure.models.event import Base

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope='session')
def faker() -> Faker:
    return Faker()


@pytest.fixture(scope='session')
def config() -> Config:
    return Config()


@pytest.fixture(scope='session')
async def session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
    database_uri = (
        f'postgresql+psycopg://{config.pg.user}:{config.pg.password}@{config.pg.host}:{config.pg.port}/{config.pg.db}'
    )
    engine = create_async_engine(database_uri)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return async_sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)


@pytest.fixture
async def session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        session.commit = AsyncMock()
        yield session
        await session.rollback()
