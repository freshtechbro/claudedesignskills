---
name: lightweight-3d-effects
description: Lightweight 3D effects for decorative elements and micro-interactions using Zdog, Vanta.js, and Vanilla-Tilt.js. Use this skill when adding pseudo-3D illustrations, animated backgrounds, parallax tilt effects, decorative 3D elements, or subtle depth effects without heavy frameworks. Triggers on tasks involving Zdog pseudo-3D, Vanta.js backgrounds, Vanilla-Tilt parallax, card tilt effects, hero section animations, or lightweight landing page visuals. Ideal for performance-focused designs.
---

# Lightweight 3D Effects Skill

## Overview

This skill combines three powerful libraries for decorative 3D elements and micro-interactions:
- **Zdog**: Pseudo-3D engine for designer-friendly vector illustrations
- **Vanta.js**: Animated 3D backgrounds powered by Three.js/p5.js
- **Vanilla-Tilt.js**: Smooth parallax tilt effects responding to mouse/gyroscope

## When to Use This Skill
- Add decorative 3D illustrations without heavy frameworks
- Create animated backgrounds for hero sections
- Implement subtle parallax tilt effects on cards/images
- Build lightweight landing pages with visual depth
- Add micro-interactions that enhance UX without performance impact

## Zdog - Pseudo-3D Illustrations

### Core Concepts

Zdog is a pseudo-3D engine that renders flat, round designs in 3D space using Canvas or SVG.

**Key Features:**
- Designer-friendly declarative API
- Small file size (~28kb minified)
- Canvas or SVG rendering
- Drag rotation built-in
- Smooth animations

### Basic Setup

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/zdog@1/dist/zdog.dist.min.js"></script>
  <style>
    .zdog-canvas {
      display: block;
      margin: 0 auto;
      background: #FDB;
      cursor: move;
    }
  </style>
</head>
<body>
  <canvas class="zdog-canvas" width="240" height="240"></canvas>

  <script>
    let isSpinning = true;

    let illo = new Zdog.Illustration({
      element: '.zdog-canvas',
      zoom: 4,
      dragRotate: true,
      onDragStart: function() {
        isSpinning = false;
      },
    });

    // Add shapes
    new Zdog.Ellipse({
      addTo: illo,
      diameter: 20,
      translate: { z: 10 },
      stroke: 5,
      color: '#636',
    });

    new Zdog.Rect({
      addTo: illo,
      width: 20,
      height: 20,
      translate: { z: -10 },
      stroke: 3,
      color: '#E62',
      fill: true,
    });

    function animate() {
      illo.rotate.y += isSpinning ? 0.03 : 0;
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }
    animate();
  </script>
</body>
</html>
```

### Zdog Shapes

**Basic Shapes:**

```javascript
// Circle
new Zdog.Ellipse({
  addTo: illo,
  diameter: 80,
  stroke: 20,
  color: '#636',
});

// Rectangle
new Zdog.Rect({
  addTo: illo,
  width: 80,
  height: 60,
  stroke: 10,
  color: '#E62',
  fill: true,
});

// Rounded Rectangle
new Zdog.RoundedRect({
  addTo: illo,
  width: 60,
  height: 40,
  cornerRadius: 10,
  stroke: 4,
  color: '#C25',
  fill: true,
});

// Polygon
new Zdog.Polygon({
  addTo: illo,
  radius: 40,
  sides: 5,
  stroke: 8,
  color: '#EA0',
  fill: true,
});

// Line
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -40, y: 0 },
    { x: 40, y: 0 },
  ],
  stroke: 6,
  color: '#636',
});

// Bezier Curve
new Zdog.Shape({
  addTo: illo,
  path: [
    { x: -40, y: -20 },
    {
      bezier: [
        { x: -40, y: 20 },
        { x: 40, y: 20 },
        { x: 40, y: -20 },
      ],
    },
  ],
  stroke: 4,
  color: '#C25',
  closed: false,
});
```

### Zdog Groups

Organize shapes into groups for complex models:

```javascript
// Create a group
let head = new Zdog.Group({
  addTo: illo,
  translate: { y: -40 },
});

