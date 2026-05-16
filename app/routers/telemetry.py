from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List, Optional
from datetime import datetime
from .. import crud, schemas, database, deps, models

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.get("/{device_id}", response_model=List[schemas.TelemetryData])
async def get_telemetry(
    device_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    return await crud.get_telemetry_paginated(
        db, device_id=device_id, skip=skip, limit=limit, 
        start_time=start_time, end_time=end_time
    )

@router.post("/{device_id}", response_model=schemas.TelemetryData)
async def create_telemetry(
    device_id: uuid.UUID, 
    telemetry: schemas.TelemetryDataCreate, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    return await crud.create_telemetry(db, device_id, telemetry)
