---
name: scroll-reveal-libraries
description: Simple scroll-triggered reveal animations using AOS (Animate On Scroll). Use this skill when building marketing pages, landing pages, or content-heavy sites requiring basic fade/slide effects without complex animation orchestration. Triggers on tasks involving scroll animations, scroll-triggered reveals, AOS, simple animations, or basic scroll effects. Alternative to GSAP ScrollTrigger and Locomotive Scroll for simpler use cases. Compare with motion-framer for React-specific animations.
---

# Scroll Reveal Libraries

## Overview

This skill covers AOS (Animate On Scroll), a lightweight CSS-driven library for scroll-triggered animations. AOS excels at simple fade, slide, and zoom effects activated when elements enter the viewport.

**Key Features**:
- **Minimal Setup**: Single JavaScript file + CSS
- **Data Attribute API**: Configure animations in HTML
- **Performance**: CSS-driven, GPU-accelerated animations
- **50+ Built-in Animations**: Fades, slides, zooms, flips
- **Framework Agnostic**: Works with vanilla JS, React, Vue, etc.

**When to Use**:
- Marketing/landing pages with simple scroll effects
- Content-heavy sites (blogs, documentation)
- Quick prototypes requiring scroll animations
- Projects where GSAP/Framer Motion complexity isn't needed

**When NOT to Use**:
- Complex animation timelines or orchestration → Use GSAP ScrollTrigger
- Physics-based animations → Use React Spring or Framer Motion
- Precise scroll-synced animations → Use GSAP ScrollTrigger
- Heavy interactive animations → Use Framer Motion

## Core Concepts

### Installation

**CDN (Quickest)**:
```html
<head>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
</head>
<body>
  <!-- Content with data-aos attributes -->

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init();
  </script>
</body>
```

**NPM/Yarn (Recommended)**:
```bash
npm install aos@next
# or
yarn add aos@next
```

```javascript
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();
```

### Basic Usage

Apply animations using the `data-aos` attribute:

```html
<!-- Fade in -->
<div data-aos="fade-in">Content</div>

<!-- Fade up -->
<div data-aos="fade-up">Content</div>

<!-- Slide from right -->
<div data-aos="slide-left">Content</div>

<!-- Zoom in -->
<div data-aos="zoom-in">Content</div>
```

### Configuration Options

**Global Configuration**:
```javascript
AOS.init({
  // Animation settings
  duration: 800,  // Animation duration (ms): 0-3000
  delay: 0,       // Delay before animation (ms): 0-3000
  offset: 120,    // Offset from trigger point (px)
  easing: 'ease', // Easing function
  once: false,    // Animate only once (true) or every time (false)
  mirror: false,  // Animate out when scrolling past

  // Placement
  anchorPlacement: 'top-bottom', // Which position triggers animation

  // Performance
  disable: false,                // Disable on mobile/tablet
  startEvent: 'DOMContentLoaded', // Initialization event
  debounceDelay: 50,             // Window resize debounce
  throttleDelay: 99              // Scroll throttle
});
```

**Per-Element Overrides**:
```html
<div
  data-aos="fade-up"
  data-aos-duration="1000"
  data-aos-delay="200"
  data-aos-offset="50"
  data-aos-easing="ease-in-out"
  data-aos-once="true"
  data-aos-mirror="true"
  data-aos-anchor-placement="center-bottom"
>
  Custom configured element
</div>
```

## Common Patterns

### 1. Landing Page Hero Section

```html
<section class="hero">
  <!-- Staggered heading words -->
  <h1
    data-aos="fade-down"
    data-aos-duration="800"
  >
    Welcome to the Future
  </h1>

  <!-- Delayed subheading -->
  <p
    data-aos="fade-up"
    data-aos-delay="200"
    data-aos-duration="600"
  >
    Transform your ideas into reality
  </p>

  <!-- CTA button -->
  <button
    data-aos="zoom-in"
    data-aos-delay="400"
    data-aos-duration="500"
  >
    Get Started
  </button>
</section>
```

### 2. Feature Cards Grid

```html
<div class="features-grid">
  <!-- Stagger cards with increasing delays -->
  <div
    class="feature-card"
    data-aos="fade-up"
    data-aos-duration="600"
    data-aos-delay="0"
  >
    <h3>Feature 1</h3>
    <p>Description...</p>
  </div>

  <div
    class="feature-card"
    data-aos="fade-up"
    data-aos-duration="600"
    data-aos-delay="100"
  >
    <h3>Feature 2</h3>
    <p>Description...</p>
  </div>

  <div
    class="feature-card"
    data-aos="fade-up"
    data-aos-duration="600"
    data-aos-delay="200"
  >
    <h3>Feature 3</h3>
    <p>Description...</p>
  </div>
</div>
```

### 3. Alternating Content Sections

```html
<!-- Content from left -->
<div class="section">
  <div
    class="content"
    data-aos="slide-right"
    data-aos-duration="800"
  >
    <h2>Section Title</h2>
    <p>Content slides in from left...</p>
  </div>
  <img
    src="image1.jpg"
    data-aos="fade-left"
    data-aos-delay="200"
  />
</div>

<!-- Content from right -->
<div class="section reverse">
  <img
    src="image2.jpg"
    data-aos="fade-right"
  />
  <div
    class="content"
    data-aos="slide-left"
    data-aos-duration="800"
    data-aos-delay="200"
  >
    <h2>Section Title</h2>
    <p>Content slides in from right...</p>
  </div>
</div>
```

### 4. Scroll-Triggered Testimonials

```html
<div class="testimonials">
  <div
    class="testimonial"
    data-aos="zoom-in"
    data-aos-duration="500"
  >
    <blockquote>"Amazing product!"</blockquote>
    <cite>- John Doe</cite>
  </div>

  <div
    class="testimonial"
    data-aos="zoom-in"
    data-aos-duration="500"
    data-aos-delay="100"
  >
    <blockquote>"Exceeded expectations"</blockquote>
    <cite>- Jane Smith</cite>
  </div>
</div>
```

### 5. Custom Anchor Triggers

Trigger animations based on a different element's scroll position:

```html
<!-- Fixed sidebar animates based on main content scroll -->
<div class="main-content">
  <div id="trigger-point" data-aos-id="sidebar-trigger">
    <!-- Content -->
  </div>
</div>

<aside
  class="sidebar"
  data-aos="fade-left"
  data-aos-anchor="#trigger-point"
>
  Sidebar content
</aside>
```

### 6. Sequential Animation Chain

```html
<div class="animation-sequence">
  <!-- Step 1: Heading -->
  <h2
    data-aos="fade-down"
    data-aos-duration="600"
    data-aos-delay="0"
  >
    Our Process
  </h2>

  <!-- Step 2: Description -->
  <p
    data-aos="fade-up"
    data-aos-duration="600"
    data-aos-delay="200"
  >
    Follow these simple steps
  </p>

  <!-- Step 3-5: Process cards -->
  <div
    class="process-step"
    data-aos="flip-left"
    data-aos-delay="400"
  >
    Step 1
  </div>

  <div
    class="process-step"
    data-aos="flip-left"
    data-aos-delay="600"
  >
    Step 2
  </div>

  <div
    class="process-step"
    data-aos="flip-left"
    data-aos-delay="800"
  >
    Step 3
  </div>
</div>
```

### 7. Image Gallery with Zoom Effects

```html
<div class="gallery">
  <img
    src="photo1.jpg"
    data-aos="zoom-in-up"
    data-aos-duration="800"
  />
  <img
    src="photo2.jpg"
    data-aos="zoom-in-up"
    data-aos-duration="800"
    data-aos-delay="100"
  />
  <img
    src="photo3.jpg"
    data-aos="zoom-in-up"
    data-aos-duration="800"
    data-aos-delay="200"
  />
</div>
```

## Integration Patterns

### React Integration

**Basic Setup**:
```jsx
import { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';

function App() {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
      offset: 100
    });
  }, []);

  return (
    <div>
      <h1 data-aos="fade-down">Welcome</h1>
      <p data-aos="fade-up">Content here</p>
    </div>
  );
}
```

**Refreshing on Route Changes**:
```jsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import AOS from 'aos';

function App() {
  const location = useLocation();

  useEffect(() => {
    AOS.init({ duration: 800 });
  }, []);

  // Refresh AOS on route change
  useEffect(() => {
    AOS.refresh();
  }, [location]);

  return <Routes>{/* routes */}</Routes>;
}
```

**Dynamic Content Updates**:
```jsx
import { useState, useEffect } from 'react';
import AOS from 'aos';

function DynamicList() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    AOS.init();
  }, []);

  const addItem = () => {
    setItems([...items, { id: Date.now(), text: 'New Item' }]);

    // Refresh AOS to detect new elements
    setTimeout(() => AOS.refresh(), 50);
  };

  return (
    <div>
      <button onClick={addItem}>Add Item</button>
      <ul>
        {items.map((item) => (
          <li key={item.id} data-aos="fade-in">
            {item.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Component Wrapper Pattern**:
```jsx
import AOS from 'aos';
import 'aos/dist/aos.css';

function AnimatedSection({ children, animation = "fade-up", delay = 0, ...props }) {
  return (
    <div
      data-aos={animation}
      data-aos-delay={delay}
      {...props}
    >
      {children}
    </div>
  );
}

// Usage
<AnimatedSection animation="slide-right" delay={200}>
  <h2>Animated Content</h2>
</AnimatedSection>
```

### Vue.js Integration

```vue
<template>
  <div>
    <h1 data-aos="fade-down">Vue + AOS</h1>
    <div
      v-for="(item, index) in items"
      :key="item.id"
      data-aos="fade-up"
      :data-aos-delay="index * 100"
    >
      {{ item.text }}
    </div>
  </div>
</template>

<script>
import AOS from 'aos';
import 'aos/dist/aos.css';

export default {
  mounted() {
    AOS.init({ duration: 800 });
  },
  updated() {
    // Refresh when component updates
    this.$nextTick(() => {
      AOS.refresh();
    });
  },
  data() {
    return {
      items: [/*...*/]
    };
  }
};
</script>
```

### Next.js Integration

```jsx
// pages/_app.js
import { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true
    });
  }, []);

  return <Component {...pageProps} />;
}

export default MyApp;
```

```jsx
// pages/index.js
export default function Home() {
  return (
    <main>
      <h1 data-aos="fade-down">Next.js + AOS</h1>
      <p data-aos="fade-up">Server-side rendered content with animations</p>
    </main>
  );
}
```

## Performance Optimization

### 1. Disable on Mobile Devices

```javascript
AOS.init({
  disable: 'mobile', // Disable on mobile
  // Or use function for custom logic
  disable: function() {
    return window.innerWidth < 768;
  }
});
```

### 2. Use Once for Better Performance

```javascript
AOS.init({
  once: true, // Animate only once (better performance)
  mirror: false // Don't animate out
});
```

### 3. Optimize Throttle and Debounce

```javascript
AOS.init({
  throttleDelay: 99,  // Scroll event throttle (default)
  debounceDelay: 50   // Resize event debounce (default)
});
```

### 4. Disable Mutation Observer for Static Content

```javascript
AOS.init({
  disableMutationObserver: true // Disable for fully static content
});
```

### 5. Reduce Animation Complexity

```html
<!-- Simpler animations perform better -->
<div data-aos="fade-in">Simple fade</div>

<!-- Complex animations may cause jank -->
<div data-aos="flip-left">Complex flip</div>
```

### 6. Use RequestIdleCallback for Initialization

```javascript
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    AOS.init({ duration: 800 });
  });
} else {
  AOS.init({ duration: 800 });
}
```

## Common Pitfalls

### 1. Forgetting to Refresh After DOM Changes

**Problem**: New elements don't animate after being added dynamically.

**Solution**: Call `AOS.refresh()` or `AOS.refreshHard()`:

```javascript
// After adding elements to DOM
const newElement = document.createElement('div');
newElement.setAttribute('data-aos', 'fade-in');
container.appendChild(newElement);

// Refresh AOS
AOS.refresh(); // Recalculate positions
// or
AOS.refreshHard(); // Reinitialize completely
```

### 2. Animations Not Working in React

**Problem**: AOS doesn't detect elements on first render or route changes.

**Solution**: Initialize in `useEffect` and refresh on route/content changes:

```jsx
useEffect(() => {
  AOS.init();
  return () => AOS.refresh(); // Cleanup
}, []);

useEffect(() => {
  AOS.refresh(); // Refresh on route change
}, [location.pathname]);
```

### 3. Scroll Performance Issues

**Problem**: Page scrolling feels janky with many animated elements.

**Solution**: Reduce animated elements and use `once: true`:

```javascript
AOS.init({
  once: true, // Animate only once
  disable: window.innerWidth < 768 // Disable on mobile
});
```

### 4. CSS Conflicts

**Problem**: Custom CSS interferes with AOS animations.

**Solution**: Use more specific selectors and avoid `!important`:

```css
/* Bad: Conflicts with AOS */
div {
  opacity: 1 !important;
}