// Add shapes to group
new Zdog.Ellipse({
  addTo: head,
  diameter: 60,
  stroke: 30,
  color: '#FED',
});

// Eyes
new Zdog.Ellipse({
  addTo: head,
  diameter: 8,
  stroke: 4,
  color: '#333',
  translate: { x: -10, z: 15 },
});

new Zdog.Ellipse({
  addTo: head,
  diameter: 8,
  stroke: 4,
  color: '#333',
  translate: { x: 10, z: 15 },
});

// Mouth
new Zdog.Shape({
  addTo: head,
  path: [
    { x: -10, y: 0 },
    {
      bezier: [
        { x: -5, y: 5 },
        { x: 5, y: 5 },
        { x: 10, y: 0 },
      ],
    },
  ],
  stroke: 2,
  color: '#333',
  translate: { y: 5, z: 15 },
  closed: false,
});

// Rotate entire group
head.rotate.y = Math.PI / 4;
```

### Zdog Animation

```javascript
// Continuous rotation
function animate() {
  illo.rotate.y += 0.03;
  illo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();

// Bounce animation
let t = 0;
function bounceAnimate() {
  t += 0.05;
  illo.translate.y = Math.sin(t) * 20;
  illo.updateRenderGraph();
  requestAnimationFrame(bounceAnimate);
}
bounceAnimate();

// Interactive rotation with easing
let targetRotateY = 0;
let currentRotateY = 0;

document.addEventListener('mousemove', (event) => {
  targetRotateY = (event.clientX / window.innerWidth - 0.5) * Math.PI;
});

function smoothAnimate() {
  // Ease towards target
  currentRotateY += (targetRotateY - currentRotateY) * 0.1;
  illo.rotate.y = currentRotateY;
  illo.updateRenderGraph();
  requestAnimationFrame(smoothAnimate);
}
smoothAnimate();
```

---

## Vanta.js - Animated 3D Backgrounds

### Core Concepts

Vanta.js provides animated WebGL backgrounds with minimal setup, powered by Three.js or p5.js.

**Key Features:**
- 14+ animated effects (Waves, Birds, Net, Clouds, etc.)
- Mouse/touch interaction
- Customizable colors and settings
- ~120KB total (including Three.js)
- 60fps on most devices

### Basic Setup

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    #vanta-bg {
      width: 100%;
      height: 100vh;
    }
    .content {
      position: relative;
      z-index: 1;
      color: white;
      text-align: center;
      padding: 100px 20px;
    }
  </style>
</head>
<body>
  <div id="vanta-bg">
    <div class="content">
      <h1>My Animated Background</h1>
      <p>Content goes here</p>
    </div>
  </div>

  <!-- Three.js (required) -->
  <script src="https://cdn.jsdelivr.net/npm/three@0.134.0/build/three.min.js"></script>

  <!-- Vanta.js effect -->
  <script src="https://cdn.jsdelivr.net/npm/vanta@0.5.24/dist/vanta.waves.min.js"></script>

  <script>
    VANTA.WAVES({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0x23153c,
      shininess: 30.00,
      waveHeight: 15.00,
      waveSpeed: 0.75,
      zoom: 0.65
    });
  </script>
</body>
</html>
```

### Available Effects

**1. WAVES** (Three.js)
```javascript
VANTA.WAVES({
  el: "#vanta-bg",
  color: 0x23153c,
  shininess: 30,
  waveHeight: 15,
  waveSpeed: 0.75,
  zoom: 0.65
});
```

**2. CLOUDS** (Three.js)
```javascript
VANTA.CLOUDS({
  el: "#vanta-bg",
  skyColor: 0x68b8d7,
  cloudColor: 0xadc1de,
  cloudShadowColor: 0x183550,
  sunColor: 0xff9919,
  sunGlareColor: 0xff6633,
  sunlightColor: 0xff9933,
  speed: 1.0
});
```

**3. BIRDS** (p5.js required)
```html
<script src="https://cdn.jsdelivr.net/npm/p5@1.4.0/lib/p5.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@0.5.24/dist/vanta.birds.min.js"></script>

<script>
  VANTA.BIRDS({
    el: "#vanta-bg",
    backgroundColor: 0x23153c,
    color1: 0xff0000,
    color2: 0x0000ff,
    birdSize: 1.5,
    wingSpan: 20,
    speedLimit: 5,
    separation: 40,
    alignment: 40,
    cohesion: 40,
    quantity: 3
  });
</script>
```

**4. NET** (Three.js)
```javascript
VANTA.NET({
  el: "#vanta-bg",
  color: 0x3fff00,
  backgroundColor: 0x23153c,
  points: 10,
  maxDistance: 20,
  spacing: 15,
  showDots: true
});
```

**5. CELLS** (p5.js required)
```javascript
VANTA.CELLS({
  el: "#vanta-bg",
  color1: 0x00ff00,
  color2: 0xff0000,
  size: 1.5,
  speed: 1.0,
  scale: 1.0
});
```

**6. FOG** (Three.js)
```javascript
VANTA.FOG({
  el: "#vanta-bg",
  highlightColor: 0xff3f81,
  midtoneColor: 0x1d004d,
  lowlightColor: 0x2b1a5e,
  baseColor: 0x000000,
  blurFactor: 0.6,
  speed: 1.0,
  zoom: 1.0
});
```

**Other effects:** GLOBE, TRUNK, TOPOLOGY, DOTS, HALO, RINGS

### Configuration Options

```javascript
// Common options for all effects
{
  el: "#element-id",              // Required: target element
  mouseControls: true,             // Enable mouse interaction
  touchControls: true,             // Enable touch interaction
  gyroControls: false,             // Device orientation
  minHeight: 200.00,               // Minimum height
  minWidth: 200.00,                // Minimum width
  scale: 1.00,                     // Size scale
  scaleMobile: 1.00,               // Mobile scale

  // Colors (hex numbers, not strings)
  color: 0x23153c,
  backgroundColor: 0x000000,

  // Performance
  forceAnimate: false,             // Force animation even when hidden

  // Effect-specific options vary by effect
}
```

### Vanta.js Methods

```javascript
// Initialize and store reference
const vantaEffect = VANTA.WAVES({
  el: "#vanta-bg",
  // ... options
});

// Destroy when done (important for SPAs)
vantaEffect.destroy();

// Update options dynamically
vantaEffect.setOptions({
  color: 0xff0000,
  waveHeight: 20
});

// Resize (usually automatic)
vantaEffect.resize();
```

### React Integration

```jsx
import { useEffect, useRef, useState } from 'react';
import VANTA from 'vanta/dist/vanta.waves.min';
import * as THREE from 'three';

function VantaBackground() {
  const vantaRef = useRef(null);
  const [vantaEffect, setVantaEffect] = useState(null);

  useEffect(() => {
    if (!vantaEffect) {
      setVantaEffect(VANTA.WAVES({
        el: vantaRef.current,
        THREE: THREE,
        mouseControls: true,
        touchControls: true,
        color: 0x23153c,
        shininess: 30,
        waveHeight: 15,
        waveSpeed: 0.75
      }));
    }

    return () => {
      if (vantaEffect) vantaEffect.destroy();
    };
  }, [vantaEffect]);

  return (
    <div ref={vantaRef} style={{ width: '100%', height: '100vh' }}>
      <div className="content">
        <h1>React + Vanta.js</h1>
      </div>
    </div>
  );
}
```

---

## Vanilla-Tilt.js - Parallax Tilt Effects

### Core Concepts

Vanilla-Tilt.js adds smooth 3D tilt effects responding to mouse movement and device orientation.

**Key Features:**
- Lightweight (~8.5kb minified)
- No dependencies
- Gyroscope support
- Optional glare effect
- Smooth transitions

### Basic Setup

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .tilt-card {
      width: 300px;
      height: 400px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 15px;
      margin: 50px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 24px;
      transform-style: preserve-3d;
    }

    .tilt-inner {
      transform: translateZ(60px);
    }
  </style>
</head>
<body>
  <div class="tilt-card" data-tilt>
    <div class="tilt-inner">Hover Me!</div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js"></script>
</body>
</html>
```

### Configuration Options

```javascript
VanillaTilt.init(document.querySelector(".tilt-card"), {
  // Rotation
  max: 25,                    // Max tilt angle (degrees)
  reverse: false,             // Reverse tilt direction
  startX: 0,                  // Initial tilt X (degrees)
  startY: 0,                  // Initial tilt Y (degrees)

  // Appearance
  perspective: 1000,          // Transform perspective (lower = more intense)
  scale: 1.1,                 // Scale on hover (1 = no scale)

  // Animation
  speed: 400,                 // Transition speed (ms)
  transition: true,           // Enable smooth transitions
  easing: "cubic-bezier(.03,.98,.52,.99)",

  // Behavior
  axis: null,                 // Restrict to "x" or "y" axis
  reset: true,                // Reset on mouse leave
  "reset-to-start": true,     // Reset to start position vs [0,0]

  // Glare effect
  glare: true,                // Enable glare
  "max-glare": 0.5,          // Glare opacity (0-1)
  "glare-prerender": false,   // Pre-render glare elements

  // Advanced
  full-page-listening: false, // Listen to entire page
  gyroscope: true,            // Enable device orientation
  gyroscopeMinAngleX: -45,    // Min X angle
  gyroscopeMaxAngleX: 45,     // Max X angle
  gyroscopeMinAngleY: -45,    // Min Y angle
  gyroscopeMaxAngleY: 45,     // Max Y angle
  gyroscopeSamples: 10        // Calibration samples
});
```

### Advanced Examples

**Card with Glare Effect:**

```html
<div class="tilt-card" data-tilt
     data-tilt-glare
     data-tilt-max-glare="0.5"
     data-tilt-scale="1.1">
  <div class="tilt-inner">
    <h3>Premium Card</h3>
    <p>With glare effect</p>
  </div>
</div>
```

**Layered 3D Effect:**

```html
<style>
  .tilt-card {
    transform-style: preserve-3d;
  }
  .layer-1 {
    transform: translateZ(20px);
  }
  .layer-2 {
    transform: translateZ(40px);
  }
  .layer-3 {
    transform: translateZ(60px);
  }
</style>

<div class="tilt-card" data-tilt data-tilt-max="15">
  <div class="layer-1">Background</div>
  <div class="layer-2">Middle</div>
  <div class="layer-3">Front</div>
</div>
```

**Programmatic Control:**

```javascript
const element = document.querySelector(".tilt-card");

VanillaTilt.init(element, {
  max: 25,
  speed: 400,
  glare: true,
  "max-glare": 0.5
});

// Get tilt values
element.addEventListener("tiltChange", (e) => {
  console.log("Tilt:", e.detail);
});

// Reset programmatically
element.vanillaTilt.reset();

// Destroy instance
element.vanillaTilt.destroy();

// Get current values
const values = element.vanillaTilt.getValues();
console.log(values); // { tiltX, tiltY, percentageX, percentageY, angle }
```

### React Integration

```jsx
import { useEffect, useRef } from 'react';
import VanillaTilt from 'vanilla-tilt';

function TiltCard({ children, options }) {
  const tiltRef = useRef(null);

  useEffect(() => {
    const element = tiltRef.current;

    VanillaTilt.init(element, {
      max: 25,
      speed: 400,
      glare: true,
      "max-glare": 0.5,
      ...options
    });

    return () => {
      element.vanillaTilt.destroy();
    };
  }, [options]);

  return (
    <div ref={tiltRef} className="tilt-card">
      {children}
    </div>
  );
}

// Usage
<TiltCard options={{ max: 30, scale: 1.1 }}>
  <h3>My Card</h3>
</TiltCard>
```

---

## Common Patterns

### Pattern 1: Hero Section with Vanta + Content

```html
<section id="hero">
  <div class="hero-content">
    <h1>Welcome</h1>
    <p>Animated background with content overlay</p>
    <button>Get Started</button>
  </div>
</section>

<style>
  #hero {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
  }

  .hero-content {
    position: relative;
    z-index: 1;
    color: white;
    text-align: center;
    padding-top: 20vh;
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/three@0.134.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@0.5.24/dist/vanta.waves.min.js"></script>

<script>
  VANTA.WAVES({
    el: "#hero",
    mouseControls: true,
    touchControls: true,
    color: 0x23153c,
    waveHeight: 20,
    waveSpeed: 1.0
  });
</script>
```

### Pattern 2: Zdog Icon Grid

```html
<div class="icon-grid">
  <canvas class="icon" width="120" height="120"></canvas>
  <canvas class="icon" width="120" height="120"></canvas>
  <canvas class="icon" width="120" height="120"></canvas>
</div>

<script src="https://unpkg.com/zdog@1/dist/zdog.dist.min.js"></script>

<script>
  document.querySelectorAll('.icon').forEach((canvas, index) => {
    let illo = new Zdog.Illustration({
      element: canvas,
      zoom: 3,
      dragRotate: true
    });

    // Create different icon for each canvas
    const icons = [
      createHeartIcon,
      createStarIcon,
      createCheckIcon
    ];

    icons[index](illo);

    function animate() {
      illo.rotate.y += 0.02;
      illo.updateRenderGraph();
      requestAnimationFrame(animate);
    }
    animate();
  });

  function createHeartIcon(illo) {
    new Zdog.Shape({
      addTo: illo,
      path: [
        { x: 0, y: -10 },
        {
          bezier: [
            { x: -20, y: -20 },
            { x: -20, y: 0 },
            { x: 0, y: 10 }
          ]
        },
        {
          bezier: [
            { x: 20, y: 0 },
            { x: 20, y: -20 },
            { x: 0, y: -10 }
          ]
        }
      ],
      stroke: 6,
      color: '#E62',
      fill: true,
      closed: false
    });
  }
</script>
```

### Pattern 3: Tilt Card Gallery

```html
<div class="card-gallery">
  <div class="card" data-tilt data-tilt-glare data-tilt-max-glare="0.3">
    <img src="product1.jpg" alt="Product 1">
    <h3>Product 1</h3>
  </div>

  <div class="card" data-tilt data-tilt-glare data-tilt-max-glare="0.3">
    <img src="product2.jpg" alt="Product 2">
    <h3>Product 2</h3>
  </div>

  <div class="card" data-tilt data-tilt-glare data-tilt-max-glare="0.3">
    <img src="product3.jpg" alt="Product 3">
    <h3>Product 3</h3>
  </div>
</div>

<style>
  .card-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    padding: 50px;
  }

  .card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transform-style: preserve-3d;
  }

  .card img {
    width: 100%;
    border-radius: 10px;
    transform: translateZ(40px);
  }

  .card h3 {
    margin-top: 15px;
    transform: translateZ(60px);
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js"></script>
```

### Pattern 4: Combined Effect - Vanta Background + Tilt Cards

```html
<div id="vanta-section">
  <div class="container">
    <h1>Our Services</h1>

    <div class="services-grid">
      <div class="service-card" data-tilt data-tilt-scale="1.05">
        <div class="icon">🚀</div>
        <h3>Fast</h3>
        <p>Lightning quick performance</p>
      </div>

      <div class="service-card" data-tilt data-tilt-scale="1.05">
        <div class="icon">🎨</div>
        <h3>Beautiful</h3>
        <p>Stunning visual design</p>
      </div>

      <div class="service-card" data-tilt data-tilt-scale="1.05">
        <div class="icon">💪</div>
        <h3>Powerful</h3>
        <p>Feature-rich platform</p>
      </div>
    </div>
  </div>
</div>

<script>
  // Vanta background
  VANTA.NET({
    el: "#vanta-section",
    color: 0x3fff00,
    backgroundColor: 0x23153c,
    points: 10,
    maxDistance: 20
  });

  // Tilt cards
  VanillaTilt.init(document.querySelectorAll(".service-card"), {
    max: 15,
    speed: 400,
    glare: true,
    "max-glare": 0.3
  });
</script>
```

---

## Performance Best Practices

### Zdog Optimization

1. **Limit Shape Count**: Keep total shapes under 100 for smooth 60fps
2. **Use Groups**: Organize related shapes for easier management
3. **Optimize Animation Loop**: Only call `updateRenderGraph()` when needed
4. **Canvas vs SVG**: Canvas is faster for animations, SVG for static illustrations

### Vanta.js Optimization

1. **Single Instance**: Use only 1-2 Vanta effects per page
2. **Mobile Fallback**: Disable on mobile or use static background
3. **Destroy on Unmount**: Always call `.destroy()` in SPAs
4. **Reduce Particle Count**: Lower `points`, `quantity` for better performance

```javascript
// Mobile detection and fallback
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (!isMobile) {
  VANTA.WAVES({
    el: "#hero",
    // ... options
  });
} else {
  document.getElementById('hero').style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
}
```

### Vanilla-Tilt Optimization

1. **Limit Instances**: Apply to visible elements only
2. **Reduce `gyroscopeSamples`**: Lower for better mobile performance
3. **Disable on Low-End Devices**: Check device capabilities
4. **Use CSS `will-change`**: Hint browser for transforms

```css
.tilt-card {
  will-change: transform;
}
```

---

## Common Pitfalls

### Pitfall 1: Multiple Vanta Instances

**Problem**: Multiple Vanta effects cause performance issues

**Solution**: Use only one effect, or lazy-load effects per section

```javascript
// Intersection Observer to load Vanta only when visible
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !entry.target.vantaEffect) {
      entry.target.vantaEffect = VANTA.WAVES({
        el: entry.target,
        // ... options
      });
    }
  });
});

