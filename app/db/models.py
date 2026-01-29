from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint, Index, func
from app.db.database import Base

class DailyMetrics(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)

    # Digital Behaviour Metrics
    screen_minutes_social = Column(Float, default=0.0)
    screen_minutes_productivity = Column(Float, default=0.0)
    screen_minutes_entertainment = Column(Float, default=0.0)
    continuous_screen_minutes = Column(Float, default=0.0)
    app_switch_count = Column(Integer, default=0)
    night_usage_minutes = Column(Float, default=0.0)

    # Physical Recovery Metrics
    step_count = Column(Integer, default=0)
    active_minutes = Column(Float, default=0.0)
    screen_break_minutes = Column(Float, default=0.0)
    morning_activity_minutes = Column(Float, default=0.0)

    # Cognitive Load Metrics
    task_deep_minutes = Column(Float, default=0.0)
    task_light_minutes = Column(Float, default=0.0)
    task_switch_count = Column(Integer, default=0)
    
    # New metrics for energy engine
    sleep_hours = Column(Float, default=0.0)
    task_completion_rate = Column(Float, default=0.0)

    # Future Energy Engine Compatibility
    energy_score = Column(Float, nullable=True)
    energy_level = Column(String, nullable=True)
    energy_confidence = Column(Float, nullable=True)
    energy_calc_version = Column(Integer, default=1)

    # Metadata Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    data_version = Column(Integer, default=1)

    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='_user_date_uc'),
        Index('idx_user_id_date', 'user_id', 'date'),
    )
