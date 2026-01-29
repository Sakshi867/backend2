from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import insert as gen_insert
from models import DailyMetrics
from schemas import DailyMetricsCreate
import energy_service

def upsert_daily_metrics(db: Session, metrics_data: DailyMetricsCreate, user_id: str):
    # Prepare data
    data = metrics_data.model_dump()
    data['user_id'] = user_id
    metrics_date = data['date']

    # Use PostgreSQL specific UPSERT if applicable, or generic logic
    # Here we'll use a fetch-and-update approach for broad compatibility
    db_record = db.query(DailyMetrics).filter(
        DailyMetrics.user_id == user_id,
        DailyMetrics.date == metrics_date
    ).first()

    if db_record:
        for key, value in data.items():
            setattr(db_record, key, value)
    else:
        db_record = DailyMetrics(**data)
        db.add(db_record)

    db.commit()
    db.refresh(db_record)

    # Calculate Energy Intelligence
    energy_result = energy_service.calculate_daily_energy(db_record)
    
    db_record.energy_score = energy_result["energy_score"]
    db_record.energy_level = energy_result["energy_level"]
    db_record.energy_confidence = energy_result["energy_confidence"]
    db_record.energy_calc_version = energy_result["energy_calc_version"]
    db_record.primary_driver = energy_result.get("primary_driver")
    
    db.commit()
    db.refresh(db_record)
    
    return db_record
