# Modern Web Design Assets

## Overview

This directory contains design system templates, starter files, and reusable assets for modern web development. All assets follow accessibility, performance, and modern design best practices.

## Available Assets

### 1. Design Tokens

**Location**: Would be in `tokens/` subdirectory

**What's included**:
- CSS custom properties (variables) for:
  - Colors (OKLCH color space, AAA compliant)
  - Typography scales (fluid sizing with clamp())
  - Spacing scales (consistent rhythm)
  - Shadows (elevation system)
  - Border radius (consistent rounding)
  - Animation timing (duration & easing)

**Usage**:
```css
/* Import design tokens */
@import url('tokens/colors.css');
@import url('tokens/typography.css');
@import url('tokens/spacing.css');

/* Use in your styles */
.button {
  background: var(--color-primary);
  padding: var(--space-md) var(--space-lg);
  font-size: var(--font-size-base);
  transition: transform var(--duration-fast) var(--ease-out);
}
```

### 2. Component Library

**Location**: Would be in `components/` subdirectory

**What's included**:
- Button variants (primary, secondary, ghost, danger)
- Form components (inputs, textareas, select, checkbox, radio)
- Card layouts
- Navigation components
- Modal/Dialog components
- Toast notifications
- Loading states (spinners, skeletons, progress bars)

**Features**:
- Fully accessible (WCAG AAA where possible)
- Keyboard navigable
- Screen reader friendly
- Dark mode variants
- Responsive by default

### 3. Layout Templates

**Location**: Would be in `layouts/` subdirectory

**What's included**:
- Landing page template
- Portfolio/Agency template
- Blog/Article template
- Dashboard/App template
- E-commerce template

**Features**:
- Modern CSS Grid & Flexbox
- Responsive breakpoints
- Print stylesheets
- Semantic HTML5

### 4. Animation Presets

**Location**: Would be in `animations/` subdirectory

**What's included**:
- CSS keyframe animations
- Transition presets
- Easing functions
- GSAP animation snippets
- Framer Motion variants

**Categories**:
- Fade (in/out, up/down/left/right)
- Slide (all directions)
- Scale (grow/shrink)
- Rotate
- Bounce
- Elastic
- Custom easings

### 5. Icon System

**Location**: Would be in `icons/` subdirectory

**What's included**:
- SVG icon set (inline-ready)
- Icon sprite sheet
- Icon font (optional)

**Features**:
- Accessibility ready (proper aria-hidden/labels)
- Consistent sizing
- Color customizable via CSS

### 6. Utility Classes

**Location**: Would be in `utilities/` subdirectory

**What's included**:
- Display utilities (flex, grid, block, inline, none)
- Spacing utilities (margin, padding)
- Typography utilities (size, weight, align)
- Color utilities (text, background)
- Layout utilities (container, aspect-ratio)
- Accessibility utilities (sr-only, focus-visible)

**Example**:
```html
<div class="flex items-center gap-md p-lg bg-primary text-white rounded-lg">
  Content
</div>
```

### 7. Reset & Base Styles

**Location**: Would be in `base/` subdirectory

**What's included**:
- Modern CSS reset (based on modern-normalize)
- Base typography styles
- Accessible focus styles
- Print styles

---

## How to Use These Assets

### Option 1: Copy Individual Files

Copy only the files you need into your project:

```bash
# Copy design tokens
cp assets/tokens/colors.css src/styles/
cp assets/tokens/typography.css src/styles/

# Copy specific components
cp assets/components/button.css src/components/
```

### Option 2: Import Everything

Import the complete design system:

```html
<link rel="stylesheet" href="assets/design-system.css">
```

Or in your CSS:

```css
@import url('../assets/design-system.css');
```

### Option 3: Use as Reference

Browse the assets to understand patterns and adapt them to your own design system.

---

## Customization Guide

### Colors

Modify color tokens to match your brand:

