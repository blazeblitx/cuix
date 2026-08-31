"""
Unit tests for Task 12: Closed-Loop Autonomous Pipeline Execution
"""

import unittest
from core.closed_loop_pipeline import ClosedLoopPipeline

class TestTask12ClosedLoop(unittest.TestCase):
    def setUp(self):
        self.pipeline = ClosedLoopPipeline("user_closed_loop_test")

    def test_full_closed_loop_execution(self):
        mock_graph = {
            "pageUrl": "https://test-shop.com",
            "domain": "test-shop.com",
            "summary": {"totalNodes": 25, "actionCount": 5},
            "root": {
                "id": "node_1",
                "role": "filter",
                "confidence": 0.90,
                "selector": "button.filter-btn",
                "children": []
            }
        }
        mock_events = [
            {"timestamp": 1000, "eventType": "click", "targetSelector": "button.nav", "dwellTimeMs": 12000},
            {"timestamp": 13000, "eventType": "backtrack", "targetSelector": "body"}
        ]

        record = self.pipeline.execute_closed_loop_step(mock_graph, mock_events)

        self.assertIsNotNone(record)
        self.assertEqual(record.domain, "test-shop.com")
        self.assertEqual(record.friction_assessment["level"], "HIGH_FRICTION")
        self.assertIn("type", record.selected_intervention)
        self.assertIn("task_success_rate_error", record.prediction_errors)
        self.assertTrue(record.model_updated)
        self.assertEqual(len(self.pipeline.episode_history), 1)

if __name__ == '__main__':
    unittest.main()
