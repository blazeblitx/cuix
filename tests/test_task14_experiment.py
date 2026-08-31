"""
Unit tests for Task 14: Reproducible Scientific Experiment Framework
"""

import unittest
import os
from core.experiment_framework import CUIXBenchmarkExperiment

class TestTask14Experiment(unittest.TestCase):
    def setUp(self):
        self.exp = CUIXBenchmarkExperiment(random_seed=42)

    def test_run_full_experiment_suite(self):
        res = self.exp.run_full_experiment_suite(trials_per_group=30)
        self.assertIn("group_summaries", res)
        self.assertIn("GROUP_A_CONTROL", res["group_summaries"])
        self.assertIn("GROUP_B_RULE_BASED", res["group_summaries"])
        self.assertIn("GROUP_C_FULL_CUIX", res["group_summaries"])

        # Check CI95 calculation
        group_c = res["group_summaries"]["GROUP_C_FULL_CUIX"]
        self.assertGreater(group_c["task_success_rate"]["mean"], 0.88)
        self.assertGreater(group_c["task_success_rate"]["ci95"], 0.0)
        self.assertLess(group_c["disruption_cls"]["mean"], 0.10)

        # Takeaway metrics
        self.assertGreater(res["key_takeaways"]["tsr_improvement_cuix_vs_control"], 0.20)

    def test_export_anonymized_report(self):
        res = self.exp.run_full_experiment_suite(trials_per_group=10)
        export_path = os.path.join(os.path.dirname(__file__), '..', 'exports', 'test_results.json')
        out_file = self.exp.export_anonymized_report(res, export_path=export_path)
        self.assertTrue(os.path.exists(out_file))

if __name__ == '__main__':
    unittest.main()
