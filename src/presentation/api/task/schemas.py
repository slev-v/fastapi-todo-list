from pydantic import BaseModel, Field

from src.domain.entities import Status


class TaskRequest(BaseModel):
    title: str = Field(..., title="Task title")
    description: str = Field(..., title="Task description")
    status: Status = Field(..., title="Task status")


class CreateTaskResponse(BaseModel):
    uuid: str = Field(..., title="Task UUID")


class TaskResponse(BaseModel):
    uuid: str = Field(..., title="Task UUID")
    title: str = Field(..., title="Task title")
    description: str = Field(..., title="Task description")
    status: Status = Field(..., title="Task status")


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse] = Field(..., title="List of tasks")
