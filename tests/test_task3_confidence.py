"""
Unit tests for Task 3: Multi-Signal Interface Graph & Confidence Scoring
"""

import unittest
from tests.harness.site_evaluator import classify_element_with_confidence
from core.interface_graph.builder import InterfaceGraphAnalyzer

class TestTask3Confidence(unittest.TestCase):
    def test_high_confidence_button(self):
        el = {"tag": "button", "id": "cta", "class": "btn", "role": "button", "aria_label": "Submit Form", "type": "", "placeholder": ""}
        role, conf = classify_element_with_confidence(el)
        self.assertEqual(role, "action")
        self.assertGreaterEqual(conf, 0.95)

    def test_search_confidence_scoring(self):
        el = {"tag": "input", "id": "search-box", "class": "", "role": "search", "aria_label": "Search products", "type": "search", "placeholder": "Search..."}
        role, conf = classify_element_with_confidence(el)
        self.assertEqual(role, "search")
        self.assertGreaterEqual(conf, 0.95)

    def test_python_graph_confidence_filtering(self):
        raw_graph = {
            "pageUrl": "https://example.com",
            "domain": "example.com",
            "summary": {"totalNodes": 2, "avgConfidence": 0.90},
            "root": {
                "id": "node_1",
                "role": "action",
                "confidence": 0.95,
                "children": [
                    {"id": "node_2", "role": "action", "confidence": 0.45, "children": []}
                ]
            }
        }
        analyzer = InterfaceGraphAnalyzer(raw_graph)
        high_conf_actions = analyzer.find_nodes_by_role("action", min_confidence=0.80)
        self.assertEqual(len(high_conf_actions), 1)
        self.assertEqual(high_conf_actions[0]["id"], "node_1")

if __name__ == '__main__':
    unittest.main()
