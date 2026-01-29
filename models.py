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

    # Energy Intelligence Fields
    energy_score = Column(Float, nullable=True)
    energy_level = Column(String, nullable=True)
    energy_confidence = Column(Float, nullable=True)
    energy_calc_version = Column(Integer, default=1)

    # Internal Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='_user_date_uc'),
        Index('idx_user_id_date', 'user_id', 'date'),
    )
