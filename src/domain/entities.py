from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    uuid: str
    title: str
    description: str
    status: Status
