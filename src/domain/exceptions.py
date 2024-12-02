from dataclasses import dataclass


@dataclass(eq=False)
class TaskNotFoundException(Exception):
    task_uuid: str

    @property
    def message(self):
        return f"Task with uuid: {self.task_uuid} has not been found."
