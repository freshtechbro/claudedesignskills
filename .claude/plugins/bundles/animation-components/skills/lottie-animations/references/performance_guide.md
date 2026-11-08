# Lottie Performance Optimization Guide

Comprehensive strategies for optimizing Lottie animation performance in production.

## Performance Metrics

**Target Performance:**
- **Desktop:** 60 FPS minimum
- **Mobile:** 30-60 FPS
- **File Size:** <100 KB ideal, <200 KB acceptable
- **Load Time:** <500ms for animation ready
- **Memory:** <50 MB per animation instance

## File Size Optimization

### 1. Use dotLottie Format

```javascript
// 90% smaller file size
<DotLottieReact src="animation.lottie" />  // ✅ 10-50 KB
// vs
<Lottie animationData={jsonData} />        // ❌ 100-500 KB
```

**Benefits:**
- ZIP compression (up to 90% reduction)
- Multiple animations in one file
- Theme support
- Faster parsing

### 2. Optimize JSON

**Before Export (After Effects):**
```
- Simplify paths (reduce anchor points)
- Merge shapes when possible
- Remove unused layers/keyframes
- Use solid colors over gradients
- Enable "Compress JSON" in Bodymovin
```

**After Export:**
```bash
# Use Lottie optimizer
https://lottiefiles.com/tools/lottie-editor

# Or gzip compression (server-side)
gzip animation.json  # 60-80% reduction
```

### 3. Lazy Loading

```jsx
import { lazy, Suspense } from 'react';

const LottieAnimation = lazy(() => import('./LottieAnimation'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LottieAnimation />
    </Suspense>
  );
}
```

**Intersection Observer Pattern:**

```jsx
const LazyLottie = ({ src }) => {
  const [shouldLoad, setShouldLoad] = useState(false);
  const ref = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShouldLoad(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref}>
      {shouldLoad ? <DotLottieReact src={src} /> : <div style={{ height: 300 }} />}
    </div>
  );
};
```

## Runtime Performance

### 1. Renderer Selection

**SVG Renderer:**
```javascript
// Best quality, slower performance
// Use for: Simple icons, small animations, few instances
lottie.loadAnimation({
  renderer: 'svg',  // Vector-based, scalable
  container: element,
  path: 'animation.json'
});
```

**Canvas Renderer:**
```javascript
// Better performance, rasterized
// Use for: Complex animations, many instances, mobile
new DotLottie({
  canvas: canvasElement,  // ✅ Recommended for complex animations
  src: 'animation.lottie'
});
```

**Performance Comparison:**

| Renderer | Quality | Performance | Use Case |
|----------|---------|-------------|----------|
| SVG      | Excellent | Good (simple animations) | Icons, logos, simple UI |
| Canvas   | Good | Excellent | Complex animations, mobile |
| HTML     | Poor | Poor | Legacy support only |

### 2. Web Workers (Best Performance)

```javascript
import { DotLottieWorker } from '@lottiefiles/dotlottie-web';

// Offload rendering to separate thread
new DotLottieWorker({
  canvas: document.getElementById('canvas'),
  src: 'heavy-animation.lottie',
  autoplay: true,
  loop: true,
  workerId: 'worker-1'
});
```

**Benefits:**
- No main thread blocking
- Smooth scroll performance
- Multiple animations without lag
- Better mobile performance

**When to use:**
- Animation >100 KB
- Multiple simultaneous animations
- Scroll-driven animations
- Mobile devices

### 3. Device Pixel Ratio Optimization

```javascript
// Reduce quality on low-end devices
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const isLowEnd = navigator.deviceMemory < 4; // GB

new DotLottie({
  canvas: canvas,
  src: 'animation.lottie',
  renderConfig: {
    devicePixelRatio: (isMobile || isLowEnd) ? 1 : window.devicePixelRatio
    // 1 = standard definition (faster)
    // 2 = retina (slower, better quality)
  }
});
```

### 4. Animation Complexity Control

