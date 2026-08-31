# 🚀 CUIX — Cognitive User Interface eXtension

> **Adaptive Browser Engine for Frictionless Web Interaction & Personal User Twin Modeling**

CUIX is a real-time, browser-native adaptive system that analyzes unfamiliar web interfaces, models personal user interaction behavior (Personal Interaction Twin), detects cognitive friction, evaluates counterfactual interventions using a low-disruption optimization engine, and dynamically applies minimal effective visual/structural adaptations.

---

## 🗺️ System Architecture

```
                         ┌──────────────┐
                         │   WEBSITE    │
                         └──────┬───────┘
                                ↓
                   ┌────────────────────────┐
                   │  1. WEB UNDERSTANDING  │
                   │ (DOM + A11y + Visual)  │
                   └────────────┬───────────┘
                                ↓
                   ┌────────────────────────┐
                   │   2. INTERFACE GRAPH   │
                   └────────────┬───────────┘
                                ↓
             ┌──────────────────┴─────────────────┐
             ↓                                    ↓
   ┌────────────────────┐               ┌────────────────────┐
   │   3. USER TWIN     │               │ 4. TASK MODEL      │
   │ (Behavior Profile) │               │ (Goal Progression) │
   └──────────┬─────────┘               └──────────┬─────────┘
              └──────────────────┬─────────────────┘
                                 ↓
                    ┌────────────────────────┐
                    │  5. FRICTION DETECTOR  │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 6. INTERVENTION ENGINE │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 7. COUNTERFACTUAL      │
                    │       SIMULATOR        │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 8. OPTIMIZER           │
                    │ Utility = Gain-Disrupt │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 9. ADAPTATION LAYER    │
                    └────────────┬───────────┘
                                 ↓
                              USER
```

---

## 🎯 Master Fallback Levels & Progress

| Level | Scope | Capabilities | Status |
|---|---|---|---|
| **Level 1** | Minimum Viable | Site-agnostic UI Graph, Telemetry Recorder, Personal User Twin vector | ✅ Implemented |
| **Level 2** | Research Core | Task Goal Progression Tracker + Cross-Site Generalization Testbed | ✅ Implemented |
| **Level 3** | Adaptive Engine | ML Interaction Friction Classifier (Dwell, Backtrack & Stale Signals) | ✅ Implemented |
| **Level 4** | Predictive Counterfactual | Multi-Candidate Generator, Counterfactual Simulator & Utility Optimizer | ✅ Implemented |
| **Level 5** | Closed-Loop Autonomous | Real DOM Adaptation Injection Layer, Rollback Manager & Dashboard | ✅ Implemented |

---

## 🛠️ Repository Structure

- `docs/`: Architecture specifications, privacy boundary rules, evaluation metrics, phase timeline.
- `extension/`: Manifest V3 extension, content script DOM observer, interface graph builder, popup & dashboard.
- `core/`: Python engine modules for UI Graph Parsing, Telemetry Processing, User Twin, Task Engine, Friction Detector, Counterfactual Simulator, Utility Optimizer, Adaptation Controller.
- `tests/`: Automated unit & integration tests.

---

## 🧪 Running Verification Tests

```bash
# Run complete Python engine test suite
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License & IP

Formulated for research paper publication & patent filing: *"Personalized counterfactual evaluation and minimum-disruption intervention selection for previously unseen web interfaces."*
