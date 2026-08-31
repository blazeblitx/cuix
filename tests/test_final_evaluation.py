"""
Automated Test Suite for CUIX Final Boss Evaluation across 5 Unseen Web Interfaces
"""

import unittest
import os
from tests.final_benchmark_evaluator import FinalCapstoneEvaluator

class TestFinalEvaluation(unittest.TestCase):
    def setUp(self):
        self.evaluator = FinalCapstoneEvaluator()

    def test_final_comprehensive_evaluation(self):
        report = self.evaluator.run_comprehensive_evaluation()
        self.assertEqual(report["tested_unseen_interfaces_count"], 5)
        
        metrics = report["capstone_metrics"]
        self.assertGreaterEqual(metrics["interface_understanding_avg_confidence"], 0.60)
        self.assertGreaterEqual(metrics["user_behavior_prediction_accuracy"], 0.70)
        self.assertGreater(metrics["cross_site_transfer_accuracy_gain"], 0.0)
        self.assertLessEqual(metrics["intervention_disruption_cls"], 0.10)
        self.assertLessEqual(metrics["rollback_rate_pct"], 5.0)

        # Failure cases explicitly identified
        failures = report["explicit_failure_cases_identified"]
        self.assertGreaterEqual(len(failures), 2)
        self.assertEqual(failures[0]["failure_case_id"], "FAIL_001")

        # Export final report
        export_path = os.path.join(os.path.dirname(__file__), '..', 'exports', 'final_cuix_eval_report.json')
        out = self.evaluator.export_report(report, path=export_path)
        self.assertTrue(os.path.exists(out))

if __name__ == '__main__':
    unittest.main()
