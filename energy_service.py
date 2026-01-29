from typing import Dict, Any
from models import DailyMetrics

ENERGY_CALC_VERSION = 1

def calculate_daily_energy(metrics: DailyMetrics) -> Dict[str, Any]:
    """
    Placeholder for future energy calculation logic.
    Provides a simple deterministic baseline for now.
    """
    # Simple example logic: energy depends on screen time and tasks completed
    # (High screen time = lower energy, High tasks = higher energy)
    
    score = 70.0 # Start baseline
    
    # Fatigue penalty
    screen_penalty = (metrics.screen_time / 60.0) * 2.0
    score -= screen_penalty
    
    # Accomplishment bonus
    task_bonus = metrics.tasks_completed * 5.0
    score += task_bonus

    # Motion bonus (Active State Logic)
    # motion_score is 0-1. 1.0 = highly active => +10 points
    motion_bonus = (metrics.motion_score or 0.0) * 10.0
    score += motion_bonus
    
    # Clamp
    score = min(max(score, 0), 100)
    
    # Determine Primary Driver
    drivers = [
        ("High Screen Strain", screen_penalty),
        ("Productivity Boost", task_bonus),
        ("Physical Activity", motion_bonus)
    ]
    # Find the factor with the largest magnitude (absolute impact)
    # Simple logic: if screen penalty is the biggest detractor, blame that.
    # If bonuses are high, credit them.
    
    primary_driver = "Balanced"
    if score < 60:
        # Negative drivers focus
        if screen_penalty > 10:
            primary_driver = "High Screen Strain"
        elif (metrics.motion_score or 0) < 0.2:
            primary_driver = "Sedentary Behavior"
    else:
        # Positive drivers focus
        if task_bonus > 15:
            primary_driver = "High Productivity"
        elif motion_bonus > 5:
            primary_driver = "Active Movement"
    
    if score < 40:
        level = "LOW"
    elif score < 70:
        level = "MEDIUM"
    else:
        level = "HIGH"
        
    return {
        "energy_score": round(score, 2),
        "energy_level": level,
        "energy_confidence": 0.8,
        "energy_calc_version": ENERGY_CALC_VERSION,
        "primary_driver": primary_driver
    }
