from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.task import BaseTaskRepo, TaskRepo
from src.presentation.api.di.stub import provide_session_stub, provide_task_repo_stub
from src.application.interfaces import TaskCreator, TaskReader
from src.application.interactors import TaskCreatorImpl, TaskReaderImpl


async def provide_task_repo(
    session: AsyncSession = Depends(provide_session_stub),
) -> BaseTaskRepo:
    return TaskRepo(session)


async def provide_task_creator(
    repo: BaseTaskRepo = Depends(provide_task_repo_stub),
) -> TaskCreator:
    return TaskCreatorImpl(repo)


async def provide_task_reader(
    repo: BaseTaskRepo = Depends(provide_task_repo_stub),
) -> TaskReader:
    return TaskReaderImpl(repo)
