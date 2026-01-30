from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint, Index, func
from database import Base

class DailyMetrics(Base):
    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)

    # Core Metrics
    screen_time = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)
    motion_score = Column(Float, default=0.0)

    # Energy Intelligence Fields
    energy_score = Column(Float, nullable=True)
    energy_level = Column(String, nullable=True)
    energy_confidence = Column(Float, nullable=True)
    energy_calc_version = Column(Integer, default=1)
    primary_driver = Column(String, nullable=True)

    # Internal Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='_user_date_uc'),
        Index('idx_user_id_date', 'user_id', 'date'),
    )

class SensorMetric(Base):
    __tablename__ = "sensor_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)
    data_type = Column(String, index=True, nullable=False)  # e.g., 'accelerometer', 'screen_on', 'app_usage'
    payload = Column(String, nullable=False) # Storing JSON string for flexibility (SQLite compatible)
    
    # Internal Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_sensor_user_time', 'user_id', 'timestamp'),
    )
