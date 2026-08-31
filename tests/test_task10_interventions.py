"""
Unit tests for Task 10: Reversible UI Interventions Engine
"""

import unittest
from core.adaptive_layer.interventions import (
    HighlightIntervention, ProminenceIntervention, ContextualHintIntervention, ShortcutOverlayIntervention
)

class TestTask10Interventions(unittest.TestCase):
    def test_all_four_interventions_interface(self):
        interventions = [
            HighlightIntervention("i1", "button#filter"),
            ProminenceIntervention("i2", "button#filter"),
            ContextualHintIntervention("i3", "button#filter", hint_text="Click here to filter"),
            ShortcutOverlayIntervention("i4", "button#filter", key_shortcut="Alt+F")
        ]

        for item in interventions:
            payload = item.get_payload()
            self.assertIn("id", payload)
            self.assertIn("type", payload)
            self.assertEqual(payload["targetSelector"], "button#filter")
            self.assertGreater(payload["expected_benefit"], 0.0)
            self.assertIn("cost", payload)
            self.assertIn("disruption", payload)

if __name__ == '__main__':
    unittest.main()
