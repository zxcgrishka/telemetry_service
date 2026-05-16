from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Auth schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Device schemas
class DeviceBase(BaseModel):
    user_id: int

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# Telemetry schemas
class TelemetryDataBase(BaseModel):
    x: float
    y: float
    z: float

class TelemetryDataCreate(TelemetryDataBase):
    pass

class TelemetryData(TelemetryDataBase):
    id: int
    device_id: UUID
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

# Analytics schemas
class AnalyticsRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {}
            ]
        }
    )

class AnalysisTaskResponse(BaseModel):
    task_id: str

class AnalysisTaskResult(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
