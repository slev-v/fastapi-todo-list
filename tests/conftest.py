import httpx
import pytest
from fastapi import FastAPI

from src.presentation.api.di.providers import (
    provide_task_deleter,
    provide_task_creator,
    provide_task_reader,
    provide_task_updater,
)
from src.presentation.api.di.stub import (
    provide_session_stub,
    provide_task_deleter_stub,
    provide_task_repo_stub,
    provide_task_creator_stub,
    provide_task_reader_stub,
    provide_task_updater_stub,
)
from src.presentation.api.task.handlers import router as task_router

from tests.mocks import MockTaskRepo, MockSession


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def mock_task_repo():
    return MockTaskRepo()


@pytest.fixture
def mock_session():
    return MockSession()


@pytest.fixture
async def client(mock_task_repo, mock_session):
    app = FastAPI(
        title="todo-list",
        debug=True,
    )

    app.dependency_overrides[provide_session_stub] = lambda: mock_session
    app.dependency_overrides[provide_task_repo_stub] = lambda: mock_task_repo
    app.dependency_overrides[provide_task_creator_stub] = provide_task_creator
    app.dependency_overrides[provide_task_reader_stub] = provide_task_reader
    app.dependency_overrides[provide_task_updater_stub] = provide_task_updater
    app.dependency_overrides[provide_task_deleter_stub] = provide_task_deleter

    app.include_router(task_router)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
