"""
CUIX Phase 6: Interaction Friction Detector Model
Classifies interaction state into NORMAL, POSSIBLE_FRICTION, or HIGH_FRICTION
based on telemetry features, user twin profile, and task progression.
"""

from typing import Dict, Any

class FrictionDetector:
    def __init__(
        self,
        dwell_threshold_ms: float = 8000.0,
        backtrack_threshold: float = 0.40,
        rapid_click_threshold: int = 4
    ):
        self.dwell_threshold_ms = dwell_threshold_ms
        self.backtrack_threshold = backtrack_threshold
        self.rapid_click_threshold = rapid_click_threshold

    def evaluate_friction(
        self,
        telemetry_metrics: Dict[str, Any],
        user_twin_profile: Dict[str, Any],
        task_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates cognitive/interaction friction level.
        Returns: Friction level ('NORMAL', 'POSSIBLE_FRICTION', 'HIGH_FRICTION'), score [0.0 - 1.0], and signals.
        """
        friction_signals = []
        score = 0.0

        avg_dwell = telemetry_metrics.get('avg_dwell_time_ms', 0.0)
        backtrack_rate = telemetry_metrics.get('backtrack_rate', 0.0)
        user_baseline_dwell = user_twin_profile.get('avg_decision_time_sec', 2.5) * 1000.0

        # Pause / Confusion Signal
        if avg_dwell > (user_baseline_dwell * 2.5):
            friction_signals.append("Unusually long decision pause before action")
            score += 0.35

        # Navigation Loop / Backtracking Signal
        if backtrack_rate > self.backtrack_threshold:
            friction_signals.append("High navigation backtrack / reversal frequency")
            score += 0.40

        # Stalled Task Progression Signal
        if task_progress.get("status") == "IN_PROGRESS" and not task_progress.get("advanced"):
            friction_signals.append("Stalled progress on expected task progression step")
            score += 0.20

        score = min(round(score, 2), 1.0)

        if score >= 0.65:
            level = "HIGH_FRICTION"
        elif score >= 0.30:
            level = "POSSIBLE_FRICTION"
        else:
            level = "NORMAL"

        return {
            "level": level,
            "score": score,
            "signals": friction_signals
        }
