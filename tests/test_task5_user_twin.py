"""
Unit tests for Task 5: Learning User Twin & Online Telemetry Updates
Demonstrates online evolution of Search Preference trait and uncertainty reduction over 10 sessions.
"""

import unittest
from core.user_twin.learning_twin import LongTermUserTwin, ShortTermSessionState

class TestTask5UserTwin(unittest.TestCase):
    def test_initial_neutral_twin(self):
        twin = LongTermUserTwin("user_demo")
        self.assertEqual(twin.search_preference, 0.50)
        self.assertEqual(twin.search_pref_uncertainty, 1.00)
        self.assertEqual(twin.total_sessions_learned, 0)

    def test_online_learning_progression(self):
        twin = LongTermUserTwin("user_demo")
        initial_search_pref = twin.search_preference
        initial_uncertainty = twin.search_pref_uncertainty

        # Simulate 10 sequential sessions where user heavily uses search box
        for session_idx in range(1, 11):
            session = ShortTermSessionState(f"sess_{session_idx}")
            search_events = [
                {"eventType": "click", "targetSelector": "input#search-bar"},
                {"eventType": "click", "targetSelector": "input#search-bar"},
                {"eventType": "click", "targetSelector": "input#search-bar"},
                {"eventType": "click", "targetSelector": "button.nav"}
            ]
            session.update_from_events(search_events)
            vec = session.get_session_feature_vector()
            twin.apply_online_session_update(vec)

            if session_idx == 1:
                session1_search_pref = twin.search_preference
                session1_uncertainty = twin.search_pref_uncertainty

        session10_search_pref = twin.search_preference
        session10_uncertainty = twin.search_pref_uncertainty

        # Verify progression: Initial (0.50) -> Session 1 (0.56+) -> Session 10 (0.70+)
        self.assertGreater(session1_search_pref, initial_search_pref)
        self.assertGreater(session10_search_pref, session1_search_pref)
        self.assertGreaterEqual(session10_search_pref, 0.70)

        # Verify uncertainty reduction: Initial (1.00) -> Session 10 (0.20-0.35)
        self.assertLess(session10_uncertainty, session1_uncertainty)
        self.assertLessEqual(session10_uncertainty, 0.35)

if __name__ == '__main__':
    unittest.main()
