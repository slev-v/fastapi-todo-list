from fastapi import APIRouter


router = APIRouter(prefix="/tasks")


@router.get("/")
async def test_route():
    return {"message": "Hello, World!"}
