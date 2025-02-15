from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from src.infra.database.models.base import Base
from src.domain.entities import Status


class Task(Base):
    __tablename__ = "tasks"
    __mapper_args__ = {"eager_defaults": True}

    uuid: Mapped[str] = mapped_column(
        "uuid", primary_key=True, unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column("title", nullable=False)
    description: Mapped[str] = mapped_column("description", nullable=False)
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status_enum"), nullable=False
    )
