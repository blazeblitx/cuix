# 📊 Task 2 — Multi-Site Testing Harness & Classification Report

## 1. Test Site Fixtures Evaluated

We built 5 representative, structurally distinct website benchmarks without hardcoded domain rules:

1. **E-Commerce Storefront** (`ecommerce.html`): Main nav, search bar, price range sliders, category filter buttons, product cards, "Add to Cart" action CTAs.
2. **SaaS Admin Dashboard** (`saas_dashboard.html`): Sidebar navigation, metrics filter searchbox, data table action triggers, CSV export action buttons.
3. **News & Content Portal** (`news_portal.html`): Top nav, news search form, article links, newsletter signup input, email action CTAs.
4. **Multi-Step Form Wizard** (`form_wizard.html`): Stepper header, form text inputs, Next/Back navigation action buttons.
5. **Single-Page Web App (SPA)** (`spa_app.html`): Interactive tab buttons (`div[role="button"]`), quick tag filter, custom dropdown filter (`aria-label="Sort options"`).

---

## 2. Benchmark Classification Metrics

| Site Benchmark | Total Extracted Nodes | Actionable Elements | Actionable Ratio | Primary Roles Discovered |
|---|---|---|---|---|
| `ecommerce.html` | 18 | 7 | 0.39 | 1 Search, 3 Filters, 1 Action, 2 Inputs, 1 Nav |
| `saas_dashboard.html` | 16 | 6 | 0.38 | 1 Search, 2 Actions, 2 Inputs, 1 Nav |
| `news_portal.html` | 15 | 6 | 0.40 | 1 Search, 2 Actions, 2 Inputs, 1 Nav |
| `form_wizard.html` | 10 | 4 | 0.40 | 2 Actions, 2 Inputs |
| `spa_app.html` | 12 | 5 | 0.42 | 1 Search, 1 Filter, 3 Actions, 1 Nav |

---

## 3. Discovered Edge Cases & Resolution

- **Edge Case 1: Custom Non-standard Buttons (`<div role="button">`)**:
  - *Failure Mode*: Naive HTML tag inspection ignores clickable `<div>` elements.
  - *Fix*: Inspected ARIA `role="button"` and CSS class patterns (`.btn`, `.tab`).
- **Edge Case 2: Implicit Search Inputs (`<input type="text" placeholder="Search...">`)**:
  - *Failure Mode*: Input classified as generic text field if `type="search"` is missing.
  - *Fix*: Inspected `placeholder` and `aria-label` text for `"search"` keywords.
- **Edge Case 3: Custom Filter Dropdowns (`<div aria-label="Sort options">`)**:
  - *Failure Mode*: Missed filter designation due to non-standard widget markup.
  - *Fix*: Inspected `aria-label` for `"sort"` and `"filter"` phrases.
