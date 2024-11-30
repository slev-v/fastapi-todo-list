import os
from dataclasses import dataclass

HOST = "DB_HOST"
PORT = "DB_PORT"
LOGIN = "DB_LOGIN"
PASSWORD = "DB_PASSWORD"
DATABASE = "DB_NAME"


class ConfigParseError(ValueError):
    pass


@dataclass
class WebConfig:
    async_db_uri: str
    db_uri: str


def get_str_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_web_config() -> WebConfig:
    async_db_uri = f"postgresql+asyncpg://{get_str_env(LOGIN)}:{get_str_env(PASSWORD)}@{get_str_env(HOST)}:{get_str_env(PORT)}/{get_str_env(DATABASE)}"
    db_uri = f"postgresql://{get_str_env(LOGIN)}:{get_str_env(PASSWORD)}@{get_str_env(HOST)}:{get_str_env(PORT)}/{get_str_env(DATABASE)}"
    return WebConfig(
        async_db_uri=async_db_uri,
        db_uri=db_uri,
    )
