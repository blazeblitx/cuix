"""
Unit tests for Task 6: Cross-Site Generalization Experiment Engine
Verifies transferability of learned Personal Interaction Twin to an unseen domain D without site-specific rules.
"""

import unittest
from core.user_twin.cross_site_experiment import CrossSiteTransferExperiment

class TestTask6CrossSite(unittest.TestCase):
    def test_cross_site_transfer_experiment(self):
        exp = CrossSiteTransferExperiment()

        # Site A (Ecommerce): Search user
        site_a = [
            {"eventType": "click", "targetSelector": "input#search-box"},
            {"eventType": "click", "targetSelector": "input#search-box"}
        ]
        # Site B (SaaS): Search user
        site_b = [
            {"eventType": "click", "targetSelector": "input.searchbox"},
            {"eventType": "click", "targetSelector": "input.searchbox"}
        ]
        # Site C (News): Search user
        site_c = [
            {"eventType": "click", "targetSelector": "input.news-search"}
        ]

        # Unseen Site D (SPA): User demonstrates search preference
        site_d_unseen = [
            {"eventType": "click", "targetSelector": "input.search-bar-spa"},
            {"eventType": "click", "targetSelector": "input.search-bar-spa"}
        ]

        res = exp.run_experiment([site_a, site_b, site_c], site_d_unseen)
        
        self.assertTrue(res["transfer_metrics"]["transfer_successful"])
        self.assertGreater(
            res["personalized_twin"]["accuracy"],
            res["baseline_model"]["accuracy"]
        )
        self.assertLess(
            res["personalized_twin"]["error_rate"],
            res["baseline_model"]["error_rate"]
        )

if __name__ == '__main__':
    unittest.main()
