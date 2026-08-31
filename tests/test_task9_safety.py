"""
Unit tests for Task 9: Intervention Safety Policy Layer
"""

import unittest
from core.adaptive_layer.safety_policy import SafetyPolicyEngine, ElementRiskClassifier

class TestTask9Safety(unittest.TestCase):
    def setUp(self):
        self.safety = SafetyPolicyEngine()
        self.classifier = ElementRiskClassifier()

    def test_prohibited_elements_classification(self):
        self.assertEqual(
            self.classifier.classify_target_risk("input[type='password']"), "PROHIBITED"
        )
        self.assertEqual(
            self.classifier.classify_target_risk("button[aria-label='Delete Account']"), "PROHIBITED"
        )
        self.assertEqual(
            self.classifier.classify_target_risk("input[name='card_number']"), "PROHIBITED"
        )

    def test_medium_and_low_risk_classification(self):
        self.assertEqual(
            self.classifier.classify_target_risk("button#reposition-menu"), "MEDIUM"
        )
        self.assertEqual(
            self.classifier.classify_target_risk("button.filter-btn"), "LOW"
        )

    def test_safety_policy_enforcement(self):
        # 1. Prohibited Candidate -> Rejected
        prohibited_cand = {"id": "int_bad", "targetSelector": "button[id='pay-now']"}
        res1 = self.safety.evaluate_intervention_safety(prohibited_cand)
        self.assertFalse(res1["allowed"])
        self.assertEqual(res1["risk_level"], "PROHIBITED")
        self.assertIsNotNone(res1["rejection_reason"])

        # 2. Low Risk Candidate -> Allowed automatically
        low_cand = {"id": "int_good", "targetSelector": "button.filter-btn"}
        res2 = self.safety.evaluate_intervention_safety(low_cand)
        self.assertTrue(res2["allowed"])
        self.assertFalse(res2["requires_user_confirmation"])

if __name__ == '__main__':
    unittest.main()
