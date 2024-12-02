from uuid import uuid4

from src.application.interfaces import TaskCreator, TaskDeleter, TaskReader, TaskUpdater
from src.domain.entities import Task, Status
from src.infra.database.repositories.task import BaseTaskRepo


class TaskCreatorImpl(TaskCreator):
    """
    Класс для создания задач в системе.
    Имплементирует интерфейс TaskCreator.
    """

    def __init__(self, task_repo: BaseTaskRepo) -> None:
        """
        Инициализация класса.

        :param task_repo: Репозиторий для работы с задачами в базе данных.
        """
        self._task_repo = task_repo

    async def create_new_task(
        self, title: str, description: str, status: Status
    ) -> str:
        """
        Создание новой задачи.

        :param title: Заголовок задачи.
        :param description: Описание задачи.
        :param status: Статус задачи.
        """
        uuid = str(uuid4())
        task = Task(uuid=uuid, title=title, description=description, status=status)
        await self._task_repo.create_new_task(task)
        return uuid


class TaskReaderImpl(TaskReader):
    """
    Класс для получения задач из системы.
    Имплементирует интерфейс TaskReader.
    """

    def __init__(self, task_repo: BaseTaskRepo) -> None:
        """
        Инициализация класса.

        :param task_repo: Репозиторий для работы с задачами в базе данных.
        """
        self._task_repo = task_repo

    async def get_task_by_uuid(self, uuid: str) -> Task:
        """
        Получение задачи по уникальному идентификатору.

        :param uuid: Уникальный идентификатор задачи.
        :return: Задача, соответствующая переданному uuid.
        """
        return await self._task_repo.get_task(uuid)

    async def get_all_tasks(self, status: Status | None) -> list[Task]:
        """
        Получение всех задач по статусу.

        :param status: Статус задач (может быть None, если нужно получить все задачи).
        :return: Список задач с заданным статусом.
        """
        return await self._task_repo.get_tasks(status)


class TaskUpdaterImpl(TaskUpdater):
    """
    Класс для обновления задач в системе.
    Имплементирует интерфейс TaskUpdater.
    """

    def __init__(self, task_repo: BaseTaskRepo) -> None:
        """
        Инициализация класса.

        :param task_repo: Репозиторий для работы с задачами в базе данных.
        """
        self._task_repo = task_repo

    async def update_task(
        self, uuid: str, title: str, description: str, status: Status
    ) -> None:
        """
        Обновление данных задачи.

        :param uuid: Уникальный идентификатор задачи.
        :param title: Новый заголовок задачи.
        :param description: Новое описание задачи.
        :param status: Новый статус задачи.
        """
        task = Task(uuid=uuid, title=title, description=description, status=status)
        await self._task_repo.update_task(task)


class TaskDeleterImpl(TaskDeleter):
    """
    Класс для удаления задач из системы.
    Имплементирует интерфейс TaskDeleter.
    """

    def __init__(self, task_repo: BaseTaskRepo) -> None:
        """
        Инициализация класса.

        :param task_repo: Репозиторий для работы с задачами в базе данных.
        """
        self._task_repo = task_repo

    async def delete_task(self, uuid: str) -> None:
        """
        Удаление задачи по уникальному идентификатору.

        :param uuid: Уникальный идентификатор задачи.
        """
        await self._task_repo.delete_task(uuid)
