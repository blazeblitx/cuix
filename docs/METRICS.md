# 📊 CUIX Evaluation Metrics & Benchmark Suite

This document defines the quantitative evaluation suite for testing CUIX across static UIs, basic adaptive baselines, and full CUIX counterfactual optimization.

---

## 1. Core Evaluation Metrics

| Metric | Target / Unit | Description & Calculation |
|---|---|---|
| **Task Success Rate (TSR)** | % (higher is better) | Proportion of controlled user tasks completed without abandonment. |
| **Completion Time (TCT)** | Seconds (lower is better) | Total elapsed duration from task initialization to goal node execution. |
| **Error / Backtrack Rate** | Count per session | Number of erroneous clicks, form validation failures, or page backtrack actions. |
| **Intervention Conservative Index** | Integer count | Average number of adaptations applied per session (measures conservatism). |
| **Cross-Site Generalization Score** | Accuracy % | Prediction accuracy of User Twin on unseen domain $D_{\text{unseen}}$ trained only on domains $A, B, C$. |
| **CLS Disruption Penalty** | Cumulative Layout Shift (0.0 to 1.0) | Standard layout shift score caused by injected adaptations. |
| **Rollback Frequency** | % of interventions | Rate at which user triggers rollback / undo on an intervention. |

---

## 2. Experimental Group Matrix (Phase 14 Testbed)

- **Group A (Control)**: Standard unmodified static interface.
- **Group B (Heuristic Baseline)**: Rule-based static adaptations (e.g. highlight most clicked element).
- **Group C (Full CUIX)**: Personal User Twin + Counterfactual Simulator + Utility Optimizer.
