"""
Unit tests for CUIX Telemetry Processor and User Twin Model (Phases 3 & 4)
"""

import unittest
from core.telemetry.processor import TelemetryProcessor
from core.user_twin.model import PersonalInteractionTwin

class TestTelemetryTwin(unittest.TestCase):
    def setUp(self):
        self.mock_events = [
            {"timestamp": 1000, "eventType": "click", "targetSelector": "button#search"},
            {"timestamp": 3000, "eventType": "scroll", "targetSelector": "body"},
            {"timestamp": 5000, "eventType": "click", "targetSelector": "input#filter"},
            {"timestamp": 5200, "eventType": "keypress", "targetSelector": "input#filter"},
            {"timestamp": 5400, "eventType": "keypress", "targetSelector": "input#filter"},
            {"timestamp": 8000, "eventType": "click", "targetSelector": "button#submit"}
        ]

    def test_telemetry_processor(self):
        processor = TelemetryProcessor(self.mock_events)
        metrics = processor.compute_session_metrics()
        self.assertEqual(metrics["total_events"], 6)
        self.assertEqual(metrics["click_count"], 3)
        self.assertGreater(metrics["avg_dwell_time_ms"], 0)

    def test_twin_adaptation(self):
        twin = PersonalInteractionTwin("user_test")
        initial_kb = twin.keyboard_usage
        twin.update_from_session(self.mock_events)
        # Should adapt keyboard usage vector based on keypress events
        self.assertNotEqual(twin.keyboard_usage, initial_kb)
        self.assertEqual(twin.sample_count, 1)

if __name__ == '__main__':
    unittest.main()
