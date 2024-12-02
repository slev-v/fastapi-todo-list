from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities import Status
from src.domain.entities import Task as TaskEntity
from src.domain.exceptions import TaskNotFoundException
from src.infra.database.models.task import Task as TaskModel
from src.infra.database.converters import (
    convert_task_entity_to_task_model,
    convert_task_model_to_task_entity,
)


@dataclass
class BaseTaskRepo(ABC):
    """
    Абстрактный базовый репозиторий для работы с задачами.
    Определяет методы для создания, получения, обновления и удаления задач.
    """

    @abstractmethod
    async def create_new_task(self, task: TaskEntity) -> None: ...

    @abstractmethod
    async def get_task(self, task_uuid: str) -> TaskEntity: ...

    @abstractmethod
    async def get_tasks(self, status: Status | None) -> list[TaskEntity]: ...

    @abstractmethod
    async def update_task(self, task: TaskEntity) -> None: ...

    @abstractmethod
    async def delete_task(self, task_uuid: str) -> None: ...


@dataclass
class TaskRepo(BaseTaskRepo):
    _session: AsyncSession

    async def create_new_task(self, task: TaskEntity) -> None:
        """
        Создание новой задачи в базе данных.

        :param task: Сущность задачи, которую необходимо сохранить.
        """
        self._session.add(convert_task_entity_to_task_model(task))
        await self._session.commit()

    async def get_task(self, task_uuid: str) -> TaskEntity:
        """
        Получение задачи из базы данных по UUID.

        :param task_uuid: Уникальный идентификатор задачи.
        :return: Сущность задачи.
        :raises TaskNotFoundException: Если задача не найдена.
        """
        task = await self._session.get(TaskModel, task_uuid)
        if not task:
            raise TaskNotFoundException(task_uuid=task_uuid)
        return convert_task_model_to_task_entity(task)

    async def get_tasks(self, status: Status | None) -> list[TaskEntity]:
        """
        Получение всех задач с заданным статусом.

        :param status: Статус задач (может быть None, если нужно получить все задачи).
        :return: Список сущностей задач.
        """
        query = select(TaskModel)
        if status:
            query = query.where(TaskModel.status == status)

        result = await self._session.execute(query)
        tasks = result.scalars().all()
        return [convert_task_model_to_task_entity(task) for task in tasks]

    async def update_task(self, task: TaskEntity) -> None:
        """
        Обновление задачи в базе данных.

        :param task: Сущность задачи, содержащая обновленные данные.
        :raises TaskNotFoundException: Если задача не найдена.
        """
        task_model = await self._session.get(TaskModel, task.uuid)
        if not task_model:
            raise TaskNotFoundException(task_uuid=task.uuid)

        task_model.title = task.title
        task_model.description = task.description
        task_model.status = Status(task.status)

        await self._session.commit()

    async def delete_task(self, task_uuid: str) -> None:
        """
        Удаление задачи по UUID.

        :param task_uuid: Уникальный идентификатор задачи.
        """
        task = await self._session.get(TaskModel, task_uuid)

        await self._session.delete(task)
        await self._session.commit()
