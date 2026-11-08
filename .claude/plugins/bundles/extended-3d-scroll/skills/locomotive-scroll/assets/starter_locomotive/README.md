# Locomotive Scroll Starter Template

Complete starter template demonstrating Locomotive Scroll features including smooth scrolling, parallax effects, sticky elements, viewport detection, and scroll events.

## Features

This template includes examples of:

- ✅ **Smooth Scrolling** - Hardware-accelerated smooth scroll with customizable lerp
- ✅ **Parallax Effects** - Multi-layered parallax with different speeds
- ✅ **Sticky Elements** - Elements that stick within defined boundaries
- ✅ **Viewport Detection** - Track when elements enter/exit viewport
- ✅ **Scroll Events** - Monitor scroll position, speed, and direction
- ✅ **Call Events** - Trigger callbacks when elements become visible
- ✅ **Progress Tracking** - Track element visibility progress (0 to 1)
- ✅ **Programmatic Scrolling** - Scroll to elements via JavaScript
- ✅ **Mobile Responsive** - Optimized settings for tablet and smartphone

## Quick Start

### Installation

```bash
npm install
```

### Development Server

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

### Build for Production

```bash
npm run build
```

## File Structure

```
starter_locomotive/
├── index.html          # Main HTML with Locomotive Scroll markup
├── style.css           # Styles including responsive design
├── main.js             # Locomotive Scroll initialization and events
├── package.json        # Dependencies
└── README.md           # This file
```

## Understanding the Code

### HTML Structure

Every Locomotive Scroll project requires specific data attributes:

```html
<!-- Main scroll container (required) -->
<div data-scroll-container>

  <!-- Section wrapper (optional, improves performance) -->
  <div data-scroll-section>

    <!-- Tracked element -->
    <h1 data-scroll data-scroll-speed="2">
      Smooth Parallax
    </h1>

  </div>
</div>
```

### Key Data Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `data-scroll` | Enable detection | `data-scroll` |
| `data-scroll-speed` | Parallax speed | `data-scroll-speed="2"` |
| `data-scroll-sticky` | Sticky positioning | `data-scroll-sticky` |
| `data-scroll-call` | Event trigger | `data-scroll-call="fadeIn"` |
| `data-scroll-id` | Unique identifier | `data-scroll-id="hero"` |

### Initialization Options

The template uses these configuration options:

```javascript
const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,         // Enable smooth scrolling
  lerp: 0.1,            // Smoothness (0-1, lower = smoother)
  multiplier: 1,        // Speed multiplier
  class: 'is-inview',   // Class added to visible elements
  repeat: true,         // Repeat in-view detection
  offset: ['10%', 0],   // Global offset [bottom, top]
  getSpeed: true,       // Track scroll speed
  getDirection: true,   // Track scroll direction

  // Mobile settings
  smartphone: {
    smooth: true,
    breakpoint: 768
  }
});
```

## Examples in the Template

### 1. Parallax Effects

```html
<!-- Slow parallax (background) -->
<div data-scroll data-scroll-speed="0.5">
  Background Layer
</div>

<!-- Fast parallax (foreground) -->
<div data-scroll data-scroll-speed="3">
  Foreground Layer
</div>

<!-- Reverse parallax -->
<div data-scroll data-scroll-speed="-2">
  Reverse Layer
</div>
```

### 2. Sticky Element

```html
<div data-scroll-section>
  <div data-scroll data-scroll-sticky>
    I stick while section is in view
  </div>
</div>
```

### 3. Scroll Call Events

```html
<div data-scroll data-scroll-call="fadeIn">
  Triggers callback when visible
</div>
```

```javascript
scroll.on('call', (func, way) => {
  if (func === 'fadeIn' && way === 'enter') {
    // Element entered viewport
  }
});
```

### 4. Progress Tracking

```html
<h1 data-scroll data-scroll-id="hero-title">
  Hero Title
</h1>
```

```javascript
scroll.on('scroll', (args) => {
  if (args.currentElements['hero-title']) {
    const progress = args.currentElements['hero-title'].progress;
    // progress ranges from 0 to 1
  }
});
```

### 5. Programmatic Scrolling

```javascript
// Scroll to top
scroll.scrollTo('top');

// Scroll to element
scroll.scrollTo('#section');

// Scroll with options
scroll.scrollTo('#section', {
  offset: -100,
  duration: 1000,
  callback: () => console.log('Done!')
});
```

## Performance Optimization

### Use data-scroll-section

Segment long pages into sections for better performance:

```html
<div data-scroll-container>
  <div data-scroll-section>Section 1</div>
  <div data-scroll-section>Section 2</div>
  <div data-scroll-section>Section 3</div>
</div>
```

### Update on Resize

The template includes resize handling:

```javascript
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => scroll.update(), 250);
});
```

### Cleanup

Always destroy the scroll instance:

```javascript
window.addEventListener('beforeunload', () => {
  scroll.destroy();
});
```

## Mobile Optimization

The template includes mobile-specific settings:

```javascript
smartphone: {
  smooth: true,      // Enable/disable smooth scroll
  breakpoint: 768    // Breakpoint in pixels
},
tablet: {
  smooth: true,
  breakpoint: 1024
}
```

For best mobile performance, consider:
- Disabling smooth scroll on smartphones: `smooth: false`
- Reducing parallax speeds
- Limiting number of tracked elements

## Accessibility

The template includes:
- Semantic HTML structure
- Proper heading hierarchy
- Color contrast compliance
- Keyboard navigation support

Consider adding:
- `prefers-reduced-motion` detection
- Skip to content link
- ARIA labels where appropriate

## Next Steps

1. **Customize styles** - Edit `style.css` to match your design
2. **Add content** - Replace placeholder content in `index.html`
3. **Integrate GSAP** - See GSAP integration examples in skill references
4. **Add animations** - Use scroll events to trigger custom animations
5. **Optimize** - Test on real devices and optimize for performance

## Troubleshooting

### Fixed elements not working?

Place fixed elements outside the scroll container:

```html
<nav style="position: fixed;">Navigation</nav>

<div data-scroll-container>
  <!-- Content -->
</div>
```

### Scroll position not updating?

Call `update()` after DOM changes:

```javascript
addContent();
scroll.update();
```

### Accessibility concerns?

Provide option to disable smooth scroll:

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const scroll = new LocomotiveScroll({
  smooth: !prefersReducedMotion
});
```

## Resources

- [Locomotive Scroll GitHub](https://github.com/locomotivemtl/locomotive-scroll)
- [Official Documentation](https://locomotivemtl.github.io/locomotive-scroll/)
- [CodePen Examples](https://codepen.io/tag/locomotive-scroll)

## License

This starter template is free to use for any purpose.
