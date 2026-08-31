# 🌐 CUIX System Architecture & Data Pipeline Contract

This document specifies the technical data flow, schema interfaces, and execution stages of the CUIX system.

---

## 1. Pipeline Overview

```
[ Web Page DOM / A11y Tree ]
             │
             ▼
 ┌───────────────────────┐
 │ Interface Graph Engine │ ──► InterfaceGraph JSON
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Telemetry Recorder    │ ──► TelemetryFrame JSON (Local IndexedDB)
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Personal User Twin    │ ──► UserTwin Vector / Feature Matrix
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Task & Friction Model │ ──► FrictionScore (NORMAL, POSSIBLE_FRICTION, HIGH_FRICTION)
 └───────────────────────┘
             │
             ▼ (If HIGH_FRICTION)
 ┌───────────────────────┐
 │ Intervention Generator│ ──► Candidate Interventions [A, B, C, ...]
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Counterfactual Sim    │ ──► Predicted Success Rates & Layout Shift Scores
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Utility Optimizer     │ ──► Selected Intervention (Minimum Effective Disruption)
 └───────────────────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Adaptation Layer      │ ──► Dynamic DOM Highlight / CSS Overlay / Undo Checkpoint
 └───────────────────────┘
```

---

## 2. Module Interface Specs

### Interface Graph (Phase 2)
```typescript
interface InterfaceNode {
  id: string;
  role: 'navigation' | 'search' | 'filter' | 'action' | 'input' | 'content';
  tag: string;
  selector: string;
  text: string;
  ariaLabel?: string;
  isVisible: boolean;
  boundingBox: { x: number; y: number; width: number; height: number };
  children: InterfaceNode[];
}

interface InterfaceGraph {
  pageUrl: string;
  title: string;
  timestamp: number;
  root: InterfaceNode;
}
```

### Telemetry Frame (Phase 3)
```typescript
interface TelemetryEvent {
  timestamp: number;
  eventType: 'click' | 'scroll' | 'keypress' | 'hover' | 'focus' | 'backtrack';
  targetSelector: string;
  cursorPos?: { x: number; y: number };
  scrollOffset?: { top: number; left: number };
  dwellTimeMs?: number;
}

interface UserSession {
  sessionId: string;
  domain: string;
  startTime: number;
  events: TelemetryEvent[];
}
```

### Personal Interaction Twin (Phase 4 & 7)
```typescript
interface UserTwinProfile {
  userId: string;
  searchPreferenceScore: number;  // 0.0 (visual menu browser) to 1.0 (heavy search bar user)
  keyboardUsageRatio: number;      // Ratio of keyboard shortcuts/navigation to mouse clicks
  menuDepthPreference: number;     // Tendency to drill down nested menus
  backtrackingRate: number;        // Frequency of back-button / page navigation reversal
  avgDecisionTimeMs: number;       // Mean pause time prior to high-confidence click
}
```

### Counterfactual Simulation & Optimization (Phase 9 & 10)
```typescript
interface InterventionCandidate {
  id: string;
  type: 'HIGHLIGHT_ELEMENT' | 'INCREASE_PROMINENCE' | 'CONTEXTUAL_HINT' | 'EXPOSE_HIDDEN' | 'ADAPTIVE_SHORTCUT';
  targetSelector: string;
  payload: Record<string, any>;
}

interface SimulationOutcome {
  candidate: InterventionCandidate;
  predictedSuccessRate: number; // e.g. 0.85
  disruptionScore: number;       // Cumulative Layout Shift (CLS) + visual entropy delta
  modificationCost: number;     // Complexity of DOM mutation
  riskFactor: number;           // Penalty for proximity to critical controls
  computedUtility: number;      // Output of Objective Function
}
```
