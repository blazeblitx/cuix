"""
Automated Test Suite for Task 2 & 3 Testing Harness & Discovered Edge Cases
"""

import unittest
import os
from tests.harness.site_evaluator import SiteBenchmarkEvaluator, classify_element_with_confidence

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures', 'test_sites')

class TestSiteHarness(unittest.TestCase):
    def setUp(self):
        self.evaluator = SiteBenchmarkEvaluator(FIXTURES_DIR)

    def test_evaluate_all_five_sites(self):
        results = self.evaluator.evaluate_all()
        self.assertEqual(len(results), 5)
        
        filenames = [r['file'] for r in results]
        self.assertIn('ecommerce.html', filenames)
        self.assertIn('saas_dashboard.html', filenames)
        self.assertIn('news_portal.html', filenames)
        self.assertIn('form_wizard.html', filenames)
        self.assertIn('spa_app.html', filenames)

        for res in results:
            self.assertGreater(res['total_nodes'], 0)
            self.assertIn('role_counts', res)
            self.assertGreater(res['avg_confidence'], 0.50)

    def test_edge_case_div_role_button(self):
        el = {"tag": "div", "id": "", "class": "tab", "role": "button", "aria_label": "", "type": "", "placeholder": ""}
        role, conf = classify_element_with_confidence(el)
        self.assertEqual(role, "action")
        self.assertGreaterEqual(conf, 0.80)

    def test_edge_case_placeholder_search(self):
        el = {"tag": "input", "id": "q", "class": "", "role": "", "aria_label": "", "type": "text", "placeholder": "Search news..."}
        role, conf = classify_element_with_confidence(el)
        self.assertEqual(role, "search")
        self.assertGreaterEqual(conf, 0.70)

    def test_edge_case_aria_label_filter(self):
        el = {"tag": "div", "id": "", "class": "custom-dropdown", "role": "button", "aria_label": "Sort options", "type": "", "placeholder": ""}
        role, conf = classify_element_with_confidence(el)
        self.assertEqual(role, "filter")
        self.assertGreaterEqual(conf, 0.85)

if __name__ == '__main__':
    unittest.main()
