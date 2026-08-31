"""
CUIX Personal Interaction Twin Model (Phase 4 & Task 5)
Refactored online learning wrapper for LongTermUserTwin.
"""

from typing import Dict, Any, List
from core.user_twin.learning_twin import LongTermUserTwin, ShortTermSessionState

class PersonalInteractionTwin:
    def __init__(self, user_id: str):
        self.learning_twin = LongTermUserTwin(user_id)
        self.active_session = ShortTermSessionState(session_id="sess_init")

    @property
    def keyboard_usage(self) -> float:
        return self.learning_twin.keyboard_usage

    @property
    def search_preference(self) -> float:
        return self.learning_twin.search_preference

    @property
    def sample_count(self) -> int:
        return self.learning_twin.total_sessions_learned

    def update_from_session(self, session_telemetry: List[Dict[str, Any]]) -> None:
        self.active_session.update_from_events(session_telemetry)
        vector = self.active_session.get_session_feature_vector()
        self.learning_twin.apply_online_session_update(vector)

    def to_dict(self) -> Dict[str, Any]:
        data = self.learning_twin.to_dict()
        data["search_preference"] = data["traits"]["search_preference"]
        data["keyboard_usage"] = data["traits"]["keyboard_usage"]
        data["backtrack_rate"] = data["traits"]["backtracking_tendency"]
        data["avg_decision_time_sec"] = data["traits"]["avg_decision_time_sec"]
        data["sample_count"] = data["total_sessions_learned"]
        return data
