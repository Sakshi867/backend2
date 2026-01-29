import logging
from typing import Dict, Any, Tuple
from app.db.models import DailyMetrics

logger = logging.getLogger(__name__)

ENERGY_CALC_VERSION = 1

# Thresholds
LOW_THRESHOLD = 40
MEDIUM_THRESHOLD = 70

# Weights (Sum = 1.0 or weights specifically adjusted)
W_SLEEP = 3.0  # Weight for sleep hours (target 8h)
W_DEEP_WORK = 0.5 # Weight for deep work minutes (target 180m)
W_SCREEN_FATIGUE = 0.1 # Penalty for screen minutes
W_INTERRUPT = 2.0 # Penalty per switch
W_COMPLETION = 20.0 # Bonus for completion rate (0-1)

def calculate_daily_energy(metrics: DailyMetrics) -> Dict[str, Any]:
    """
    Calculates energy score, level, and confidence based on behavioral metrics.
    Deterministic Baseline Model (V1).
    """
    try:
        # 1. Normalization & Extract Metrics
        sleep = metrics.sleep_hours or 0.0
        deep_work = metrics.task_deep_minutes or 0.0
        screen_time = (
            (metrics.screen_minutes_social or 0.0) +
            (metrics.screen_minutes_productivity or 0.0) +
            (metrics.screen_minutes_entertainment or 0.0)
        )
        interrupts = (metrics.app_switch_count or 0) + (metrics.task_switch_count or 0)
        completion_rate = metrics.task_completion_rate or 0.0

        # Outlier Clamping
        sleep = min(max(sleep, 0), 12) # 0-12 hours
        deep_work = min(max(deep_work, 0), 480) # 0-8 hours
        screen_time = min(max(screen_time, 0), 1440) # Max minutes in day
        interrupts = min(max(interrupts, 0), 500) # Reasonable max
        completion_rate = min(max(completion_rate, 0), 1.0)

        # 2. Score Calculation
        # Base score starts at 50
        score = 50.0
        
        # Positive Drivers
        score += (sleep - 7.0) * W_SLEEP # Bonus/penalty relative to 7h sleep
        score += (deep_work / 60.0) * W_DEEP_WORK * 10.0 # ~5 points per hour of deep work
        score += (completion_rate * W_COMPLETION)
        
        # Negative Drivers (Fatigue)
        score -= (screen_time / 60.0) * W_SCREEN_FATIGUE * 10.0 # ~1 point per hour screen
        score -= (interrupts / 20.0) * W_INTERRUPT # -2 points per 20 switches
        
        # Final Clamp
        score = min(max(score, 0), 100)

        # 3. Energy Level Classification
        if score < LOW_THRESHOLD:
            level = "LOW"
        elif score < MEDIUM_THRESHOLD:
            level = "MEDIUM"
        else:
            level = "HIGH"

        # 4. Confidence Calculation
        missing_fields = 0
        fields = ["sleep_hours", "task_deep_minutes", "app_switch_count", "task_completion_rate"]
        for field in fields:
            if getattr(metrics, field) is None or getattr(metrics, field) == 0:
                missing_fields += 1
        
        confidence = 1.0 - (missing_fields * 0.15)
        
        # Extra penalty if extreme outliers detected (simple version)
        if screen_time > 600 or interrupts > 200:
            confidence -= 0.1
            
        confidence = min(max(confidence, 0.1), 1.0)

        logger.info(f"Energy Calc V{ENERGY_CALC_VERSION}: Score={score}, Level={level}, Conf={confidence}")

        return {
            "energy_score": round(score, 2),
            "energy_level": level,
            "energy_confidence": round(confidence, 2),
            "energy_calc_version": ENERGY_CALC_VERSION
        }

    except Exception as e:
        logger.error(f"Energy engine failure: {str(e)}")
        return {
            "energy_score": 50.0,
            "energy_level": "MEDIUM",
            "energy_confidence": 0.3,
            "energy_calc_version": ENERGY_CALC_VERSION
        }
