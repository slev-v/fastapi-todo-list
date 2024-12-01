from fastapi import APIRouter, Depends

from src.application.interfaces import TaskCreator
from src.domain.entities import Status
from src.presentation.api.di.stub import provide_task_creator_stub


router = APIRouter(prefix="/tasks")


@router.get("/")
async def test_route():
    return {"message": "Hello, World!"}


@router.post("/")
async def create_task(
    title: str,
    description: str,
    status: Status,
    interactor: TaskCreator = Depends(provide_task_creator_stub),
) -> None:
    await interactor.create_new_task(title, description, status)
