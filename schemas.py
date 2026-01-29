from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class DailyMetricsBase(BaseModel):
    screen_time: float = 0.0
    tasks_completed: int = 0
    motion_score: float = 0.0

class DailyMetricsCreate(DailyMetricsBase):
    date: date

class DailyMetricsResponse(DailyMetricsBase):
    user_id: str
    date: date
    energy_score: Optional[float] = None
    energy_level: Optional[str] = None
    energy_confidence: Optional[float] = None
    energy_calc_version: int
    primary_driver: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
