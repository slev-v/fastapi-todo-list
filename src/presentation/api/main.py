from fastapi import FastAPI

from src.presentation.api.config import load_web_config
from src.presentation.api.di.di import init_dependencies
from src.presentation.api.task.handlers import router as task_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="todo-list",
        debug=True,
    )

    config = load_web_config()

    init_dependencies(app, config)

    app.include_router(task_router)

    return app
