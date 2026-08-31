"""
CUIX Personal Interaction Twin Model (Phase 4 & Phase 7)
Models long-term behavioral preferences and interaction traits.
"""

from typing import Dict, Any, List

class PersonalInteractionTwin:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Long-term behavioral trait baseline
        self.search_preference: float = 0.5  # [0.0 = Menu Explorer, 1.0 = Search Heavy]
        self.keyboard_usage: float = 0.5     # [0.0 = Mouse Only, 1.0 = Keyboard Shortcuts]
        self.menu_depth_pref: float = 0.5    # [0.0 = Flat UI, 1.0 = Deep Hierarchies]
        self.backtrack_rate: float = 0.1     # Frequency of navigation reversals
        self.avg_decision_time: float = 2.5   # Mean pause time before interaction (sec)
        self.sample_count: int = 0

    def update_from_session(self, session_telemetry: List[Dict[str, Any]]) -> None:
        """Update twin features using online incremental learning."""
        if not session_telemetry:
            return
        
        click_count = sum(1 for e in session_telemetry if e.get('eventType') == 'click')
        keypress_count = sum(1 for e in session_telemetry if e.get('eventType') == 'keypress')
        total_actions = click_count + keypress_count
        
        if total_actions > 0:
            kb_ratio = keypress_count / total_actions
            # Exponential moving average update
            self.keyboard_usage = 0.8 * self.keyboard_usage + 0.2 * kb_ratio
        
        self.sample_count += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "search_preference": round(self.search_preference, 2),
            "keyboard_usage": round(self.keyboard_usage, 2),
            "menu_depth_pref": round(self.menu_depth_pref, 2),
            "backtrack_rate": round(self.backtrack_rate, 2),
            "avg_decision_time_sec": round(self.avg_decision_time, 2),
            "sample_count": self.sample_count
        }