observer.observe(document.getElementById('hero'));
```

### Pitfall 2: Memory Leaks in SPAs

**Problem**: Vanta/Tilt not destroyed on component unmount

**Solution**: Always clean up

```javascript
// React useEffect cleanup
useEffect(() => {
  const effect = VANTA.WAVES({ el: vantaRef.current });

  return () => {
    effect.destroy(); // Important!
  };
}, []);
```

### Pitfall 3: Zdog Not Rendering

**Problem**: Canvas appears blank

**Causes**:
- Forgot to call `updateRenderGraph()`
- Canvas size is 0
- Shapes are outside view

**Solution**:

```javascript
// Always call updateRenderGraph after shape changes
illo.updateRenderGraph();

// Ensure canvas has dimensions
<canvas width="240" height="240"></canvas>

// Check shape positions are visible
new Zdog.Ellipse({
  addTo: illo,
  diameter: 20,
  translate: { z: 0 }, // Keep close to origin
});
```

### Pitfall 4: Tilt Not Working on Mobile

**Problem**: Tilt doesn't respond on mobile devices

**Solution**: Enable gyroscope controls

```javascript
VanillaTilt.init(element, {
  gyroscope: true,
  gyroscopeMinAngleX: -45,
  gyroscopeMaxAngleX: 45
});
```

### Pitfall 5: Color Format Confusion (Vanta.js)

**Problem**: Colors don't work

**Cause**: Vanta.js uses hex **numbers**, not strings

```javascript
// ❌ Wrong
color: "#23153c"

// ✅ Correct
color: 0x23153c
```

---

## Resources

**Zdog:**
- [Zdog Documentation](https://zzz.dog/)
- [Zdog GitHub](https://github.com/metafizzy/zdog)
- [Zdog Codepen Examples](https://codepen.io/collection/DzdGMe/)

**Vanta.js:**
- [Vanta.js Official Site](https://www.vantajs.com/)
- [Vanta.js GitHub](https://github.com/tengbao/vanta)
- [Effect Customizer](https://www.vantajs.com/?effect=waves)

**Vanilla-Tilt.js:**
- [Vanilla-Tilt GitHub](https://github.com/micku7zu/vanilla-tilt.js)
- [NPM Package](https://www.npmjs.com/package/vanilla-tilt)

## Related Skills

- **threejs-webgl**: For more complex 3D graphics beyond decorative effects
- **gsap-scrolltrigger**: For animating these effects on scroll
- **motion-framer**: For React component animations alongside these effects
- **react-three-fiber**: Advanced 3D when lightweight effects aren't enough
