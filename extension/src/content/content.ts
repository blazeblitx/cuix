// CUIX Content Script — Interface Observer, Telemetry Recorder & Graph Extractor
import { buildInterfaceGraph } from './interface_graph';
import { TelemetryEvent } from '../shared/types';

console.log('[CUIX ContentScript] Injecting DOM, Telemetry & Interface Graph engine into:', window.location.hostname);

const eventBuffer: TelemetryEvent[] = [];
const SESSION_ID = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;

// Phase 2: Interface Graph Extraction
function extractAndPublishGraph() {
  try {
    const graph = buildInterfaceGraph();
    console.log('[CUIX Interface Graph] Extracted node summary:', graph.summary);
    chrome.runtime.sendMessage({
      type: 'CUIX_INTERFACE_GRAPH',
      graph
    });
  } catch (err) {
    console.error('[CUIX Interface Graph] Extraction error:', err);
  }
}

// Initial extraction after DOM settles
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(extractAndPublishGraph, 1000);
} else {
  window.addEventListener('DOMContentLoaded', () => setTimeout(extractAndPublishGraph, 1000));
}

// Phase 3: Telemetry Event Recorder
function recordTelemetry(eventType: TelemetryEvent['eventType'], target: HTMLElement, extra?: Record<string, any>) {
  if (!target) return;

  // Privacy Protection Boundary: Exclude sensitive inputs
  if (target.matches && target.matches('input[type="password"], input[autocomplete*="cc-"], input[name*="cvv"]')) {
    return;
  }

  const selector = target.tagName.toLowerCase() + (target.id ? `#${target.id}` : '');
  
  eventBuffer.push({
    id: `evt_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
    sessionId: SESSION_ID,
    timestamp: Date.now(),
    eventType,
    targetSelector: selector,
    cursorPos: extra?.cursorPos,
    scrollOffset: extra?.scrollOffset,
    dwellTimeMs: extra?.dwellTimeMs
  });

  if (eventBuffer.length >= 5) {
    chrome.runtime.sendMessage({
      type: 'CUIX_TELEMETRY_BATCH',
      events: [...eventBuffer]
    });
    eventBuffer.length = 0;
  }
}

document.addEventListener('click', (e) => {
  recordTelemetry('click', e.target as HTMLElement, {
    cursorPos: { x: e.clientX, y: e.clientY }
  });
}, true);

document.addEventListener('scroll', () => {
  recordTelemetry('scroll', document.body, {
    scrollOffset: { top: window.scrollY, left: window.scrollX }
  });
}, { passive: true });
