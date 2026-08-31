// CUIX Task 3: Multi-Signal Interface Classifier with Confidence Scoring
import { InterfaceGraph, InterfaceNode, ElementRole, BoundingBox } from '../shared/types';

export interface ClassificationResult {
  role: ElementRole;
  confidence: number;
}

/**
 * Combines DOM Semantics, Accessibility attributes, Computed Styles, Geometry,
 * and Visible Text into a normalized role classification with an explicit confidence score [0.00 - 1.00].
 */
export function classifyElementRoleWithConfidence(el: HTMLElement): ClassificationResult {
  const tag = el.tagName.toLowerCase();
  const roleAttr = el.getAttribute('role')?.toLowerCase() || '';
  const ariaLabel = el.getAttribute('aria-label')?.toLowerCase() || '';
  const placeholder = el.getAttribute('placeholder')?.toLowerCase() || '';
  const textContent = (el.textContent || '').trim().toLowerCase();
  const idAndClass = `${el.id} ${el.className}`.toLowerCase();
  const style = window.getComputedStyle(el);

  // 1. Search Signal
  if (
    tag === 'input' && (el.getAttribute('type') === 'search' || placeholder.includes('search')) ||
    roleAttr === 'search' ||
    ariaLabel.includes('search') ||
    idAndClass.includes('search')
  ) {
    let conf = 0.70;
    if (tag === 'input' && el.getAttribute('type') === 'search') conf += 0.25;
    if (roleAttr === 'search') conf += 0.20;
    if (ariaLabel.includes('search')) conf += 0.10;
    return { role: 'search', confidence: Math.min(roundTwo(conf), 0.98) };
  }

  // 2. Navigation Signal
  if (tag === 'nav' || roleAttr === 'navigation' || idAndClass.includes('nav') || idAndClass.includes('menu-item')) {
    let conf = 0.65;
    if (tag === 'nav') conf += 0.30;
    if (roleAttr === 'navigation') conf += 0.25;
    return { role: 'navigation', confidence: Math.min(roundTwo(conf), 0.98) };
  }

  // 3. Filter Signal
  if (
    idAndClass.includes('filter') || 
    idAndClass.includes('sort') || 
    ariaLabel.includes('filter') || 
    ariaLabel.includes('sort') ||
    placeholder.includes('filter')
  ) {
    let conf = 0.65;
    if (ariaLabel.includes('filter') || ariaLabel.includes('sort')) conf += 0.25;
    if (tag === 'select' || tag === 'button') conf += 0.10;
    return { role: 'filter', confidence: Math.min(roundTwo(conf), 0.95) };
  }

  // 4. Action / Button Signal
  if (tag === 'button' || roleAttr === 'button' || tag === 'a' || idAndClass.includes('btn') || style.cursor === 'pointer') {
    let conf = 0.60;
    if (tag === 'button') conf += 0.30;
    if (roleAttr === 'button') conf += 0.25;
    if (style.cursor === 'pointer') conf += 0.10;
    return { role: 'action', confidence: Math.min(roundTwo(conf), 0.98) };
  }

  // 5. Input Signal
  if (tag === 'input' || tag === 'textarea' || tag === 'select') {
    let conf = 0.85;
    if (el.getAttribute('name') || el.id) conf += 0.10;
    return { role: 'input', confidence: Math.min(roundTwo(conf), 0.98) };
  }

  // 6. Heading Signal
  if (/^h[1-6]$/.test(tag) || roleAttr === 'heading') {
    let conf = 0.85;
    if (/^h[1-3]$/.test(tag)) conf += 0.10;
    return { role: 'heading', confidence: Math.min(roundTwo(conf), 0.98) };
  }

  // 7. Form Container
  if (tag === 'form' || roleAttr === 'form') {
    return { role: 'form', confidence: 0.90 };
  }

  return { role: 'content', confidence: 0.50 };
}

function roundTwo(num: number): number {
  return Math.round(num * 100) / 100;
}

export function getUniqueSelector(el: HTMLElement): string {
  if (el.id) return `#${CSS.escape(el.id)}`;
  if (el === document.body) return 'body';

  let path = el.tagName.toLowerCase();
  if (el.className && typeof el.className === 'string' && el.className.trim()) {
    const firstClass = el.className.trim().split(/\s+/)[0];
    if (firstClass && !firstClass.startsWith('cuix-')) {
      path += `.${CSS.escape(firstClass)}`;
    }
  }
  return path;
}

export function buildInterfaceGraph(): InterfaceGraph {
  let nodeIdCounter = 0;
  let totalNodes = 0, navigationCount = 0, searchCount = 0, filterCount = 0, actionCount = 0, inputCount = 0;
  let totalConfidenceSum = 0;

  function parseNode(el: HTMLElement): InterfaceNode | null {
    const tag = el.tagName?.toLowerCase();
    if (!tag || ['script', 'style', 'noscript', 'svg', 'path'].includes(tag)) {
      return null;
    }

    const rect = el.getBoundingClientRect();
    const isVisible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';

    if (!isVisible && el !== document.body) {
      return null;
    }

    const { role, confidence } = classifyElementRoleWithConfidence(el);
    totalNodes++;
    totalConfidenceSum += confidence;

    switch (role) {
      case 'navigation': navigationCount++; break;
      case 'search': searchCount++; break;
      case 'filter': filterCount++; break;
      case 'action': actionCount++; break;
      case 'input': inputCount++; break;
    }

    const node: InterfaceNode = {
      id: `node_${++nodeIdCounter}`,
      role,
      confidence,
      tag,
      selector: getUniqueSelector(el),
      text: (el.textContent || '').trim().slice(0, 50),
      ariaLabel: el.getAttribute('aria-label') || undefined,
      isVisible,
      boundingBox: {
        x: Math.round(rect.x),
        y: Math.round(rect.y),
        width: Math.round(rect.width),
        height: Math.round(rect.height)
      },
      children: []
    };

    for (let i = 0; i < el.children.length; i++) {
      const childEl = el.children[i] as HTMLElement;
      if (childEl) {
        const childNode = parseNode(childEl);
        if (childNode) {
          node.children.push(childNode);
        }
      }
    }

    return node;
  }

  const rootNode = parseNode(document.body) || {
    id: 'root',
    role: 'content',
    confidence: 0.50,
    tag: 'body',
    selector: 'body',
    text: '',
    isVisible: true,
    boundingBox: { x: 0, y: 0, width: window.innerWidth, height: window.innerHeight },
    children: []
  };

  const avgConfidence = totalNodes > 0 ? roundTwo(totalConfidenceSum / totalNodes) : 0.50;

  return {
    pageUrl: window.location.href,
    domain: window.location.hostname,
    title: document.title,
    timestamp: Date.now(),
    root: rootNode,
    summary: {
      totalNodes,
      navigationCount,
      searchCount,
      filterCount,
      actionCount,
      inputCount,
      avgConfidence
    }
  };
}
