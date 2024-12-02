from fastapi import APIRouter, Depends, HTTPException

from src.application.interfaces import TaskCreator, TaskDeleter, TaskReader, TaskUpdater
from src.presentation.api.di.stub import (
    provide_task_creator_stub,
    provide_task_deleter_stub,
    provide_task_reader_stub,
    provide_task_updater_stub,
)
from src.presentation.api.task.schemas import (
    CreateTaskRequest,
    UpdateTaskRequest,
    TaskResponse,
    TaskListResponse,
)


router = APIRouter(prefix="/tasks")


@router.post("/")
async def create_task(
    data: CreateTaskRequest,
    interactor: TaskCreator = Depends(provide_task_creator_stub),
) -> None:
    await interactor.create_new_task(data.title, data.description, data.status)


@router.get("/")
async def get_tasks(
    interactor: TaskReader = Depends(provide_task_reader_stub),
) -> TaskListResponse:
    tasks = await interactor.get_all_tasks()
    return TaskListResponse(
        tasks=[
            TaskResponse(
                uuid=t.uuid, title=t.title, description=t.description, status=t.status
            )
            for t in tasks
        ]
    )


@router.get("/{task_uuid}")
async def get_task_by_uuid(
    uuid: str, interactor: TaskReader = Depends(provide_task_reader_stub)
) -> TaskResponse:
    task = await interactor.get_task_by_uuid(uuid)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )


@router.put("/{task_uuid}")
async def update_task(
    data: UpdateTaskRequest,
    interactor: TaskUpdater = Depends(provide_task_updater_stub),
) -> None:
    await interactor.update_task(data.uuid, data.title, data.description, data.status)


@router.delete("/{task_uuid}")
async def delete_task(
    uuid: str,
    interactor: TaskDeleter = Depends(provide_task_deleter_stub),
) -> None:
    await interactor.delete_task(uuid)
