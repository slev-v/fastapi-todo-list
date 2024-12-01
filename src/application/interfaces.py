from abc import abstractmethod
from typing import Protocol

from src.domain.entities import Status


class TaskCreator(Protocol):
    @abstractmethod
    async def create_new_task(
        self, title: str, description: str, status: Status
    ) -> None: ...
