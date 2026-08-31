# 🛡️ CUIX Privacy & Safety Governance Framework

This framework governs data handling, client-side isolation, non-interfered UI targets, and user-override safety switches in CUIX.

---

## 1. Zero-Telemetry Leakage Policy

1. **Local Processing First**: All telemetry ingestion, telemetry feature aggregation, friction modeling, and counterfactual simulation MUST run locally inside the client browser runtime (`chrome.storage.local` / local WebAssembly / service worker).
2. **No Remote Keylogging or Text Payload Collection**: Text typed into input fields (`<input>`, `<textarea>`, `contenteditable`) is NEVER recorded verbatim. Only metadata (e.g. keypress count, backspace frequency, inter-key latency) is captured.
3. **Domain Anonymization**: Session analytics track interactions per abstract page structure rather than capturing user-private URL query parameters.

---

## 2. Strictly Excluded UI Targets & Safety Boundaries

> [!CAUTION]
> Under NO circumstances may CUIX inspect, record value contents from, or inject DOM adaptations near the following elements:

```typescript
const EXCLUDED_SELECTORS = [
  // Sensitive Data & Credentials
  'input[type="password"]',
  'input[type="hidden"][name*="token"]',
  'input[autocomplete*="cc-"]',
  'input[name*="cvv"]',
  'input[name*="card"]',
  
  // Security & Authentication
  'iframe[src*="captcha"]',
  'iframe[src*="stripe"]',
  'iframe[src*="paypal"]',
  '[data-testid*="2fa"]',
  
  // High-Risk Destructive Actions
  'button[data-action="delete"]',
  'button[aria-label*="Delete"]',
  'button[aria-label*="Remove"]',
  'form[action*="checkout"] button[type="submit"]',
  'button[id*="pay"]'
];
```

---

## 3. Safe Rollback Guarantee (Phase 12)

- Every adaptation applied by CUIX generates an atomic `AdaptationCheckpoint`.
- If the user clicks "Undo CUIX Change" or triggers a negative interaction signal (e.g., immediate page reload, repeated rapid backclicks), CUIX instantly restores the DOM to its unmodified state.
- All modified styles are scoped under isolation classes (e.g. `.cuix-adapted-element`) and can be stripped globally via a single toggle in the extension popup.
