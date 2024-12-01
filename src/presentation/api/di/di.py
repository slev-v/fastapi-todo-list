from functools import partial

from fastapi import FastAPI

from src.infra.database.connection import create_session_maker, new_session
from src.presentation.api.config import WebConfig
from src.presentation.api.di.providers import (
    provide_task_repo,
    provide_task_creator,
    provide_task_reader,
)
from src.presentation.api.di.stub import (
    provide_session_stub,
    provide_task_repo_stub,
    provide_task_creator_stub,
    provide_task_reader_stub,
)


def init_dependencies(app: FastAPI, config: WebConfig) -> None:
    session_maker = create_session_maker(config)
    app.dependency_overrides[provide_session_stub] = partial(new_session, session_maker)
    app.dependency_overrides[provide_task_repo_stub] = provide_task_repo
    app.dependency_overrides[provide_task_creator_stub] = provide_task_creator
    app.dependency_overrides[provide_task_reader_stub] = provide_task_reader
