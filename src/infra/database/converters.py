from src.domain.entities import Task as TaskEntity
from src.infra.database.models.task import Task as TaskModel


def convert_task_entity_to_task_model(task: TaskEntity) -> TaskModel:
    """
    Преобразование сущности задачи (TaskEntity) в модель задачи для базы данных (TaskModel).

    :param task: Сущность задачи.
    :return: Модель задачи для сохранения в базе данных.
    """
    return TaskModel(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )


def convert_task_model_to_task_entity(task: TaskModel) -> TaskEntity:
    """
    Преобразование модели задачи из базы данных (TaskModel) в сущность задачи (TaskEntity).

    :param task: Модель задачи из базы данных.
    :return: Сущность задачи.
    """
    return TaskEntity(
        uuid=task.uuid,
        title=task.title,
        description=task.description,
        status=task.status,
    )
