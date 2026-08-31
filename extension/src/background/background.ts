// CUIX Service Worker — Connected Local Background Intelligence Worker
const CUIX_BACKEND_URL = 'http://localhost:8000/api';

console.log('[CUIX ServiceWorker] Engine initialized. Connected backend target:', CUIX_BACKEND_URL);

chrome.runtime.onInstalled.addListener(() => {
  console.log('[CUIX] Service Worker registered successfully.');
});

async function sendToBackend(endpoint: string, payload: any): Promise<any> {
  try {
    const res = await fetch(`${CUIX_BACKEND_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await res.json();
  } catch (err) {
    console.warn(`[CUIX ServiceWorker] Backend connection error (${endpoint}):`, err);
    return null;
  }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'CUIX_INTERFACE_GRAPH') {
    sendToBackend('/interface-graph', message.graph).then(response => {
      console.log('[CUIX Backend] Interface Graph ingested:', response);
      sendResponse(response);
    });
    return true;
  }

  if (message.type === 'CUIX_TELEMETRY_BATCH') {
    sendToBackend('/telemetry', { events: message.events }).then(() => {
      // Trigger evaluation after telemetry batch
      return sendToBackend('/evaluate', {});
    }).then(evaluation => {
      if (evaluation?.selected_intervention && sender.tab?.id) {
        console.log('[CUIX Optimizer] Selected intervention payload:', evaluation.selected_intervention);
        // Relay adaptation command to active tab content script
        chrome.tabs.sendMessage(sender.tab.id, {
          type: 'CUIX_APPLY_ADAPTATION',
          intervention: evaluation.selected_intervention,
          checkpoint: evaluation.checkpoint
        });
      }
      sendResponse(evaluation);
    });
    return true;
  }

  if (message.type === 'CUIX_TRIGGER_ROLLBACK') {
    sendToBackend('/rollback', { checkpoint_id: message.checkpointId }).then(res => {
      if (sender.tab?.id) {
        chrome.tabs.sendMessage(sender.tab.id, {
          type: 'CUIX_EXECUTE_ROLLBACK',
          checkpointId: message.checkpointId
        });
      }
      sendResponse(res);
    });
    return true;
  }

  if (message.type === 'CUIX_GET_HEALTH') {
    fetch(`${CUIX_BACKEND_URL}/health`).then(res => res.json()).then(data => sendResponse(data)).catch(() => sendResponse(null));
    return true;
  }
});
