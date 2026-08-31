"""
Unit tests for Task 4: Gemini Semantic Interface Analyzer & Validation Guardrails
"""

import unittest
from core.interface_graph.gemini_analyzer import GeminiInterfaceAnalyzer
from core.interface_graph.builder import InterfaceGraphAnalyzer

class TestTask4Gemini(unittest.TestCase):
    def setUp(self):
        self.gemini = GeminiInterfaceAnalyzer()

    def test_sanitize_node(self):
        node = {
            "tag": "button",
            "selector": "button#cta",
            "ariaLabel": "Submit",
            "text": "SECRET_PASSWORD_PAYLOAD_DO_NOT_INCLUDE",
            "boundingBox": {"x": 10, "y": 20, "width": 100, "height": 40},
            "children": [{"tag": "span"}]
        }
        sanitized = self.gemini.sanitize_node_representation(node)
        self.assertNotIn("text", sanitized)
        self.assertEqual(sanitized["tag"], "button")
        self.assertEqual(sanitized["children_count"], 1)

    def test_validate_llm_json_response_success(self):
        raw_llm = '{"role": "filter", "confidence": 0.88, "reasoning": "Element handles product sorting."}'
        validated = self.gemini.validate_llm_response(raw_llm)
        self.assertTrue(validated["valid"])
        self.assertEqual(validated["role"], "filter")
        self.assertEqual(validated["confidence"], 0.88)

    def test_validate_llm_malformed_json_fallback(self):
        raw_llm = "This is hallucinated free text without valid JSON markup!"
        validated = self.gemini.validate_llm_response(raw_llm)
        self.assertFalse(validated["valid"])
        self.assertEqual(validated["role"], "content")
        self.assertEqual(validated["confidence"], 0.50)

    def test_high_confidence_bypasses_gemini(self):
        raw_graph = {
            "pageUrl": "https://example.com",
            "domain": "example.com",
            "root": {
                "id": "node_1",
                "role": "action",
                "confidence": 0.95,
                "children": []
            }
        }
        analyzer = InterfaceGraphAnalyzer(raw_graph, gemini_analyzer=self.gemini)
        res = analyzer.resolve_element_role_with_fallback(raw_graph["root"])
        self.assertEqual(res["source"], "DETERMINISTIC_DOM_A11Y")
        self.assertEqual(res["confidence"], 0.95)

    def test_low_confidence_invokes_gemini_fallback(self):
        raw_graph = {
            "pageUrl": "https://example.com",
            "domain": "example.com",
            "root": {
                "id": "ambiguous_1",
                "role": "content",
                "confidence": 0.45,
                "tag": "div",
                "selector": "div.custom-widget",
                "children": []
            }
        }
        analyzer = InterfaceGraphAnalyzer(raw_graph, gemini_analyzer=self.gemini)
        res = analyzer.resolve_element_role_with_fallback(raw_graph["root"])
        self.assertEqual(res["source"], "DETERMINISTIC_FALLBACK")
        self.assertGreaterEqual(res["confidence"], 0.70)

if __name__ == '__main__':
    unittest.main()
