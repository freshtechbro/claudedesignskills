---
name: locomotive-scroll
description: Comprehensive skill for Locomotive Scroll smooth scrolling library with parallax effects, viewport detection, and scroll-driven animations. Use this skill when implementing smooth scrolling experiences, creating parallax effects, building scroll-triggered animations, or developing immersive scrolling websites. Triggers on tasks involving Locomotive Scroll, smooth scrolling, parallax, scroll detection, scroll events, sticky elements, horizontal scrolling, or GSAP ScrollTrigger integration. Integrates with GSAP for advanced scroll-driven animations.
---

# Locomotive Scroll

Comprehensive guide for implementing smooth scrolling, parallax effects, and scroll-driven animations using Locomotive Scroll.

## Overview

Locomotive Scroll is a JavaScript library that provides:
- **Smooth scrolling**: Hardware-accelerated smooth scroll with customizable easing
- **Parallax effects**: Element-level speed control for depth
- **Viewport detection**: Track when elements enter/exit viewport
- **Scroll events**: Monitor scroll progress for animation synchronization
- **Sticky elements**: Pin elements within defined boundaries
- **Horizontal scrolling**: Support for horizontal scroll layouts

**When to use Locomotive Scroll:**
- Building immersive landing pages with parallax
- Creating smooth, Apple-style scroll experiences
- Implementing scroll-triggered animations
- Developing narrative/storytelling websites
- Adding depth and motion to long-form content

**Trade-offs:**
- Scroll-hijacking can impact accessibility (provide disable option)
- Performance overhead on low-end devices (detect and disable)
- Mobile touch scrolling feels different (test extensively)
- Fixed positioning requires workarounds

## Installation

```bash
npm install locomotive-scroll
```

```javascript
// ES6
import LocomotiveScroll from 'locomotive-scroll';
import 'locomotive-scroll/dist/locomotive-scroll.css';

// Or via CDN
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/locomotive-scroll/dist/locomotive-scroll.min.css">
<script src="https://cdn.jsdelivr.net/npm/locomotive-scroll/dist/locomotive-scroll.min.js"></script>
```

## Core Concepts

### 1. HTML Structure

Every Locomotive Scroll implementation requires specific data attributes:

```html
<!-- Scroll container (required) -->
<div data-scroll-container>

  <!-- Scroll sections (optional, improves performance) -->
  <div data-scroll-section>

    <!-- Tracked elements -->
    <h1 data-scroll>Basic detection</h1>

    <!-- Parallax element -->
    <div data-scroll data-scroll-speed="2">
      Moves faster than scroll
    </div>

    <!-- Sticky element -->
    <div data-scroll data-scroll-sticky>
      Sticks within section
    </div>

    <!-- Element with ID for tracking -->
    <div data-scroll data-scroll-id="hero">
      Accessible via JavaScript
    </div>

    <!-- Call event trigger -->
    <div data-scroll data-scroll-call="fadeIn">
      Triggers custom event
    </div>

  </div>
</div>
```

### 2. Initialization

```javascript
const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  lerp: 0.1,        // Smoothness (0-1, lower = smoother)
  multiplier: 1,    // Speed multiplier
  class: 'is-inview', // Class added to visible elements
  repeat: false,    // Repeat in-view detection
  offset: [0, 0]    // Global trigger offset [bottom, top]
});
```

### 3. Data Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `data-scroll` | Enable detection | `data-scroll` |
| `data-scroll-speed` | Parallax speed | `data-scroll-speed="2"` |
| `data-scroll-direction` | Parallax axis | `data-scroll-direction="horizontal"` |
| `data-scroll-sticky` | Sticky positioning | `data-scroll-sticky` |
| `data-scroll-target` | Sticky boundary | `data-scroll-target="#section"` |
| `data-scroll-offset` | Trigger offset | `data-scroll-offset="20%"` |
| `data-scroll-repeat` | Repeat detection | `data-scroll-repeat` |
| `data-scroll-call` | Event trigger | `data-scroll-call="myFunction"` |
| `data-scroll-id` | Unique identifier | `data-scroll-id="hero"` |
| `data-scroll-class` | Custom class | `data-scroll-class="is-visible"` |

