// CUIX Phase 2: Site-Agnostic Interface Graph Builder
import { InterfaceGraph, InterfaceNode, ElementRole, BoundingBox } from '../shared/types';

/**
 * Classifies an element's UI semantic role based on HTML5 tags, ARIA attributes,
 * and visual/functional characteristics without domain-specific hardcoding.
 */
export function classifyElementRole(el: HTMLElement): ElementRole {
  const tag = el.tagName.toLowerCase();
  const roleAttr = el.getAttribute('role')?.toLowerCase() || '';
  const ariaLabel = el.getAttribute('aria-label')?.toLowerCase() || '';
  const idAndClass = `${el.id} ${el.className}`.toLowerCase();

  // Search Controls
  if (
    tag === 'input' && (el.getAttribute('type') === 'search' || idAndClass.includes('search')) ||
    roleAttr === 'search' ||
    idAndClass.includes('search-bar') || idAndClass.includes('searchbox')
  ) {
    return 'search';
  }

  // Inputs
  if (tag === 'input' || tag === 'textarea' || tag === 'select') {
    return 'input';
  }

  // Navigation
  if (tag === 'nav' || roleAttr === 'navigation' || idAndClass.includes('nav') || idAndClass.includes('menu-item')) {
    return 'navigation';
  }

  // Filters
  if (
    idAndClass.includes('filter') || 
    idAndClass.includes('sort') || 
    ariaLabel.includes('filter') ||
    ariaLabel.includes('sort')
  ) {
    return 'filter';
  }

  // Actions / Buttons
  if (tag === 'button' || roleAttr === 'button' || tag === 'a' || idAndClass.includes('btn') || idAndClass.includes('cta')) {
    return 'action';
  }

  // Headings
  if (/^h[1-6]$/.test(tag) || roleAttr === 'heading') {
    return 'heading';
  }

  // Form Container
  if (tag === 'form' || roleAttr === 'form') {
    return 'form';
  }

  return 'content';
}

/**
 * Generates a unique CSS selector for an element
 */
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

  const parent = el.parentElement;
  if (parent) {
    const siblings = Array.from(parent.children).filter(c => c.tagName === el.tagName);
    if (siblings.length > 1) {
      const index = siblings.indexOf(el) + 1;
      path += `:nth-of-type(${index})`;
    }
  }

  return path;
}

/**
 * Traverses DOM recursively to construct an InterfaceGraph tree
 */
export function buildInterfaceGraph(): InterfaceGraph {
  let nodeIdCounter = 0;
  let totalNodes = 0;
  let navigationCount = 0;
  let searchCount = 0;
  let filterCount = 0;
  let actionCount = 0;
  let inputCount = 0;

  function parseNode(el: HTMLElement): InterfaceNode | null {
    // Exclude hidden elements or script/style tags
    const tag = el.tagName?.toLowerCase();
    if (!tag || ['script', 'style', 'noscript', 'svg', 'path'].includes(tag)) {
      return null;
    }

    const rect = el.getBoundingClientRect();
    const isVisible = rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none';

    if (!isVisible && el !== document.body) {
      return null;
    }

    const role = classifyElementRole(el);
    totalNodes++;

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

    // Recursively parse children (limit depth to preserve performance)
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
    tag: 'body',
    selector: 'body',
    text: '',
    isVisible: true,
    boundingBox: { x: 0, y: 0, width: window.innerWidth, height: window.innerHeight },
    children: []
  };

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
      inputCount
    }
  };
}
