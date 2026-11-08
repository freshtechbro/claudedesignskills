# Lightweight 3D Effects - Production Examples

Real-world patterns and examples combining Vanta.js, Zdog, and Vanilla-Tilt for production applications.

---

## Table of Contents

1. [Hero Sections](#1-hero-sections)
2. [Product Cards](#2-product-cards)
3. [Portfolio Layouts](#3-portfolio-layouts)
4. [Interactive Dashboards](#4-interactive-dashboards)
5. [Marketing Pages](#5-marketing-pages)
6. [E-Commerce](#6-e-commerce)
7. [SaaS Landing Pages](#7-saas-landing-pages)
8. [Performance Patterns](#8-performance-patterns)

---

## 1. Hero Sections

### Example 1.1: Split Hero with Vanta + Zdog Logo

**Use Case**: SaaS landing page with animated background and brand icon

```html
<div class="hero-split">
  <div id="vanta-bg"></div>

  <div class="hero-content">
    <canvas class="logo-zdog" width="200" height="200"></canvas>
    <h1>Welcome to Your Product</h1>
    <p>Tagline describing your amazing service</p>
    <button class="cta-button tilt-btn" data-tilt>Get Started</button>
  </div>
</div>
```

```css
.hero-split {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

#vanta-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.hero-content {
  text-align: center;
  z-index: 1;
  color: white;
}

.logo-zdog {
  display: block;
  margin: 0 auto 2rem;
  filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
}

.cta-button {
  padding: 1rem 3rem;
  font-size: 1.2rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  border-radius: 50px;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transform-style: preserve-3d;
}
```

```javascript
// Vanta background
VANTA.NET({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  color: 0x3fafff,
  backgroundColor: 0x23153c,
  points: 10,
  maxDistance: 20
});

// Zdog logo
const logoIllo = new Zdog.Illustration({
  element: '.logo-zdog',
  zoom: 3,
  dragRotate: false
});

// Create your brand icon here
const logo = new Zdog.Shape({
  addTo: logoIllo,
  path: [
    { x: -30, y: -30 },
    { x: 30, y: -30 },
    { x: 0, y: 30 }
  ],
  closed: true,
  stroke: 8,
  color: '#fff',
  fill: true
});

function animate() {
  logo.rotate.y += 0.02;
  logoIllo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();

// Tilt button
VanillaTilt.init(document.querySelector(".cta-button"), {
  max: 15,
  glare: true,
  "max-glare": 0.5,
  scale: 1.1
});
```

---

### Example 1.2: Full-Screen Hero with Scroll Indicator

**Use Case**: Portfolio site with immersive background and scroll prompt

```html
<section class="hero-fullscreen">
  <div id="vanta-bg"></div>

  <div class="hero-content">
    <h1 class="hero-title">Creative Developer</h1>
    <p class="hero-subtitle">Building beautiful experiences</p>

    <div class="scroll-indicator">
      <canvas class="scroll-zdog" width="60" height="80"></canvas>
      <span>Scroll to explore</span>
    </div>
  </div>
</section>
```

```javascript
// Vanta clouds
VANTA.CLOUDS({
  el: "#vanta-bg",
  skyColor: 0x68b8d7,
  cloudColor: 0xadc1de,
  speed: 0.5
});

// Animated scroll indicator
const scrollIllo = new Zdog.Illustration({
  element: '.scroll-zdog',
  zoom: 2
});

// Mouse with scrolling animation
const mouse = new Zdog.RoundedRect({
  addTo: scrollIllo,
  width: 20,
  height: 30,
  cornerRadius: 10,
  stroke: 2,
  color: '#fff'
});

const wheel = new Zdog.Ellipse({
  addTo: scrollIllo,
  diameter: 4,
  translate: { y: -8 },
  stroke: 2,
  color: '#fff',
  fill: true
});

let wheelY = -8;
function animate() {
  wheelY += 0.5;
  if (wheelY > 8) wheelY = -8;
  wheel.translate.y = wheelY;

  scrollIllo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();
```

---

## 2. Product Cards

### Example 2.1: Pricing Cards with Tilt + Zdog Icons

**Use Case**: SaaS pricing page with interactive plan cards

```html
<div class="pricing-grid">
  <div class="pricing-card tilt-card" data-tilt>
    <canvas class="plan-icon" width="100" height="100"></canvas>
    <h3>Starter</h3>
    <p class="price">$9<span>/mo</span></p>
    <ul>
      <li>Feature 1</li>
      <li>Feature 2</li>
      <li>Feature 3</li>
    </ul>
    <button class="select-btn">Select Plan</button>
  </div>

  <!-- Repeat for Pro and Enterprise -->
</div>
```

```javascript
// Initialize tilt for all cards
VanillaTilt.init(document.querySelectorAll(".pricing-card"), {
  max: 10,
  speed: 400,
  glare: true,
  "max-glare": 0.2,
  scale: 1.02
});

// Create unique Zdog icon for each plan
const starterIcon = new Zdog.Illustration({
  element: document.querySelectorAll('.plan-icon')[0],
  zoom: 2
});

new Zdog.Ellipse({
  addTo: starterIcon,
  diameter: 30,
  stroke: 5,
  color: '#4CAF50',
  fill: true
});

// Animate
function animate() {
  starterIcon.rotate.y += 0.02;
  starterIcon.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();
```

```css
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
}

.pricing-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  transform-style: preserve-3d;
}

.plan-icon {
  display: block;
  margin: 0 auto 1.5rem;
  transform: translateZ(30px);
}

.price {
  font-size: 3rem;
  font-weight: 700;
  transform: translateZ(20px);
}

.select-btn {
  transform: translateZ(40px);
  /* Additional button styles */
}
```

---

### Example 2.2: Product Showcase Gallery

**Use Case**: E-commerce product grid with hover effects

```html
<div class="product-gallery">
  <div class="product-card tilt-card" data-tilt>
    <div class="product-badge">NEW</div>
    <img src="product1.jpg" alt="Product" class="product-image">
    <canvas class="product-icon" width="80" height="80"></canvas>
    <h3>Product Name</h3>
    <p class="product-price">$99.99</p>
    <button class="add-to-cart">Add to Cart</button>
  </div>
</div>
```

```javascript
VanillaTilt.init(document.querySelectorAll(".product-card"), {
  max: 12,
  speed: 400,
  glare: true,
  "max-glare": 0.3,
  scale: 1.05
});

// Add floating Zdog indicator on each card
document.querySelectorAll('.product-icon').forEach((canvas, i) => {
  const illo = new Zdog.Illustration({
    element: canvas,
    zoom: 1.5
  });

  // Star rating indicator
  for (let j = 0; j < 5; j++) {
    new Zdog.Polygon({
      addTo: illo,
      sides: 5,
      radius: 6,
      translate: { x: (j - 2) * 14 },
      stroke: 2,
      color: '#FFD700',
      fill: true
    });
  }

  function animate() {
    illo.rotate.z = Math.sin(Date.now() * 0.001 + i) * 0.1;
    illo.updateRenderGraph();
    requestAnimationFrame(animate);
  }
  animate();
});
```

---

## 3. Portfolio Layouts

### Example 3.1: Project Grid with Vanta Backgrounds

**Use Case**: Portfolio with per-project animated backgrounds

```html
<div class="portfolio-grid">
  <div class="project-card">
    <div class="project-vanta" data-effect="waves"></div>
    <div class="project-content tilt-content" data-tilt>
      <canvas class="project-icon" width="80" height="80"></canvas>
      <h3>Project Title</h3>
      <p>Project description</p>
      <a href="#" class="view-project">View Project →</a>
    </div>
  </div>
</div>
```

```javascript
// Initialize Vanta for each project card
document.querySelectorAll('.project-card').forEach((card, index) => {
  const vantaEl = card.querySelector('.project-vanta');
  const effect = vantaEl.dataset.effect;

  const effects = {
    waves: () => VANTA.WAVES({
      el: vantaEl,
      color: 0x23153c,
      waveHeight: 10,
      zoom: 0.75
    }),
    cells: () => VANTA.CELLS({
      el: vantaEl,
      color1: 0x18b0c6,
      size: 1.5
    }),
    net: () => VANTA.NET({
      el: vantaEl,
      color: 0x3fafff,
      points: 8
    })
  };

  effects[effect]();

  // Tilt only the content overlay
  VanillaTilt.init(card.querySelector('.project-content'), {
    max: 8,
    scale: 1.02,
    glare: true,
    "max-glare": 0.2
  });
});
```

```css
.project-card {
  position: relative;
  height: 400px;
  border-radius: 20px;
  overflow: hidden;
}

.project-vanta {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.project-content {
  position: relative;
  z-index: 2;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  padding: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transform-style: preserve-3d;
}

.project-icon {
  transform: translateZ(30px);
}

.project-content h3 {
  transform: translateZ(20px);
}
```

---

## 4. Interactive Dashboards

### Example 4.1: Stats Dashboard with Zdog Charts

**Use Case**: Analytics dashboard with 3D data visualization

```html
<div class="dashboard">
  <div id="vanta-bg"></div>

  <div class="stats-grid">
    <div class="stat-card tilt-card" data-tilt>
      <canvas class="stat-chart" width="200" height="200"></canvas>
      <h3>Users</h3>
      <p class="stat-value">12,345</p>
      <span class="stat-change">+12.5%</span>
    </div>
  </div>
</div>
```

```javascript
// Subtle background
VANTA.TOPOLOGY({
  el: "#vanta-bg",
  color: 0x667eea,
  backgroundColor: 0xf8f9fa
});

// Zdog bar chart
const chartIllo = new Zdog.Illustration({
  element: '.stat-chart',
  zoom: 2,
  dragRotate: true
});

const data = [10, 25, 15, 30, 20, 35, 28];
const barWidth = 8;
const spacing = 12;

data.forEach((value, i) => {
  new Zdog.Box({
    addTo: chartIllo,
    width: barWidth,
    height: value,
    depth: barWidth,
    translate: {
      x: (i - 3) * spacing,
      y: value / 2
    },
    stroke: 1,
    color: `hsl(${220 + i * 10}, 70%, 60%)`,
    fill: true,
    topFace: '#667eea',
    bottomFace: '#764ba2'
  });
});

function animate() {
  chartIllo.rotate.y += 0.01;
  chartIllo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();

// Tilt cards
VanillaTilt.init(document.querySelectorAll(".stat-card"), {
  max: 5,
  glare: false,
  scale: 1.01
});
```

---

## 5. Marketing Pages

### Example 5.1: Feature Showcase with Staggered Animations

**Use Case**: Product marketing page with animated feature cards

```html
<section class="features-section">
  <div id="vanta-bg"></div>

  <div class="features-container">
    <div class="feature-item tilt-card" data-tilt>
      <canvas class="feature-icon" width="120" height="120"></canvas>
      <h3>Lightning Fast</h3>
      <p>Optimized for performance</p>
    </div>

    <div class="feature-item tilt-card" data-tilt data-delay="100">
      <canvas class="feature-icon" width="120" height="120"></canvas>
      <h3>Secure</h3>
      <p>Enterprise-grade security</p>
    </div>

    <div class="feature-item tilt-card" data-tilt data-delay="200">
      <canvas class="feature-icon" width="120" height="120"></canvas>
      <h3>Scalable</h3>
      <p>Grows with your business</p>
    </div>
  </div>
</section>
```

```javascript
// Vanta background
VANTA.DOTS({
  el: "#vanta-bg",
  color: 0xff3f81,
  backgroundColor: 0xffffff,
  size: 2,
  spacing: 30
});

// Staggered tilt initialization
document.querySelectorAll('.feature-item').forEach((item, index) => {
  const delay = parseInt(item.dataset.delay) || 0;

  setTimeout(() => {
    VanillaTilt.init(item, {
      max: 12,
      speed: 400,
      glare: true,
      "max-glare": 0.2
    });

    // Fade in animation
    item.style.opacity = '1';
    item.style.transform = 'translateY(0)';
  }, delay);

  // Initial state
  item.style.opacity = '0';
  item.style.transform = 'translateY(20px)';
  item.style.transition = 'opacity 0.6s, transform 0.6s';
});

// Create unique Zdog icons
const icons = document.querySelectorAll('.feature-icon');

// Lightning icon
const lightning = new Zdog.Illustration({
  element: icons[0],
  zoom: 2
});

new Zdog.Shape({
  addTo: lightning,
  path: [
    { x: 0, y: -30 },
    { x: 10, y: 0 },
    { x: -5, y: 0 },
    { x: 0, y: 30 }
  ],
  closed: true,
  stroke: 3,
  color: '#FFD700',
  fill: true
});

function animateLightning() {
  lightning.rotate.z = Math.sin(Date.now() * 0.002) * 0.2;
  lightning.updateRenderGraph();
  requestAnimationFrame(animateLightning);
}
animateLightning();

// Similar patterns for other icons...
```

---

## 6. E-Commerce

### Example 6.1: Product Detail Page with 360° View

**Use Case**: Product page with interactive 3D model

```html
<div class="product-detail">
  <div class="product-view">
    <canvas class="product-3d" width="600" height="600"></canvas>
    <div class="view-controls">
      <button id="rotate-left">←</button>
      <button id="rotate-right">→</button>
      <button id="zoom-in">+</button>
      <button id="zoom-out">−</button>
    </div>
  </div>

  <div class="product-info tilt-card" data-tilt>
    <h1>Product Name</h1>
    <p class="price">$299.99</p>
    <button class="buy-now">Buy Now</button>
  </div>
</div>
```

```javascript
// Zdog 3D product model
const productIllo = new Zdog.Illustration({
  element: '.product-3d',
  zoom: 3,
  dragRotate: true
});

// Example: Watch model
const watch = new Zdog.Anchor({
  addTo: productIllo
});

// Watch body
new Zdog.Cylinder({
  addTo: watch,
  diameter: 30,
  length: 10,
  stroke: 2,
  color: '#333',
  fill: true
});

// Watch face
new Zdog.Ellipse({
  addTo: watch,
  diameter: 28,
  translate: { z: 6 },
  stroke: 1,
  color: '#fff',
  fill: true
});

// Watch hands
new Zdog.Shape({
  addTo: watch,
  path: [{ y: 0 }, { y: -10 }],
  translate: { z: 7 },
  stroke: 2,
  color: '#333'
});

let rotationSpeed = 0;

function animate() {
  watch.rotate.y += rotationSpeed;
  productIllo.updateRenderGraph();
  requestAnimationFrame(animate);
}
animate();

// Control buttons
document.getElementById('rotate-left').addEventListener('click', () => {
  rotationSpeed = -0.05;
  setTimeout(() => rotationSpeed = 0, 500);
});

document.getElementById('rotate-right').addEventListener('click', () => {
  rotationSpeed = 0.05;
  setTimeout(() => rotationSpeed = 0, 500);
});

let currentZoom = 3;
document.getElementById('zoom-in').addEventListener('click', () => {
  currentZoom += 0.5;
  productIllo.zoom = currentZoom;
});

document.getElementById('zoom-out').addEventListener('click', () => {
  currentZoom = Math.max(1, currentZoom - 0.5);
  productIllo.zoom = currentZoom;
});

// Tilt info card
VanillaTilt.init(document.querySelector('.product-info'), {
  max: 8,
  glare: true,
  "max-glare": 0.2
});
```

---

## 7. SaaS Landing Pages

### Example 7.1: Feature Comparison Table

**Use Case**: SaaS pricing page with interactive comparison

```html
<section class="comparison-section">
  <div id="vanta-bg"></div>

  <table class="comparison-table">
    <thead>
      <tr>
        <th>Features</th>
        <th class="plan-column tilt-column" data-tilt>
          <canvas class="plan-icon" width="60" height="60"></canvas>
          <span>Starter</span>
        </th>
        <th class="plan-column tilt-column" data-tilt>
          <canvas class="plan-icon" width="60" height="60"></canvas>
          <span>Pro</span>
        </th>
        <th class="plan-column tilt-column" data-tilt>
          <canvas class="plan-icon" width="60" height="60"></canvas>
          <span>Enterprise</span>
        </th>
      </tr>
    </thead>
    <tbody>
      <!-- Feature rows -->
    </tbody>
  </table>
</section>
```

```javascript
// Subtle background
VANTA.RINGS({
  el: "#vanta-bg",
  backgroundColor: 0xf8f9fa,
  color: 0x667eea
});

// Tilt plan columns
VanillaTilt.init(document.querySelectorAll('.plan-column'), {
  max: 5,
  glare: true,
  "max-glare": 0.1,
  scale: 1.02,
  axis: 'y'  // Only tilt vertically
});

// Zdog icons for each plan
const plans = document.querySelectorAll('.plan-icon');

// Starter: Single star
const starter = new Zdog.Illustration({
  element: plans[0],
  zoom: 1.5
});

new Zdog.Polygon({
  addTo: starter,
  sides: 5,
  radius: 15,
  stroke: 2,
  color: '#4CAF50',
  fill: true
});

// Pro: Two stars
const pro = new Zdog.Illustration({
  element: plans[1],
  zoom: 1.5
});

[-8, 8].forEach(x => {
  new Zdog.Polygon({
    addTo: pro,
    sides: 5,
    radius: 12,
    translate: { x },
    stroke: 2,
    color: '#2196F3',
    fill: true
  });
});

// Enterprise: Three stars
const enterprise = new Zdog.Illustration({
  element: plans[2],
  zoom: 1.5
});

[-12, 0, 12].forEach(x => {
  new Zdog.Polygon({
    addTo: enterprise,
    sides: 5,
    radius: 10,
    translate: { x },
    stroke: 2,
    color: '#9C27B0',
    fill: true
  });
});

// Animate all
function animate() {
  starter.rotate.z += 0.02;
  pro.rotate.z += 0.02;
  enterprise.rotate.z += 0.02;

  starter.updateRenderGraph();
  pro.updateRenderGraph();
  enterprise.updateRenderGraph();

  requestAnimationFrame(animate);
}
animate();
```

---

## 8. Performance Patterns

### Example 8.1: Lazy Loading Vanta Backgrounds

**Use Case**: Improve initial page load by deferring Vanta initialization

```javascript
// Lazy load Vanta when section is visible
const vantaSections = document.querySelectorAll('[data-vanta]');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const section = entry.target;
      const effect = section.dataset.vanta;

      // Load effect
      if (effect === 'waves') {
        VANTA.WAVES({
          el: section,
          color: 0x23153c,
          waveHeight: 15
        });
      }

      // Stop observing
      observer.unobserve(section);
    }
  });
}, { threshold: 0.1 });

vantaSections.forEach(section => observer.observe(section));
```

---

### Example 8.2: Conditional Effect Loading Based on Device

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const isLowEnd = navigator.hardwareConcurrency <= 4;

if (!isMobile && !isLowEnd) {
  // Full effects
  VANTA.WAVES({
    el: "#vanta-bg",
    color: 0x23153c,
    waveHeight: 20,
    waveSpeed: 1.0
  });

  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 25,
    glare: true,
    "max-glare": 0.5
  });
} else if (isMobile && !isLowEnd) {
  // Mobile-optimized
  VANTA.DOTS({  // Lighter effect
    el: "#vanta-bg",
    size: 2,
    spacing: 40
  });

  // No tilt on mobile, use gyro instead
  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 10,
    gyroscope: true,
    glare: false
  });
} else {
  // Low-end devices: static gradient
  document.getElementById('vanta-bg').style.background =
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';

  // No tilt effects
}
```

---

### Example 8.3: Request Idle Callback for Zdog Animations

```javascript
// Use requestIdleCallback for non-critical animations
let zdogQueue = [];

function animateZdog() {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      zdogQueue.forEach(illo => illo.updateRenderGraph());
      requestAnimationFrame(animateZdog);
    });
  } else {
    // Fallback
    zdogQueue.forEach(illo => illo.updateRenderGraph());
    requestAnimationFrame(animateZdog);
  }
}

// Add illustrations to queue
zdogQueue.push(illo1, illo2, illo3);
animateZdog();
```

---

### Example 8.4: Debounced Resize Handling

```javascript
let resizeTimer;
let vantaEffect;

function initVanta() {
  vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });
}

