from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import Task as TaskEntity
from src.domain.exceptions import TaskNotFoundException
from src.infra.database.models.task import Status, Task as TaskModel
from src.infra.database.converters import (
    convert_task_entity_to_task_model,
    convert_task_model_to_task_entity,
)


@dataclass
class BaseTaskRepo(ABC):
    @abstractmethod
    async def create_new_task(self, task: TaskEntity) -> None: ...

    @abstractmethod
    async def get_task(self, task_uuid: str) -> TaskEntity: ...

    @abstractmethod
    async def get_tasks(self) -> list[TaskEntity]: ...

    @abstractmethod
    async def update_task(self, task: TaskEntity) -> None: ...

    @abstractmethod
    async def delete_task(self, task_uuid: str) -> None: ...


@dataclass
class TaskRepo(BaseTaskRepo):
    _session: AsyncSession

    async def create_new_task(self, task: TaskEntity) -> None:
        self._session.add(convert_task_entity_to_task_model(task))
        await self._session.commit()

    async def get_task(self, task_uuid: str) -> TaskEntity:
        task = await self._session.get(TaskModel, task_uuid)
        if not task:
            raise TaskNotFoundException(task_uuid=task_uuid)
        return convert_task_model_to_task_entity(task)

    async def get_tasks(self) -> list[TaskEntity]:
        result = await self._session.execute(select(TaskModel))
        tasks = result.scalars().all()
        return [convert_task_model_to_task_entity(task) for task in tasks]

    async def update_task(self, task: TaskEntity) -> None:
        task_model = await self._session.get(TaskModel, task.uuid)
        if not task_model:
            raise TaskNotFoundException(task_uuid=task.uuid)

        task_model.title = task.title
        task_model.description = task.description
        task_model.status = Status(task.status)

        await self._session.commit()

    async def delete_task(self, task_uuid: str) -> None:
        task = await self._session.get(TaskModel, task_uuid)

        await self._session.delete(task)
        await self._session.commit()
