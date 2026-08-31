// CUIX Content Script — Interface Observer & DOM Adaptation Injector

console.log('[CUIX ContentScript] Injecting DOM & Telemetry observer into:', window.location.hostname);

interface TelemetryPayload {
  timestamp: number;
  type: string;
  target: string;
}

const buffer: TelemetryPayload[] = [];

// Record click interaction safely
document.addEventListener('click', (event) => {
  const target = event.target as HTMLElement;
  if (!target) return;

  // Sensitive selector safety guard check
  if (target.matches('input[type="password"], input[autocomplete*="cc-"]')) {
    return;
  }

  buffer.push({
    timestamp: Date.now(),
    type: 'click',
    target: target.tagName.toLowerCase() + (target.id ? `#${target.id}` : '')
  });

  if (buffer.length >= 5) {
    chrome.runtime.sendMessage({
      type: 'CUIX_TELEMETRY_BATCH',
      events: [...buffer]
    });
    buffer.length = 0;
  }
}, true);
