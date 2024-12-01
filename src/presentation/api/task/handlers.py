from fastapi import APIRouter, Depends, HTTPException

from src.application.interfaces import TaskCreator, TaskDeleter, TaskReader, TaskUpdater
from src.domain.entities import Status, Task
from src.presentation.api.di.stub import (
    provide_task_creator_stub,
    provide_task_deleter_stub,
    provide_task_reader_stub,
    provide_task_updater_stub,
)


router = APIRouter(prefix="/tasks")


@router.post("/")
async def create_task(
    title: str,
    description: str,
    status: Status,
    interactor: TaskCreator = Depends(provide_task_creator_stub),
) -> None:
    await interactor.create_new_task(title, description, status)


@router.get("/")
async def get_tasks(
    interactor: TaskReader = Depends(provide_task_reader_stub),
) -> list[Task]:
    tasks = await interactor.get_all_tasks()
    return tasks


@router.get("/{task_uuid}")
async def get_task_by_uuid(
    uuid: str, interactor: TaskReader = Depends(provide_task_reader_stub)
) -> Task:
    task = await interactor.get_task_by_uuid(uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_uuid}")
async def update_task(
    uuid: str,
    title: str,
    description: str,
    status: Status,
    interactor: TaskUpdater = Depends(provide_task_updater_stub),
) -> None:
    await interactor.update_task(uuid, title, description, status)


@router.delete("/{task_uuid}")
async def delete_task(
    uuid: str,
    interactor: TaskDeleter = Depends(provide_task_deleter_stub),
) -> None:
    await interactor.delete_task(uuid)
