from fastapi import APIRouter, Depends, HTTPException, status, Response

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
    CreateTaskRequest,
    UpdateTaskRequest,
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
            "description": "Задача создана успешно",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации",
        },
    },
    summary="Создание новой задачи",
    response_class=Response,
)
async def create_task(
    data: CreateTaskRequest,
    interactor: TaskCreator = Depends(provide_task_creator_stub),
) -> None:
    await interactor.create_new_task(data.title, data.description, data.status)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Endpoint для получения списка всех задач.",
    responses={
        status.HTTP_200_OK: {"model": TaskListResponse, "description": "Список задач"},
    },
    summary="Получение списка всех задач",
)
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
    uuid: str, interactor: TaskReader = Depends(provide_task_reader_stub)
) -> TaskResponse:
    try:
        task = await interactor.get_task_by_uuid(uuid)

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
    data: UpdateTaskRequest,
    interactor: TaskUpdater = Depends(provide_task_updater_stub),
) -> None:
    try:
        await interactor.update_task(
            data.uuid, data.title, data.description, data.status
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
    uuid: str,
    interactor: TaskDeleter = Depends(provide_task_deleter_stub),
) -> None:
    try:
        await interactor.delete_task(uuid)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