## Common Patterns

### 1. Basic Smooth Scrolling

```javascript
import LocomotiveScroll from 'locomotive-scroll';

const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true
});
```

```html
<div data-scroll-container>
  <div data-scroll-section>
    <h1>Smooth scrolling enabled</h1>
  </div>
</div>
```

### 2. Parallax Effects

```html
<!-- Slow parallax -->
<div data-scroll data-scroll-speed="0.5">
  Moves slower than scroll (background effect)
</div>

<!-- Fast parallax -->
<div data-scroll data-scroll-speed="3">
  Moves faster than scroll (foreground effect)
</div>

<!-- Reverse parallax -->
<div data-scroll data-scroll-speed="-2">
  Moves in opposite direction
</div>

<!-- Horizontal parallax -->
<div data-scroll data-scroll-speed="2" data-scroll-direction="horizontal">
  Moves horizontally
</div>
```

### 3. Viewport Detection and Callbacks

```javascript
// Track scroll progress
scroll.on('scroll', (args) => {
  console.log(args.scroll.y); // Current scroll position
  console.log(args.speed);    // Scroll speed
  console.log(args.direction); // Scroll direction

  // Access specific element progress
  if (args.currentElements['hero']) {
    const progress = args.currentElements['hero'].progress;
    console.log(`Hero progress: ${progress}`); // 0 to 1
  }
});

// Call events
scroll.on('call', (value, way, obj) => {
  console.log(`Event triggered: ${value}`);
  // value = data-scroll-call attribute value
  // way = 'enter' or 'exit'
  // obj = {id, el}
});
```

```html
<div data-scroll data-scroll-id="hero">Hero section</div>
<div data-scroll data-scroll-call="playVideo">Video section</div>
```

### 4. Sticky Elements

```html
<!-- Stick within parent section -->
<div data-scroll-section>
  <div data-scroll data-scroll-sticky>
    I stick while section is in view
  </div>
</div>

<!-- Stick with specific target -->
<div id="sticky-container">
  <div data-scroll data-scroll-sticky data-scroll-target="#sticky-container">
    I stick within #sticky-container
  </div>
</div>
```

### 5. Programmatic Scrolling

```javascript
// Scroll to element
scroll.scrollTo('#target-section');

// Scroll to top
scroll.scrollTo('top');

// Scroll to bottom
scroll.scrollTo('bottom');

// Scroll with options
scroll.scrollTo('#target', {
  offset: -100,      // Offset in pixels
  duration: 1000,    // Duration in ms
  easing: [0.25, 0.0, 0.35, 1.0], // Cubic bezier
  disableLerp: true, // Disable smooth lerp
  callback: () => console.log('Scrolled!')
});

// Scroll to pixel value
scroll.scrollTo(500);
```

### 6. Horizontal Scrolling

```javascript
const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  direction: 'horizontal'
});
```

```html
<div data-scroll-container>
  <div data-scroll-section style="display: flex; width: 300vw;">
    <div>Section 1</div>
    <div>Section 2</div>
    <div>Section 3</div>
  </div>
</div>
```

### 7. Mobile Responsiveness

```javascript
const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,

  // Tablet settings
  tablet: {
    smooth: true,
    breakpoint: 1024
  },

  // Smartphone settings
  smartphone: {
    smooth: false, // Disable on mobile for performance
    breakpoint: 768
  }
});
```

## Integration with GSAP ScrollTrigger

Locomotive Scroll and GSAP ScrollTrigger work together for advanced animations:

```javascript
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const locoScroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true
});

// Sync Locomotive Scroll with ScrollTrigger
locoScroll.on('scroll', ScrollTrigger.update);

ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  scrollTop(value) {
    return arguments.length
      ? locoScroll.scrollTo(value, 0, 0)
      : locoScroll.scroll.instance.scroll.y;
  },
  getBoundingClientRect() {
    return {
      top: 0,
      left: 0,
      width: window.innerWidth,
      height: window.innerHeight
    };
  },
  pinType: document.querySelector('[data-scroll-container]').style.transform
    ? 'transform'
    : 'fixed'
});

// GSAP animation with ScrollTrigger
gsap.to('.fade-in', {
  scrollTrigger: {
    trigger: '.fade-in',
    scroller: '[data-scroll-container]',
    start: 'top bottom',
    end: 'top center',
    scrub: true
  },
  opacity: 1,
  y: 0
});

// Update ScrollTrigger when Locomotive updates
ScrollTrigger.addEventListener('refresh', () => locoScroll.update());
ScrollTrigger.refresh();
```

## Instance Methods

```javascript
const scroll = new LocomotiveScroll();

// Lifecycle
scroll.init();     // Reinitialize
scroll.update();   // Refresh element positions
scroll.destroy();  // Clean up
scroll.start();    // Resume scrolling
scroll.stop();     // Pause scrolling

// Navigation
scroll.scrollTo(target, options);
scroll.setScroll(x, y);

// Events
scroll.on('scroll', callback);
scroll.on('call', callback);
scroll.off('scroll', callback);
```

## Performance Optimization

1. **Use `data-scroll-section`** to segment long pages:
```html
<div data-scroll-container>
  <div data-scroll-section>Section 1</div>
  <div data-scroll-section>Section 2</div>
  <div data-scroll-section>Section 3</div>
</div>
```

2. **Limit parallax elements** - Too many can impact performance

3. **Disable on mobile** if performance is poor:
```javascript
smartphone: { smooth: false }
```

4. **Update on resize**:
```javascript
window.addEventListener('resize', () => {
  scroll.update();
});
```

5. **Destroy when not needed**:
```javascript
scroll.destroy();
```

## Common Pitfalls

### 1. Fixed Positioning Issues

**Problem**: `position: fixed` elements break with smooth scroll

**Solution**: Use `data-scroll-sticky` instead or add fixed elements outside container:
```html
<!-- Fixed nav outside container -->
<nav style="position: fixed;">Navigation</nav>

<div data-scroll-container>
  <!-- Page content -->
</div>
```

### 2. Images Not Lazy Loading

**Problem**: All images load at once

**Solution**: Integrate with lazy loading:
```html
<img data-scroll data-src="image.jpg" class="lazy">
```

```javascript
scroll.on('call', (func) => {
  if (func === 'lazyLoad') {
    // Trigger lazy load
  }
});
```

### 3. Scroll Position Not Updating

**Problem**: Dynamic content doesn't update scroll positions

**Solution**: Call `update()` after DOM changes:
```javascript
// After adding content
addDynamicContent();
scroll.update();
```

### 4. Accessibility Concerns

**Problem**: Screen readers and keyboard navigation broken

**Solution**: Provide disable option:
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const scroll = new LocomotiveScroll({
  smooth: !prefersReducedMotion
});
```

### 5. Memory Leaks

**Problem**: Scroll instance not cleaned up on route changes (SPAs)

**Solution**: Always destroy on unmount:
```javascript
// React example
useEffect(() => {
  const scroll = new LocomotiveScroll();

  return () => scroll.destroy();
}, []);
```

### 6. Z-Index Fighting

**Problem**: Parallax elements overlap incorrectly

**Solution**: Set explicit z-index on parallax layers:
```css
[data-scroll-speed] {
  position: relative;
  z-index: var(--layer-depth);
}
```

## Related Skills

- **gsap-scrolltrigger**: Advanced scroll-driven animations (use together)
- **barba-js**: Page transitions with Locomotive Scroll integration
- **scroll-reveal-libraries**: Simpler alternative for basic fade-in effects
- **react-three-fiber**: Scroll-driven 3D scenes (sync with Locomotive events)
- **motion-framer**: Alternative scroll animations in React

## Resources

- **Scripts**: `generate_config.py` - Configuration generator, `integration_helper.py` - GSAP integration code
- **References**: `api_reference.md` - Complete API, `gsap_integration.md` - GSAP ScrollTrigger patterns
- **Assets**: `starter_locomotive/` - Complete starter template with examples
