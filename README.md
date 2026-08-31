# 🚀 CUIX — Cognitive User Interface eXtension

> **Adaptive Browser Engine for Frictionless Web Interaction**

CUIX is an intelligent browser extension that observes how users interact with web applications, builds a generalized **Personal Interaction Twin**, automatically detects cognitive friction, simulates potential UI adaptations using a **Counterfactual Simulator**, and applies **minimum-disruption adaptations** in real time.

---

## 🎯 Master Roadmap & Fallback Levels

| Level | Scope | Capabilities | Status |
|---|---|---|---|
| **Level 1** | Minimum Viable | Web understanding, telemetry recording, user twin modeling, action prediction | 🚧 Phase 0 - Phase 4 |
| **Level 2** | Research Core | Task progression tracker + Cross-site user twin transfer evaluation | 📋 Phase 5 & Phase 7 |
| **Level 3** | Adaptive Engine | Real-time interaction friction detector (ML classification) | 📋 Phase 6 |
| **Level 4** | Predictive Counterfactual | Multi-candidate intervention simulator & low-disruption optimizer | 📋 Phase 8 - Phase 10 |
| **Level 5** | Closed-Loop Autonomous | Real DOM adaptation layer, safe rollback controller, closed-loop model update | 📋 Phase 11 - Phase 14 |

---

## 📐 Architecture Overview

```
                         ┌──────────────┐
                         │   WEBSITE    │
                         └──────┬───────┘
                                ↓
                   ┌────────────────────────┐
                   │ 1. INTERFACE GRAPH     │
                   │ (DOM + A11y + Visual)  │
                   └────────────┬───────────┘
                                ↓
             ┌──────────────────┴─────────────────┐
             ↓                                    ↓
   ┌────────────────────┐               ┌────────────────────┐
   │ 2. USER TWIN       │               │ 3. TASK ENGINE     │
   │ (Behavior Profile) │               │ (Goal Progression) │
   └──────────┬─────────┘               └──────────┬─────────┘
              └──────────────────┬─────────────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 4. FRICTION DETECTOR   │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 5. COUNTERFACTUAL SIM  │
                    │ & UTILITY OPTIMIZER    │
                    └────────────┬───────────┘
                                 ↓
                    ┌────────────────────────┐
                    │ 6. ADAPTATION LAYER    │
                    └────────────┬───────────┘
                                 ↓
                              USER
```

---

## 👥 Team Work Breakdown Structure (6 Sub-Teams)

- **Team 1 — Browser & Runtime**: Manifest V3 Content Scripting, DOM Observers, Adaptation Injection Engine, Rollback Controller.
- **Team 2 — Interface Intelligence**: Semantic UI Classification, Accessible Tree Parsing, Interface Graph Generation.
- **Team 3 — User Interaction Twin**: Telemetry Processing, Dwell/Navigation Feature Extraction, Personal Interaction Twin.
- **Team 4 — Task & Friction Analysis**: Task Goal Representation, Progression Tracking, Friction Detection Classifiers.
- **Team 5 — Counterfactual Simulation & Optimization**: Multi-Intervention Generator, Outcome Simulator, Utility Optimization.
- **Team 6 — Platform Infrastructure & Evaluation**: Dashboard, Closed-Loop Telemetry, Automated Benchmark Suite, Patent/Paper Documentation.

---

## 🛠️ Repository Quickstart

```bash
# Clone & install dependencies
cd extension
npm install

# Build extension for development
npm run build
```

---

## 📄 Documentation

- [System Architecture Specification](docs/ARCHITECTURE.md)
- [Privacy & Safety Rules](docs/PRIVACY_SAFETY.md)
- [Evaluation Metrics & Benchmarks](docs/METRICS.md)
- [Complete 16-Phase Timeline](docs/PHASE_ROADMAP.md)
