# Web Performance Optimization Checklist

## Overview

Comprehensive performance optimization guide targeting Core Web Vitals and 60 FPS experiences. This checklist covers measurement, optimization strategies, and modern best practices.

**Performance Budget Targets**:
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1
- Interaction to Next Paint (INP): < 200ms
- Time to Interactive (TTI): < 3.8s
- First Contentful Paint (FCP): < 1.8s

---

## Table of Contents

1. [Core Web Vitals](#core-web-vitals)
2. [Animation Performance](#animation-performance)
3. [Image Optimization](#image-optimization)
4. [Font Loading](#font-loading)
5. [JavaScript Optimization](#javascript-optimization)
6. [CSS Optimization](#css-optimization)
7. [3D & WebGL Optimization](#3d--webgl-optimization)
8. [Loading Strategies](#loading-strategies)
9. [Caching & CDN](#caching--cdn)
10. [Monitoring & Measurement](#monitoring--measurement)

---

## Core Web Vitals

### Largest Contentful Paint (LCP)

**Target**: < 2.5 seconds

**What it measures**: Time until largest content element is visible.

**Optimization Checklist**:
- [ ] Optimize hero images (WebP/AVIF, < 100KB)
- [ ] Preload critical resources (`<link rel="preload">`)
- [ ] Eliminate render-blocking resources
- [ ] Use CDN for static assets
- [ ] Implement efficient server response time (< 200ms TTFB)
- [ ] Remove unused CSS/JS
- [ ] Enable compression (Brotli/gzip)

**Implementation**:
```html
<!-- Preload critical resources -->
<link rel="preload" as="image" href="hero.webp" type="image/webp">
<link rel="preload" as="font" href="inter-var.woff2" type="font/woff2" crossorigin>

<!-- Modern image formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero" loading="eager" fetchpriority="high">
</picture>
```

**Debugging**:
```javascript
// Measure LCP
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
}).observe({ entryTypes: ['largest-contentful-paint'] });
```

---

### First Input Delay (FID) / Interaction to Next Paint (INP)

**Target**: FID < 100ms, INP < 200ms

**What it measures**: Responsiveness to user interactions.

**Optimization Checklist**:
- [ ] Split long tasks (< 50ms each)
- [ ] Defer non-critical JavaScript
- [ ] Use web workers for heavy computation
- [ ] Implement code splitting
- [ ] Avoid long-running event handlers
- [ ] Debounce scroll/resize listeners
- [ ] Use passive event listeners

**Implementation**:
```javascript
// Split long tasks
function yieldToMain() {
  return new Promise(resolve => {
    setTimeout(resolve, 0);
  });
}

async function processLargeArray(array) {
  for (let i = 0; i < array.length; i++) {
    processItem(array[i]);

    // Yield every 50 items
    if (i % 50 === 0) {
      await yieldToMain();
    }
  }
}

// Passive event listeners
window.addEventListener('scroll', handleScroll, { passive: true });

// Debounced resize handler
const debouncedResize = debounce(() => {
  handleResize();
}, 150);

window.addEventListener('resize', debouncedResize);
```

---

### Cumulative Layout Shift (CLS)

**Target**: < 0.1

**What it measures**: Visual stability during page load.

**Optimization Checklist**:
- [ ] Reserve space for images (use `aspect-ratio`)
- [ ] Reserve space for ads and embeds
- [ ] Avoid inserting content above existing content
- [ ] Use CSS transforms instead of position changes
- [ ] Set explicit dimensions for iframes
- [ ] Avoid web fonts that cause FOUT/FOIT
- [ ] Use `font-display: swap` or `font-display: optional`

**Implementation**:
```css
/* Reserve space for images */
img {
  aspect-ratio: attr(width) / attr(height);
  width: 100%;
  height: auto;
}

/* Or explicit aspect ratio */
.hero-image {
  aspect-ratio: 16 / 9;
}

/* Animations: use transform, not position */
.animated {
  transform: translateX(0);
  transition: transform 0.3s;
}

.animated.active {
  transform: translateX(100px); /* Good */
  /* left: 100px; Bad - causes layout shift */
}
```

**Debugging**:
```javascript
// Measure CLS
let clsValue = 0;
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      clsValue += entry.value;
      console.log('CLS:', clsValue);
    }
  }
}).observe({ entryTypes: ['layout-shift'] });
```

---

## Animation Performance

### 60 FPS Checklist

**Target**: < 16.67ms per frame

**GPU-Accelerated Properties (Use These)**:
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (some, like blur - be careful)

**Avoid Animating**:
- `top`, `left`, `right`, `bottom`
- `width`, `height`
- `margin`, `padding`
- `border-width`

**Implementation**:
```css
/* Good: GPU-accelerated */
.animated {
  transform: translateX(0);
  opacity: 1;
  transition: transform 0.3s, opacity 0.3s;
}

.animated.active {
  transform: translateX(100px) scale(1.1);
  opacity: 0.8;
}

/* Bad: triggers layout/paint */
.animated-bad {
  left: 0;
  width: 100px;
  transition: left 0.3s, width 0.3s;
}
```

### Will-Change Optimization

**Use Sparingly**:
```css
/* Only during animation */
.will-animate {
  /* Don't set will-change here */
}

.will-animate.animating {
  will-change: transform; /* Set on animation start */
}

.will-animate.done {
  will-change: auto; /* Remove after animation */
}
```

**JavaScript Control**:
```javascript
element.addEventListener('mouseenter', () => {
  element.style.willChange = 'transform';
});

element.addEventListener('mouseleave', () => {
  // Remove after animation completes
  element.addEventListener('transitionend', () => {
    element.style.willChange = 'auto';
  }, { once: true });
});
```

### RequestAnimationFrame

**Always use for JavaScript animations**:
```javascript
// Good
function animate() {
  element.style.transform = `translateX(${x}px)`;
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);

// Bad
setInterval(() => {
  element.style.transform = `translateX(${x}px)`;
}, 16); // Not synced with browser paint
```

### Performance Monitoring

**Chrome DevTools**:
```javascript
// Mark start of expensive operation
performance.mark('animation-start');

// ... do animation work ...

// Mark end
performance.mark('animation-end');

// Measure duration
performance.measure('animation-duration', 'animation-start', 'animation-end');

// Get measurement
const measure = performance.getEntriesByName('animation-duration')[0];
console.log(`Animation took ${measure.duration}ms`);
```

---

## Image Optimization

### Format Selection

**Decision Tree**:
1. **Photos**: AVIF > WebP > JPEG
2. **Graphics/logos**: SVG > WebP > PNG
3. **Animations**: WebP animated > GIF
4. **Icons**: SVG or icon fonts

**Implementation**:
```html
<picture>
  <!-- Modern browsers: AVIF (best compression) -->
  <source srcset="image.avif" type="image/avif">

  <!-- Fallback: WebP (good compression) -->
  <source srcset="image.webp" type="image/webp">

  <!-- Final fallback: JPEG -->
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

### Responsive Images

**Checklist**:
- [ ] Use `srcset` for multiple resolutions
- [ ] Define `sizes` attribute
- [ ] Serve appropriately sized images (not full-res everywhere)
- [ ] Use lazy loading for below-fold images
- [ ] Set explicit dimensions to prevent CLS

**Implementation**:
```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 50vw,
    33vw
  "
  alt="Description"
  loading="lazy"
  width="1200"
  height="800"
>
```

### Image Compression

**Tools**:
- **CLI**: ImageMagick, Sharp (Node.js)
- **GUI**: Squoosh (web), ImageOptim (Mac)
- **Build tools**: imagemin, @squoosh/lib

**Example (Sharp)**:
```javascript
const sharp = require('sharp');

await sharp('input.jpg')
  .resize(1200, 800, { fit: 'cover' })
  .webp({ quality: 80 })
  .toFile('output.webp');

await sharp('input.jpg')
  .resize(1200, 800, { fit: 'cover' })
  .avif({ quality: 70 })
  .toFile('output.avif');
```

### Lazy Loading

**Native Lazy Loading**:
```html
<!-- Lazy load below-fold images -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Eager load above-fold images -->
<img src="hero.jpg" loading="eager" fetchpriority="high" alt="Hero">
```

**Intersection Observer (Advanced)**:
```javascript
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});
```

---

## Font Loading

### Font Display Strategy

**Options**:
- `swap`: Show fallback, swap when loaded (FOUT - Flash of Unstyled Text)
- `optional`: Use cached font if available, otherwise use fallback
- `fallback`: Brief block, swap if fast, fallback if slow

**Recommended**:
```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap; /* Show fallback immediately */
}
```

### Font Subsetting

**Reduce file size by including only needed characters**:

**Tools**: `pyftsubset` (part of fonttools)

```bash
# Include only Latin characters
pyftsubset input.ttf \
  --output-file=output.woff2 \
  --flavor=woff2 \
  --layout-features=* \
  --unicodes=U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD
```

### Preload Critical Fonts

```html
<link
  rel="preload"
  as="font"
  href="/fonts/inter-var.woff2"
  type="font/woff2"
  crossorigin
>
```

### System Font Stack

**Performance-first approach**:
```css
body {
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    sans-serif;
}
```

---

## JavaScript Optimization

### Code Splitting

**Route-based splitting**:
```javascript
// React Router
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Gallery = lazy(() => import('./pages/Gallery'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/about" element={<About />} />
    <Route path="/gallery" element={<Gallery />} />
  </Routes>
</Suspense>
```

**Component-based splitting**:
```javascript
// Load heavy components only when needed
const HeavyChart = lazy(() => import('./components/HeavyChart'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Skeleton />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### Tree Shaking

**Ensure tree shaking works**:
```javascript
// Good: Named imports
import { map, filter } from 'lodash-es';

// Bad: Default import (imports entire library)
import _ from 'lodash';
```

### Bundle Analysis

**Webpack Bundle Analyzer**:
```bash
npm install --save-dev webpack-bundle-analyzer

# Add to webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

plugins: [
  new BundleAnalyzerPlugin()
]
```

**Vite**:
```bash
npm install --save-dev rollup-plugin-visualizer

# vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [visualizer({ open: true })]
}
```

---

## CSS Optimization

### Critical CSS

**Inline above-the-fold CSS**:
```html
<style>
  /* Critical CSS inlined */
  body { font-family: sans-serif; }
  .hero { height: 100vh; }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>
```

**Tools**:
- Critical (npm package)
- Critters (Vite/Webpack plugin)

### Remove Unused CSS

**PurgeCSS**:
```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('@fullhuman/postcss-purgecss')({
      content: ['./src/**/*.html', './src/**/*.jsx'],
      defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || []
    })
  ]
}
```

### CSS Containment

**Improve rendering performance**:
```css
.card {
  /* Isolate layout calculations */
  contain: layout style paint;
}

.article {
  /* More aggressive containment */
  contain: strict;
}
```

---

## 3D & WebGL Optimization

### Loading Strategy

**Checklist**:
- [ ] Show placeholder while loading
- [ ] Load 3D content below fold lazily
- [ ] Use low-poly models initially
- [ ] Progressive enhancement with high-poly

**Implementation**:
```javascript
// Lazy load Three.js scene
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      loadThreeJSScene();
      observer.unobserve(entry.target);
    }
  });
});

observer.observe(document.querySelector('.3d-container'));
```

### Runtime Performance

**Checklist**:
- [ ] Implement object pooling (reuse objects)
- [ ] Use LOD (Level of Detail)
- [ ] Frustum culling (don't render off-screen objects)
- [ ] Texture compression (Basis Universal, KTX2)
- [ ] Reduce polygon count (< 100k for real-time)
- [ ] Limit draw calls (< 100 per frame)
- [ ] Use instancing for repeated geometry

**Three.js Example**:
```javascript
// Object pooling
const objectPool = [];

function getObject() {
  return objectPool.length > 0 ? objectPool.pop() : createNewObject();
}

function releaseObject(obj) {
  objectPool.push(obj);
}

// LOD (Level of Detail)
const lod = new THREE.LOD();
lod.addLevel(highPolyMesh, 0);   // 0-50m
lod.addLevel(mediumPolyMesh, 50); // 50-100m
lod.addLevel(lowPolyMesh, 100);   // 100m+
scene.add(lod);

// Instancing
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial();
const count = 10000;

const mesh = new THREE.InstancedMesh(geometry, material, count);
scene.add(mesh);
```

### Texture Optimization

**Checklist**:
- [ ] Use power-of-two dimensions (512, 1024, 2048)
- [ ] Compress textures (Basis, KTX2)
- [ ] Use texture atlases
- [ ] Reduce texture resolution (don't use 4K everywhere)
- [ ] Enable mipmaps

---

## Loading Strategies

### Critical Rendering Path

**Optimize the order**:

1. **HTML** (initial)
2. **Critical CSS** (inlined)
3. **Critical JavaScript** (defer rest)
4. **Fonts** (preload, font-display: swap)
5. **Images** (lazy load below-fold)

**Implementation**:
```html
<!DOCTYPE html>
<html>
<head>
  <!-- Critical CSS inlined -->
  <style>/* Critical styles */</style>

  <!-- Preload critical resources -->
  <link rel="preload" as="font" href="font.woff2" type="font/woff2" crossorigin>
  <link rel="preload" as="image" href="hero.webp">

  <!-- Defer non-critical CSS -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

  <!-- Defer JavaScript -->
  <script defer src="main.js"></script>
</head>
<body>
  <!-- Content -->
</body>
</html>
```

### Resource Hints

**Preconnect** (DNS, TCP, TLS):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com">
```

**DNS-Prefetch**:
```html
<link rel="dns-prefetch" href="https://analytics.example.com">
```

**Prefetch** (next page):
```html
<link rel="prefetch" href="/next-page.html">
```

---

## Caching & CDN

### HTTP Caching Headers

**Static Assets** (immutable):
```
Cache-Control: public, max-age=31536000, immutable
```

**HTML** (revalidate):
```
Cache-Control: no-cache
```

**API Responses**:
```
Cache-Control: public, max-age=3600, must-revalidate
```

### Service Worker Caching

**Workbox**:
```javascript
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { CacheFirst, NetworkFirst } from 'workbox-strategies';

// Precache build assets
precacheAndRoute(self.__WB_MANIFEST);

// Cache images
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({ cacheName: 'images' })
);

// Network-first for HTML
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({ cacheName: 'pages' })
);
```

---

## Monitoring & Measurement

### Real User Monitoring (RUM)

**Web Vitals**:
```bash
npm install web-vitals
```

```javascript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics({ name, value, id }) {
  // Send to your analytics endpoint
  fetch('/analytics', {
    method: 'POST',
    body: JSON.stringify({ name, value, id })
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Performance Budget

**Lighthouse CI**:
```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "first-contentful-paint": ["error", {"maxNumericValue": 1800}],
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-blocking-time": ["error", {"maxNumericValue": 200}]
      }
    }
  }
}
```

### Chrome DevTools

**Performance Panel**:
1. Open DevTools (F12)
2. Performance tab
3. Click Record
4. Interact with page
5. Stop recording
6. Analyze flame chart

**Look for**:
- Long tasks (> 50ms)
- Excessive layout thrashing
- Forced synchronous layouts
- Paint flashing

---

## Quick Wins Checklist

**Immediate Impact**:
- [ ] Enable Brotli/gzip compression
- [ ] Implement lazy loading for images
- [ ] Add `width` and `height` to images (prevent CLS)
- [ ] Use modern image formats (WebP/AVIF)
- [ ] Preload critical resources
- [ ] Defer non-critical JavaScript
- [ ] Use CDN for static assets
- [ ] Enable HTTP/2 or HTTP/3
- [ ] Minify CSS and JavaScript
- [ ] Remove unused CSS/JS

**High Impact**:
- [ ] Implement code splitting
- [ ] Optimize images (< 100KB)
- [ ] Use system fonts or preload web fonts
- [ ] Inline critical CSS
- [ ] Implement service worker caching
- [ ] Optimize animation performance (use transforms)
- [ ] Reduce JavaScript bundle size (< 200KB)
- [ ] Set up performance monitoring

---

*Last updated: 2024*
*Benchmarks based on median 4G mobile connections*
