from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class DailyMetricsBase(BaseModel):
    # Digital Behaviour Metrics
    screen_minutes_social: float = 0.0
    screen_minutes_productivity: float = 0.0
    screen_minutes_entertainment: float = 0.0
    continuous_screen_minutes: float = 0.0
    app_switch_count: int = 0
    night_usage_minutes: float = 0.0

    # Physical Recovery Metrics
    step_count: int = 0
    active_minutes: float = 0.0
    screen_break_minutes: float = 0.0
    morning_activity_minutes: float = 0.0

    # Cognitive Load Metrics
    task_deep_minutes: float = 0.0
    task_light_minutes: float = 0.0
    task_switch_count: int = 0

    # New Energy Engine Metrics
    sleep_hours: float = 0.0
    task_completion_rate: float = 0.0

class DailyMetricsCreate(DailyMetricsBase):
    timestamp: date = Field(..., alias='timestamp')

    class Config:
        populate_by_name = True

class DailyMetricsResponse(DailyMetricsBase):
    user_id: str
    date: date
    energy_score: Optional[float] = None
    energy_level: Optional[str] = None
    energy_confidence: Optional[float] = None
    energy_calc_version: int
    data_version: int

    class Config:
        from_attributes = True
