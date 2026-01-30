from sqlalchemy.orm import Session
from models import SensorMetric, DailyMetrics
from schemas import SensorDataCreate
from datetime import datetime, date
import json
import httpx
from config import settings

def create_sensor_metric(db: Session, metric: SensorDataCreate, user_id: str):
    """
    Store a raw sensor reading in the database.
    """
    db_metric = SensorMetric(
        user_id=user_id,
        timestamp=metric.timestamp,
        data_type=metric.data_type,
        payload=json.dumps(metric.payload)
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

async def aggregate_and_forward(db: Session, user_id: str):
    """
    aggregates metrics for today and forwards to Backend3.
    """
    today = date.today()
    
    # 1. Simple Aggregation (Proof of concept: count movements)
    # In a real app, you'd do complex SQL queries here
    # For now, let's just count how many 'movement' entries we have today
    
    # This is a placeholer logic. Real logic depends on payload structure.
    # We update the DailyMetrics table which we already have.
    
    daily_metric = db.query(DailyMetrics).filter(
        DailyMetrics.user_id == user_id,
        DailyMetrics.date == today
    ).first()

    if not daily_metric:
        daily_metric = DailyMetrics(user_id=user_id, date=today)
        db.add(daily_metric)
    
    # Update aggregation timestamp
    daily_metric.updated_at = datetime.now()
    
    # Example: Recalculate based on recent sensor data (if we were doing that)
    # For now we just trust the client sent us screen_time/tasks via the daily endpoint
    # OR we can say "we are triggering a sync".
    
    db.commit()
    db.refresh(daily_metric)

    # 2. Forward to Backend3
    if not settings.BACKEND3_URL:
        print("Backend3 URL not configured, skipping forward.")
        return {"status": "skipped", "reason": "no_url"}

    forward_payload = {
        "user_id": user_id,
        "date": str(today),
        "metrics": {
            "screen_time": daily_metric.screen_time,
            "tasks_completed": daily_metric.tasks_completed,
            "motion_score": daily_metric.motion_score
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # We assume backend3 has an endpoint /api/energy/update
            # We might need to pass a service token if backend3 requires it.
            # detailed auth is left for later refined security steps.
            response = await client.post(
                f"{settings.BACKEND3_URL}/api/energy/update",
                json=forward_payload,
                timeout=5.0
            )
            response.raise_for_status()
            return {"status": "success", "backend3_response": response.json()}
        except Exception as e:
            print(f"Failed to forward to Backend3: {e}")
            return {"status": "error", "message": str(e)}
