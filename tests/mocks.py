from typing import List

from src.domain.entities import Task as TaskEntity, Status
from src.domain.exceptions import TaskNotFoundException


class MockTaskRepo:
    def __init__(self):
        self._tasks: List[TaskEntity] = []

    async def create_new_task(self, task: TaskEntity) -> None:
        self._tasks.append(task)

    async def get_task(self, task_uuid: str) -> TaskEntity:
        for task in self._tasks:
            if task.uuid == task_uuid:
                return task
        raise TaskNotFoundException(task_uuid=task_uuid)

    async def get_tasks(self, status: Status | None = None) -> List[TaskEntity]:
        if status is None:
            return self._tasks
        return [task for task in self._tasks if task.status == status]

    async def update_task(self, task: TaskEntity) -> None:
        for idx, existing_task in enumerate(self._tasks):
            if existing_task.uuid == task.uuid:
                self._tasks[idx] = task
                return
        raise TaskNotFoundException(task_uuid=task.uuid)

    async def delete_task(self, task_uuid: str) -> None:
        for idx, task in enumerate(self._tasks):
            if task.uuid == task_uuid:
                del self._tasks[idx]
                return
        raise TaskNotFoundException(task_uuid=task_uuid)


class MockSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass
