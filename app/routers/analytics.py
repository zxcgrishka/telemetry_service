from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, database, worker, deps, models
from typing import Optional
import uuid

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/device/{device_id}", response_model=schemas.AnalysisTaskResponse)
async def trigger_device_analysis(
    device_id: uuid.UUID, 
    params: Optional[schemas.AnalyticsRequest] = None, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if params is None:
        params = schemas.AnalyticsRequest()

    task = worker.analyze_device_telemetry.delay(
        str(device_id), 
        params.start_time.isoformat() if params.start_time else None,
        params.end_time.isoformat() if params.end_time else None
    )
    await crud.create_analysis_task(db, task.id)
    return {"task_id": task.id}

@router.post("/user/{user_id}", response_model=schemas.AnalysisTaskResponse)
async def trigger_user_analysis(
    user_id: int, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    task = worker.analyze_user_telemetry.delay(user_id)
    await crud.create_analysis_task(db, task.id)
    return {"task_id": task.id}

@router.get("/task/{task_id}", response_model=schemas.AnalysisTaskResult)
async def get_task_status(
    task_id: str, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    db_task = await crud.get_analysis_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
