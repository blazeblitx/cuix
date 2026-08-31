// CUIX Shared Type Definitions across Extension & Core Engine

export type ElementRole = 
  | 'navigation' 
  | 'search' 
  | 'filter' 
  | 'action' 
  | 'input' 
  | 'form' 
  | 'menu' 
  | 'heading' 
  | 'content'
  | 'unknown';

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface InterfaceNode {
  id: string;
  role: ElementRole;
  confidence: number; // Task 3: Classification Confidence Score [0.00 to 1.00]
  tag: string;
  selector: string;
  text: string;
  ariaLabel?: string;
  isVisible: boolean;
  boundingBox: BoundingBox;
  children: InterfaceNode[];
}

export interface InterfaceGraph {
  pageUrl: string;
  domain: string;
  title: string;
  timestamp: number;
  root: InterfaceNode;
  summary: {
    totalNodes: number;
    navigationCount: number;
    searchCount: number;
    filterCount: number;
    actionCount: number;
    inputCount: number;
    avgConfidence: number;
  };
}

export type EventType = 
  | 'click' 
  | 'scroll' 
  | 'keypress' 
  | 'typing' 
  | 'hover' 
  | 'focus' 
  | 'navigation' 
  | 'backtrack' 
  | 'dwell';

export interface TelemetryEvent {
  id: string;
  sessionId: string;
  timestamp: number;
  eventType: EventType;
  targetSelector: string;
  targetRole?: ElementRole;
  cursorPos?: { x: number; y: number };
  scrollOffset?: { top: number; left: number };
  dwellTimeMs?: number;
}

export interface UserTwinProfile {
  userId: string;
  searchPreferenceScore: number;
  keyboardUsageRatio: number;
  menuDepthPreference: number;
  backtrackingRate: number;
  avgDecisionTimeMs: number;
  sampleCount: number;
}

export type FrictionLevel = 'NORMAL' | 'POSSIBLE_FRICTION' | 'HIGH_FRICTION';

export interface FrictionAssessment {
  level: FrictionLevel;
  score: number;
  reasons: string[];
  timestamp: number;
}

export type InterventionType = 
  | 'HIGHLIGHT_ELEMENT' 
  | 'INCREASE_PROMINENCE' 
  | 'CONTEXTUAL_HINT' 
  | 'EXPOSE_HIDDEN_CONTROL' 
  | 'ADAPTIVE_SHORTCUT';

export interface InterventionCandidate {
  id: string;
  type: InterventionType;
  targetSelector: string;
  description: string;
  payload: Record<string, any>;
  predictedGain: number;
  disruptionScore: number;
  costScore: number;
  riskScore: number;
  utilityScore?: number;
}
