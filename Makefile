DOCKER_COMPOSE = docker-compose
SERVICE_NAME = main-app
MIGRATE_CMD = alembic upgrade head
MIGRATION_DIR = /app/alembic.ini

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

rebuild:
	$(DOCKER_COMPOSE) up -d --build

migrate:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "alembic -c $(MIGRATION_DIR) upgrade head"

test:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) sh -c "pytest"
