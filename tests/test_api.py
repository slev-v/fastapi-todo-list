import pytest


@pytest.mark.anyio
async def test_create_task(client, mock_task_repo):
    response = await client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "todo",
        },
    )
    assert response.status_code == 201

    tasks = await mock_task_repo.get_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "This is a test task"
    assert tasks[0].status.value == "todo"
    assert tasks[0].uuid == response.json()["uuid"]


@pytest.mark.anyio
async def test_create_task_invalid_status(client, mock_task_repo):
    response = await client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "invalid",
        },
    )
    assert response.status_code == 422

    tasks = await mock_task_repo.get_tasks()
    assert len(tasks) == 0


@pytest.mark.anyio
async def test_get_task_by_uuid(client):
    create_task = await client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "status": "todo",
        },
    )
    task_uuid = create_task.json()["uuid"]

    response = await client.get(f"/tasks/{task_uuid}")

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == task_uuid
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == "todo"


@pytest.mark.anyio
async def test_get_task_by_invalid_uuid(client):
    response = await client.get("/tasks/invalid-uuid")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_filter_tasks_by_status(client, mock_task_repo):
    response = await client.post(
        "/tasks/",
        json={"title": "Task 1", "description": "Test 1", "status": "in_progress"},
    )
    uuid1 = response.json()["uuid"]

    response = await client.post(
        "/tasks/",
        json={"title": "Task 2", "description": "Test 2", "status": "done"},
    )
    uuid2 = response.json()["uuid"]

    response = await client.get("/tasks/?status=in_progress")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Task 1"
    assert data["tasks"][0]["uuid"] == uuid1

    response = await client.get("/tasks/?status=done")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Task 2"
    assert data["tasks"][0]["uuid"] == uuid2
