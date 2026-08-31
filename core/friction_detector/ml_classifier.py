"""
CUIX Task 7: ML-Based Friction Classifier & Model Benchmark Pipeline
Refactors friction detection into a trainable probabilistic decision model while retaining rule-based detector as baseline.
"""

from typing import Dict, Any, List, Tuple
import math

class MLFrictionClassifier:
    """Trainable ML classifier model for cognitive friction detection."""
    def __init__(self):
        # Learned feature weights initialized to empirical baseline priors
        self.weights = {
            "dwell_ratio": 1.20,
            "backtrack_rate": 1.80,
            "stalled_task": 1.10,
            "click_velocity": 0.50,
            "complexity_load": 0.80
        }
        self.bias = -1.50
        self.is_trained = False

    def _sigmoid(self, z: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, z))))

    def extract_feature_vector(
        self,
        telemetry_metrics: Dict[str, Any],
        user_twin_profile: Dict[str, Any],
        task_progress: Dict[str, Any],
        interface_complexity: float = 0.40
    ) -> Dict[str, float]:
        user_baseline_dwell = user_twin_profile.get('avg_decision_time_sec', 2.5) * 1000.0
        avg_dwell = telemetry_metrics.get('avg_dwell_time_ms', 0.0)
        dwell_ratio = avg_dwell / max(user_baseline_dwell, 1000.0)

        backtrack_rate = telemetry_metrics.get('backtrack_rate', 0.0)
        stalled = 1.0 if (task_progress.get("status") == "IN_PROGRESS" and not task_progress.get("advanced")) else 0.0
        click_velocity = telemetry_metrics.get('click_frequency_per_min', 0.0) / 60.0

        return {
            "dwell_ratio": round(dwell_ratio, 3),
            "backtrack_rate": round(backtrack_rate, 3),
            "stalled_task": stalled,
            "click_velocity": round(click_velocity, 3),
            "complexity_load": round(interface_complexity, 3)
        }

    def predict_friction(self, features: Dict[str, float]) -> Dict[str, Any]:
        z = self.bias + sum(features.get(k, 0.0) * w for k, w in self.weights.items())
        prob = self._sigmoid(z)

        if prob >= 0.70:
            level = "HIGH_FRICTION"
            confidence = prob
        elif prob >= 0.35:
            level = "POSSIBLE_FRICTION"
            confidence = prob
        else:
            level = "NORMAL"
            confidence = 1.0 - prob

        return {
            "level": level,
            "probability": round(prob, 3),
            "confidence": round(confidence, 3),
            "features_used": features,
            "model_type": "ML_LOGISTIC_REGRESSION"
        }

    def train_and_evaluate(
        self, dataset: List[Tuple[Dict[str, float], str]]
    ) -> Dict[str, Any]:
        """Trains model weights on 80/20 train/test split and computes precision/recall/F1 metrics."""
        split_idx = int(len(dataset) * 0.8)
        train_data = dataset[:split_idx]
        test_data = dataset[split_idx:]

        # Simple SGD weight update iteration
        for epoch in range(10):
            for features, label in train_data:
                target = 1.0 if label == "HIGH_FRICTION" else 0.0
                z = self.bias + sum(features.get(k, 0.0) * w for k, w in self.weights.items())
                pred = self._sigmoid(z)
                err = target - pred
                lr = 0.05
                self.bias += lr * err
                for k in self.weights:
                    self.weights[k] += lr * err * features.get(k, 0.0)

        self.is_trained = True

        # Test set evaluation
        correct = 0
        tp, fp, fn = 0, 0, 0
        for features, label in test_data:
            res = self.predict_friction(features)
            pred_label = res["level"]
            if (pred_label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"]) == (label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"]):
                correct += 1
            if pred_label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"] and label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"]:
                tp += 1
            elif pred_label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"] and label == "NORMAL":
                fp += 1
            elif pred_label == "NORMAL" and label in ["HIGH_FRICTION", "POSSIBLE_FRICTION"]:
                fn += 1

        acc = round(correct / max(len(test_data), 1), 3)
        precision = round(tp / max(tp + fp, 1), 3)
        recall = round(tp / max(tp + fn, 1), 3)
        f1 = round(2 * precision * recall / max(precision + recall, 0.001), 3)

        return {
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "test_samples": len(test_data)
        }
