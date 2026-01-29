from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.db.models import DailyMetrics
from app.schemas.metrics import DailyMetricsCreate
from app.services import energy_service
from datetime import datetime

def upsert_daily_metrics(db: Session, metrics_data: DailyMetricsCreate, user_id: str):
    # Prepare data for upsert
    data = metrics_data.dict(by_alias=True)
    metrics_date = data.pop('timestamp')
    data['user_id'] = user_id
    data['date'] = metrics_date
    
    # SQLAlchemy expression for PostgreSQL UPSERT
    stmt = insert(DailyMetrics).values(
        **data
    )
    
    # Fields to update on conflict
    update_dict = {
        c.name: stmt.excluded[c.name] 
        for c in DailyMetrics.__table__.columns 
        if c.name not in ['id', 'user_id', 'date', 'created_at']
    }
    
    # Performance optimized upsert
    upsert_stmt = stmt.on_conflict_do_update(
        constraint='_user_date_uc',
        set_=update_dict
    )
    
    db.execute(upsert_stmt)
    db.commit()
    
    # Fetch the record
    db_metrics = db.query(DailyMetrics).filter(
        DailyMetrics.user_id == user_id,
        DailyMetrics.date == metrics_date
    ).first()

    # 2. Calculate Energy Intelligence
    if db_metrics:
        energy_result = energy_service.calculate_daily_energy(db_metrics)
        
        # Update record with energy results
        db_metrics.energy_score = energy_result["energy_score"]
        db_metrics.energy_level = energy_result["energy_level"]
        db_metrics.energy_confidence = energy_result["energy_confidence"]
        db_metrics.energy_calc_version = energy_result["energy_calc_version"]
        
        db.commit()
        db.refresh(db_metrics)
    
    return db_metrics
