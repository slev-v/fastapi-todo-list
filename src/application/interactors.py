from uuid import uuid4

from src.application.interfaces import TaskCreator, TaskReader, TaskUpdater
from src.domain.entities import Task, Status
from src.infra.database.repositories.task import BaseTaskRepo


class TaskCreatorImpl(TaskCreator):
    def __init__(self, task_repo: BaseTaskRepo) -> None:
        self._task_repo = task_repo

    async def create_new_task(
        self, title: str, description: str, status: Status
    ) -> None:
        uuid = str(uuid4())
        task = Task(uuid=uuid, title=title, description=description, status=status)
        await self._task_repo.create_new_task(task)


class TaskReaderImpl(TaskReader):
    def __init__(self, task_repo: BaseTaskRepo) -> None:
        self._task_repo = task_repo

    async def get_task_by_uuid(self, uuid: str) -> Task | None:
        return await self._task_repo.get_task(uuid)

    async def get_all_tasks(self) -> list[Task]:
        return await self._task_repo.get_tasks()


class TaskUpdaterImpl(TaskUpdater):
    def __init__(self, task_repo: BaseTaskRepo) -> None:
        self._task_repo = task_repo

    async def update_task(
        self, uuid: str, title: str, description: str, status: Status
    ) -> None:
        task = Task(uuid=uuid, title=title, description=description, status=status)
        await self._task_repo.update_task(task)
