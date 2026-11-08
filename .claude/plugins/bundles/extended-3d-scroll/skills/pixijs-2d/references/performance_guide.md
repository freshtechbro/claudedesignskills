# PixiJS Performance Optimization Guide

Comprehensive guide to optimizing PixiJS applications for maximum performance and smooth 60 FPS rendering.

---

## Table of Contents

1. [Performance Profiling](#performance-profiling)
2. [Rendering Optimization](#rendering-optimization)
3. [Texture Management](#texture-management)
4. [Container Optimization](#container-optimization)
5. [Filter Performance](#filter-performance)
6. [Text Rendering](#text-rendering)
7. [Memory Management](#memory-management)
8. [Mobile Optimization](#mobile-optimization)
9. [Advanced Techniques](#advanced-techniques)

---

## Performance Profiling

### Built-in Stats

```javascript
import { Application } from 'pixi.js';

const app = new Application();
await app.init({ width: 800, height: 600 });

// Access stats
app.ticker.add(() => {
  const stats = app.renderer.stats;

  console.log('FPS:', Math.round(1000 / app.ticker.deltaMS));
  console.log('Draw calls:', stats.drawCalls);
  console.log('Texture bind count:', stats.textureCount);
  console.log('Shader bind count:', stats.shaderCount);
});
```

### Custom Performance Monitor

```javascript
class PerformanceMonitor {
  constructor(app) {
    this.app = app;
    this.frameCount = 0;
    this.lastTime = performance.now();
    this.fps = 60;
    this.drawCalls = 0;

    this.createDisplay();
    this.app.ticker.add(this.update.bind(this));
  }

  createDisplay() {
    this.container = document.createElement('div');
    this.container.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0,0,0,0.8);
      color: #0f0;
      padding: 10px;
      font-family: monospace;
      font-size: 12px;
      z-index: 10000;
    `;
    document.body.appendChild(this.container);
  }

  update() {
    this.frameCount++;
    const now = performance.now();

    if (now - this.lastTime >= 1000) {
      this.fps = Math.round(this.frameCount * 1000 / (now - this.lastTime));
      this.frameCount = 0;
      this.lastTime = now;

      const stats = this.app.renderer.stats;
      this.drawCalls = stats.drawCalls.total;

      this.render();
    }
  }

  render() {
    const color = this.fps >= 55 ? '#0f0' : this.fps >= 30 ? '#ff0' : '#f00';
    this.container.style.color = color;

    this.container.innerHTML = `
      FPS: ${this.fps}<br>
      Draw Calls: ${this.drawCalls}<br>
      Sprites: ${this.countSprites()}<br>
      Memory: ${this.getMemoryUsage()}
    `;
  }

  countSprites() {
    let count = 0;
    const traverse = (container) => {
      if (container.children) {
        container.children.forEach(child => {
          count++;
          traverse(child);
        });
      }
    };
    traverse(this.app.stage);
    return count;
  }

  getMemoryUsage() {
    if (performance.memory) {
      const mb = (performance.memory.usedJSHeapSize / 1048576).toFixed(2);
      return `${mb} MB`;
    }
    return 'N/A';
  }
}

// Usage
const monitor = new PerformanceMonitor(app);
```

---

## Rendering Optimization

### 1. Use ParticleContainer for Large Sprite Counts

**Problem**: Rendering 1,000+ sprites with regular Container is slow.

**Solution**: Use ParticleContainer with static properties.

```javascript
import { ParticleContainer, Particle, Texture } from 'pixi.js';

// ❌ BAD: Regular container (slow)
const container = new Container();
for (let i = 0; i < 10000; i++) {
  const sprite = new Sprite(texture);
  sprite.x = Math.random() * 800;
  sprite.y = Math.random() * 600;
  container.addChild(sprite);
}

// ✅ GOOD: ParticleContainer (10x faster)
const particles = new ParticleContainer({
  maxSize: 10000,
  dynamicProperties: {
    position: true,   // Only if you need to update positions
    scale: false,     // Static scale
    rotation: false,  // Static rotation
    color: false      // Static color
  }
});

for (let i = 0; i < 10000; i++) {
  const particle = new Particle({
    texture,
    x: Math.random() * 800,
    y: Math.random() * 600
  });
  particles.addParticle(particle);
}

app.stage.addChild(particles);
```

**Performance Gain**: Up to 10x faster rendering for static properties.

---

### 2. Minimize Draw Calls

**Problem**: Each texture/shader switch triggers a new draw call.

**Solution**: Batch sprites with the same texture and blend mode.

```javascript
// ❌ BAD: Different textures interspersed
const sprites = [];
for (let i = 0; i < 100; i++) {
  const tex = i % 2 === 0 ? texture1 : texture2;
  sprites.push(new Sprite(tex));
}

// ✅ GOOD: Group by texture
const group1 = new Container();
const group2 = new Container();

for (let i = 0; i < 50; i++) {
  group1.addChild(new Sprite(texture1));
  group2.addChild(new Sprite(texture2));
}

app.stage.addChild(group1, group2);
```

**Tip**: Use sprite atlases (texture packing) to combine multiple images into one texture.

---

### 3. Enable Culling for Off-Screen Objects

**Problem**: Rendering objects outside viewport wastes GPU cycles.

**Solution**: Enable viewport culling.

```javascript
import { Application } from 'pixi.js';

const app = new Application();
await app.init({
  width: 800,
  height: 600,
  cullable: true  // Enable automatic culling
});

// Or per-object
sprite.cullable = true;

// Manual culling
app.ticker.add(() => {
  const bounds = app.screen;

  sprites.forEach(sprite => {
    const spriteBounds = sprite.getBounds();

    // Check if sprite is in viewport
    sprite.renderable = (
      spriteBounds.x < bounds.width &&
      spriteBounds.x + spriteBounds.width > 0 &&
      spriteBounds.y < bounds.height &&
      spriteBounds.y + spriteBounds.height > 0
    );
  });
});
```

**CullerPlugin**:
```javascript
// Automatic viewport culling plugin
import { CullerPlugin } from 'pixi.js';

// Enabled by default in Application
app.cullable = true;
```

**Performance Gain**: Up to 50% for scenes with many off-screen objects.

---

### 4. Cache Static Graphics as Bitmaps

**Problem**: Complex vector graphics re-render every frame.

**Solution**: Convert to texture using `cacheAsBitmap`.

```javascript
import { Graphics } from 'pixi.js';

const complexShape = new Graphics();

// Draw many shapes
for (let i = 0; i < 100; i++) {
  complexShape.circle(
    Math.random() * 200,
    Math.random() * 200,
    Math.random() * 10
  ).fill(Math.random() * 0xffffff);
}

// ✅ Cache as bitmap for static graphics
complexShape.cacheAsBitmap = true;

// ❌ Don't use for frequently changing graphics
// complexShape.cacheAsBitmap = false;  // If updating often
```

**When to Use**:
- ✅ Static UI elements
- ✅ Backgrounds
- ✅ Complex shapes that don't change
- ❌ Animated graphics
- ❌ Frequently updated elements

---

### 5. Reduce Resolution on Low-End Devices

**Problem**: High-resolution rendering on mobile drains battery and causes lag.

**Solution**: Adjust resolution based on device capabilities.

```javascript
const isMobile = /Mobi|Android/i.test(navigator.userAgent);
const resolution = isMobile ? 1 : window.devicePixelRatio || 1;

const app = new Application();
await app.init({
  width: 800,
  height: 600,
  resolution,
  autoDensity: true
});

// Dynamic resolution scaling
function adjustResolution() {
  const fps = Math.round(1000 / app.ticker.deltaMS);

  if (fps < 30 && app.renderer.resolution > 1) {
    app.renderer.resolution *= 0.9;
  } else if (fps > 55 && app.renderer.resolution < window.devicePixelRatio) {
    app.renderer.resolution = Math.min(app.renderer.resolution * 1.1, window.devicePixelRatio);
  }
}

app.ticker.add(adjustResolution);
```

---

## Texture Management

### 1. Destroy Unused Textures

**Problem**: Textures consume GPU memory even when not displayed.

**Solution**: Explicitly destroy textures when done.

```javascript
import { Texture } from 'pixi.js';

const texture = Texture.from('image.png');
const sprite = new Sprite(texture);

// When done
sprite.destroy({ texture: true, baseTexture: true });

// Or destroy texture directly
texture.destroy(true);  // true = also destroy baseTexture
```

**Batch Destruction with Delay**:
```javascript
// Prevent frame drops by staggering destruction
const textures = [tex1, tex2, tex3, tex4];

textures.forEach((tex, index) => {
  setTimeout(() => {
    tex.destroy(true);
  }, index * 50 + Math.random() * 50);
});
```

---

### 2. Use Texture Atlases (Sprite Sheets)

**Problem**: Loading many individual images causes numerous HTTP requests and draw calls.

**Solution**: Pack images into sprite sheets.

```javascript
import { Assets, Sprite } from 'pixi.js';

// Load sprite sheet
await Assets.load('spritesheet.json');

// Access individual frames
const texture1 = Texture.from('frame1.png');
const texture2 = Texture.from('frame2.png');

const sprite1 = new Sprite(texture1);
const sprite2 = new Sprite(texture2);

// All batched in single draw call
app.stage.addChild(sprite1, sprite2);
```

**Tools for Creating Sprite Sheets**:
- TexturePacker: https://www.codeandweb.com/texturepacker
- ShoeBox: https://renderhjs.net/shoebox/
- Free Texture Packer: https://free-tex-packer.com/

---

### 3. Optimize Texture Sizes

**Problem**: Large textures consume excessive memory.

**Solution**: Use appropriate sizes and compression.

```javascript
// ❌ BAD: 4096x4096 texture (64MB RGBA)
const hugeTexture = Texture.from('huge-image-4k.png');

// ✅ GOOD: 1024x1024 texture (4MB RGBA)
const optimizedTexture = Texture.from('optimized-image-1k.png');

// Power-of-2 sizes for best performance
// Good sizes: 256, 512, 1024, 2048
// Avoid odd sizes: 300, 500, 1500

// Use NEAREST for pixel art
texture.baseTexture.scaleMode = SCALE_MODES.NEAREST;

// Use LINEAR for photos
texture.baseTexture.scaleMode = SCALE_MODES.LINEAR;
```

---

### 4. Lazy Load Assets

**Problem**: Loading all assets upfront delays game start.

**Solution**: Load assets on-demand.

```javascript
import { Assets } from 'pixi.js';

// Preload critical assets
const criticalAssets = await Assets.load([
  'ui/background.png',
  'ui/logo.png'
]);

// Background load game assets
Assets.backgroundLoad([
  'characters/hero.png',
  'characters/enemy.png',
  'levels/level1.jpg'
]);

// Check if asset is loaded
if (Assets.cache.has('characters/hero.png')) {
  const heroTexture = Assets.get('characters/hero.png');
  const hero = new Sprite(heroTexture);
}

// Load on-demand
async function showLevel(levelNumber) {
  const levelTexture = await Assets.load(`levels/level${levelNumber}.jpg`);
  // Use texture
}
```

---

## Container Optimization

### 1. Disable Unnecessary Features

```javascript
import { Container } from 'pixi.js';

const container = new Container();

// ❌ Don't enable unless needed
container.sortableChildren = false;  // Z-index sorting (expensive)
container.interactiveChildren = false;  // Child interaction (expensive)

// ✅ Enable only when required
if (needsSorting) {
  container.sortableChildren = true;
}
```

---

### 2. Use Object Pooling

**Problem**: Creating/destroying objects causes garbage collection pauses.

**Solution**: Reuse objects via pooling.

```javascript
class SpritePool {
  constructor(texture, initialSize = 100) {
    this.texture = texture;
    this.available = [];
    this.active = [];

    for (let i = 0; i < initialSize; i++) {
      this.createSprite();
    }
  }

  createSprite() {
    const sprite = new Sprite(this.texture);
    sprite.visible = false;
    this.available.push(sprite);
    return sprite;
  }

  spawn(x, y) {
    let sprite = this.available.pop();

    if (!sprite) {
      sprite = this.createSprite();
    }

    sprite.position.set(x, y);
    sprite.visible = true;
    this.active.push(sprite);

    return sprite;
  }

  despawn(sprite) {
    sprite.visible = false;
    const index = this.active.indexOf(sprite);

    if (index > -1) {
      this.active.splice(index, 1);
      this.available.push(sprite);
    }
  }

  reset() {
    this.active.forEach(sprite => {
      sprite.visible = false;
      this.available.push(sprite);
    });
    this.active = [];
  }
}

// Usage
const bulletPool = new SpritePool(bulletTexture, 50);

// Spawn
const bullet = bulletPool.spawn(100, 200);
app.stage.addChild(bullet);

// Despawn
bulletPool.despawn(bullet);
```

**Performance Gain**: Eliminates GC pauses, smoother frame times.

---

### 3. Flatten Hierarchy

**Problem**: Deep nesting requires traversing many containers.

**Solution**: Keep hierarchy shallow when possible.

```javascript
// ❌ BAD: Deep nesting
const root = new Container();
const level1 = new Container();
const level2 = new Container();
const level3 = new Container();

root.addChild(level1);
level1.addChild(level2);
level2.addChild(level3);
level3.addChild(sprite);

// ✅ GOOD: Flat structure
const root = new Container();
root.addChild(sprite);

// Use position offsets instead of nested containers
sprite.x = parentX + childX;
sprite.y = parentY + childY;
```

---

## Filter Performance

### 1. Limit Filter Usage

**Problem**: Filters are expensive WebGL operations.

**Solution**: Use sparingly, optimize where possible.

```javascript
import { BlurFilter } from 'pixi.js';

// ❌ BAD: Filter on every sprite
sprites.forEach(sprite => {
  sprite.filters = [new BlurFilter()];
});

// ✅ GOOD: Filter on container
const container = new Container();
sprites.forEach(sprite => container.addChild(sprite));
container.filters = [new BlurFilter()];

// ✅ BETTER: Bake filter into texture
const filteredTexture = renderer.filters.generateFilteredTexture({
  texture: originalTexture,
  filters: [new BlurFilter({ strength: 5 })]
});

const sprite = new Sprite(filteredTexture);
```

---

### 2. Specify Filter Area

**Problem**: PixiJS measures filter bounds at runtime (expensive).

**Solution**: Manually specify `filterArea`.

```javascript
import { BlurFilter, Rectangle } from 'pixi.js';

const sprite = new Sprite(texture);
sprite.filters = [new BlurFilter()];

// ✅ Specify filter area for performance
sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);

// Update if sprite resizes
sprite.on('resize', () => {
  sprite.filterArea = new Rectangle(0, 0, sprite.width, sprite.height);
});
```

**Performance Gain**: Avoids runtime bounds calculation.

---

### 3. Release Filters When Not Needed

```javascript
// Enable filter
sprite.filters = [new BlurFilter()];

// Disable filter (releases GPU memory)
sprite.filters = null;

// Toggle based on game state
if (gameState === 'paused') {
  sprite.filters = [new BlurFilter()];
} else {
  sprite.filters = null;
}
```

---

## Text Rendering

### 1. Use BitmapText for Dynamic Text

**Problem**: Standard Text re-renders texture on every update.

**Solution**: Use BitmapText for frequently changing text.

```javascript
import { Text, BitmapText } from 'pixi.js';

// ❌ BAD: Standard Text (expensive updates)
const scoreText = new Text({ text: 'Score: 0' });

app.ticker.add(() => {
  scoreText.text = `Score: ${++score}`;  // Re-renders texture every frame
});

// ✅ GOOD: BitmapText (much faster)
const scoreBitmap = new BitmapText({
  text: 'Score: 0',
  style: { fontFamily: 'MyBitmapFont', fontSize: 24 }
});

app.ticker.add(() => {
  scoreBitmap.text = `Score: ${++score}`;  // Fast glyph updates
});
```

**Performance**: BitmapText is 10-50x faster for dynamic text.

---

### 2. Reduce Text Resolution

**Problem**: High-resolution text consumes memory.

**Solution**: Lower resolution for less critical text.

```javascript
import { Text, TextStyle } from 'pixi.js';

const style = new TextStyle({ fontSize: 36 });
const text = new Text({ text: 'Hello', style });

// Default resolution matches renderer (e.g., 2 on Retina)
text.resolution = 1;  // Reduce to 1 for memory savings

// Still looks good, uses less memory
```

---

### 3. Bake Filters into Text

**Problem**: Runtime filters on text are expensive.

**Solution**: Apply filters at texture creation.

```javascript
import { Text, TextStyle, BlurFilter } from 'pixi.js';

const style = new TextStyle({
  fontFamily: 'Arial',
  fontSize: 36,
  fill: '#ffffff',
  filters: [new BlurFilter()]  // Baked into texture at creation
});

const text = new Text({ text: 'Glowing Text', style });

// Filter applied once at creation, not every frame
```

---

## Memory Management

### 1. Destroy Display Objects Properly

```javascript
import { Sprite, Container } from 'pixi.js';

const sprite = new Sprite(texture);
const container = new Container();

// ✅ GOOD: Destroy with options
sprite.destroy({
  children: true,      // Destroy children
  texture: false,      // Keep texture (if used elsewhere)
  baseTexture: false   // Keep baseTexture
});

// Destroy container and all children
container.destroy({ children: true });

// Destroy texture when completely done
texture.destroy(true);  // true = also destroy baseTexture
```

---

### 2. Clear Event Listeners

```javascript
const sprite = new Sprite(texture);

sprite.on('pointerdown', onPointerDown);
sprite.on('pointermove', onPointerMove);

// ✅ Remove listeners before destroying
sprite.off('pointerdown', onPointerDown);
sprite.off('pointermove', onPointerMove);

// Or remove all
sprite.removeAllListeners();

sprite.destroy();
```

---

### 3. Monitor Memory Usage

```javascript
function logMemoryUsage() {
  if (performance.memory) {
    const used = (performance.memory.usedJSHeapSize / 1048576).toFixed(2);
    const total = (performance.memory.totalJSHeapSize / 1048576).toFixed(2);
    const limit = (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2);

    console.log(`Memory: ${used}MB / ${total}MB (Limit: ${limit}MB)`);
  }
}

setInterval(logMemoryUsage, 5000);
```

---

## Mobile Optimization

### 1. Disable Anti-Aliasing

```javascript
const app = new Application();
await app.init({
  width: 800,
  height: 600,
  antialias: false,  // Faster on mobile
  resolution: 1       // Lower resolution
});
```

---

### 2. Reduce Particle Count

```javascript
const isMobile = /Mobi|Android/i.test(navigator.userAgent);
const particleCount = isMobile ? 1000 : 5000;

for (let i = 0; i < particleCount; i++) {
  particles.addParticle(new Particle({ texture }));
}
```

---

### 3. Limit Frame Rate on Battery

```javascript
import { Ticker } from 'pixi.js';

function checkBattery() {
  if ('getBattery' in navigator) {
    navigator.getBattery().then(battery => {
      if (battery.charging === false && battery.level < 0.2) {
        Ticker.shared.maxFPS = 30;  // Reduce to 30 FPS
      } else {
        Ticker.shared.maxFPS = 60;
      }
    });
  }
}

checkBattery();
```

---

## Advanced Techniques

### 1. Use WebWorkers for Heavy Calculations

```javascript
// worker.js
self.onmessage = function(e) {
  const { particles, delta } = e.data;

  // Update particle physics
  particles.forEach(p => {
    p.vx += (Math.random() - 0.5) * 0.1;
    p.vy += 0.05;
    p.x += p.vx * delta;
    p.y += p.vy * delta;
  });

  self.postMessage(particles);
};

// main.js
const worker = new Worker('worker.js');

worker.onmessage = function(e) {
  const updatedParticles = e.data;

  // Apply to PixiJS particles
  updatedParticles.forEach((data, i) => {
    particles.particleChildren[i].x = data.x;
    particles.particleChildren[i].y = data.y;
  });
};

app.ticker.add((ticker) => {
  const particleData = particles.particleChildren.map(p => ({
    x: p.x,
    y: p.y,
    vx: p.vx || 0,
    vy: p.vy || 0
  }));

  worker.postMessage({ particles: particleData, delta: ticker.deltaTime });
});
```

---

### 2. Implement Spatial Hashing for Collision Detection

```javascript
class SpatialHash {
  constructor(cellSize) {
    this.cellSize = cellSize;
    this.grid = new Map();
  }

  clear() {
    this.grid.clear();
  }

  insert(sprite) {
    const cells = this.getCells(sprite);
    cells.forEach(cell => {
      const key = `${cell.x},${cell.y}`;
      if (!this.grid.has(key)) {
        this.grid.set(key, []);
      }
      this.grid.get(key).push(sprite);
    });
  }

  getCells(sprite) {
    const bounds = sprite.getBounds();
    const cells = [];

    const minX = Math.floor(bounds.x / this.cellSize);
    const maxX = Math.floor((bounds.x + bounds.width) / this.cellSize);
    const minY = Math.floor(bounds.y / this.cellSize);
    const maxY = Math.floor((bounds.y + bounds.height) / this.cellSize);

    for (let x = minX; x <= maxX; x++) {
      for (let y = minY; y <= maxY; y++) {
        cells.push({ x, y });
      }
    }

    return cells;
  }

  getNearby(sprite) {
    const cells = this.getCells(sprite);
    const nearby = new Set();

    cells.forEach(cell => {
      const key = `${cell.x},${cell.y}`;
      const sprites = this.grid.get(key);
      if (sprites) {
        sprites.forEach(s => {
          if (s !== sprite) nearby.add(s);
        });
      }
    });

    return Array.from(nearby);
  }
}

// Usage
const spatialHash = new SpatialHash(100);

app.ticker.add(() => {
  spatialHash.clear();

  // Insert all sprites
  sprites.forEach(sprite => spatialHash.insert(sprite));

  // Check collisions only with nearby sprites
  sprites.forEach(sprite => {
    const nearby = spatialHash.getNearby(sprite);
    nearby.forEach(other => {
      if (checkCollision(sprite, other)) {
        handleCollision(sprite, other);
      }
    });
  });
});
```

**Performance**: O(n) instead of O(n²) for collision detection.

---

## Performance Checklist

✅ **Rendering**
- [ ] Use ParticleContainer for 1,000+ sprites
- [ ] Batch sprites by texture
- [ ] Enable culling for off-screen objects
- [ ] Cache static graphics as bitmaps
- [ ] Minimize draw calls

✅ **Textures**
- [ ] Destroy unused textures
- [ ] Use sprite atlases
- [ ] Optimize texture sizes (power-of-2)
- [ ] Lazy load non-critical assets

✅ **Containers**
- [ ] Disable sortableChildren unless needed
- [ ] Use object pooling
- [ ] Keep hierarchy shallow

✅ **Filters**
- [ ] Limit filter usage (1-2 per scene)
- [ ] Specify filterArea
- [ ] Release filters when not needed
- [ ] Bake filters into textures

✅ **Text**
- [ ] Use BitmapText for dynamic text
- [ ] Reduce text resolution
- [ ] Bake filters into TextStyle

✅ **Memory**
- [ ] Destroy objects properly
- [ ] Clear event listeners
- [ ] Monitor memory usage

✅ **Mobile**
- [ ] Disable anti-aliasing
- [ ] Reduce particle counts
- [ ] Lower resolution
- [ ] Limit frame rate on battery

---

## Debugging Performance Issues

### Identify Bottlenecks

```javascript
// Measure specific operations
console.time('particleUpdate');
updateParticles();
console.timeEnd('particleUpdate');

// Profile draw calls
console.log('Draw calls:', app.renderer.stats.drawCalls.total);

// Check texture count
console.log('Textures bound:', app.renderer.stats.textureCount);
```

### Common Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Low FPS | Too many draw calls | Batch sprites, use atlases |
| Stuttering | GC pauses | Use object pooling |
| High memory | Texture leaks | Destroy textures properly |
| Slow filters | Too many filters | Limit usage, bake into textures |
| Laggy text | Text updates | Use BitmapText |

---

This guide provides comprehensive strategies for optimizing PixiJS applications to achieve smooth 60 FPS performance across devices.
