"""
Unit & Integration Tests for Task Engine, Friction Detector, Simulator & Rollback Manager (Phases 5, 6, 9, 10, 11, 12)
"""

import unittest
from core.task_engine.tracker import TaskProgressionTracker, TaskGoal, TaskStep
from core.friction_detector.classifier import FrictionDetector
from core.simulator.counterfactual import CounterfactualSimulator
from core.optimizer.utility import InterventionOptimizer
from core.adaptive_layer.controller import AdaptationController

class TestFrictionTaskPipeline(unittest.TestCase):
    def test_task_progression(self):
        steps = [
            TaskStep("s1", "Search for backpack", "search"),
            TaskStep("s2", "Filter by price", "filter"),
            TaskStep("s3", "Click Add to Cart", "action")
        ]
        goal = TaskGoal("g1", "Buy Backpack", steps)
        tracker = TaskProgressionTracker(goal)

        res1 = tracker.process_interaction("click", "search")
        self.assertTrue(res1["advanced"])
        self.assertEqual(res1["current_step"], 1)

        res2 = tracker.process_interaction("click", "filter")
        self.assertTrue(res2["advanced"])

    def test_friction_detection(self):
        detector = FrictionDetector()
        telemetry = {"avg_dwell_time_ms": 12000.0, "backtrack_rate": 0.50}
        twin = {"avg_decision_time_sec": 2.0}
        task = {"status": "IN_PROGRESS", "advanced": False}

        assessment = detector.evaluate_friction(telemetry, twin, task)
        self.assertIn(assessment["level"], ["POSSIBLE_FRICTION", "HIGH_FRICTION"])
        self.assertGreater(assessment["score"], 0.5)

    def test_end_to_end_counterfactual_selection(self):
        simulator = CounterfactualSimulator()
        optimizer = InterventionOptimizer()

        candidates = simulator.generate_candidate_interventions(
            target_node={"selector": "button#filter-btn", "role": "filter"},
            friction_assessment={"level": "HIGH_FRICTION"}
        )
        self.assertEqual(len(candidates), 5)

        simulated = simulator.simulate_outcomes(candidates)
        best = optimizer.select_best_intervention(simulated)
        self.assertIsNotNone(best)
        self.assertIn("utility_score", best)

    def test_adaptation_rollback(self):
        controller = AdaptationController()
        chk = controller.create_checkpoint("int_A", "button#filter", "color: blue;")
        self.assertTrue(chk.is_active)

        rolled = controller.rollback_checkpoint(chk.checkpoint_id)
        self.assertIsNotNone(rolled)
        self.assertFalse(chk.is_active)

if __name__ == '__main__':
    unittest.main()
