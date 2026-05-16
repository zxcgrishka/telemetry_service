from fastapi import FastAPI
from .routers import users, devices, telemetry, analytics

app = FastAPI(title="Telemetry Service")

app.include_router(users.router)
app.include_router(devices.router)
app.include_router(telemetry.router)
app.include_router(analytics.router)

@app.get("/")
async def root():
    return {"message": "Telemetry Service API is running"}
