from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from app.services.task_service import TaskService
from app.api.dependencies import get_task_service
from app.config.config import settings


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("/create")
async def create_task(
    file_id: int,
    task_type: str,
    smart_type_id: int,
    smart_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    token: str,
    ):
    if token != settings.token:
        raise HTTPException(status_code=403, detail="Invalid token")

    result = await task_service.execute_task(file_id, smart_type_id, smart_id, task_type)
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result.get('message', 'Unknown error occurred'))

    return result
