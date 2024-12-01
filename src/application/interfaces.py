from abc import abstractmethod
from typing import Protocol

from src.domain.entities import Status, Task


class TaskCreator(Protocol):
    @abstractmethod
    async def create_new_task(
        self, title: str, description: str, status: Status
    ) -> None: ...


class TaskReader(Protocol):
    @abstractmethod
    async def get_task_by_uuid(self, uuid: str) -> Task | None: ...

    @abstractmethod
    async def get_all_tasks(self) -> list[Task]: ...
