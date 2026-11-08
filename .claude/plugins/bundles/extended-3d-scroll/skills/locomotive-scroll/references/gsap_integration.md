# GSAP ScrollTrigger Integration with Locomotive Scroll

Complete guide for integrating Locomotive Scroll with GSAP ScrollTrigger for advanced scroll-driven animations.

## Table of Contents

- [Why Combine Them](#why-combine-them)
- [Basic Integration](#basic-integration)
- [ScrollTrigger Proxy Setup](#scrolltrigger-proxy-setup)
- [Common Animation Patterns](#common-animation-patterns)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## Why Combine Them

**Locomotive Scroll** provides:
- Smooth scrolling UX
- Parallax effects
- Viewport detection

**GSAP ScrollTrigger** provides:
- Advanced timeline control
- Precise scrubbing
- Pin/snap functionality
- Complex animation sequencing

**Together** they create:
- Smooth scroll + scroll-driven animations
- Parallax + complex timelines
- Premium scroll experiences

## Basic Integration

### 1. Installation

```bash
npm install locomotive-scroll gsap
```

### 2. Complete Integration Setup

```javascript
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Initialize Locomotive Scroll
const locoScroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  smartphone: {
    smooth: true
  },
  tablet: {
    smooth: true
  }
});

// Sync Locomotive Scroll with ScrollTrigger
locoScroll.on('scroll', ScrollTrigger.update);

// Tell ScrollTrigger to use Locomotive Scroll's scroller
ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  scrollTop(value) {
    return arguments.length
      ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
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

// Update ScrollTrigger when Locomotive Scroll updates
ScrollTrigger.addEventListener('refresh', () => locoScroll.update());

// Refresh both after DOM loads
ScrollTrigger.refresh();
```

## ScrollTrigger Proxy Setup

### Understanding scrollerProxy

The `scrollerProxy` tells ScrollTrigger how to interact with Locomotive Scroll's custom scroller:

```javascript
ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  // Get/Set scroll position
  scrollTop(value) {
    if (arguments.length) {
      // Setter - scroll to position
      locoScroll.scrollTo(value, {
        duration: 0,        // Instant
        disableLerp: true   // No smooth interpolation
      });
    } else {
      // Getter - return current position
      return locoScroll.scroll.instance.scroll.y;
    }
  },

  // Define scroller dimensions
  getBoundingClientRect() {
    return {
      top: 0,
      left: 0,
      width: window.innerWidth,
      height: window.innerHeight
    };
  },

  // pinType determines how pinning works
  // 'transform' for smooth scroll, 'fixed' for native
  pinType: document.querySelector('[data-scroll-container]').style.transform
    ? 'transform'
    : 'fixed'
});
```

### For Horizontal Scroll

```javascript
ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  scrollLeft(value) {
    return arguments.length
      ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
      : locoScroll.scroll.instance.scroll.x;
  },
  getBoundingClientRect() {
    return {
      top: 0,
      left: 0,
      width: window.innerWidth,
      height: window.innerHeight
    };
  }
});
```

## Common Animation Patterns

### 1. Fade In on Scroll

```javascript
gsap.to('.fade-in', {
  scrollTrigger: {
    trigger: '.fade-in',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 50%',
    scrub: true,
    markers: true // Debug markers
  },
  opacity: 1,
  y: 0,
  duration: 1
});
```

```html
<div class="fade-in" style="opacity: 0; transform: translateY(50px);">
  Fades in on scroll
</div>
```

### 2. Pin Section While Scrolling

```javascript
ScrollTrigger.create({
  trigger: '#pinned-section',
  scroller: '[data-scroll-container]',
  pin: true,
  start: 'top top',
  end: 'bottom bottom',
  pinSpacing: false
});
```

```html
<div data-scroll-section id="pinned-section">
  This section pins while you scroll
</div>
```

### 3. Scrubbed Timeline Animation

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '#animated-section',
    scroller: '[data-scroll-container]',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1, // Smooth scrubbing (1 second delay)
    pin: true
  }
});

tl.from('.box-1', { x: -100, opacity: 0 })
  .from('.box-2', { x: 100, opacity: 0 })
  .from('.box-3', { y: 100, opacity: 0 })
  .to('.box-1', { rotation: 360, scale: 1.5 });
```

### 4. Progress-Based Animation

Sync animations with Locomotive Scroll's progress values:

```javascript
locoScroll.on('scroll', (args) => {
  if (args.currentElements['hero']) {
    const progress = args.currentElements['hero'].progress;

    // Animate based on progress (0 to 1)
    gsap.to('#hero-image', {
      scale: 1 + progress * 0.5,
      rotation: progress * 360,
      duration: 0
    });
  }
});
```

```html
<div data-scroll data-scroll-id="hero">
  <img id="hero-image" src="hero.jpg" alt="Hero">
</div>
```

### 5. Horizontal Scroll Animation

```javascript
const sections = gsap.utils.toArray('.panel');

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '#horizontal-container',
    scroller: '[data-scroll-container]',
    pin: true,
    scrub: 1,
    end: () => `+=${document.querySelector('#horizontal-container').offsetWidth}`
  }
});
```

```html
<div data-scroll-section id="horizontal-container">
  <div class="panel">Panel 1</div>
  <div class="panel">Panel 2</div>
  <div class="panel">Panel 3</div>
</div>
```

```css
#horizontal-container {
  display: flex;
  width: 300vw;
}
.panel {
  width: 100vw;
  height: 100vh;
}
```

### 6. Stagger Animation

```javascript
gsap.from('.item', {
  scrollTrigger: {
    trigger: '.items-container',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 30%',
    scrub: 1
  },
  y: 100,
  opacity: 0,
  stagger: 0.2
});
```

```html
<div class="items-container" data-scroll-section>
  <div class="item">Item 1</div>
  <div class="item">Item 2</div>
  <div class="item">Item 3</div>
  <div class="item">Item 4</div>
</div>
```

### 7. Image Reveal Effect

```javascript
gsap.to('.reveal-image img', {
  scrollTrigger: {
    trigger: '.reveal-image',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 30%',
    scrub: true
  },
  scale: 1,
  clipPath: 'inset(0% 0% 0% 0%)'
});
```

```html
<div class="reveal-image">
  <img src="image.jpg" style="scale: 1.2; clip-path: inset(10% 10% 10% 10%);">
</div>
```

### 8. Text Split Animation

```javascript
// Split text into characters
const text = document.querySelector('.split-text');
const chars = text.textContent.split('');
text.innerHTML = chars.map(char => `<span>${char}</span>`).join('');

// Animate each character
gsap.from('.split-text span', {
  scrollTrigger: {
    trigger: '.split-text',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 50%',
    scrub: 1
  },
  opacity: 0,
  y: 50,
  rotationX: -90,
  stagger: 0.02
});
```

## Performance Optimization

### 1. Refresh Strategy

Only refresh when needed:

```javascript
// Update Locomotive Scroll on window resize
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    locoScroll.update();
    ScrollTrigger.refresh();
  }, 250);
});
```

### 2. Lazy Initialization

Create ScrollTriggers only when sections are near viewport:

```javascript
locoScroll.on('call', (func, way, obj) => {
  if (func === 'initAnimations' && way === 'enter') {
    // Initialize animations for this section
    initSectionAnimations(obj.el);
  }
});
```

```html
<div data-scroll data-scroll-call="initAnimations">
  <!-- Animations initialized only when visible -->
</div>
```

### 3. Kill ScrollTriggers

Destroy when no longer needed:

```javascript
const st = ScrollTrigger.create({
  trigger: '.temp-animation',
  scroller: '[data-scroll-container]',
  onEnter: () => {
    // Animation complete
    st.kill(); // Remove ScrollTrigger
  }
});
```

### 4. Use will-change Sparingly

```css
[data-scroll] {
  /* Only on elements that actually animate */
  will-change: transform;
}
```

### 5. Normalize ScrollTrigger Updates

```javascript
// Throttle updates
let ticking = false;

locoScroll.on('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      ScrollTrigger.update();
      ticking = false;
    });
    ticking = true;
  }
});
```

## Complete React Example

```javascript
import { useEffect, useRef } from 'react';
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

function App() {
  const scrollRef = useRef(null);
  const locoScrollRef = useRef(null);

  useEffect(() => {
    const locoScroll = new LocomotiveScroll({
      el: scrollRef.current,
      smooth: true,
      smartphone: { smooth: true },
      tablet: { smooth: true }
    });

    locoScrollRef.current = locoScroll;

    locoScroll.on('scroll', ScrollTrigger.update);

    ScrollTrigger.scrollerProxy(scrollRef.current, {
      scrollTop(value) {
        return arguments.length
          ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
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
      pinType: scrollRef.current.style.transform ? 'transform' : 'fixed'
    });

    ScrollTrigger.addEventListener('refresh', () => locoScroll.update());
    ScrollTrigger.refresh();

    // Cleanup
    return () => {
      locoScroll.destroy();
      ScrollTrigger.getAll().forEach(st => st.kill());
    };
  }, []);

  useEffect(() => {
    // Animation example
    gsap.to('.animated-element', {
      scrollTrigger: {
        trigger: '.animated-element',
        scroller: scrollRef.current,
        start: 'top 80%',
        scrub: true
      },
      opacity: 1,
      y: 0
    });
  }, []);

  return (
    <div data-scroll-container ref={scrollRef}>
      <div data-scroll-section>
        <h1 className="animated-element">Hello World</h1>
      </div>
    </div>
  );
}
```

## Troubleshooting

### Issue: Animations Don't Trigger

**Cause**: ScrollTrigger not synced properly

**Solution**: Ensure scroller proxy is set correctly:
```javascript
ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  // ... proxy setup
});
```

### Issue: Pin Not Working

**Cause**: pinType mismatch

**Solution**: Check transform vs fixed:
```javascript
pinType: document.querySelector('[data-scroll-container]').style.transform
  ? 'transform'
  : 'fixed'
```

### Issue: Scroll Position Jumps

**Cause**: Conflicting smooth scroll implementations

**Solution**: Disable lerp in scrollTo:
```javascript
scrollTop(value) {
  return arguments.length
    ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
    : locoScroll.scroll.instance.scroll.y;
}
```

### Issue: Markers Not Showing

**Cause**: Markers are positioned for native scroll

**Solution**: Use ScrollTrigger's built-in markers with scroller specified:
```javascript
scrollTrigger: {
  scroller: '[data-scroll-container]',
  markers: true
}
```

### Issue: Performance Degradation

**Solutions**:
1. Reduce `scrub` value (use `scrub: 1` instead of `scrub: true`)
2. Limit number of ScrollTriggers
3. Use `once: true` for one-time animations
4. Throttle scroll updates

### Issue: React/SPA Route Changes

**Cause**: ScrollTriggers and Locomotive Scroll not cleaned up

**Solution**: Always destroy on unmount:
```javascript
useEffect(() => {
  const scroll = new LocomotiveScroll();

  return () => {
    scroll.destroy();
    ScrollTrigger.getAll().forEach(st => st.kill());
  };
}, []);
```

## Advanced Pattern: Locomotive + ScrollTrigger + Three.js

```javascript
import * as THREE from 'three';

// Three.js scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight);
const renderer = new THREE.WebGLRenderer();

// Locomotive Scroll + ScrollTrigger setup
const locoScroll = new LocomotiveScroll({ /* ... */ });

// Sync 3D camera with scroll
locoScroll.on('scroll', (args) => {
  const scrollY = args.scroll.y;
  camera.position.y = scrollY * 0.001;
  renderer.render(scene, camera);
});

// GSAP timeline for 3D objects
gsap.to(mesh.rotation, {
  scrollTrigger: {
    trigger: '#3d-section',
    scroller: '[data-scroll-container]',
    scrub: 1
  },
  y: Math.PI * 2
});
```

## Resources

- [Locomotive Scroll GitHub](https://github.com/locomotivemtl/locomotive-scroll)
- [GSAP ScrollTrigger Docs](https://greensock.com/docs/v3/Plugins/ScrollTrigger)
- [CodePen Examples](https://codepen.io/tag/locomotive-scroll)
