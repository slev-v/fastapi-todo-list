from functools import partial

from fastapi import FastAPI

from src.infra.database.connection import create_session_maker, new_session
from src.presentation.api.config import WebConfig
from src.presentation.api.di.providers import (
    provide_task_repo,
)
from src.presentation.api.di.stub import (
    get_session_stub,
    provide_task_repo_stub,
)


def init_dependencies(app: FastAPI, config: WebConfig) -> None:
    session_maker = create_session_maker(config)
    app.dependency_overrides[get_session_stub] = partial(new_session, session_maker)
    app.dependency_overrides[provide_task_repo_stub] = provide_task_repo
