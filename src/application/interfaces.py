from abc import abstractmethod
from typing import Protocol

from src.domain.entities import Status, Task


class TaskCreator(Protocol):
    """
    Интерфейс для создания задач.
    """

    @abstractmethod
    async def create_new_task(
        self, title: str, description: str, status: Status
    ) -> str: ...


class TaskReader(Protocol):
    """
    Интерфейс для чтения задач.
    """

    @abstractmethod
    async def get_task_by_uuid(self, uuid: str) -> Task: ...

    @abstractmethod
    async def get_all_tasks(self, status: Status | None) -> list[Task]: ...


class TaskUpdater(Protocol):
    """
    Интерфейс для обновления задач.
    """

    @abstractmethod
    async def update_task(
        self, uuid: str, title: str, description: str, status: Status
    ) -> None: ...


class TaskDeleter(Protocol):
    """
    Интерфейс для удаления задач.
    """

    @abstractmethod
    async def delete_task(self, uuid: str) -> None: ...
