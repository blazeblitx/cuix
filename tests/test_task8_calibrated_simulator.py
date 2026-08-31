"""
Unit tests for Task 8: Calibrated Counterfactual Simulator & Episode Outcome Logger
"""

import unittest
from core.simulator.calibrated_simulator import CalibratedCounterfactualSimulator
from core.simulator.counterfactual import CounterfactualSimulator

class TestTask8CalibratedSimulator(unittest.TestCase):
    def setUp(self):
        self.calibrated_sim = CalibratedCounterfactualSimulator()
        self.base_sim = CounterfactualSimulator()

    def test_calibrated_outcome_prediction(self):
        candidates = self.base_sim.generate_candidate_interventions(
            target_node={"selector": "button#filter", "role": "filter"},
            friction_assessment={"level": "HIGH_FRICTION"}
        )
        user_twin = {"search_preference": 0.85, "avg_decision_time_sec": 3.0, "keyboard_usage": 0.70}
        
        calibrated = self.calibrated_sim.simulate_candidate_outcomes(candidates, user_twin, interface_complexity=0.50)
        self.assertEqual(len(calibrated), 5)

        for cand in calibrated:
            self.assertIn("predicted_task_success_rate", cand)
            self.assertIn("predicted_completion_time_sec", cand)
            self.assertIn("predicted_error_probability", cand)
            self.assertGreater(cand["predicted_task_success_rate"], 0.50)
            self.assertGreater(cand["predicted_completion_time_sec"], 0.0)

    def test_episode_logging_and_prediction_error(self):
        candidate = {
            "id": "int_A",
            "targetSelector": "button.nav",
            "predicted_task_success_rate": 0.82,
            "predicted_completion_time_sec": 2.10,
            "predicted_error_probability": 0.08
        }
        episode = self.calibrated_sim.log_episode(candidate)
        self.assertEqual(episode.candidate_id, "int_A")
        
        # Simulate realized outcome after applying adaptation
        realized = {
            "task_success_rate": 0.85,
            "completion_time_sec": 1.95,
            "error_probability": 0.05
        }
        errors = episode.record_realized_outcome(realized)
        self.assertIn("task_success_rate_error", errors)
        self.assertEqual(errors["task_success_rate_error"], 0.03)

if __name__ == '__main__':
    unittest.main()
