"""
End-to-End Integration Test for Task 1
Executes full pipeline: Webpage Graph -> Telemetry -> User Twin -> Friction -> Candidates -> Utility Optimizer -> Adaptation -> Rollback
"""

import unittest
import threading
import time
import urllib.request
import json
from core.server import run_server

SERVER_PORT = 8008
BASE_URL = f"http://localhost:{SERVER_PORT}/api"

class TestEndToEndPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start local Python server in background daemon thread
        cls.server_thread = threading.Thread(target=run_server, args=(SERVER_PORT,), daemon=True)
        cls.server_thread.start()
        time.sleep(0.5)  # Allow server socket to bind

    def _post_json(self, endpoint: str, payload: dict) -> dict:
        req = urllib.request.Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))

    def _get_json(self, endpoint: str) -> dict:
        req = urllib.request.Request(f"{BASE_URL}{endpoint}")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))

    def test_end_to_end_flow(self):
        # 1. Healthcheck
        health = self._get_json('/health')
        self.assertEqual(health['status'], 'HEALTHY')

        # 2. Webpage -> Interface Graph ingestion
        graph_payload = {
            "pageUrl": "https://test-shop.com/backpacks",
            "domain": "test-shop.com",
            "title": "Backpack Store",
            "timestamp": 1700000000,
            "summary": {"totalNodes": 30, "actionCount": 8, "filterCount": 2},
            "root": {
                "id": "root_1",
                "role": "content",
                "tag": "body",
                "selector": "body",
                "isVisible": True,
                "children": [
                    {
                        "id": "node_filter",
                        "role": "filter",
                        "tag": "button",
                        "selector": "button.filter-btn",
                        "text": "Filter under $50",
                        "isVisible": True,
                        "children": []
                    }
                ]
            }
        }
        res_graph = self._post_json('/interface-graph', graph_payload)
        self.assertEqual(res_graph['status'], 'GRAPH_RECEIVED')
        self.assertEqual(res_graph['domain'], 'test-shop.com')

        # 3. Telemetry -> User Twin update
        telemetry_payload = {
            "events": [
                {"timestamp": 1000, "eventType": "click", "targetSelector": "button.nav"},
                {"timestamp": 15000, "eventType": "click", "targetSelector": "button.nav"},
                {"timestamp": 15100, "eventType": "backtrack", "targetSelector": "body"},
                {"timestamp": 30000, "eventType": "click", "targetSelector": "button.nav"},
                {"timestamp": 30100, "eventType": "backtrack", "targetSelector": "body"}
            ]
        }
        res_telemetry = self._post_json('/telemetry', telemetry_payload)
        self.assertEqual(res_telemetry['status'], 'TELEMETRY_UPDATED')
        self.assertGreater(res_telemetry['metrics']['avg_dwell_time_ms'], 5000)

        # 4. Friction Assessment -> Intervention Candidates -> Utility Optimization -> Checkpoint Creation
        res_eval = self._post_json('/evaluate', {})
        self.assertEqual(res_eval['status'], 'EVALUATED')
        self.assertIn(res_eval['friction_assessment']['level'], ['POSSIBLE_FRICTION', 'HIGH_FRICTION'])
        
        selected = res_eval['selected_intervention']
        self.assertIsNotNone(selected)
        self.assertIn('utility_score', selected)
        self.assertEqual(selected['targetSelector'], 'button.filter-btn')

        checkpoint = res_eval['checkpoint']
        self.assertIsNotNone(checkpoint)
        self.assertTrue(checkpoint['checkpoint_id'].startswith('chk_'))

        # 5. UI Adaptation Rollback
        res_rollback = self._post_json('/rollback', {"checkpoint_id": checkpoint['checkpoint_id']})
        self.assertEqual(res_rollback['status'], 'ROLLBACK_SUCCESSFUL')
        self.assertIn(checkpoint['checkpoint_id'], res_rollback['rolled_back_checkpoints'])

if __name__ == '__main__':
    unittest.main()