window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);

  resizeTimer = setTimeout(() => {
    // Destroy and recreate on significant resize
    if (vantaEffect) {
      vantaEffect.destroy();
    }

    initVanta();
  }, 500);
});

initVanta();
```

---

## Complete Integration Example

### Full-Stack Landing Page

Combining all three libraries for a production landing page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Production Landing Page</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- Hero with Vanta -->
  <section class="hero" id="hero">
    <div id="vanta-bg"></div>
    <div class="hero-content">
      <canvas class="logo-zdog" width="200" height="200"></canvas>
      <h1>Your Amazing Product</h1>
      <p>The tagline that converts</p>
      <button class="cta-btn tilt-btn" data-tilt>Get Started Free</button>
    </div>
  </section>

  <!-- Features with Tilt Cards -->
  <section class="features">
    <h2>Features</h2>
    <div class="feature-grid">
      <div class="feature-card tilt-card" data-tilt>
        <canvas class="feature-icon" width="100" height="100"></canvas>
        <h3>Fast</h3>
        <p>Lightning-fast performance</p>
      </div>

      <div class="feature-card tilt-card" data-tilt>
        <canvas class="feature-icon" width="100" height="100"></canvas>
        <h3>Secure</h3>
        <p>Bank-level security</p>
      </div>

      <div class="feature-card tilt-card" data-tilt>
        <canvas class="feature-icon" width="100" height="100"></canvas>
        <h3>Scalable</h3>
        <p>Grows with you</p>
      </div>
    </div>
  </section>

  <!-- Pricing with Zdog + Tilt -->
  <section class="pricing" data-vanta="topology">
    <h2>Pricing</h2>
    <div class="pricing-grid">
      <!-- Pricing cards here -->
    </div>
  </section>

  <!-- Scripts -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.topology.min.js"></script>
  <script src="https://unpkg.com/zdog@1/dist/zdog.dist.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.8.1/vanilla-tilt.min.js"></script>
  <script src="app.js"></script>
</body>
</html>
```

