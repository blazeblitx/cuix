"""
Unit tests for CUIX Interface Graph Analyzer (Phase 2)
"""

import unittest
from core.interface_graph.builder import InterfaceGraphAnalyzer

MOCK_GRAPH = {
    "pageUrl": "https://example.com/shop",
    "domain": "example.com",
    "title": "Example Shop",
    "timestamp": 1700000000,
    "summary": {
        "totalNodes": 45,
        "navigationCount": 4,
        "searchCount": 1,
        "filterCount": 3,
        "actionCount": 12,
        "inputCount": 2
    },
    "root": {
        "id": "node_1",
        "role": "content",
        "tag": "body",
        "selector": "body",
        "text": "",
        "isVisible": True,
        "boundingBox": {"x": 0, "y": 0, "width": 1280, "height": 800},
        "children": [
            {
                "id": "node_2",
                "role": "search",
                "tag": "input",
                "selector": "#search-input",
                "text": "",
                "ariaLabel": "Search products",
                "isVisible": True,
                "boundingBox": {"x": 100, "y": 20, "width": 300, "height": 40},
                "children": []
            },
            {
                "id": "node_3",
                "role": "filter",
                "tag": "button",
                "selector": ".filter-btn",
                "text": "Filter by Price",
                "isVisible": True,
                "boundingBox": {"x": 100, "y": 80, "width": 120, "height": 30},
                "children": []
            }
        ]
    }
}

class TestInterfaceGraph(unittest.TestCase):
    def test_analyzer_parsing(self):
        analyzer = InterfaceGraphAnalyzer(MOCK_GRAPH)
        self.assertEqual(analyzer.domain, "example.com")
        
        searches = analyzer.find_nodes_by_role("search")
        self.assertEqual(len(searches), 1)
        self.assertEqual(searches[0]["selector"], "#search-input")
        
        actionables = analyzer.get_actionable_elements()
        self.assertEqual(len(actionables), 2)
        
        complexity = analyzer.compute_interface_complexity_score()
        self.assertTrue(0.0 <= complexity <= 1.0)

if __name__ == '__main__':
    unittest.main()
