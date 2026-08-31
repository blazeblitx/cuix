// CUIX Content Script — Interface Observer, Telemetry Recorder & Adaptation Injector
import { buildInterfaceGraph } from './interface_graph';
import { TelemetryEvent, InterventionCandidate } from '../shared/types';

console.log('[CUIX ContentScript] Injecting DOM, Telemetry & Interface Graph engine into:', window.location.hostname);

const eventBuffer: TelemetryEvent[] = [];
const SESSION_ID = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
const activeSnapshots: Map<string, { element: HTMLElement; originalStyle: string }> = new Map();

// Inject CSS styles for CUIX adaptations dynamically
function ensureStylesInjected() {
  if (document.getElementById('cuix-injected-styles')) return;
  const styleEl = document.createElement('style');
  styleEl.id = 'cuix-injected-styles';
  styleEl.textContent = `
    .cuix-adapted-highlight {
      outline: 3px solid #38bdf8 !important;
      outline-offset: 3px !important;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.5) !important;
      transition: all 0.3s ease !important;
    }
    .cuix-tooltip-hint {
      position: absolute;
      background: #0f172a;
      color: #38bdf8;
      border: 1px solid #38bdf8;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      z-index: 99999;
      pointer-events: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
  `;
  document.head.appendChild(styleEl);
}

// Apply real DOM adaptation
function applyDomAdaptation(intervention: InterventionCandidate, checkpointId?: string) {
  ensureStylesInjected();
  const selector = intervention.targetSelector || 'button';
  const target = document.querySelector(selector) as HTMLElement;

  if (!target) {
    console.warn('[CUIX Adaptation] Target element not found for selector:', selector);
    return;
  }

  // Save original inline style snapshot for atomic rollback
  const chkKey = checkpointId || `chk_${Date.now()}`;
  if (!activeSnapshots.has(chkKey)) {
    activeSnapshots.set(chkKey, {
      element: target,
      originalStyle: target.getAttribute('style') || ''
    });
  }

  if (intervention.type === 'HIGHLIGHT_ELEMENT' || intervention.type === 'INCREASE_PROMINENCE') {
    target.classList.add('cuix-adapted-highlight');
  } else if (intervention.type === 'CONTEXTUAL_HINT') {
    target.classList.add('cuix-adapted-highlight');
    const rect = target.getBoundingClientRect();
    const tooltip = document.createElement('div');
    tooltip.className = 'cuix-tooltip-hint';
    tooltip.setAttribute('data-cuix-chk', chkKey);
    tooltip.textContent = `💡 CUIX Hint: Try using ${target.textContent || 'this option'}`;
    tooltip.style.top = `${window.scrollY + rect.top - 36}px`;
    tooltip.style.left = `${window.scrollX + rect.left}px`;
    document.body.appendChild(tooltip);
  }

  console.log(`[CUIX Adaptation] Successfully applied ${intervention.type} to ${selector}`);
}

// Perform instant atomic rollback
function rollbackDomAdaptation(checkpointId?: string) {
  if (checkpointId && activeSnapshots.has(checkpointId)) {
    const item = activeSnapshots.get(checkpointId)!;
    item.element.classList.remove('cuix-adapted-highlight');
    item.element.setAttribute('style', item.originalStyle);
    activeSnapshots.delete(checkpointId);
  } else {
    // Rollback all active adaptations
    activeSnapshots.forEach((item) => {
      item.element.classList.remove('cuix-adapted-highlight');
      item.element.setAttribute('style', item.originalStyle);
    });
    activeSnapshots.clear();
  }

  // Remove tooltip elements
  document.querySelectorAll('.cuix-tooltip-hint').forEach(el => el.remove());
  console.log('[CUIX Rollback] Restored DOM state to original checkpoint.');
}

// Message Listener for Adaptation Commands
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'CUIX_APPLY_ADAPTATION') {
    applyDomAdaptation(message.intervention, message.checkpoint?.checkpoint_id);
  } else if (message.type === 'CUIX_EXECUTE_ROLLBACK') {
    rollbackDomAdaptation(message.checkpointId);
  }
});

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

if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(extractAndPublishGraph, 1000);
} else {
  window.addEventListener('DOMContentLoaded', () => setTimeout(extractAndPublishGraph, 1000));
}

// Phase 3: Telemetry Event Recorder
function recordTelemetry(eventType: TelemetryEvent['eventType'], target: HTMLElement, extra?: Record<string, any>) {
  if (!target) return;

  // Sensitive selector safety guard check
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
