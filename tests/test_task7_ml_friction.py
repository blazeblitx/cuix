"""
Unit tests for Task 7: ML Friction Detector vs Baseline Model Comparison
"""

import unittest
from core.friction_detector.classifier import FrictionDetector as BaselineFrictionDetector
from core.friction_detector.ml_classifier import MLFrictionClassifier

class TestTask7MLFriction(unittest.TestCase):
    def setUp(self):
        self.baseline = BaselineFrictionDetector()
        self.ml_classifier = MLFrictionClassifier()

    def test_feature_extraction(self):
        telemetry = {"avg_dwell_time_ms": 10000.0, "backtrack_rate": 0.45, "click_frequency_per_min": 12.0}
        twin = {"avg_decision_time_sec": 2.5}
        task = {"status": "IN_PROGRESS", "advanced": False}

        features = self.ml_classifier.extract_feature_vector(telemetry, twin, task, interface_complexity=0.50)
        self.assertIn("dwell_ratio", features)
        self.assertEqual(features["stalled_task"], 1.0)
        self.assertEqual(features["dwell_ratio"], 4.0)

    def test_ml_prediction_confidence(self):
        features = {
            "dwell_ratio": 5.0,
            "backtrack_rate": 0.60,
            "stalled_task": 1.0,
            "click_velocity": 0.20,
            "complexity_load": 0.60
        }
        res = self.ml_classifier.predict_friction(features)
        self.assertEqual(res["level"], "HIGH_FRICTION")
        self.assertGreaterEqual(res["confidence"], 0.70)
        self.assertIn("probability", res)

    def test_train_and_evaluate_pipeline(self):
        # Generate synthetic benchmark dataset
        dataset = []
        for i in range(50):
            # High friction samples
            hf_feat = {"dwell_ratio": 4.5, "backtrack_rate": 0.55, "stalled_task": 1.0, "click_velocity": 0.1, "complexity_load": 0.6}
            dataset.append((hf_feat, "HIGH_FRICTION"))
            # Normal samples
            norm_feat = {"dwell_ratio": 1.0, "backtrack_rate": 0.05, "stalled_task": 0.0, "click_velocity": 0.3, "complexity_load": 0.3}
            dataset.append((norm_feat, "NORMAL"))

        metrics = self.ml_classifier.train_and_evaluate(dataset)
        self.assertGreaterEqual(metrics["accuracy"], 0.85)
        self.assertGreaterEqual(metrics["f1_score"], 0.80)
        self.assertTrue(self.ml_classifier.is_trained)

if __name__ == '__main__':
    unittest.main()
