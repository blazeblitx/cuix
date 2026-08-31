"""
CUIX Python Local API Backend Server (Task 1)
Bridge connecting Chrome Extension client runtime with CUIX Core Intelligence Engine.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Dict, Any

from core.interface_graph.builder import InterfaceGraphAnalyzer
from core.telemetry.processor import TelemetryProcessor
from core.user_twin.model import PersonalInteractionTwin
from core.task_engine.tracker import TaskProgressionTracker, TaskGoal, TaskStep
from core.friction_detector.classifier import FrictionDetector
from core.simulator.counterfactual import CounterfactualSimulator
from core.optimizer.utility import InterventionOptimizer
from core.adaptive_layer.controller import AdaptationController

# In-memory runtime state for single-user local extension session
SESSION_TWIN = PersonalInteractionTwin(user_id="local_user")
TASK_TRACKER = TaskProgressionTracker()
FRICTION_DETECTOR = FrictionDetector()
SIMULATOR = CounterfactualSimulator()
OPTIMIZER = InterventionOptimizer()
ADAPTATION_CONTROLLER = AdaptationController()

# Active interface graph cache
LATEST_GRAPH: Dict[str, Any] = {}
SESSION_TELEMETRY: list = []

class CUIXRequestHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, data: Dict[str, Any], code: int = 200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/health':
            self._send_json_response({
                "status": "HEALTHY",
                "engine": "CUIX Core",
                "user_twin": SESSION_TWIN.to_dict(),
                "active_checkpoints": len(ADAPTATION_CONTROLLER.checkpoints)
            })
        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}

        if self.path == '/api/interface-graph':
            global LATEST_GRAPH
            LATEST_GRAPH = data
            analyzer = InterfaceGraphAnalyzer(data)
            complexity = analyzer.compute_interface_complexity_score()
            self._send_json_response({
                "status": "GRAPH_RECEIVED",
                "domain": analyzer.domain,
                "complexity_score": complexity,
                "actionable_elements_count": len(analyzer.get_actionable_elements())
            })

        elif self.path == '/api/telemetry':
            events = data.get('events', [])
            SESSION_TELEMETRY.extend(events)
            SESSION_TWIN.update_from_session(events)
            processor = TelemetryProcessor(SESSION_TELEMETRY)
            metrics = processor.compute_session_metrics()
            self._send_json_response({
                "status": "TELEMETRY_UPDATED",
                "metrics": metrics,
                "twin": SESSION_TWIN.to_dict()
            })

        elif self.path == '/api/evaluate':
            processor = TelemetryProcessor(SESSION_TELEMETRY)
            metrics = processor.compute_session_metrics()
            task_status = TASK_TRACKER.process_interaction("click", "unknown")
            
            assessment = FRICTION_DETECTOR.evaluate_friction(
                metrics, SESSION_TWIN.to_dict(), task_status
            )

            selected_intervention = None
            checkpoint_info = None

            if assessment.get('level') in ['POSSIBLE_FRICTION', 'HIGH_FRICTION']:
                target_node = {"selector": "button.filter-btn", "role": "filter"}
                if LATEST_GRAPH and LATEST_GRAPH.get('root'):
                    analyzer = InterfaceGraphAnalyzer(LATEST_GRAPH)
                    actionables = analyzer.get_actionable_elements()
                    if actionables:
                        target_node = actionables[0]

                candidates = SIMULATOR.generate_candidate_interventions(target_node, assessment)
                simulated = SIMULATOR.simulate_outcomes(candidates)
                selected_intervention = OPTIMIZER.select_best_intervention(simulated)

                if selected_intervention:
                    chk = ADAPTATION_CONTROLLER.create_checkpoint(
                        selected_intervention.get('id', 'int_1'),
                        selected_intervention.get('targetSelector', 'body'),
                        "original-style-snapshot"
                    )
                    checkpoint_info = {
                        "checkpoint_id": chk.checkpoint_id,
                        "target_selector": chk.target_selector
                    }

            self._send_json_response({
                "status": "EVALUATED",
                "friction_assessment": assessment,
                "selected_intervention": selected_intervention,
                "checkpoint": checkpoint_info
            })

        elif self.path == '/api/rollback':
            checkpoint_id = data.get('checkpoint_id')
            if checkpoint_id:
                rolled = ADAPTATION_CONTROLLER.rollback_checkpoint(checkpoint_id)
                rolled_list = [rolled.checkpoint_id] if rolled else []
            else:
                rolled_objs = ADAPTATION_CONTROLLER.rollback_all()
                rolled_list = [r.checkpoint_id for r in rolled_objs]

            self._send_json_response({
                "status": "ROLLBACK_SUCCESSFUL",
                "rolled_back_checkpoints": rolled_list
            })

        else:
            self._send_json_response({"error": "Endpoint not found"}, 404)

def run_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CUIXRequestHandler)
    print(f"[CUIX Server] Listening on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
