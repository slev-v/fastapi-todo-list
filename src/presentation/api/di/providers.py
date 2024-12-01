from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.task import BaseTaskRepo, TaskRepo
from src.presentation.api.di.stub import (
    get_session_stub,
)


async def provide_task_repo(
    session: AsyncSession = Depends(get_session_stub),
) -> BaseTaskRepo:
    return TaskRepo(session)
