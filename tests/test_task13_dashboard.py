"""
Unit tests for Task 13: CUIX Research Dashboard & Experiment Comparison Payload
"""

import unittest
from core.closed_loop_pipeline import ClosedLoopPipeline

class TestTask13Dashboard(unittest.TestCase):
    def setUp(self):
        self.pipeline = ClosedLoopPipeline("user_dash_test")

    def test_dashboard_payload_generation(self):
        mock_graph = {
            "pageUrl": "https://test-shop.com",
            "domain": "test-shop.com",
            "summary": {"totalNodes": 30, "actionCount": 6, "avgConfidence": 0.94},
            "root": {"id": "n1", "role": "filter", "confidence": 0.95, "children": []}
        }
        mock_events = [{"timestamp": 1000, "eventType": "click", "targetSelector": "button.nav", "dwellTimeMs": 10000}]
        
        record = self.pipeline.execute_closed_loop_step(mock_graph, mock_events)
        
        # Verify complete payload structure
        self.assertEqual(record.domain, "test-shop.com")
        self.assertIn("level", record.friction_assessment)
        self.assertIn("type", record.selected_intervention)
        self.assertTrue(record.model_updated)

if __name__ == '__main__':
    unittest.main()