**Adaptive Quality:**

```javascript
const getAnimationSrc = () => {
  const isMobile = /Mobile/i.test(navigator.userAgent);
  const isSlowDevice = navigator.hardwareConcurrency < 4;

  if (isMobile || isSlowDevice) {
    return 'animation-low.lottie';  // Simplified version
  }
  return 'animation-high.lottie';    // Full quality
};

<DotLottieReact src={getAnimationSrc()} />
```

**Frame Rate Reduction:**

```javascript
// Reduce frame rate on slow devices
const targetFPS = isMobile ? 30 : 60;

new DotLottie({
  canvas: canvas,
  src: 'animation.lottie',
  speed: 1,
  // Implemented via requestAnimationFrame throttling
});
```

## Memory Management

### 1. Proper Cleanup

```jsx
const AnimationComponent = () => {
  const [dotLottie, setDotLottie] = useState(null);

  useEffect(() => {
    return () => {
      // CRITICAL: Destroy on unmount
      dotLottie?.destroy();
    };
  }, [dotLottie]);

  return <DotLottieReact dotLottieRefCallback={setDotLottie} />;
};
```

### 2. Event Listener Cleanup

```javascript
useEffect(() => {
  if (!dotLottie) return;

  const handleComplete = () => console.log('Done');

  dotLottie.addEventListener('complete', handleComplete);

  // CRITICAL: Remove listeners
  return () => {
    dotLottie.removeEventListener('complete', handleComplete);
  };
}, [dotLottie]);
```

### 3. Instance Pooling

```javascript
// Reuse animation instances
class LottiePool {
  constructor() {
    this.pool = [];
    this.active = new Set();
  }

  acquire(src) {
    let instance = this.pool.find(i => i.src === src && !this.active.has(i));

    if (!instance) {
      instance = new DotLottie({ canvas: createCanvas(), src });
      this.pool.push(instance);
    }

    this.active.add(instance);
    return instance;
  }

  release(instance) {
    instance.stop();
    this.active.delete(instance);
  }

  cleanup() {
    this.pool.forEach(i => i.destroy());
    this.pool = [];
    this.active.clear();
  }
}
```

## Network Optimization

### 1. CDN Hosting

```jsx
// Host on CDN for better caching
<DotLottieReact
  src="https://cdn.example.com/animations/hero.lottie"
  loop
  autoplay
/>
```

**Benefits:**
- Edge caching (faster loads)
- Reduced server load
- Better global performance

### 2. Preloading Critical Animations

```html
<!-- Preload animation for faster display -->
<link rel="preload" href="/animations/hero.lottie" as="fetch" crossorigin>
```

```javascript
// Programmatic preload
const preloadAnimation = async (src) => {
  const response = await fetch(src);
  const blob = await response.blob();
  return URL.createObjectURL(blob);
};

// Use preloaded blob
const blobUrl = await preloadAnimation('/animation.lottie');
<DotLottieReact src={blobUrl} />
```

### 3. Service Worker Caching

```javascript
// service-worker.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('lottie-v1').then((cache) => {
      return cache.addAll([
        '/animations/hero.lottie',
        '/animations/loading.lottie'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.url.endsWith('.lottie')) {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  }
});
```

## Mobile Optimization

### 1. Reduce Quality on Mobile

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

<DotLottieReact
  src={isMobile ? 'animation-mobile.lottie' : 'animation-desktop.lottie'}
  renderConfig={{
    devicePixelRatio: isMobile ? 1 : window.devicePixelRatio
  }}
