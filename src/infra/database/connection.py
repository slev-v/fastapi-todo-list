from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import AsyncContextManager, AsyncGenerator, Callable

from src.presentation.api.config import WebConfig


def create_session_maker(config: WebConfig) -> Callable[[], AsyncContextManager]:
    """
    Функция для создания фабрики сессий для работы с базой данных.

    :param config: Конфигурация, содержащая строку подключения к базе данных.
    :return: Фабрика сессий, которая может быть использована для создания асинхронных сессий.
    """
    db_uri = config.async_db_uri

    engine = create_async_engine(db_uri, echo=True, pool_size=15, max_overflow=15)

    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(
    session_maker: Callable[[], AsyncContextManager],
) -> AsyncGenerator:
    """
    Асинхронная функция для создания новой сессии.

    :param session_maker: Фабрика сессий.
    :yield: Асинхронная сессия для работы с базой данных.
    """
    async with session_maker() as session:
        yield session
