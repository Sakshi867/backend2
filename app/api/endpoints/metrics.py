from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.metrics import DailyMetricsCreate, DailyMetricsResponse
from app.core.security import get_current_user
from app.services import metrics_service
from datetime import datetime

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.post("/daily", response_model=DailyMetricsResponse)
async def create_daily_metrics(
    metrics: DailyMetricsCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        db_metrics = metrics_service.upsert_daily_metrics(db, metrics, user_id)
        return db_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
