# Web Accessibility Guide (WCAG AAA Compliance)

## Overview

Comprehensive guide to web accessibility compliance following WCAG 2.1/2.2 Level AAA standards. This guide covers the most critical accessibility requirements for modern web design.

**Target Standard**: WCAG 2.1 Level AAA (where practical) with Level AA as minimum baseline.

---

## Table of Contents

1. [Color & Contrast](#color--contrast)
2. [Typography & Readability](#typography--readability)
3. [Keyboard Navigation](#keyboard-navigation)
4. [Screen Reader Support](#screen-reader-support)
5. [Motion & Animation](#motion--animation)
6. [Touch Targets & Mobile](#touch-targets--mobile)
7. [Forms & Input](#forms--input)
8. [Focus Management](#focus-management)
9. [Semantic HTML](#semantic-html)
10. [Testing & Auditing](#testing--auditing)

---

## Color & Contrast

### WCAG Contrast Requirements

**Level AA (Minimum)**:
- Normal text (< 18pt): 4.5:1 contrast ratio
- Large text (≥ 18pt or 14pt bold): 3:1 contrast ratio

**Level AAA (Enhanced)**:
- Normal text: **7:1 contrast ratio**
- Large text: **4.5:1 contrast ratio**

### Checking Contrast

**Manual Calculation**:
```javascript
function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function getContrastRatio(rgb1, rgb2) {
  const l1 = getLuminance(...rgb1);
  const l2 = getLuminance(...rgb2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Example usage
const textColor = [0, 0, 0]; // Black
const bgColor = [255, 255, 255]; // White
const ratio = getContrastRatio(textColor, bgColor);
console.log(ratio); // 21:1 (AAA compliant)
```

**Tools**:
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Stark (Figma plugin)
- Chrome DevTools Accessibility Panel

### Color System (AAA Compliant)

**Using OKLCH Color Space**:
```css
:root {
  /* Text on white background (AAA compliant) */
  --color-text-primary: oklch(20% 0 0); /* #1a1a1a, 11.6:1 */
  --color-text-secondary: oklch(40% 0 0); /* #666666, 7.3:1 */

  /* Backgrounds */
  --color-bg-primary: oklch(98% 0 0); /* Near white */
  --color-bg-secondary: oklch(95% 0 0); /* Light gray */

  /* Accent colors (AAA on white) */
  --color-accent-blue: oklch(45% 0.2 250); /* 7.1:1 */
  --color-accent-green: oklch(50% 0.15 140); /* 7.2:1 */

  /* Interactive states */
  --color-link: oklch(40% 0.2 250); /* Blue, 8.3:1 */
  --color-link-hover: oklch(35% 0.25 250); /* Darker blue, 10.5:1 */
}
```

### Color Blindness Considerations

**Avoid**:
- Red-green as only distinguisher (affects 8% of males)
- Relying on color alone for meaning

**Best Practices**:
- Use patterns, shapes, or icons alongside color
- Test with color blindness simulators
- Provide high-contrast mode

**Simulation Tools**:
- Chrome DevTools: Rendering > Emulate vision deficiencies
- Colorblindly (browser extension)
- Stark (Figma)

---

## Typography & Readability

### Font Size Requirements

**WCAG Guidelines**:
- Body text: Minimum 16px (1rem)
- Small text: Minimum 14px (0.875rem)
- Users must be able to zoom to 200% without loss of functionality

**Recommended Sizes**:
```css
:root {
  /* Fluid typography */
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
  --font-size-lg: clamp(1.25rem, 1.1rem + 0.75vw, 1.75rem);
  --font-size-xl: clamp(1.75rem, 1.5rem + 1.25vw, 2.5rem);
}

body {
  font-size: var(--font-size-base);
  line-height: 1.5; /* WCAG minimum for body text */
}
```

### Line Height & Spacing

**WCAG 1.4.12 (Level AAA)**:
- Line height: Minimum 1.5× font size
- Paragraph spacing: Minimum 2× font size
- Letter spacing: Minimum 0.12× font size
- Word spacing: Minimum 0.16× font size

**Implementation**:
```css
p {
  font-size: 1rem;
  line-height: 1.6; /* 1.5× minimum */
  margin-bottom: 2rem; /* 2× font size */
  letter-spacing: 0.01em; /* Slight increase */
  word-spacing: 0.05em;
}
```

### Font Choices

**Accessible Fonts**:
- Sans-serif: Inter, Roboto, Open Sans, Atkinson Hyperlegible
- Serif: Georgia, Merriweather, Lora
- Avoid: Overly decorative, thin weights (< 300), all-caps for long text

**Dyslexia-Friendly**:
- OpenDyslexic
- Atkinson Hyperlegible
- Comic Sans (surprisingly good for dyslexia)

---

## Keyboard Navigation

### Requirements

**All interactive elements must be**:
- Focusable with Tab key
- Activatable with Enter or Space
- Dismissible with Escape (modals, dropdowns)
- Navigable with arrow keys (where appropriate)

### Tab Order

**Logical Tab Order**:
```html
<!-- Natural DOM order is best -->
<button tabindex="0">First</button>
<button tabindex="0">Second</button>
<button tabindex="0">Third</button>

<!-- Avoid tabindex > 0 (creates unpredictable order) -->
<button tabindex="3">Third</button> <!-- BAD -->
<button tabindex="1">First</button> <!-- BAD -->
```

**Skip Links**:
```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<nav>...</nav>

<main id="main-content">
  <!-- Main content -->
</main>
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Focus Indicators

**WCAG 2.4.7 (Level AA)**:
- Focus indicator must be visible
- Minimum 2px thick
- Sufficient contrast (3:1 against background)

**Modern Focus Styles**:
```css
/* Remove default outline */
*:focus {
  outline: none;
}

/* Custom focus indicator */
:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Remove focus ring for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}

/* Button focus */
button:focus-visible {
  outline: 3px solid #3b82f6;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}
```

### Keyboard Patterns

**Modal Dialogs**:
```javascript
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }

    if (e.key === 'Escape') {
      closeModal();
    }
  });

  firstFocusable.focus();
}
```

**Dropdown Menus**:
```javascript
function handleDropdownKeys(e) {
  const items = Array.from(dropdown.querySelectorAll('[role="menuitem"]'));
  const currentIndex = items.indexOf(document.activeElement);

  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % items.length;
      items[nextIndex].focus();
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevIndex = (currentIndex - 1 + items.length) % items.length;
      items[prevIndex].focus();
      break;

    case 'Home':
      e.preventDefault();
      items[0].focus();
      break;

    case 'End':
      e.preventDefault();
      items[items.length - 1].focus();
      break;

    case 'Escape':
      closeDropdown();
      triggerButton.focus();
      break;
  }
}
```

---

## Screen Reader Support

### ARIA Attributes

**Essential ARIA**:

**Landmarks**:
```html
<header role="banner">
  <nav role="navigation" aria-label="Main">
    <!-- Navigation -->
  </nav>
</header>

<main role="main">
  <!-- Main content -->
</main>

<aside role="complementary" aria-label="Related articles">
  <!-- Sidebar -->
</aside>

<footer role="contentinfo">
  <!-- Footer -->
</footer>
```

**Buttons**:
```html
<!-- Icon button needs label -->
<button aria-label="Close menu">
  <svg>...</svg>
</button>

<!-- Button with visible text -->
<button>
  <svg aria-hidden="true">...</svg>
  Submit
</button>
```

**Live Regions**:
```html
<!-- Announce loading state -->
<div role="status" aria-live="polite" aria-atomic="true">
  Loading content...
</div>

<!-- Announce errors -->
<div role="alert" aria-live="assertive">
  Error: Form submission failed.
</div>
```

**Custom Components**:
```html
<!-- Accordion -->
<div class="accordion">
  <h3>
    <button
      aria-expanded="false"
      aria-controls="panel-1"
      id="button-1"
    >
      Section 1
    </button>
  </h3>
  <div
    id="panel-1"
    role="region"
    aria-labelledby="button-1"
    hidden
  >
    Content...
  </div>
</div>

<!-- Tab panel -->
<div role="tablist" aria-label="Content sections">
  <button role="tab" aria-selected="true" aria-controls="panel-1">
    Tab 1
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">
    Tab 2
  </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Panel content...
</div>
```

### Alt Text Guidelines

**Images**:
```html
<!-- Informative image -->
<img src="chart.png" alt="Bar chart showing 50% increase in sales">

<!-- Decorative image -->
<img src="decorative.png" alt="" role="presentation">

<!-- Complex image -->
<img src="infographic.png" alt="Sales data for Q4" longdesc="sales-data.html">
```

**Best Practices**:
- Describe the content/function, not "image of..."
- Keep under 150 characters (screen readers pause)
- Use empty alt (`alt=""`) for decorative images
- Provide long descriptions for complex images

---

## Motion & Animation

### Reduced Motion Preference

**WCAG 2.3.3 (Level AAA)**:
Users must be able to disable non-essential motion.

**Implementation**:
```css
/* Default: animations enabled */
.animated-element {
  animation: slide-in 0.5s ease;
}

/* Respect user preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Keep essential animations but reduce */
  .loading-spinner {
    animation-duration: 1s; /* Slower */
  }
}
```

**JavaScript Detection**:
```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (prefersReducedMotion) {
  // Disable or simplify animations
  gsap.config({ nullTargetWarn: false, force3D: false });

  // Skip scroll animations
  ScrollTrigger.getAll().forEach(st => st.kill());
}
```

### Animation Guidelines

**Safe Animations**:
- Fade in/out (opacity)
- Slide short distances (< 50px)
- Scale small amounts (0.95-1.05)
- Avoid: flashing, rapid movement, parallax

**Vestibular Disorders**:
Avoid animations that can cause dizziness or nausea:
- Large parallax effects
- Continuous rotation
- Zoom effects
- Perspective transforms

---

## Touch Targets & Mobile

### WCAG 2.5.5 (Level AAA)

**Target Size**: Minimum 44×44px (iOS) or 48×48px (Android)

**Spacing**: Minimum 8px between targets

**Implementation**:
```css
button, a {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
  /* Touch target includes padding */
}

/* Increase tap target without changing visual size */
button::before {
  content: '';
  position: absolute;
  inset: -8px; /* Extends tap target by 8px all sides */
}
```

### Mobile Considerations

**Viewport**:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
```
*Note*: Allow zoom up to 5× (WCAG requirement)

**Touch Gestures**:
- Avoid complex gestures (multi-finger, long-press)
- Provide alternative interactions
- Don't rely on hover states

---

## Forms & Input

### Labels & Instructions

**WCAG 3.3.2 (Level A)**:
Every input must have a visible label.

**Implementation**:
```html
<!-- Explicit label -->
<label for="email">Email address</label>
<input id="email" type="email" required aria-describedby="email-help">
<small id="email-help">We'll never share your email.</small>

<!-- Error state -->
<input
  id="email"
  type="email"
  aria-invalid="true"
  aria-describedby="email-error"
>
<div id="email-error" role="alert">
  Please enter a valid email address.
</div>
```

### Form Validation

**Accessible Validation**:
```javascript
function validateEmail(input) {
  const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);

  if (isValid) {
    input.setAttribute('aria-invalid', 'false');
    input.removeAttribute('aria-describedby');
    removeError(input);
  } else {
    input.setAttribute('aria-invalid', 'true');
    input.setAttribute('aria-describedby', `${input.id}-error`);
    showError(input, 'Please enter a valid email address.');
  }
}

function showError(input, message) {
  const errorElement = document.getElementById(`${input.id}-error`) ||
                       createErrorElement(input.id);
  errorElement.textContent = message;
  errorElement.setAttribute('role', 'alert'); // Announces to screen readers
}
```

### Required Fields

**Indication**:
```html
<label for="name">
  Full name
  <abbr title="required" aria-label="required">*</abbr>
</label>
<input id="name" type="text" required aria-required="true">
```

**Visual + Programmatic**:
- Visual indicator (asterisk, "required")
- `required` attribute
- `aria-required="true"`

---

## Focus Management

### Managing Focus States

**After Modal Opens**:
```javascript
function openModal() {
  modal.style.display = 'block';
  modal.setAttribute('aria-hidden', 'false');

  // Focus first focusable element
  const firstFocusable = modal.querySelector('button, [href], input');
  firstFocusable.focus();

  // Trap focus
  trapFocus(modal);
}
```

**After Modal Closes**:
```javascript
function closeModal() {
  modal.style.display = 'none';
  modal.setAttribute('aria-hidden', 'true');

  // Return focus to trigger button
  triggerButton.focus();
}
```

### Focus Order

**Best Practices**:
- Follow visual order (top to bottom, left to right)
- Group related elements
- Use `tabindex="-1"` for programmatic focus only
- Avoid `tabindex > 0` (creates unpredictable order)

---

## Semantic HTML

### Heading Hierarchy

**WCAG 1.3.1 (Level A)**:
Use proper heading levels (h1-h6) without skipping.

**Correct**:
```html
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h3>Another Subsection</h3>
<h2>Another Section</h2>
```

**Incorrect**:
```html
<h1>Page Title</h1>
<h3>Section</h3> <!-- Skipped h2 -->
```

### Landmark Regions

**Essential Landmarks**:
```html
<header>
  <nav aria-label="Main navigation">
    <!-- Primary nav -->
  </nav>
</header>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
    </header>
    <!-- Article content -->
  </article>

  <aside aria-label="Related links">
    <!-- Sidebar -->
  </aside>
</main>

<footer>
  <nav aria-label="Footer navigation">
    <!-- Footer nav -->
  </nav>
</footer>
```

### Lists & Tables

**Lists**:
```html
<!-- Use proper list elements -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>

<!-- Not divs styled as lists -->
```

**Tables**:
```html
<table>
  <caption>Sales Data Q4 2024</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>October</td>
      <td>$50,000</td>
    </tr>
  </tbody>
</table>
```

---

## Testing & Auditing

### Automated Testing Tools

**Browser Extensions**:
- axe DevTools (Chrome/Firefox)
- WAVE (Web Accessibility Evaluation Tool)
- Lighthouse (Chrome DevTools)

**Command Line**:
```bash
# pa11y
npm install -g pa11y
pa11y https://example.com

# axe-core CLI
npm install -g @axe-core/cli
axe https://example.com
```

### Manual Testing Checklist

**Keyboard Navigation**:
- [ ] Tab through all interactive elements
- [ ] Activate with Enter/Space
- [ ] Close modals with Escape
- [ ] Navigate dropdowns with arrow keys

**Screen Reader Testing**:
- [ ] Test with NVDA (Windows), VoiceOver (Mac), JAWS
- [ ] Check heading structure
- [ ] Verify alt text
- [ ] Test form labels and errors

**Visual Testing**:
- [ ] Zoom to 200%
- [ ] Test color contrast
- [ ] Check focus indicators
- [ ] Review with color blindness simulator

**Motion Testing**:
- [ ] Enable `prefers-reduced-motion`
- [ ] Verify animations are disabled/reduced
- [ ] Check for essential animations that remain

### Screen Reader Testing Commands

**NVDA (Windows)**:
- Toggle: Caps Lock or Insert
- Next heading: H
- Next landmark: D
- Read all: Caps Lock + Down Arrow

**VoiceOver (Mac)**:
- Toggle: Cmd + F5
- Rotor: Ctrl + Option + U
- Next heading: Ctrl + Option + Cmd + H

**JAWS (Windows)**:
- List headings: Insert + F6
- List links: Insert + F7
- Next heading: H

---

## Common Accessibility Patterns

### Accessible Modal

```jsx
function AccessibleModal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);
  const triggerRef = useRef(document.activeElement);

  useEffect(() => {
    if (isOpen) {
      // Trap focus
      trapFocus(modalRef.current);

      // Focus first element
      const firstFocusable = modalRef.current.querySelector('button, [href], input');
      firstFocusable?.focus();

      // Prevent body scroll
      document.body.style.overflow = 'hidden';
    } else {
      // Return focus
      triggerRef.current?.focus();
      document.body.style.overflow = '';
    }

    // Listen for Escape key
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);

    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="modal-backdrop"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        className="modal"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 id="modal-title">Modal Title</h2>
        {children}
        <button onClick={onClose} aria-label="Close modal">
          ×
        </button>
      </div>
    </div>
  );
}
```

### Accessible Accordion

```html
<div class="accordion">
  <h3>
    <button
      aria-expanded="false"
      aria-controls="panel-1"
      id="accordion-button-1"
    >
      <span class="accordion-title">Section 1</span>
      <svg class="accordion-icon" aria-hidden="true">...</svg>
    </button>
  </h3>
  <div
    id="panel-1"
    role="region"
    aria-labelledby="accordion-button-1"
    hidden
  >
    <p>Content for section 1...</p>
  </div>
</div>
```

```javascript
function initAccordion() {
  const buttons = document.querySelectorAll('.accordion button');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      const panel = document.getElementById(button.getAttribute('aria-controls'));

      button.setAttribute('aria-expanded', !expanded);
      panel.hidden = expanded;
    });
  });
}
```

---

## WCAG Quick Reference

**Level A (Must Have)**:
- Text alternatives (alt text)
- Keyboard accessible
- Color not only means of conveying info
- Labeled form inputs
- Proper heading hierarchy

**Level AA (Should Have)**:
- 4.5:1 contrast for normal text
- 3:1 contrast for large text
- Resize text to 200%
- Focus visible
- Multiple ways to find pages

**Level AAA (Nice to Have)**:
- 7:1 contrast for normal text
- 4.5:1 contrast for large text
- Target size 44×44px minimum
- No timing restrictions
- Help available

---

*Last updated: 2024*
*Based on WCAG 2.1 and WCAG 2.2 standards*