```javascript
// app.js

// Performance check
const performanceLevel = (() => {
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  const cores = navigator.hardwareConcurrency || 2;

  if (isMobile && cores <= 4) return 'low';
  if (isMobile || cores <= 4) return 'medium';
  return 'high';
})();

console.log('Performance level:', performanceLevel);

// Conditional initialization
if (performanceLevel === 'high') {
  // Full effects
  initFullEffects();
} else if (performanceLevel === 'medium') {
  initMediumEffects();
} else {
  initLowEffects();
}

function initFullEffects() {
  // Hero Vanta
  VANTA.WAVES({
    el: "#vanta-bg",
    color: 0x23153c,
    waveHeight: 20,
    waveSpeed: 1.0
  });

  // Pricing Vanta (lazy load)
  const pricingObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        VANTA.TOPOLOGY({
          el: entry.target,
          color: 0x667eea
        });
        pricingObserver.unobserve(entry.target);
      }
    });
  });
  pricingObserver.observe(document.querySelector('[data-vanta="topology"]'));

  // Zdog icons
  initZdogIcons();

  // Vanilla Tilt
  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 15,
    glare: true,
    "max-glare": 0.3,
    scale: 1.05
  });

  VanillaTilt.init(document.querySelector(".cta-btn"), {
    max: 20,
    glare: true,
    "max-glare": 0.5,
    scale: 1.1
  });
}

function initMediumEffects() {
  // Simpler Vanta
  VANTA.DOTS({
    el: "#vanta-bg",
    size: 2,
    spacing: 40
  });

  // Zdog without heavy animations
  initZdogIcons();

  // Lighter tilt
  VanillaTilt.init(document.querySelectorAll(".tilt-card"), {
    max: 10,
    glare: false,
    scale: 1.02
  });
}

function initLowEffects() {
  // Static gradient
  document.getElementById('vanta-bg').style.background =
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';

  // Static Zdog icons
  initZdogIcons(false);  // No animation

  // No tilt effects
}

function initZdogIcons(animate = true) {
  // Logo
  const logoIllo = new Zdog.Illustration({
    element: '.logo-zdog',
    zoom: 3
  });

  const logo = new Zdog.Box({
    addTo: logoIllo,
    width: 30,
    height: 30,
    depth: 30,
    stroke: 2,
    color: '#fff',
    fill: true
  });

  if (animate) {
    function animateLogo() {
      logo.rotate.y += 0.02;
      logoIllo.updateRenderGraph();
      requestAnimationFrame(animateLogo);
    }
    animateLogo();
  } else {
    logoIllo.updateRenderGraph();
  }

  // Feature icons
  const featureIcons = document.querySelectorAll('.feature-icon');

  featureIcons.forEach((canvas, i) => {
    const illo = new Zdog.Illustration({
      element: canvas,
      zoom: 2
    });

    // Different icon for each feature
    if (i === 0) {
      // Lightning
      new Zdog.Shape({
        addTo: illo,
        path: [
          { x: 0, y: -20 },
          { x: 8, y: 0 },
          { x: -4, y: 0 },
          { x: 0, y: 20 }
        ],
        closed: true,
        stroke: 3,
        color: '#FFD700',
        fill: true
      });
    } else if (i === 1) {
      // Shield
      new Zdog.Shape({
        addTo: illo,
        path: [
          { x: 0, y: -20 },
          { x: 15, y: -10 },
          { x: 15, y: 10 },
          { x: 0, y: 20 },
          { x: -15, y: 10 },
          { x: -15, y: -10 }
        ],
        closed: true,
        stroke: 3,
        color: '#4CAF50',
        fill: true
      });
    } else {
      // Graph
      [5, 15, 10, 20].forEach((h, j) => {
        new Zdog.Rect({
          addTo: illo,
          width: 6,
          height: h,
          translate: { x: (j - 1.5) * 8, y: h / 2 - 10 },
          stroke: 2,
          color: '#2196F3',
          fill: true
        });
      });
    }

    if (animate) {
      function animateFeature() {
        illo.rotate.y += 0.01;
        illo.updateRenderGraph();
        requestAnimationFrame(animateFeature);
      }
      animateFeature();
    } else {
      illo.updateRenderGraph();
    }
  });
}

// Cleanup
window.addEventListener('beforeunload', () => {
  document.querySelectorAll('.tilt-card').forEach(card => {
    if (card.vanillaTilt) card.vanillaTilt.destroy();
  });
});
```

---

## Best Practices Summary

1. **Performance First**
   - Test on low-end devices
   - Implement conditional loading
   - Use lazy loading for off-screen effects

2. **Accessibility**
   - Provide fallbacks for disabled animations
   - Maintain sufficient color contrast
   - Ensure interactive elements are keyboard-accessible

3. **Mobile Optimization**
   - Disable heavy effects on mobile
   - Use simpler Vanta effects (DOTS, RINGS)
   - Consider using gyroscope for tilt on mobile

4. **Memory Management**
   - Always destroy effects on unmount
   - Clean up event listeners
   - Use Intersection Observer for visibility detection

5. **User Experience**
   - Keep animations subtle (max tilt: 10-15°)
   - Provide pause/play controls for accessibility
   - Test cross-browser compatibility

---

These examples demonstrate production-ready patterns for building stunning, performant web experiences with lightweight 3D effects.
