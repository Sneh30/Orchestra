from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from research_orchestrator.core.config import Settings, get_settings


def create_session_factory(settings: Settings) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=8,
        max_overflow=16,
        future=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False)


SessionFactory = create_session_factory(get_settings())


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        yield session

