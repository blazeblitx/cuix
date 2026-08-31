// CUIX Service Worker — Local Background Intelligence Hub

console.log('[CUIX ServiceWorker] Engine initialized.');

chrome.runtime.onInstalled.addListener(() => {
  console.log('[CUIX] Service Worker registered successfully.');
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'CUIX_TELEMETRY_BATCH') {
    console.log(`[CUIX Telemetry] Received ${message.events.length} telemetry events from tab ${sender.tab?.id}`);
    sendResponse({ status: 'ACK' });
  } else if (message.type === 'CUIX_GET_TWIN') {
    // Phase 4 default vector mock until local storage load
    sendResponse({
      twin: {
        searchPreferenceScore: 0.82,
        keyboardUsageRatio: 0.64,
        backtrackingRate: 0.18,
        avgDecisionTimeMs: 2400
      }
    });
  }
});
