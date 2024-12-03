from fastapi import APIRouter, Depends, HTTPException, status

from src.domain.entities import Status
from src.application.interfaces import TaskCreator, TaskDeleter, TaskReader, TaskUpdater
from src.domain.exceptions import TaskNotFoundException
from src.presentation.api.di.stub import (
    provide_task_creator_stub,
    provide_task_deleter_stub,
    provide_task_reader_stub,
    provide_task_updater_stub,
)
from src.presentation.api.schemas import ErrorSchema
from src.presentation.api.task.schemas import (
    TaskRequest,
    CreateTaskResponse,
    TaskResponse,
    TaskListResponse,
)


router = APIRouter(prefix="/tasks")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Endpoint для создания новой задачи. Поле status может принимать значения 'todo', 'in_progress' или 'done'.",
    responses={
        status.HTTP_201_CREATED: {
            "model": CreateTaskResponse,
            "description": "Задача создана успешно",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации",
        },
    },
    summary="Создание новой задачи",
)
async def create_task(
    data: TaskRequest,
    interactor: TaskCreator = Depends(provide_task_creator_stub),
) -> CreateTaskResponse:
    task_uuid = await interactor.create_new_task(
        data.title, data.description, data.status
    )
    return CreateTaskResponse(uuid=task_uuid)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Endpoint для получения списка всех задач, с возможностью фильтрации. Поле status может принимать значения 'todo', 'in_progress' или 'done'.",
    responses={
        status.HTTP_200_OK: {"model": TaskListResponse, "description": "Список задач"},
    },
    summary="Получение списка всех задач, с возможностью фильтрации",
)
async def get_tasks(
    status: Status | None = None,
    interactor: TaskReader = Depends(provide_task_reader_stub),
) -> TaskListResponse:
    tasks = await interactor.get_all_tasks(status)
    return TaskListResponse(
        tasks=[
            TaskResponse(
                uuid=t.uuid, title=t.title, description=t.description, status=t.status
            )
            for t in tasks
        ]
    )


@router.get(
    "/{task_uuid}",
    status_code=status.HTTP_200_OK,
    description="Endpoint для получения задачи по UUID.",
    responses={
        status.HTTP_200_OK: {"model": TaskResponse, "description": "Задача"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
            "description": "Задача не найдена",
        },
    },
    summary="Получение задачи по UUID",
)
async def get_task_by_uuid(
    task_uuid: str, interactor: TaskReader = Depends(provide_task_reader_stub)
) -> TaskResponse:
    try:
        task = await interactor.get_task_by_uuid(task_uuid)

    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    return TaskResponse(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )


@router.put(
    "/{task_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Endpoint для обновления задачи по UUID. Поле status может принимать значения 'todo', 'in_progress' или 'done'.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Задача обновлена успешно",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
            "description": "Задача не найдена",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации",
        },
    },
    summary="Обновление задачи по UUID",
)
async def update_task(
    task_uuid: str,
    data: TaskRequest,
    interactor: TaskUpdater = Depends(provide_task_updater_stub),
) -> None:
    try:
        await interactor.update_task(
            task_uuid, data.title, data.description, data.status
        )
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete(
    "/{task_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Endpoint для удаления задачи по UUID.",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Задача удалена успешно",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorSchema,
            "description": "Задача не найдена",
        },
    },
    summary="Удаление задачи по UUID",
)
async def delete_task(
    task_uuid: str,
    interactor: TaskDeleter = Depends(provide_task_deleter_stub),
) -> None:
    try:
        await interactor.delete_task(task_uuid)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
