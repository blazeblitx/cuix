"""
Unit tests for Task 11: Utility Optimizer & Selection Strategy Comparison Experiment
"""

import unittest
from core.optimizer.experiment_optimizer import EvaluatedOptimizer

class TestTask11Optimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = EvaluatedOptimizer(min_improvement_threshold=0.10)

    def test_utility_selection_favors_low_disruption(self):
        candidates = [
            {
                "id": "A_Highlight",
                "type": "HIGHLIGHT_ELEMENT",
                "targetSelector": "button.filter-btn",
                "predicted_gain": 0.28,
                "disruption": 0.05,
                "cost": 0.01,
                "risk": 0.0
            },
            {
                "id": "B_Reposition",
                "type": "EXPOSE_HIDDEN_CONTROL",
                "targetSelector": "button.filter-btn",
                "predicted_gain": 0.32,  # Slightly higher gain (+4%), but 12x higher disruption (0.60)!
                "disruption": 0.60,
                "cost": 0.20,
                "risk": 0.0
            }
        ]

        selected = self.optimizer.select_utility_optimized_intervention(candidates)
        self.assertIsNotNone(selected)
        self.assertEqual(selected["id"], "A_Highlight")

    def test_strategy_comparison_experiment(self):
        candidates = [
            {
                "id": "cand_greedy",
                "targetSelector": "button.nav",
                "predicted_task_success_rate": 0.90,
                "predicted_gain": 0.35,
                "disruption": 0.70,  # High disruption
                "cost": 0.30,
                "risk": 0.0
            },
            {
                "id": "cand_utility",
                "targetSelector": "button.nav",
                "predicted_task_success_rate": 0.86,
                "predicted_gain": 0.30,
                "disruption": 0.04,  # Minimal disruption
                "cost": 0.02,
                "risk": 0.0
            }
        ]

        res = self.optimizer.run_strategy_comparison_experiment(candidates)
        self.assertEqual(res["strategy_a_greedy"]["id"], "cand_greedy")
        self.assertEqual(res["strategy_b_utility_optimizer"]["id"], "cand_utility")
        self.assertGreater(res["experiment_metrics"]["disruption_reduction_pct"], 50.0)

if __name__ == '__main__':
    unittest.main()
