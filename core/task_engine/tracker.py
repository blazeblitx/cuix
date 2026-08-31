"""
CUIX Phase 5: Task Understanding & Progression Engine
Tracks expected vs actual user progression through structured tasks.
"""

from typing import Dict, Any, List, Optional

class TaskStep:
    def __init__(self, step_id: str, description: str, target_role: str, is_required: bool = True):
        self.step_id = step_id
        self.description = description
        self.target_role = target_role
        self.is_required = is_required
        self.completed = False

class TaskGoal:
    def __init__(self, task_id: str, title: str, steps: List[TaskStep]):
        self.task_id = task_id
        self.title = title
        self.steps = steps

    def get_progress_percentage(self) -> float:
        if not self.steps:
            return 100.0
        completed_count = sum(1 for s in self.steps if s.completed)
        return round((completed_count / len(self.steps)) * 100.0, 1)

class TaskProgressionTracker:
    def __init__(self, active_goal: Optional[TaskGoal] = None):
        self.active_goal = active_goal
        self.current_step_index = 0

    def set_goal(self, goal: TaskGoal):
        self.active_goal = goal
        self.current_step_index = 0

    def process_interaction(self, event_type: str, target_role: str) -> Dict[str, Any]:
        """Evaluates whether an interaction advances the active task goal."""
        if not self.active_goal or self.current_step_index >= len(self.active_goal.steps):
            return {"advanced": False, "progress": 100.0, "status": "COMPLETED_OR_NO_GOAL"}

        expected_step = self.active_goal.steps[self.current_step_index]
        advanced = False

        if target_role == expected_step.target_role:
            expected_step.completed = True
            self.current_step_index += 1
            advanced = True

        return {
            "advanced": advanced,
            "current_step": self.current_step_index,
            "total_steps": len(self.active_goal.steps),
            "progress_pct": self.active_goal.get_progress_percentage(),
            "status": "IN_PROGRESS" if self.current_step_index < len(self.active_goal.steps) else "GOAL_ACHIEVED"
        }
