from src.domain.entities import Task as TaskEntity
from src.infra.database.models.task import Task as TaskModel


def convert_task_entity_to_task_model(task: TaskEntity) -> TaskModel:
    return TaskModel(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )


def convert_task_model_to_task_entity(task: TaskModel) -> TaskEntity:
    return TaskEntity(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )
