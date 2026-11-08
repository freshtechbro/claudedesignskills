# Vanilla-Tilt.js Patterns Reference

Complete reference for Vanilla-Tilt.js - smooth 3D tilt effect for any DOM element.

**Version**: 1.8.1
**License**: MIT
**GitHub**: https://github.com/micku7zu/vanilla-tilt.js

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Configuration Options](#configuration-options)
3. [Methods](#methods)
4. [Events](#events)
5. [Common Patterns](#common-patterns)
6. [Advanced Techniques](#advanced-techniques)
7. [Framework Integration](#framework-integration)
8. [Performance](#performance)

---

## Getting Started

### CDN Installation

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js"></script>

<div class="tilt-card" data-tilt></div>

<script>
VanillaTilt.init(document.querySelector(".tilt-card"));
</script>
```

---

### NPM Installation

```bash
npm install vanilla-tilt
```

```javascript
import VanillaTilt from 'vanilla-tilt';

VanillaTilt.init(document.querySelector(".tilt-card"));
```

---

### Basic Usage

**HTML Attribute (No JavaScript)**:

```html
<div class="tilt-card" data-tilt></div>
```

**JavaScript Initialization**:

```html
<div class="tilt-card"></div>

<script>
VanillaTilt.init(document.querySelector(".tilt-card"), {
  max: 25,
  speed: 400,
  glare: true,
  "max-glare": 0.5
});
</script>
```

**Multiple Elements**:

```javascript
VanillaTilt.init(document.querySelectorAll(".tilt-card"));
```

---

## Configuration Options

### Complete Options Reference

```javascript
VanillaTilt.init(element, {
  // Rotation
  reverse: false,               // Reverse tilt direction
  max: 15,                      // Max tilt angle (degrees)
  startX: 0,                    // Starting tilt on X axis (degrees)
  startY: 0,                    // Starting tilt on Y axis (degrees)
  perspective: 1000,            // Transform perspective (px)

  // Scale
  scale: 1.0,                   // Scale on hover (2 = 200%)

  // Speed & Easing
  speed: 300,                   // Transition speed (ms)
  transition: true,             // Enable/disable transition
  easing: "cubic-bezier(.03,.98,.52,.99)",  // CSS easing

  // Axis Control
  axis: null,                   // Restrict axis ("x" or "y")
  reset: true,                  // Reset on mouseout
  "reset-to-start": true,       // Reset to startX/startY values

  // Glare Effect
  glare: false,                 // Enable glare effect
  "max-glare": 1,               // Max glare opacity (0-1)
  "glare-prerender": false,     // Pre-render glare element

  // Mouse/Touch
  "mouse-event-element": null,  // Element for mouse detection
  "full-page-listening": false, // Listen to mouse on entire page
  gyroscope: true,              // Enable gyroscope (mobile)
  gyroscopeMinAngleX: -45,      // Min gyro angle X
  gyroscopeMaxAngleX: 45,       // Max gyro angle X
  gyroscopeMinAngleY: -45,      // Min gyro angle Y
  gyroscopeMaxAngleY: 45        // Max gyro angle Y
});
```

---

## Configuration Options Details

### Rotation Options

#### max

Maximum tilt angle in degrees.

```javascript
// Subtle tilt
VanillaTilt.init(element, { max: 10 });

// Dramatic tilt
VanillaTilt.init(element, { max: 35 });

// Extreme tilt
VanillaTilt.init(element, { max: 50 });
```

**Recommended**: 15-25 for most use cases

---

#### reverse

Reverse the tilt direction.

```javascript
VanillaTilt.init(element, {
  reverse: true  // Tilts opposite to mouse movement
});
```

**Use case**: Parallax layers moving in opposite directions

---

#### startX / startY

Initial tilt angle (degrees).

```javascript
VanillaTilt.init(element, {
  startX: 10,    // Start tilted 10° on X axis
  startY: -5     // Start tilted -5° on Y axis
});
```

---

#### perspective

CSS perspective value (pixels).

```javascript
// Subtle 3D
VanillaTilt.init(element, { perspective: 2000 });

// Strong 3D
VanillaTilt.init(element, { perspective: 500 });
```

**Lower values = stronger 3D effect**

---

### Scale Options

#### scale

Element scale on hover (1.0 = 100%).

```javascript
// Subtle zoom
VanillaTilt.init(element, { scale: 1.05 });

// Noticeable zoom
VanillaTilt.init(element, { scale: 1.2 });

// Dramatic zoom
VanillaTilt.init(element, { scale: 1.5 });
```

---

### Speed & Easing

#### speed

Transition duration in milliseconds.

```javascript
// Fast (snappy)
VanillaTilt.init(element, { speed: 200 });

// Smooth (recommended)
VanillaTilt.init(element, { speed: 400 });

// Slow (fluid)
VanillaTilt.init(element, { speed: 800 });
```

---

#### easing

CSS easing function for transitions.

```javascript
// Linear
VanillaTilt.init(element, {
  easing: "linear"
});

// Ease out (recommended)
VanillaTilt.init(element, {
  easing: "cubic-bezier(.03,.98,.52,.99)"
});

// Bounce
VanillaTilt.init(element, {
  easing: "cubic-bezier(.68,-0.55,.265,1.55)"
});

// Elastic
VanillaTilt.init(element, {
  easing: "cubic-bezier(.6,.04,.98,.335)"
});
```

---

#### transition

Enable/disable CSS transitions.

```javascript
// Disable for instant response
VanillaTilt.init(element, { transition: false });
```

---

### Axis Control

#### axis

Restrict tilt to one axis.

```javascript
// Horizontal tilt only
VanillaTilt.init(element, { axis: "x" });

// Vertical tilt only
VanillaTilt.init(element, { axis: "y" });

// Both axes (default)
VanillaTilt.init(element, { axis: null });
```

---

#### reset

Reset tilt when mouse leaves element.

```javascript
// Keep tilt on mouseout
VanillaTilt.init(element, { reset: false });

// Reset on mouseout (default)
VanillaTilt.init(element, { reset: true });
```

---

#### reset-to-start

Reset to startX/startY values instead of 0.

```javascript
VanillaTilt.init(element, {
  startX: 10,
  startY: -5,
  "reset-to-start": true  // Resets to (10, -5) not (0, 0)
});
```

---

### Glare Effect

#### glare

Enable glossy glare overlay.

```javascript
VanillaTilt.init(element, {
  glare: true,
  "max-glare": 0.5  // 50% max opacity
});
```

**Note**: Automatically adds a `.js-tilt-glare` element inside the tilt element.

---

#### max-glare

Maximum glare opacity (0 to 1).

```javascript
// Subtle glare
VanillaTilt.init(element, {
  glare: true,
  "max-glare": 0.2
});

// Strong glare
VanillaTilt.init(element, {
  glare: true,
  "max-glare": 0.8
});
```

---

#### glare-prerender

Pre-render glare element in HTML (performance optimization).

```html
<div class="tilt-card" data-tilt>
  <div class="js-tilt-glare">
    <div class="js-tilt-glare-inner"></div>
  </div>
  <!-- Your content -->
</div>
```

```javascript
VanillaTilt.init(element, {
  glare: true,
  "glare-prerender": true
});
```

---

### Mouse/Touch Options

#### mouse-event-element

Use different element for mouse tracking.

```javascript
VanillaTilt.init(element, {
  "mouse-event-element": document.querySelector(".parent")
});
```

**Use case**: Tilt element based on mouse position over larger container.

---

#### full-page-listening

Track mouse position across entire page.

```javascript
VanillaTilt.init(element, {
  "full-page-listening": true
});
```

**Use case**: Parallax effects that respond to page-wide mouse movement.

---

### Gyroscope Options

#### gyroscope

Enable device orientation (mobile).

```javascript
VanillaTilt.init(element, {
  gyroscope: true,
  gyroscopeMinAngleX: -45,
  gyroscopeMaxAngleX: 45,
  gyroscopeMinAngleY: -45,
  gyroscopeMaxAngleY: 45
});
```

**Note**: Requires HTTPS and user permission on iOS.

---

## Methods

### destroy()

Remove tilt effect and event listeners.

```javascript
const element = document.querySelector(".tilt-card");
VanillaTilt.init(element);

// Later...
element.vanillaTilt.destroy();
```

**Important**: Always call `destroy()` when removing elements to prevent memory leaks.

---

### reset()

Reset tilt to default position.

```javascript
element.vanillaTilt.reset();
```

---

### getValues()

Get current tilt values.

```javascript
const values = element.vanillaTilt.getValues();

console.log(values);
// {
//   tiltX: 10.5,
//   tiltY: -5.2,
//   percentageX: 52.5,
//   percentageY: 47.8,
//   angle: 11.7
// }
```

**Return values**:
- `tiltX`: Current X-axis tilt (degrees)
- `tiltY`: Current Y-axis tilt (degrees)
- `percentageX`: Mouse X position as percentage (0-100)
- `percentageY`: Mouse Y position as percentage (0-100)
- `angle`: Total tilt angle (degrees)

---

### setOptions(options)

Update options after initialization.

```javascript
element.vanillaTilt.setOptions({
  max: 35,
  speed: 600
});
```

---

## Events

### tiltChange

Fired when tilt changes.

```javascript
element.addEventListener("tiltChange", (e) => {
  console.log("Tilt changed:", e.detail);
  // {
  //   tiltX: 10.5,
  //   tiltY: -5.2,
  //   percentageX: 52.5,
  //   percentageY: 47.8,
  //   angle: 11.7
  // }
});
```

---

### mouseLeave

Fired when mouse leaves element.

```javascript
element.addEventListener("mouseLeave", () => {
  console.log("Mouse left tilt element");
});
```

---

### mouseEnter

Fired when mouse enters element.

```javascript
element.addEventListener("mouseEnter", () => {
  console.log("Mouse entered tilt element");
});
```

---

## Common Patterns

### Pattern 1: Card Gallery

Tilting card grid with glare.

```html
<div class="card-grid">
  <div class="tilt-card" data-tilt>
    <img src="image1.jpg" alt="Card 1">
    <h3>Card Title</h3>
  </div>
  <div class="tilt-card" data-tilt>
    <img src="image2.jpg" alt="Card 2">
    <h3>Card Title</h3>
  </div>
  <!-- More cards... -->
</div>
```

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

.tilt-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  transform-style: preserve-3d;
}

.tilt-card img {
  width: 100%;
  display: block;
  transform: translateZ(20px);
}

.tilt-card h3 {
  padding: 1rem;
  transform: translateZ(40px);
}
```

```javascript
VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
  max: 15,
  speed: 400,
  glare: true,
  "max-glare": 0.3,
  scale: 1.05
});
```

---

### Pattern 2: Parallax Layers

Multiple layered elements with different tilt depths.

```html
<div class="parallax-container" data-tilt>
  <div class="layer layer-1">Background</div>
  <div class="layer layer-2">Midground</div>
  <div class="layer layer-3">Foreground</div>
</div>
```

```css
.parallax-container {
  position: relative;
  width: 400px;
  height: 400px;
  transform-style: preserve-3d;
}

.layer {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.layer-1 {
  background: #667eea;
  transform: translateZ(-50px);
}

.layer-2 {
  background: #764ba2;
  opacity: 0.8;
  transform: translateZ(0px);
}

.layer-3 {
  background: #f093fb;
  opacity: 0.6;
  transform: translateZ(50px);
}
```

```javascript
VanillaTilt.init(document.querySelector(".parallax-container"), {
  max: 25,
  speed: 400,
  perspective: 1000
});
```

---

### Pattern 3: Hover Reveal

Reveal content on tilt hover.

```html
<div class="reveal-card" data-tilt>
  <div class="card-front">
    <h2>Hover Me</h2>
  </div>
  <div class="card-back">
    <p>Hidden content revealed!</p>
  </div>
</div>
```

```css
.reveal-card {
  width: 300px;
  height: 400px;
  position: relative;
  transform-style: preserve-3d;
}

.card-front,
.card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-front {
  background: #667eea;
  transform: translateZ(20px);
}

.card-back {
  background: #764ba2;
  transform: translateZ(-20px) rotateY(180deg);
  opacity: 0;
  transition: opacity 0.3s;
}

.reveal-card:hover .card-back {
  opacity: 1;
}
```

```javascript
VanillaTilt.init(document.querySelector(".reveal-card"), {
  max: 25,
  speed: 400,
  glare: true
});
```

---

### Pattern 4: 3D Button

Elevated button with shadow that follows tilt.

```html
<button class="tilt-button" data-tilt>
  <span>Click Me</span>
</button>
```

```css
.tilt-button {
  padding: 1.5rem 3rem;
  font-size: 1.2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transform-style: preserve-3d;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  transition: box-shadow 0.3s;
}

.tilt-button span {
  display: block;
  transform: translateZ(20px);
}

.tilt-button:hover {
  box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}
```

```javascript
VanillaTilt.init(document.querySelector(".tilt-button"), {
  max: 20,
  speed: 300,
  scale: 1.1,
  glare: true,
  "max-glare": 0.5
});
```

---

### Pattern 5: Product Showcase

E-commerce product card with layered depth.

```html
<div class="product-card" data-tilt>
  <div class="product-badge">NEW</div>
  <img src="product.jpg" alt="Product" class="product-image">
  <div class="product-info">
    <h3 class="product-title">Product Name</h3>
    <p class="product-price">$99.99</p>
    <button class="product-button">Add to Cart</button>
  </div>
</div>
```

```css
.product-card {
  width: 320px;
  background: white;
  border-radius: 15px;
  overflow: hidden;
  transform-style: preserve-3d;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.product-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #ff6b6b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  transform: translateZ(60px);
  z-index: 10;
}

.product-image {
  width: 100%;
  display: block;
  transform: translateZ(30px);
}

.product-info {
  padding: 1.5rem;
  transform: translateZ(40px);
}

.product-button {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transform: translateZ(50px);
}
```

```javascript
VanillaTilt.init(document.querySelector(".product-card"), {
  max: 15,
  speed: 400,
  glare: true,
  "max-glare": 0.2,
  scale: 1.03
});
```

---

## Advanced Techniques

### Dynamic Tilt Values

Update tilt based on external data.

```javascript
const element = document.querySelector(".tilt-card");
VanillaTilt.init(element);

element.addEventListener("tiltChange", (e) => {
  const { tiltX, tiltY, angle } = e.detail;

  // Update background color based on tilt
  const hue = Math.abs(tiltX * 10);
  element.style.background = `hsl(${hue}, 70%, 50%)`;

  // Update text based on angle
  element.querySelector(".angle-display").textContent =
    `Angle: ${angle.toFixed(1)}°`;
});
```

---

### Conditional Tilt

Enable tilt based on conditions.

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (!isMobile) {
  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 25,
    speed: 400
  });
} else {
  // Enable gyroscope on mobile
  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 15,
    speed: 600,
    gyroscope: true
  });
}
```

---

### Sync Multiple Elements

Tilt multiple elements together.

```javascript
const cards = document.querySelectorAll(".sync-card");

// Initialize all cards
VanillaTilt.init(cards, {
  max: 20,
  speed: 400
});

// Sync tilt values
cards[0].addEventListener("tiltChange", (e) => {
  const { tiltX, tiltY } = e.detail;

  // Apply same tilt to other cards
  cards.forEach((card, index) => {
    if (index > 0) {
      card.style.transform =
        `perspective(1000px) rotateY(${tiltX}deg) rotateX(${-tiltY}deg)`;
    }
  });
});
```

---

### Tilt with Scroll

Combine tilt with scroll position.

```javascript
const element = document.querySelector(".tilt-card");
VanillaTilt.init(element);

window.addEventListener("scroll", () => {
  const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  const rotation = scrollPercent * 360;

  element.style.transform += ` rotate(${rotation}deg)`;
});
```

---

### Custom Glare Colors

Change glare color dynamically.

```javascript
VanillaTilt.init(element, {
  glare: true,
  "max-glare": 0.5
});

element.addEventListener("tiltChange", (e) => {
  const glareEl = element.querySelector(".js-tilt-glare-inner");
  const { percentageX } = e.detail;

  // Color shifts from blue to purple
  const hue = 200 + (percentageX * 0.8);
  glareEl.style.background =
    `linear-gradient(0deg, transparent, hsl(${hue}, 70%, 50%))`;
});
```

---

## Framework Integration

### React

```jsx
import React, { useEffect, useRef } from 'react';
import VanillaTilt from 'vanilla-tilt';

function TiltCard({ children, options }) {
  const tiltRef = useRef(null);

  useEffect(() => {
    VanillaTilt.init(tiltRef.current, options);

    return () => {
      tiltRef.current.vanillaTilt.destroy();
    };
  }, [options]);

  return (
    <div ref={tiltRef} className="tilt-card">
      {children}
    </div>
  );
}

// Usage
<TiltCard options={{ max: 25, speed: 400, glare: true }}>
  <h2>Card Content</h2>
</TiltCard>
```

---

### Vue 3

```vue
<template>
  <div ref="tiltRef" class="tilt-card">
    <slot></slot>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import VanillaTilt from 'vanilla-tilt';

const props = defineProps({
  options: {
    type: Object,
    default: () => ({ max: 25, speed: 400 })
  }
});

const tiltRef = ref(null);

onMounted(() => {
  VanillaTilt.init(tiltRef.value, props.options);
});

onUnmounted(() => {
  tiltRef.value.vanillaTilt.destroy();
});
</script>
```

---

### Angular

```typescript
import { Component, ElementRef, Input, OnInit, OnDestroy } from '@angular/core';
import VanillaTilt from 'vanilla-tilt';

@Component({
  selector: 'app-tilt-card',
  template: `
    <div class="tilt-card">
      <ng-content></ng-content>
    </div>
  `
})
export class TiltCardComponent implements OnInit, OnDestroy {
  @Input() options: any = { max: 25, speed: 400 };

  constructor(private el: ElementRef) {}

  ngOnInit() {
    VanillaTilt.init(this.el.nativeElement.querySelector('.tilt-card'), this.options);
  }

  ngOnDestroy() {
    this.el.nativeElement.querySelector('.tilt-card').vanillaTilt.destroy();
  }
}
```

---

### Svelte

```svelte
<script>
  import { onMount, onDestroy } from 'svelte';
  import VanillaTilt from 'vanilla-tilt';

  export let options = { max: 25, speed: 400 };

  let tiltRef;

  onMount(() => {
    VanillaTilt.init(tiltRef, options);
  });

  onDestroy(() => {
    if (tiltRef && tiltRef.vanillaTilt) {
      tiltRef.vanillaTilt.destroy();
    }
  });
</script>

<div bind:this={tiltRef} class="tilt-card">
  <slot></slot>
</div>
```

---

## Performance

### Optimization Tips

**1. Disable on mobile for better performance**

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (!isMobile) {
  VanillaTilt.init(document.querySelectorAll(".tilt-card"));
}
```

**2. Use transform: translateZ for GPU acceleration**

```css
.tilt-card {
  transform: translateZ(0);  /* Force GPU layer */
}
```

**3. Limit tilt to visible elements**

```javascript
let observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      VanillaTilt.init(entry.target);
    } else {
      if (entry.target.vanillaTilt) {
        entry.target.vanillaTilt.destroy();
      }
    }
  });
});

document.querySelectorAll('.tilt-card').forEach(el => {
  observer.observe(el);
});
```

**4. Reduce max angle for subtle effects**

```javascript
// Less intensive
VanillaTilt.init(element, { max: 10 });

// More intensive
VanillaTilt.init(element, { max: 50 });
```

**5. Disable glare on low-end devices**

```javascript
const hasGoodGPU = navigator.hardwareConcurrency > 4;

VanillaTilt.init(element, {
  max: 25,
  glare: hasGoodGPU,
  "max-glare": hasGoodGPU ? 0.5 : 0
});
```

---

## Troubleshooting

### Tilt Not Working

**Check**:
1. Element exists when initializing
2. Element has dimensions (width/height > 0)
3. No CSS conflicts with `transform`

```javascript
// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
  VanillaTilt.init(document.querySelector(".tilt-card"));
});
```

---

### Glare Not Showing

**Solution**: Ensure element has `overflow: hidden` or `border-radius`.

```css
.tilt-card {
  overflow: hidden;  /* Required for glare */
  border-radius: 10px;
}
```

---

### Memory Leaks in SPAs

**Solution**: Always destroy on unmount.

```javascript
// Store reference
const element = document.querySelector(".tilt-card");
VanillaTilt.init(element);

// Before removing element
element.vanillaTilt.destroy();
```

---

## Resources

- **GitHub**: https://github.com/micku7zu/vanilla-tilt.js
- **NPM**: `npm install vanilla-tilt`
- **Examples**: https://micku7zu.github.io/vanilla-tilt.js/

---

## License

MIT License - Free for commercial and personal use.
