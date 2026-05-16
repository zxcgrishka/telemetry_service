from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import uuid
from . import models, schemas, security
from typing import List, Optional
from datetime import datetime

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def get_devices_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Device).filter(models.Device.user_id == user_id))
    return result.scalars().all()

async def create_device(db: AsyncSession, device: schemas.DeviceCreate):
    db_device = models.Device(user_id=device.user_id)
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def create_telemetry(db: AsyncSession, device_id: uuid.UUID, telemetry: schemas.TelemetryDataCreate):
    db_telemetry = models.TelemetryData(device_id=device_id, **telemetry.model_dump())
    db.add(db_telemetry)
    await db.commit()
    await db.refresh(db_telemetry)
    return db_telemetry

async def get_telemetry_paginated(
    db: AsyncSession, 
    device_id: uuid.UUID, 
    skip: int = 0, 
    limit: int = 100,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    query = select(models.TelemetryData).filter(models.TelemetryData.device_id == device_id)
    if start_time:
        query = query.filter(models.TelemetryData.timestamp >= start_time)
    if end_time:
        query = query.filter(models.TelemetryData.timestamp <= end_time)
    
    result = await db.execute(query.order_by(models.TelemetryData.timestamp.desc()).offset(skip).limit(limit))
    return result.scalars().all()

async def create_analysis_task(db: AsyncSession, task_id: str):
    db_task = models.AnalysisTask(task_id=task_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_analysis_task(db: AsyncSession, task_id: str):
    result = await db.execute(select(models.AnalysisTask).filter(models.AnalysisTask.task_id == task_id))
    return result.scalars().first()

def get_telemetry_for_device(db: Session, device_id: uuid.UUID, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    query = db.query(models.TelemetryData).filter(models.TelemetryData.device_id == device_id)
    if start_time:
        query = query.filter(models.TelemetryData.timestamp >= start_time)
    if end_time:
        query = query.filter(models.TelemetryData.timestamp <= end_time)
    return query.all()

def update_analysis_task(db: Session, task_id: str, status: str, result: Optional[dict] = None):
    db_task = db.query(models.AnalysisTask).filter(models.AnalysisTask.task_id == task_id).first()
    if db_task:
        db_task.status = status
        db_task.result = result
        db.commit()
        db.refresh(db_task)
    return db_task
