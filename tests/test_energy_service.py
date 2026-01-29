import pytest
from app.services import energy_service
from app.db.models import DailyMetrics

def test_energy_score_high_productivity():
    metrics = DailyMetrics(
        sleep_hours=8.5,
        task_deep_minutes=180,
        task_completion_rate=0.9,
        screen_minutes_social=30,
        screen_minutes_productivity=120,
        screen_minutes_entertainment=30,
        app_switch_count=10,
        task_switch_count=5
    )
    result = energy_service.calculate_daily_energy(metrics)
    assert result["energy_score"] > 70
    assert result["energy_level"] == "HIGH"
    assert result["energy_confidence"] >= 0.8

def test_energy_score_low_sleep_high_screen():
    metrics = DailyMetrics(
        sleep_hours=4.0,
        task_deep_minutes=20,
        task_completion_rate=0.2,
        screen_minutes_social=240,
        screen_minutes_productivity=60,
        screen_minutes_entertainment=180,
        app_switch_count=100,
        task_switch_count=40
    )
    result = energy_service.calculate_daily_energy(metrics)
    assert result["energy_score"] < 40
    assert result["energy_level"] == "LOW"

def test_missing_fields_confidence():
    metrics = DailyMetrics(
        sleep_hours=0,
        task_deep_minutes=0,
        task_completion_rate=0,
        app_switch_count=0
    )
    result = energy_service.calculate_daily_energy(metrics)
    # 4 missing fields = 1.0 - (4 * 0.15) = 0.4
    assert result["energy_confidence"] <= 0.6
    assert result["energy_level"] == "MEDIUM" or result["energy_level"] == "LOW"

def test_extreme_clamping():
    metrics = DailyMetrics(
        sleep_hours=20, # Clamped to 12
        task_deep_minutes=1000, # Clamped to 480
        task_completion_rate=5.0, # Clamped to 1.0
        screen_minutes_social=2000 # Clamped to 1440
    )
    result = energy_service.calculate_daily_energy(metrics)
    assert 0 <= result["energy_score"] <= 100
    assert result["energy_calc_version"] == 1
