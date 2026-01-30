from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import DailyMetricsCreate, DailyMetricsResponse, SensorDataCreate, SensorDataResponse
from security import get_current_user
import metrics_service
import sensor_service
import schemas 

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

@router.post("/sensor", response_model=schemas.SensorDataResponse)
async def ingest_sensor_data(
    metric: schemas.SensorDataCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        return sensor_service.create_sensor_metric(db, metric, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/aggregate")
async def trigger_aggregation(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger data aggregation and forwarding to Backend3
    """
    try:
        result = await sensor_service.aggregate_and_forward(db, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
