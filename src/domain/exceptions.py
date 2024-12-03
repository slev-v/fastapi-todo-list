from dataclasses import dataclass


@dataclass(eq=False)
class TaskNotFoundException(Exception):
    task_uuid: str

    @property
    def message(self):
        return f"Задача с uuid: {self.task_uuid} не была найдена."
