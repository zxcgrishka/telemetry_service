import statistics
import uuid
from celery import Celery
from .config import settings
from .database import SessionLocal
from . import crud, models
from typing import Optional, List
from datetime import datetime

celery = Celery(__name__)
celery.conf.broker_url = settings.REDIS_URL
celery.conf.result_backend = settings.REDIS_URL

def calculate_metrics(data: List[float]):
    if not data:
        return None
    return {
        "min": min(data),
        "max": max(data),
        "count": len(data),
        "sum": sum(data),
        "median": statistics.median(data)
    }

@celery.task(bind=True)
def analyze_device_telemetry(self, device_id_str: str, start_time_str: Optional[str] = None, end_time_str: Optional[str] = None):
    task_id = self.request.id
    db = SessionLocal()
    try:
        device_id = uuid.UUID(device_id_str)
        start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
        end_time = datetime.fromisoformat(end_time_str) if end_time_str else None
        
        telemetry_records = crud.get_telemetry_for_device(db, device_id, start_time, end_time)
        
        if not telemetry_records:
            crud.update_analysis_task(db, task_id, "SUCCESS", {"message": "No data found"})
            return
        
        x_vals = [r.x for r in telemetry_records]
        y_vals = [r.y for r in telemetry_records]
        z_vals = [r.z for r in telemetry_records]
        
        result = {
            "x": calculate_metrics(x_vals),
            "y": calculate_metrics(y_vals),
            "z": calculate_metrics(z_vals)
        }
        
        crud.update_analysis_task(db, task_id, "SUCCESS", result)
    except Exception as e:
        crud.update_analysis_task(db, task_id, "FAILURE", {"error": str(e)})
        raise e
    finally:
        db.close()

@celery.task(bind=True)
def analyze_user_telemetry(self, user_id: int):
    task_id = self.request.id
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            crud.update_analysis_task(db, task_id, "FAILURE", {"error": "User not found"})
            return
        
        device_results = {}
        all_x, all_y, all_z = [], [], []
        
        for device in user.devices:
            telemetry_records = crud.get_telemetry_for_device(db, device.id)
            if telemetry_records:
                x_vals = [r.x for r in telemetry_records]
                y_vals = [r.y for r in telemetry_records]
                z_vals = [r.z for r in telemetry_records]
                
                device_results[f"device_{str(device.id)}"] = {
                    "x": calculate_metrics(x_vals),
                    "y": calculate_metrics(y_vals),
                    "z": calculate_metrics(z_vals)
                }
                
                all_x.extend(x_vals)
                all_y.extend(y_vals)
                all_z.extend(z_vals)
        
        result = {
            "aggregated": {
                "x": calculate_metrics(all_x),
                "y": calculate_metrics(all_y),
                "z": calculate_metrics(all_z)
            },
            "by_device": device_results
        }
        
        crud.update_analysis_task(db, task_id, "SUCCESS", result)
    except Exception as e:
        crud.update_analysis_task(db, task_id, "FAILURE", {"error": str(e)})
        raise e
    finally:
        db.close()
