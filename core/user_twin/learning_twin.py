"""
CUIX Task 5: Learning Personal Interaction Twin Engine
Implements online Bayesian-style feature updates, separates short-term session state from long-term user traits,
and exposes explicit uncertainty/confidence metrics for learned preferences.
"""

from typing import Dict, Any, List, Tuple
import math

class ShortTermSessionState:
    """Volatile session-scoped feature state."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.click_count = 0
        self.keypress_count = 0
        self.search_interactions = 0
        self.menu_interactions = 0
        self.backtrack_events = 0
        self.dwell_times_ms: List[float] = []

    def update_from_events(self, events: List[Dict[str, Any]]) -> None:
        for evt in events:
            etype = evt.get('eventType')
            target = evt.get('targetSelector', '')

            if etype == 'click':
                self.click_count += 1
                if 'search' in target:
                    self.search_interactions += 1
                elif 'nav' in target or 'menu' in target:
                    self.menu_interactions += 1
            elif etype == 'keypress':
                self.keypress_count += 1
            elif etype == 'backtrack':
                self.backtrack_events += 1

            if evt.get('dwellTimeMs'):
                self.dwell_times_ms.append(float(evt['dwellTimeMs']))

    def get_session_feature_vector(self) -> Dict[str, float]:
        total_nav = self.search_interactions + self.menu_interactions
        search_ratio = self.search_interactions / total_nav if total_nav > 0 else 0.50

        total_actions = self.click_count + self.keypress_count
        kb_ratio = self.keypress_count / total_actions if total_actions > 0 else 0.50

        backtrack_ratio = self.backtrack_events / max(self.click_count, 1)
        avg_dwell_sec = (sum(self.dwell_times_ms) / len(self.dwell_times_ms) / 1000.0) if self.dwell_times_ms else 2.5

        return {
            "search_ratio": round(search_ratio, 3),
            "keyboard_ratio": round(kb_ratio, 3),
            "backtrack_ratio": round(backtrack_ratio, 3),
            "avg_dwell_sec": round(avg_dwell_sec, 3)
        }

class LongTermUserTwin:
    """Persistent learned user interaction twin with trait values and uncertainty scores."""
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Trait baseline values [0.0 - 1.0]
        self.search_preference: float = 0.50
        self.keyboard_usage: float = 0.50
        self.backtracking_tendency: float = 0.10
        self.avg_decision_time_sec: float = 2.50

        # Trait Uncertainty scores [1.00 = Unknown, 0.00 = Highly Confident]
        self.search_pref_uncertainty: float = 1.00
        self.keyboard_uncertainty: float = 1.00
        self.backtrack_uncertainty: float = 1.00
        self.decision_time_uncertainty: float = 1.00

        self.total_sessions_learned: int = 0

    def apply_online_session_update(self, session_vector: Dict[str, float], learning_rate: float = 0.25) -> None:
        """Online incremental update with variance/uncertainty reduction."""
        self.total_sessions_learned += 1
        
        # Adaptive learning rate decays slightly over time as confidence increases
        eta = learning_rate / (1.0 + 0.1 * math.log(max(self.total_sessions_learned, 1)))

        # Update traits
        obs_search = session_vector.get("search_ratio", 0.50)
        self.search_preference = round(self.search_preference + eta * (obs_search - self.search_preference), 3)

        obs_kb = session_vector.get("keyboard_ratio", 0.50)
        self.keyboard_usage = round(self.keyboard_usage + eta * (obs_kb - self.keyboard_usage), 3)

        obs_backtrack = session_vector.get("backtrack_ratio", 0.10)
        self.backtracking_tendency = round(self.backtracking_tendency + eta * (obs_backtrack - self.backtracking_tendency), 3)

        obs_dwell = session_vector.get("avg_dwell_sec", 2.50)
        self.avg_decision_time_sec = round(self.avg_decision_time_sec + eta * (obs_dwell - self.avg_decision_time_sec), 3)

        # Decay uncertainty scores towards lower bound as observations accumulate
        decay_factor = 0.85
        self.search_pref_uncertainty = round(max(0.10, self.search_pref_uncertainty * decay_factor), 3)
        self.keyboard_uncertainty = round(max(0.10, self.keyboard_uncertainty * decay_factor), 3)
        self.backtrack_uncertainty = round(max(0.10, self.backtrack_uncertainty * decay_factor), 3)
        self.decision_time_uncertainty = round(max(0.10, self.decision_time_uncertainty * decay_factor), 3)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "total_sessions_learned": self.total_sessions_learned,
            "traits": {
                "search_preference": self.search_preference,
                "keyboard_usage": self.keyboard_usage,
                "backtracking_tendency": self.backtracking_tendency,
                "avg_decision_time_sec": self.avg_decision_time_sec
            },
            "uncertainty": {
                "search_preference": self.search_pref_uncertainty,
                "keyboard_usage": self.keyboard_uncertainty,
                "backtracking_tendency": self.backtrack_uncertainty,
                "avg_decision_time_sec": self.decision_time_uncertainty
            }
        }