```css
:root {
  /* Update these values */
  --color-primary: oklch(50% 0.2 250); /* Your brand blue */
  --color-accent: oklch(65% 0.25 30);  /* Your accent color */

  /* System will generate variants automatically */
  --color-primary-hover: oklch(45% 0.2 250);
  --color-primary-active: oklch(40% 0.2 250);
}
```

### Typography

Adjust type scale for your design:

```css
:root {
  /* Base size (1rem = 16px by default) */
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);

  /* Adjust ratio for scale */
  --font-scale-ratio: 1.25; /* Minor third */

  /* Or use pre-calculated values */
  --font-size-sm: clamp(0.875rem, ...);
  --font-size-lg: clamp(1.25rem, ...);
}
```

### Spacing

Customize spacing scale:

```css
:root {
  /* 8px base unit */
  --space-unit: 0.5rem;

  /* Scale multiples */
  --space-xs: calc(var(--space-unit) * 1);  /* 8px */
  --space-sm: calc(var(--space-unit) * 2);  /* 16px */
  --space-md: calc(var(--space-unit) * 4);  /* 32px */
  --space-lg: calc(var(--space-unit) * 6);  /* 48px */
  --space-xl: calc(var(--space-unit) * 8);  /* 64px */
}
```

---

## Design System Principles

### 1. Mobile-First

All components are designed mobile-first with progressive enhancement for larger screens.

```css
/* Mobile first */
.component {
  font-size: 1rem;
}

/* Enhance for larger screens */
@media (min-width: 768px) {
  .component {
    font-size: 1.25rem;
  }
}
```

### 2. Accessibility First

- AAA color contrast ratios where possible (7:1)
- Keyboard navigable (visible focus states)
- Screen reader friendly (proper ARIA labels)
- Respects motion preferences

### 3. Performance Optimized

- CSS-only animations where possible
- GPU-accelerated transforms
- Minimal JavaScript
- Lazy-loadable components

### 4. Design Token Driven

Everything is configurable via design tokens:
- Easy rebranding
- Consistent visual language
- Dark mode support built-in

---

## File Structure

```
assets/
├── README.md (this file)
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   ├── spacing.css
│   ├── shadows.css
│   └── animation.css
├── base/
│   ├── reset.css
│   ├── typography.css
│   └── print.css
├── components/
│   ├── button.css
│   ├── card.css
│   ├── form.css
│   ├── modal.css
│   └── ...
├── layouts/
│   ├── landing.html
│   ├── dashboard.html
│   └── ...
├── animations/
│   ├── fade.css
│   ├── slide.css
│   └── gsap-presets.js
├── utilities/
│   └── utilities.css
└── design-system.css (imports all)
```

---

## Browser Support

**Modern Browsers** (recommended):
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

**Fallbacks provided for**:
- CSS Grid → Flexbox
- CSS custom properties → Fallback values
- Modern CSS functions → Static values

**Progressive Enhancement**:
```css
/* Fallback */
.container {
  padding: 2rem; /* Static value */
}

/* Enhanced */
@supports (padding: clamp(1rem, 5vw, 3rem)) {
  .container {
    padding: clamp(1rem, 5vw, 3rem);
  }
}
```

---

## Contributing

When adding new assets:

1. **Follow naming conventions**: kebab-case for files, BEM for CSS classes
2. **Include accessibility**: ARIA labels, keyboard support, focus states
3. **Document usage**: Add examples and notes in component files
4. **Test thoroughly**: Cross-browser, keyboard, screen reader
5. **Optimize**: Remove unused code, minimize file size

---

## Related Skills

For implementation guidance, reference:
- `gsap-scrolltrigger` - Animation patterns
- `motion-framer` - React component animations
- `animated-component-libraries` - Pre-built components
- `threejs-webgl` - 3D backgrounds and effects

---

## License

All assets follow the Apache 2.0 license (same as the skill).

---

*Last updated: 2024*
