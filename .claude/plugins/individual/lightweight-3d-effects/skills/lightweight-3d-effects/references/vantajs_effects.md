# Vanta.js Effects Reference

Complete reference for Vanta.js - animated WebGL backgrounds powered by Three.js.

**Version**: 0.5.24
**License**: MIT
**Website**: https://www.vantajs.com

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Available Effects](#available-effects)
3. [Common Options](#common-options)
4. [Effect-Specific Options](#effect-specific-options)
5. [Methods](#methods)
6. [Framework Integration](#framework-integration)
7. [Performance](#performance)

---

## Getting Started

### Basic Setup

```html
<!-- Three.js (required for all effects) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>

<!-- Vanta.js effect (choose one) -->
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js"></script>

<div id="vanta-bg"></div>

<script>
VANTA.WAVES({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00
});
</script>
```

### NPM Installation

```bash
npm install vanta
```

```javascript
import * as THREE from 'three';
import WAVES from 'vanta/dist/vanta.waves.min.js';

const vantaEffect = WAVES({
  el: "#vanta-bg",
  THREE: THREE
});
```

---

## Available Effects

### 1. WAVES

Animated wave surface effect.

**CDN**: `vanta.waves.min.js`

```javascript
VANTA.WAVES({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0x23153c,         // Hex number
  shininess: 30.00,
  waveHeight: 15.00,
  waveSpeed: 0.75,
  zoom: 0.65
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color` | Number | 0x23153c | Wave color (hex number) |
| `shininess` | Number | 30 | Surface reflectivity (0-100) |
| `waveHeight` | Number | 15 | Wave amplitude |
| `waveSpeed` | Number | 0.75 | Animation speed (0-2) |
| `zoom` | Number | 0.65 | Camera zoom level |

---

### 2. CLOUDS

Volumetric cloud-like effect.

**CDN**: `vanta.clouds.min.js`

```javascript
VANTA.CLOUDS({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  skyColor: 0x68b8d7,
  cloudColor: 0xadc1de,
  cloudShadowColor: 0x183550,
  sunColor: 0xff9919,
  sunGlareColor: 0xff6633,
  sunlightColor: 0xff9933,
  speed: 1.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `skyColor` | Number | 0x68b8d7 | Sky background color |
| `cloudColor` | Number | 0xadc1de | Cloud base color |
| `cloudShadowColor` | Number | 0x183550 | Cloud shadow color |
| `sunColor` | Number | 0xff9919 | Sun body color |
| `sunGlareColor` | Number | 0xff6633 | Sun glare color |
| `sunlightColor` | Number | 0xff9933 | Sunlight color |
| `speed` | Number | 1.00 | Cloud movement speed |

---

### 3. BIRDS

Flocking birds simulation.

**CDN**: `vanta.birds.min.js`

```javascript
VANTA.BIRDS({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  backgroundColor: 0x23153c,
  color1: 0xff0090,
  color2: 0xff6633,
  colorMode: "lerp",       // "lerp" or "lerpGradient"
  birdSize: 1.00,
  wingSpan: 20.00,
  speedLimit: 5.00,
  separation: 20.00,
  alignment: 20.00,
  cohesion: 20.00,
  quantity: 3.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `backgroundColor` | Number | 0x23153c | Scene background |
| `color1` | Number | 0xff0090 | Primary bird color |
| `color2` | Number | 0xff6633 | Secondary bird color |
| `colorMode` | String | "lerp" | Color blending mode |
| `birdSize` | Number | 1.00 | Bird scale multiplier |
| `wingSpan` | Number | 20 | Wing spread distance |
| `speedLimit` | Number | 5 | Maximum flight speed |
| `separation` | Number | 20 | Avoid crowding force |
| `alignment` | Number | 20 | Align with neighbors |
| `cohesion` | Number | 20 | Move toward center |
| `quantity` | Number | 3 | Number of birds |

---

### 4. NET

Particle network with connecting lines.

**CDN**: `vanta.net.min.js`

```javascript
VANTA.NET({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0x3fafff,
  backgroundColor: 0x23153c,
  points: 10.00,
  maxDistance: 20.00,
  spacing: 15.00,
  showDots: true
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color` | Number | 0x3fafff | Line/point color |
| `backgroundColor` | Number | 0x23153c | Background color |
| `points` | Number | 10 | Number of points |
| `maxDistance` | Number | 20 | Max connection distance |
| `spacing` | Number | 15 | Point spacing |
| `showDots` | Boolean | true | Display dots |

---

### 5. CELLS

Organic cellular growth pattern.

**CDN**: `vanta.cells.min.js`

```javascript
VANTA.CELLS({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  color1: 0x18b0c6,
  color2: 0xff6633,
  size: 1.50,
  speed: 1.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color1` | Number | 0x18b0c6 | Primary cell color |
| `color2` | Number | 0xff6633 | Secondary cell color |
| `size` | Number | 1.50 | Cell size multiplier |
| `speed` | Number | 1.00 | Growth animation speed |

---

### 6. FOG

Misty fog effect with depth.

**CDN**: `vanta.fog.min.js`

```javascript
VANTA.FOG({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  highlightColor: 0xff3f81,
  midtoneColor: 0xff1f51,
  lowlightColor: 0x2d1b46,
  baseColor: 0xffebff,
  blurFactor: 0.60,
  speed: 1.00,
  zoom: 1.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `highlightColor` | Number | 0xff3f81 | Bright fog color |
| `midtoneColor` | Number | 0xff1f51 | Mid fog color |
| `lowlightColor` | Number | 0x2d1b46 | Dark fog color |
| `baseColor` | Number | 0xffebff | Base background |
| `blurFactor` | Number | 0.60 | Blur intensity (0-1) |
| `speed` | Number | 1.00 | Movement speed |
| `zoom` | Number | 1.00 | Camera zoom |

---

### 7. GLOBE

Rotating globe with points.

**CDN**: `vanta.globe.min.js`

```javascript
VANTA.GLOBE({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0x3fafff,
  color2: 0xff6633,
  size: 1.50,
  backgroundColor: 0x23153c
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color` | Number | 0x3fafff | Primary globe color |
| `color2` | Number | 0xff6633 | Secondary color |
| `size` | Number | 1.50 | Globe size |
| `backgroundColor` | Number | 0x23153c | Background color |

---

### 8. RINGS

Concentric animated rings.

**CDN**: `vanta.rings.min.js`

```javascript
VANTA.RINGS({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  backgroundColor: 0x23153c,
  color: 0xff3f81
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `backgroundColor` | Number | 0x23153c | Background color |
| `color` | Number | 0xff3f81 | Ring color |

---

### 9. HALO

Glowing halo particle effect.

**CDN**: `vanta.halo.min.js`

```javascript
VANTA.HALO({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  backgroundColor: 0x111122,
  size: 1.50,
  xOffset: 0.20,
  yOffset: 0.10
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `backgroundColor` | Number | 0x111122 | Background color |
| `size` | Number | 1.50 | Halo size |
| `xOffset` | Number | 0.20 | Horizontal position |
| `yOffset` | Number | 0.10 | Vertical position |

---

### 10. TRUNK

Abstract trunk/tree structure.

**CDN**: `vanta.trunk.min.js`

```javascript
VANTA.TRUNK({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  backgroundColor: 0x23153c,
  color: 0xff3f81,
  spacing: 2.00,
  chaos: 4.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `backgroundColor` | Number | 0x23153c | Background color |
| `color` | Number | 0xff3f81 | Trunk color |
| `spacing` | Number | 2.00 | Branch spacing |
| `chaos` | Number | 4.00 | Randomness factor |

---

### 11. TOPOLOGY

Topographic mesh surface.

**CDN**: `vanta.topology.min.js`

```javascript
VANTA.TOPOLOGY({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0xff3f81,
  backgroundColor: 0x23153c
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color` | Number | 0xff3f81 | Mesh line color |
| `backgroundColor` | Number | 0x23153c | Background color |

---

### 12. DOTS

Particle dot field effect.

**CDN**: `vanta.dots.min.js`

```javascript
VANTA.DOTS({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  scale: 1.00,
  scaleMobile: 1.00,
  color: 0xff3f81,
  color2: 0xffffff,
  backgroundColor: 0x23153c,
  size: 3.00,
  spacing: 35.00
});
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `color` | Number | 0xff3f81 | Primary dot color |
| `color2` | Number | 0xffffff | Secondary dot color |
| `backgroundColor` | Number | 0x23153c | Background color |
| `size` | Number | 3.00 | Dot size |
| `spacing` | Number | 35.00 | Dot spacing |

---

### 13. CLOUDS2

Alternative cloud implementation.

**CDN**: `vanta.clouds2.min.js`

```javascript
VANTA.CLOUDS2({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  backgroundColor: 0x23153c,
  skyColor: 0x3f7fb7,
  cloudColor: 0x28496e,
  lightColor: 0xff8800,
  speed: 1.00
});
```

---

### 14. RIPPLE

Water ripple effect.

**Dependencies**: `vanta.ripple.min.js` + `p5.js`

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.ripple.min.js"></script>
```

```javascript
VANTA.RIPPLE({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  minHeight: 200.00,
  minWidth: 200.00,
  color: 0x3f7fb7
});
```

---

## Common Options

These options work with most/all Vanta effects.

### Control Options

```javascript
{
  el: "#vanta-bg",              // Required: DOM element or selector
  mouseControls: true,          // Mouse movement interaction
  touchControls: true,          // Touch interaction
  gyroControls: false,          // Gyroscope interaction (mobile)
  minHeight: 200.00,            // Minimum height before effect pauses
  minWidth: 200.00,             // Minimum width before effect pauses
  scale: 1.00,                  // Desktop scale
  scaleMobile: 1.00             // Mobile scale multiplier
}
```

### Color Format

**IMPORTANT**: Colors must be hex numbers, NOT strings.

```javascript
// ✅ Correct
color: 0xff3f81

// ❌ Incorrect
color: "#ff3f81"
color: "0xff3f81"
```

**Conversion**:
```javascript
// String to number
let colorString = "#ff3f81";
let colorNumber = parseInt(colorString.replace("#", "0x"));

// Number to string
let colorNumber = 0xff3f81;
let colorString = "#" + colorNumber.toString(16).padStart(6, '0');
```

---

## Methods

All Vanta effects return an instance with these methods:

### destroy()

Remove the effect and clean up resources.

```javascript
let vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });

// Later...
vantaEffect.destroy();
```

**Important**: Always call `destroy()` when removing the effect to prevent memory leaks.

---

### setOptions(options)

Update effect options dynamically.

```javascript
let vantaEffect = VANTA.WAVES({
  el: "#vanta-bg",
  color: 0x23153c
});

// Update color
vantaEffect.setOptions({
  color: 0xff3f81,
  waveHeight: 20
});
```

---

### resize()

Manually trigger a resize recalculation.

```javascript
window.addEventListener('resize', () => {
  vantaEffect.resize();
});
```

**Note**: Vanta usually auto-detects resize, but manual calls help in edge cases.

---

## Framework Integration

### React

```jsx
import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';
import WAVES from 'vanta/dist/vanta.waves.min.js';

function VantaBackground() {
  const [vantaEffect, setVantaEffect] = useState(null);
  const vantaRef = useRef(null);

  useEffect(() => {
    if (!vantaEffect) {
      setVantaEffect(
        WAVES({
          el: vantaRef.current,
          THREE: THREE,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          color: 0x23153c,
          shininess: 30,
          waveHeight: 15,
          zoom: 0.65
        })
      );
    }

    return () => {
      if (vantaEffect) vantaEffect.destroy();
    };
  }, [vantaEffect]);

  return (
    <div ref={vantaRef} style={{ width: '100%', height: '100vh' }}>
      <h1>Content over Vanta</h1>
    </div>
  );
}

export default VantaBackground;
```

---

### Vue 3

```vue
<template>
  <div ref="vantaRef" class="vanta-container">
    <slot></slot>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as THREE from 'three';
import WAVES from 'vanta/dist/vanta.waves.min.js';

const vantaRef = ref(null);
let vantaEffect = null;

onMounted(() => {
  vantaEffect = WAVES({
    el: vantaRef.value,
    THREE: THREE,
    mouseControls: true,
    touchControls: true,
    color: 0x23153c
  });
});

onUnmounted(() => {
  if (vantaEffect) vantaEffect.destroy();
});
</script>

<style scoped>
.vanta-container {
  width: 100%;
  height: 100vh;
}
</style>
```

---

### Angular

```typescript
import { Component, OnInit, OnDestroy, ElementRef, ViewChild } from '@angular/core';
import * as THREE from 'three';
import WAVES from 'vanta/dist/vanta.waves.min.js';

@Component({
  selector: 'app-vanta-bg',
  template: `
    <div #vantaRef class="vanta-container">
      <ng-content></ng-content>
    </div>
  `,
  styles: [`
    .vanta-container {
      width: 100%;
      height: 100vh;
    }
  `]
})
export class VantaBgComponent implements OnInit, OnDestroy {
  @ViewChild('vantaRef') vantaRef!: ElementRef;
  vantaEffect: any;

  ngOnInit() {
    this.vantaEffect = WAVES({
      el: this.vantaRef.nativeElement,
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      color: 0x23153c
    });
  }

  ngOnDestroy() {
    if (this.vantaEffect) this.vantaEffect.destroy();
  }
}
```

---

### Svelte

```svelte
<script>
  import { onMount, onDestroy } from 'svelte';
  import * as THREE from 'three';
  import WAVES from 'vanta/dist/vanta.waves.min.js';

  let vantaRef;
  let vantaEffect;

  onMount(() => {
    vantaEffect = WAVES({
      el: vantaRef,
      THREE: THREE,
      mouseControls: true,
      touchControls: true,
      color: 0x23153c
    });
  });

  onDestroy(() => {
    if (vantaEffect) vantaEffect.destroy();
  });
</script>

<div bind:this={vantaRef} class="vanta-container">
  <slot></slot>
</div>

<style>
  .vanta-container {
    width: 100%;
    height: 100vh;
  }
</style>
```

---

## Performance

### Optimization Tips

**1. Disable unused controls**

```javascript
VANTA.WAVES({
  el: "#vanta-bg",
  mouseControls: false,    // Disable if not needed
  touchControls: false,
  gyroControls: false
});
```

**2. Reduce complexity on mobile**

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

VANTA.WAVES({
  el: "#vanta-bg",
  scaleMobile: 0.5,        // Smaller scale
  waveHeight: isMobile ? 10 : 15,
  points: isMobile ? 5 : 10
});
```

**3. Pause when not visible**

```javascript
let vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });

let observer = new IntersectionObserver(([entry]) => {
  if (entry.isIntersecting) {
    vantaEffect.restart();
  } else {
    vantaEffect.destroy();
  }
});

observer.observe(document.querySelector("#vanta-bg"));
```

**4. Set minHeight/minWidth**

```javascript
VANTA.WAVES({
  el: "#vanta-bg",
  minHeight: 200,
  minWidth: 200
  // Effect pauses below these dimensions
});
```

**5. Use simpler effects on low-end devices**

```javascript
const isLowEnd = navigator.hardwareConcurrency <= 4;

const effect = isLowEnd
  ? VANTA.DOTS  // Simpler effect
  : VANTA.WAVES; // Complex effect

effect({ el: "#vanta-bg" });
```

---

### Effect Performance Ranking

**Most performant** (lightest):
1. DOTS
2. NET
3. RINGS
4. TOPOLOGY

**Moderate**:
5. WAVES
6. CELLS
7. FOG
8. HALO

**Intensive** (heaviest):
9. BIRDS
10. CLOUDS
11. GLOBE
12. TRUNK

---

### Mobile Fallbacks

**Option 1: Disable on mobile**

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (!isMobile) {
  VANTA.WAVES({ el: "#vanta-bg" });
} else {
  document.querySelector("#vanta-bg").style.background = '#23153c';
}
```

**Option 2: Static image fallback**

```css
.vanta-container {
  background: url('fallback-image.jpg') center/cover;
}

.vanta-container.has-vanta {
  background: none;
}
```

```javascript
VANTA.WAVES({ el: "#vanta-bg" });
document.querySelector("#vanta-bg").classList.add('has-vanta');
```

---

## Troubleshooting

### Multiple Vanta Instances

**Problem**: Only one effect renders.

**Solution**: Use unique elements.

```javascript
// ❌ Wrong - same element
VANTA.WAVES({ el: ".vanta-bg" });
VANTA.BIRDS({ el: ".vanta-bg" });

// ✅ Correct - different elements
VANTA.WAVES({ el: "#vanta-bg-1" });
VANTA.BIRDS({ el: "#vanta-bg-2" });
```

---

### Memory Leaks in SPAs

**Problem**: Effect persists after navigation.

**Solution**: Always destroy on unmount.

```javascript
// Store reference
let vantaEffect = VANTA.WAVES({ el: "#vanta-bg" });

// Cleanup (React example)
useEffect(() => {
  return () => {
    if (vantaEffect) vantaEffect.destroy();
  };
}, []);
```

---

### Color Not Changing

**Problem**: Color updates don't work.

**Solution**: Use hex numbers, not strings.

```javascript
// ❌ Wrong
vantaEffect.setOptions({ color: "#ff3f81" });

// ✅ Correct
vantaEffect.setOptions({ color: 0xff3f81 });
```

---

### Effect Not Responsive

**Problem**: Effect doesn't resize with window.

**Solution**: Call resize() or enable auto-resize.

```javascript
window.addEventListener('resize', () => {
  vantaEffect.resize();
});
```

---

## Resources

- **Official Site**: https://www.vantajs.com
- **GitHub**: https://github.com/tengbao/vanta
- **Interactive Gallery**: https://www.vantajs.com/?effect=waves
- **NPM**: `npm install vanta`

---

## License

MIT License - Free for commercial and personal use.
