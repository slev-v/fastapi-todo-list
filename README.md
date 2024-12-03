# FastAPI To-Do List

> API-сервис для управления списком задач (To-Do List), созданный с использованием FastAPI и PostgreSQL.
Этот проект позволяет создавать, просматривать, обновлять и удалять задачи, а также фильтровать их по статусу.

## Функциональность

- Создание задачи: POST `/tasks/`
- Получение списка задач с фильтрацией по статусу: GET `/tasks/`
- Получение информации о задаче по ID: GET `/tasks/{task_id}/`
- Обновление задачи: PUT `/tasks/{task_id}/`
- Удаление задачи: DELETE `/tasks/{task_id}/`

## Требования

- Python 3.10+
- Docker и Docker Compose
- PostgreSQL

## Локальный запуск

1. **Клонирование репозитория**:

```bash
git clone https://github.com/slev-v/fastapi-todo-list
cd fastapi-todo-list
```

2. **Настройка переменных окружения:** Создайте файл .env в корне проекта и добавьте настройки:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. **Запуск приложения**: Убедитесь, что Docker установлен, затем выполните:

```bash
docker-compose up -d
```

4. **Проведение миграций**:

```bash
docker-compose exec main-app sh -c "alembic upgrade head"
```

5. **Доступ к приложению**: Открыть в браузере: <http://localhost:8000/docs>

## Развертывание на сервере

1. **Убедитесь, что Docker и Docker Compose установлены**:

```bash
apt update
apt install docker.io docker-compose -y
```

2. **Скопируйте файлы проекта на сервер**:

```bash
git clone https://github.com/slev-v/fastapi-todo-list
cd fastapi-todo-list
```

3. **Настройка переменных окружения**: Отредактируйте файл `.env` с настройками для production.

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

4. **Запуск приложения**:

```bash
docker-compose up -d
```

5. **Проведение миграций**:

```bash
docker-compose exec main-app sh -c "alembic upgrade head
```

6. **Открытие порта, в брандмауэре сервера**:

```bash
sudo ufw allow 8000
```

7. **Проверка работы**: API будет доступен по указанному вами домену или IP-адресу, например: `http://<ваш_домен>:8000/docs`.

## Примеры запросов к API

### Создание задачи

```bash
curl -X POST http://localhost:8000/tasks/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты",
  "description": "Список: молоко, хлеб, сыр",
  "status": "todo"
}'
```

### Получение списка задач

```bash
curl -X GET "http://localhost:8000/tasks/?status=todo" \
-H "accept: application/json"
```

### Получение задачи по ID

```bash
curl -X GET http://localhost:8000/tasks/1 \
-H "accept: application/json"
```

### Обновление задачи

```bash
curl -X PUT http://localhost:8000/tasks/1 \
-H "Content-Type: application/json" \
-d '{
  "title": "Купить продукты и напитки",
  "description": "Список: молоко, хлеб, сыр, сок",
  "status": "in_progress"
}'
```

### Удаление задачи

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Тестирование

Для запуска тестов выполните:

```bash
pytest
```

## Документация

Автоматическая документация доступна по адресу:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