/* Good: Specific selector */
.my-content > div {
  /* styles */
}
```

### 5. Anchor Placement Confusion

**Problem**: Animations trigger at unexpected scroll positions.

**Solution**: Understand anchor placement options:

```javascript
// Triggers when element's top hits viewport bottom
data-aos-anchor-placement="top-bottom"

// Triggers when element's center hits viewport center
data-aos-anchor-placement="center-center"

// Triggers when element's bottom hits viewport top
data-aos-anchor-placement="bottom-top"
```

### 6. Duration/Delay Limits

**Problem**: Values above 3000ms don't work.

**Solution**: Add custom CSS for extended durations:

```css
body[data-aos-duration='4000'] [data-aos],
[data-aos][data-aos][data-aos-duration='4000'] {
  transition-duration: 4000ms;
}
```

```html
<div data-aos="fade-in" data-aos-duration="4000">
  Long animation
</div>
```

## Built-in Animations

### Fade Animations
- `fade-in` - Simple fade in
- `fade-up` - Fade in from bottom
- `fade-down` - Fade in from top
- `fade-left` - Fade in from right
- `fade-right` - Fade in from left
- `fade-up-right` - Diagonal fade
- `fade-up-left` - Diagonal fade
- `fade-down-right` - Diagonal fade
- `fade-down-left` - Diagonal fade

### Slide Animations
- `slide-up` - Slide from bottom
- `slide-down` - Slide from top
- `slide-left` - Slide from right
- `slide-right` - Slide from left

### Zoom Animations
- `zoom-in` - Zoom in
- `zoom-in-up` - Zoom in from bottom
- `zoom-in-down` - Zoom in from top
- `zoom-in-left` - Zoom in from right
- `zoom-in-right` - Zoom in from left
- `zoom-out` - Zoom out
- `zoom-out-up` - Zoom out to top
- `zoom-out-down` - Zoom out to bottom
- `zoom-out-left` - Zoom out to left
- `zoom-out-right` - Zoom out to right

### Flip Animations
- `flip-up` - Flip from bottom
- `flip-down` - Flip from top
- `flip-left` - Flip from right
- `flip-right` - Flip from left

## Custom Animations

Create custom animations with CSS:

```css
[data-aos="custom-slide-bounce"] {
  opacity: 0;
  transform: translateY(100px);
  transition-property: transform, opacity;
}

[data-aos="custom-slide-bounce"].aos-animate {
  opacity: 1;
  transform: translateY(0);
  animation: bounce 0.5s;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
```

```html
<div data-aos="custom-slide-bounce">
  Custom animation
</div>
```

## Comparison with Alternatives

### AOS vs GSAP ScrollTrigger

| Feature | AOS | GSAP ScrollTrigger |
|---------|-----|-------------------|
| **Complexity** | Simple, data-attribute based | Advanced, JavaScript API |
| **Use Case** | Simple reveals | Complex timelines |
| **File Size** | ~13KB | ~27KB (GSAP) + ScrollTrigger |
| **Performance** | CSS-driven | JavaScript-driven |
| **Learning Curve** | Minutes | Hours |
| **Customization** | Limited | Extensive |
| **Best For** | Marketing pages | Interactive experiences |

**Use AOS when**:
- Simple fade/slide/zoom effects
- Quick implementation needed
- Minimal JavaScript preferred
- Basic scroll reveals sufficient

**Use GSAP ScrollTrigger when**:
- Complex animation sequences
- Precise scroll-synced animations
- Timeline orchestration needed
- Advanced easing/physics required

## Resources

### Official Documentation
- **AOS**: https://michalsnik.github.io/aos/
- **GitHub**: https://github.com/michalsnik/aos

### Key Scripts
- `scripts/aos_generator.py` - Generate AOS HTML boilerplate
- `scripts/config_builder.py` - Build AOS configuration

### References
- `references/aos_api.md` - Complete AOS API reference
- `references/animation_catalog.md` - All built-in animations with demos
- `references/integration_patterns.md` - Framework integration guides

### Starter Assets
- `assets/starter_aos/` - Complete AOS starter template
- `assets/examples/` - Production-ready patterns

## Related Skills

- **gsap-scrolltrigger**: For complex scroll-driven animations
- **motion-framer**: For React-specific animations with physics
- **locomotive-scroll**: For smooth scrolling with parallax
- **animated-component-libraries**: For pre-built animated React components
