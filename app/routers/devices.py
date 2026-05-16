from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas, database, deps, models

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=List[schemas.Device])
async def get_devices(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    return await crud.get_devices_by_user(db, user_id=current_user.id)

@router.post("/", response_model=schemas.Device)
async def create_device(
    device: schemas.DeviceCreate, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    if device.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create a device for another user")
        
    user = await crud.get_user(db, device.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.create_device(db, device)