/>
```

### 2. Pause on Offscreen

```javascript
useEffect(() => {
  if (!dotLottie) return;

  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      dotLottie.play();
    } else {
      dotLottie.pause();
    }
  });

  observer.observe(document.getElementById('lottie-container'));

  return () => observer.disconnect();
}, [dotLottie]);
```

### 3. Battery-Aware Performance

```javascript
// Reduce animation when low battery
navigator.getBattery?.().then((battery) => {
  if (battery.level < 0.2) {
    dotLottie.setSpeed(0.5); // Slower = less CPU
  }

  battery.addEventListener('levelchange', () => {
    if (battery.level < 0.2) {
      dotLottie.stop();
    }
  });
});
```

## Monitoring Performance

### 1. FPS Monitoring

```javascript
class FPSMonitor {
  constructor() {
    this.fps = 0;
    this.frames = 0;
    this.lastTime = performance.now();
  }

  update() {
    this.frames++;
    const currentTime = performance.now();

    if (currentTime - this.lastTime >= 1000) {
      this.fps = Math.round((this.frames * 1000) / (currentTime - this.lastTime));
      console.log(`FPS: ${this.fps}`);
      this.frames = 0;
      this.lastTime = currentTime;
    }

    requestAnimationFrame(() => this.update());
  }

  start() {
    this.update();
  }
}

const monitor = new FPSMonitor();
monitor.start();
```

### 2. Memory Usage Tracking

```javascript
if (performance.memory) {
  setInterval(() => {
    const used = (performance.memory.usedJSHeapSize / 1048576).toFixed(2);
    const total = (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2);
    console.log(`Memory: ${used} MB / ${total} MB`);
  }, 5000);
}
```

### 3. Performance Marks

```javascript
// Mark start
performance.mark('lottie-load-start');

const dotLottie = new DotLottie({...});

dotLottie.addEventListener('load', () => {
  // Mark end and measure
  performance.mark('lottie-load-end');
  performance.measure('lottie-load', 'lottie-load-start', 'lottie-load-end');

  const measure = performance.getEntriesByName('lottie-load')[0];
  console.log(`Load time: ${measure.duration}ms`);
});
```

## Common Performance Issues

### Issue 1: Animation Stutters

**Symptoms:** Dropped frames, jerky playback

**Solutions:**
```
1. Switch to Canvas renderer
2. Use DotLottieWorker for web worker rendering
3. Reduce devicePixelRatio (1 instead of 2)
4. Simplify animation (fewer shapes/keyframes)
5. Reduce number of simultaneous animations
```

### Issue 2: Slow Page Load

**Symptoms:** Long initial render time

**Solutions:**
```
1. Use lazy loading with IntersectionObserver
2. Preload critical animations only
3. Use dotLottie format (smaller files)
4. Load animations after page interactive
5. Use code splitting (React.lazy)
```

### Issue 3: Memory Leaks

**Symptoms:** Memory usage increases over time

**Solutions:**
```
1. Call destroy() on unmount
2. Remove all event listeners
3. Clear animation references
4. Avoid creating new instances repeatedly
5. Use instance pooling for frequently re-created animations
```

### Issue 4: Mobile Performance Poor

**Symptoms:** Slow on phones, smooth on desktop

**Solutions:**
```
1. Create mobile-optimized version (simpler)
2. Use Canvas renderer (not SVG)
3. Set devicePixelRatio to 1
4. Reduce animation frame rate (30 FPS)
5. Use DotLottieWorker
6. Pause when offscreen
```

## Best Practices Summary

**File Size:**
- ✅ Use dotLottie format (.lottie)
- ✅ Compress JSON
- ✅ Keep under 100 KB
- ✅ Optimize images (or remove)
- ✅ Simplify paths

**Runtime:**
- ✅ Use Canvas renderer for complex animations
- ✅ Use Web Workers (DotLottieWorker)
- ✅ Destroy instances on unmount
- ✅ Remove event listeners
- ✅ Lazy load animations

**Mobile:**
- ✅ Create mobile-optimized versions
- ✅ Set devicePixelRatio to 1
- ✅ Pause when offscreen
- ✅ Reduce quality on low-end devices

**Monitoring:**
- ✅ Track FPS (target 60 on desktop, 30 on mobile)
- ✅ Monitor memory usage
- ✅ Measure load times
- ✅ Test on real devices
