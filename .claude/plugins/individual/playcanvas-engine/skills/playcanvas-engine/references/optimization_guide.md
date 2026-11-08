# PlayCanvas Optimization Guide

Comprehensive performance optimization strategies for PlayCanvas applications.

---

## Table of Contents

1. [Performance Profiling](#performance-profiling)
2. [Rendering Optimization](#rendering-optimization)
3. [Asset Optimization](#asset-optimization)
4. [Memory Management](#memory-management)
5. [Script Optimization](#script-optimization)
6. [Mobile Optimization](#mobile-optimization)
7. [Network & Loading](#network--loading)

---

## Performance Profiling

### Built-in Profiler

**Enable Profiler**:
```javascript
// In code
app.stats = new pc.ApplicationStats(app.graphicsDevice);

// Show FPS counter
const container = document.createElement('div');
document.body.appendChild(container);
container.style.cssText = 'position:absolute;top:10px;left:10px;color:white;background:rgba(0,0,0,0.5);padding:10px;font-family:monospace;';

app.on('update', () => {
  if (app.stats) {
    container.textContent = [
      `FPS: ${Math.round(1 / app.stats.frame.updateTime * 1000)}`,
      `Draw Calls: ${app.stats.drawCalls.total}`,
      `Triangles: ${app.stats.triangles.total}`,
      `Shaders: ${app.stats.shaders}`,
      `Materials: ${app.stats.materials}`,
      `Textures: ${app.stats.vram.tex / 1024 / 1024}MB`
    ].join('\n');
  }
});
```

---

### Browser DevTools

**Performance Tab**:
- Record session
- Analyze frame timing
- Identify bottlenecks

**Key Metrics**:
- **Frame Time**: Should be < 16.67ms (60 FPS)
- **Script Time**: JavaScript execution
- **Rendering**: GPU work
- **Paint**: Browser compositing

**Console Profiling**:
```javascript
console.time('sceneLoad');
// ... load scene ...
console.timeEnd('sceneLoad');

console.profile('gameLoop');
// ... run game ...
console.profileEnd('gameLoop');
```

---

### Common Performance Bottlenecks

**Symptoms**:
```
Low FPS (< 30):
  → Too many draw calls
  → Complex materials/shaders
  → Too many triangles
  → Unoptimized scripts

High Memory Usage:
  → Large textures
  → Memory leaks
  → Too many entities

Slow Loading:
  → Large assets
  → Uncompressed textures
  → Synchronous loading
```

---

## Rendering Optimization

### 1. Reduce Draw Calls

**Problem**: Each mesh = 1 draw call. Too many = slow.

**Target**: < 100 draw calls for 60 FPS

**Solution 1: Static Batching**
```javascript
// Mark entities as static
entity.model.batchGroupId = 1;
entity2.model.batchGroupId = 1;
entity3.model.batchGroupId = 1;

// Batch all with same ID
app.batcher.generate([entity, entity2, entity3]);
```

**Solution 2: Combine Meshes**
```javascript
// Merge multiple meshes into one
// In 3D software before import, or use:

const combinedMesh = new pc.Mesh(app.graphicsDevice);
// ... combine vertex data ...
```

**Solution 3: Use Instancing**
```javascript
// For repeated objects (trees, rocks, etc.)
const mesh = entity.model.meshInstances[0];
mesh.instancingData = {
  count: 100,
  transforms: transformMatrices  // Array of Mat4
};
```

---

### 2. LOD (Level of Detail)

Reduce geometry for distant objects.

```javascript
// Manual LOD switching
const LOD_DISTANCES = [10, 50, 100];
const LOD_MODELS = [highResModel, mediumResModel, lowResModel];

app.on('update', () => {
  const distance = camera.getPosition().distance(entity.getPosition());

  let lodLevel = 0;
  for (let i = 0; i < LOD_DISTANCES.length; i++) {
    if (distance > LOD_DISTANCES[i]) {
      lodLevel = i + 1;
    }
  }

  entity.model.asset = LOD_MODELS[lodLevel];
});
```

**Better: Use Model Component LOD**
```javascript
entity.model.meshInstances[0].lodLevel = 0;  // High detail
// Automatically switches based on screen size
```

---

### 3. Frustum Culling

Don't render off-screen objects (automatic in PlayCanvas).

**Verify it's enabled**:
```javascript
camera.camera.frustumCulling = true;  // Should be true by default
```

**Manual Culling**:
```javascript
// Disable entities outside camera frustum
app.on('update', () => {
  entities.forEach(entity => {
    const inFrustum = camera.camera.frustum.containsPoint(entity.getPosition());
    entity.enabled = inFrustum;
  });
});
```

---

### 4. Occlusion Culling

Don't render objects blocked by other objects.

```javascript
// Not built-in, manual implementation:
function isOccluded(entity, camera) {
  const from = camera.getPosition();
  const to = entity.getPosition();

  const result = app.systems.rigidbody.raycastFirst(from, to);

  return result && result.entity !== entity;
}

app.on('update', () => {
  entities.forEach(entity => {
    entity.enabled = !isOccluded(entity, camera);
  });
});
```

---

### 5. Reduce Triangle Count

**Guidelines**:
- Characters: 5k-15k triangles
- Props: 500-2k triangles
- Environment: Use LOD

**Tools**:
- Blender: Decimate modifier
- Editor: Import at lower resolution

**Check Triangle Count**:
```javascript
console.log('Triangles:', app.stats.triangles.total);
```

---

### 6. Optimize Materials

**Avoid**:
- Too many unique materials (each = draw call)
- Complex shaders
- Unnecessary texture maps

**Do**:
- Reuse materials across objects
- Use material instances
- Disable unused features

```javascript
// Create material instance
const material = new pc.StandardMaterial();
material.diffuse = new pc.Color(1, 0, 0);
material.update();

// Reuse across entities
entity1.model.material = material;
entity2.model.material = material;
entity3.model.material = material;
// Still 3 draw calls, but same material
```

**Disable Unused Maps**:
```javascript
const material = new pc.StandardMaterial();
material.diffuse = new pc.Color(1, 0, 0);
// Don't set diffuseMap, normalMap, etc. if not needed
material.update();
```

---

### 7. Shadow Optimization

Shadows are expensive.

**Reduce Shadow Casters**:
```javascript
// Only important objects cast shadows
importantEntity.model.castShadows = true;
insignificantEntity.model.castShadows = false;
```

**Shadow Quality Settings**:
```javascript
light.light.shadowDistance = 40;      // Lower = better perf
light.light.shadowResolution = 1024;  // Lower = better perf (default 2048)
light.light.shadowType = pc.SHADOW_PCF3;  // PCF3 faster than PCF5
```

**Disable Shadows on Mobile**:
```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

if (isMobile) {
  app.root.findByTag('light').forEach(entity => {
    entity.light.castShadows = false;
  });
}
```

---

## Asset Optimization

### 1. Texture Compression

**Problem**: Uncompressed textures use lots of memory.

**Solution**: Use compressed formats.

```javascript
// In Editor: Select texture → Inspector → Compression

// Recommended:
// Desktop: DXT (BC1-BC7)
// iOS: PVRTC or ASTC
// Android: ETC2 or ASTC
// Universal: Basis Universal
```

**Texture Size Guidelines**:
- **UI**: 512x512 max
- **Props**: 1024x1024
- **Characters**: 2048x2048
- **Terrain**: 4096x4096 (with tiling)

**Power-of-2 Sizes**: Always use 256, 512, 1024, 2048, 4096

---

### 2. Model Optimization

**Before Import**:
- Remove non-visible geometry
- Merge vertices
- Triangulate meshes
- Bake transforms

**Vertex Count**:
- **Low**: < 5k vertices
- **Medium**: 5k-20k vertices
- **High**: 20k-50k vertices
- **Very High**: > 50k (use LOD)

**File Formats**:
- **Best**: `.glb` (binary glTF, compressed)
- **Good**: `.gltf` (text glTF)
- **Avoid**: `.fbx`, `.obj` (not optimized for web)

---

### 3. Audio Optimization

**Format**:
- **Desktop**: `.mp3` or `.ogg`
- **Mobile**: `.mp3` (better compatibility)

**Compression**:
- Music: 128 kbps
- SFX: 64 kbps

**Loading**:
```javascript
// Preload critical sounds
sound.sound.play('sfx', {
  volume: 0  // Silent preload
});

// Lazy load music
if (inMenuScene) {
  loadMusicAsset();
}
```

---

### 4. Texture Atlases

Combine multiple textures into one.

**Manual Atlas**:
```javascript
// Instead of:
// texture1.png, texture2.png, texture3.png

// Use:
// atlas.png (contains all three)

// Update UVs to reference correct portion
```

**Benefits**:
- Fewer texture bindings
- Reduced draw calls
- Better batching

---

## Memory Management

### 1. Asset Cleanup

**Problem**: Loaded assets stay in memory forever.

**Solution**: Unload when not needed.

```javascript
// Load asset
const asset = new pc.Asset('model', 'container', { url: '/model.glb' });
app.assets.add(asset);
app.assets.load(asset);

// Later, when done:
app.assets.remove(asset);
asset.unload();
```

**Scene Transition**:
```javascript
function loadScene(sceneName) {
  // Clean up current scene assets
  const oldAssets = currentSceneAssets;
  oldAssets.forEach(asset => {
    app.assets.remove(asset);
    asset.unload();
  });

  // Load new scene
  const sceneAsset = new pc.Asset(sceneName, 'scene', { url: `/${sceneName}.json` });
  app.assets.add(sceneAsset);
  app.assets.load(sceneAsset);

  currentSceneAssets = [sceneAsset];
}
```

---

### 2. Entity Pooling

Reuse entities instead of creating/destroying.

```javascript
class EntityPool {
  constructor(app, template, count) {
    this.app = app;
    this.pool = [];
    this.active = [];

    for (let i = 0; i < count; i++) {
      const entity = template.clone();
      entity.enabled = false;
      app.root.addChild(entity);
      this.pool.push(entity);
    }
  }

  spawn(position) {
    let entity = this.pool.pop();

    if (!entity) {
      console.warn('Pool exhausted, consider increasing size');
      return null;
    }

    entity.enabled = true;
    entity.setPosition(position);
    this.active.push(entity);

    return entity;
  }

  despawn(entity) {
    entity.enabled = false;

    const index = this.active.indexOf(entity);
    if (index > -1) {
      this.active.splice(index, 1);
      this.pool.push(entity);
    }
  }

  reset() {
    this.active.forEach(entity => this.despawn(entity));
  }
}

// Usage
const bulletTemplate = new pc.Entity('bullet');
bulletTemplate.addComponent('model', { type: 'sphere' });
bulletTemplate.addComponent('rigidbody', { type: pc.BODYTYPE_DYNAMIC });

const bulletPool = new EntityPool(app, bulletTemplate, 100);

// Spawn bullet
const bullet = bulletPool.spawn(new pc.Vec3(0, 0, 0));

// Later, despawn
bulletPool.despawn(bullet);
```

---

### 3. Texture Memory

**Monitor Texture Memory**:
```javascript
console.log('Texture VRAM:', app.stats.vram.tex / 1024 / 1024, 'MB');
```

**Targets**:
- **Desktop**: < 500 MB
- **Mobile**: < 200 MB

**Optimization**:
- Use mipmaps
- Enable texture compression
- Reduce texture sizes
- Unload unused textures

---

### 4. Garbage Collection

Minimize object creation in update loop.

```javascript
// ❌ Bad - creates new object every frame
app.on('update', (dt) => {
  const forward = new pc.Vec3(0, 0, -1);  // GC pressure!
  entity.translate(forward.mulScalar(speed * dt));
});

// ✅ Good - reuse objects
const forward = new pc.Vec3(0, 0, -1);  // Created once

app.on('update', (dt) => {
  const movement = forward.clone().mulScalar(speed * dt);
  entity.translate(movement);
});

// ✅ Better - pre-allocate
const forward = new pc.Vec3(0, 0, -1);
const movement = new pc.Vec3();

app.on('update', (dt) => {
  movement.copy(forward).mulScalar(speed * dt);
  entity.translate(movement);
});
```

---

## Script Optimization

### 1. Reduce Update Frequency

Not everything needs to update every frame.

```javascript
var MyScript = pc.createScript('myScript');

MyScript.prototype.initialize = function() {
  this.updateTimer = 0;
  this.updateInterval = 0.1;  // Update every 100ms instead of every frame
};

MyScript.prototype.update = function(dt) {
  this.updateTimer += dt;

  if (this.updateTimer >= this.updateInterval) {
    this.updateTimer = 0;
    this.expensiveUpdate();
  }
};

MyScript.prototype.expensiveUpdate = function() {
  // Heavy computation here
};
```

---

### 2. Event-Based Instead of Polling

```javascript
// ❌ Bad - checks every frame
app.on('update', () => {
  if (player.health <= 0) {
    gameOver();
  }
});

// ✅ Good - event-based
player.on('health:changed', (health) => {
  if (health <= 0) {
    gameOver();
  }
});
```

---

### 3. Cache Expensive Lookups

```javascript
// ❌ Bad - searches scene graph every frame
app.on('update', (dt) => {
  const player = app.root.findByName('Player');
  player.translate(0, 0, -speed * dt);
});

// ✅ Good - cache reference
const player = app.root.findByName('Player');

app.on('update', (dt) => {
  player.translate(0, 0, -speed * dt);
});
```

---

### 4. Avoid String Concatenation

```javascript
// ❌ Slower
const id = 'entity_' + index;

// ✅ Faster
const id = `entity_${index}`;

// ✅ Even faster - use numbers when possible
const id = index;
```

---

### 5. Use Object Pooling for Vectors

```javascript
// Vector pool
const VectorPool = {
  pool: [],

  get() {
    return this.pool.length > 0 ? this.pool.pop() : new pc.Vec3();
  },

  release(vec) {
    vec.set(0, 0, 0);
    this.pool.push(vec);
  }
};

// Usage
app.on('update', (dt) => {
  const direction = VectorPool.get();
  direction.set(0, 0, -1).mulScalar(speed * dt);
  entity.translate(direction);
  VectorPool.release(direction);
});
```

---

## Mobile Optimization

### 1. Detect Mobile

```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const isLowEnd = navigator.hardwareConcurrency <= 4;
```

---

### 2. Quality Settings

```javascript
if (isMobile) {
  // Reduce shadow quality
  app.root.findByTag('light').forEach(entity => {
    entity.light.castShadows = false;
  });

  // Reduce resolution
  app.graphicsDevice.maxPixelRatio = 1;

  // Disable post-processing
  camera.camera.disablePostProcessing = true;

  // Reduce texture quality
  app.assets.findAll('texture').forEach(asset => {
    asset.resource.minFilter = pc.FILTER_NEAREST;
  });
}
```

---

### 3. Mobile-Specific Textures

```javascript
function loadTexture(basePath, isMobile) {
  const size = isMobile ? '512' : '2048';
  const url = `${basePath}_${size}.jpg`;

  const asset = new pc.Asset('texture', 'texture', { url });
  app.assets.add(asset);
  app.assets.load(asset);

  return asset;
}

const texture = loadTexture('/textures/character', isMobile);
```

---

### 4. Touch Optimization

```javascript
// Throttle touch events
let lastTouch = 0;
const throttleMs = 16;  // ~60fps

app.touch.on(pc.EVENT_TOUCHMOVE, (event) => {
  const now = Date.now();
  if (now - lastTouch < throttleMs) return;

  lastTouch = now;
  handleTouch(event);
});
```

---

## Network & Loading

### 1. Asset Loading Strategy

**Preload Critical Assets**:
```javascript
const criticalAssets = [
  playerModel,
  playerTexture,
  uiFont
];

let loaded = 0;

criticalAssets.forEach(asset => {
  asset.ready(() => {
    loaded++;
    if (loaded === criticalAssets.length) {
      startGame();
    }
  });

  app.assets.load(asset);
});
```

**Lazy Load Optional Assets**:
```javascript
// Load music only when needed
function playMusic() {
  if (!musicAsset.loaded) {
    musicAsset.ready(() => {
      entity.sound.play('music');
    });
    app.assets.load(musicAsset);
  } else {
    entity.sound.play('music');
  }
}
```

---

### 2. Progressive Loading

```javascript
// Load in stages
async function loadGame() {
  // Stage 1: UI
  await loadAssets(uiAssets);
  showMainMenu();

  // Stage 2: Player
  await loadAssets(playerAssets);

  // Stage 3: Environment
  await loadAssets(environmentAssets);

  // Stage 4: Enemies (background)
  loadAssets(enemyAssets);  // Don't wait

  enableStartButton();
}
```

---

### 3. Asset Compression

**Enable gzip on server**:
```javascript
// .htaccess (Apache)
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE application/json
  AddOutputFilterByType DEFLATE application/javascript
  AddOutputFilterByType DEFLATE text/css
</IfModule>
```

**Use CDN**:
- Faster asset delivery
- Reduced server load
- Geographic distribution

---

### 4. Loading Screen

```javascript
let loadedAssets = 0;
const totalAssets = assets.length;

assets.forEach(asset => {
  asset.on('load', () => {
    loadedAssets++;
    const progress = loadedAssets / totalAssets;
    updateLoadingBar(progress);
  });

  app.assets.load(asset);
});

function updateLoadingBar(progress) {
  document.getElementById('progress-bar').style.width = `${progress * 100}%`;
  document.getElementById('progress-text').textContent = `${Math.round(progress * 100)}%`;
}
```

---

## Performance Checklist

### Before Launch

- [ ] **Draw calls < 100** (check profiler)
- [ ] **FPS ≥ 60** on target devices
- [ ] **Texture memory < 500MB** desktop, < 200MB mobile
- [ ] **All textures compressed** (Basis/DXT/ETC)
- [ ] **All textures power-of-2** sizes
- [ ] **Triangle count reasonable** for target (< 100k total)
- [ ] **Shadows optimized** (low resolution, distance limit)
- [ ] **LOD implemented** for complex models
- [ ] **Entity pooling** for frequently spawned objects
- [ ] **Assets cleaned up** on scene transitions
- [ ] **Loading screen** implemented
- [ ] **Mobile testing** complete
- [ ] **Network optimization** (gzip, CDN)
- [ ] **No memory leaks** (test long sessions)

---

## Debugging Performance Issues

### Identify Bottleneck

**Step 1: Check FPS**
```javascript
console.log('FPS:', Math.round(1 / app.stats.frame.updateTime * 1000));
```

**Step 2: Check Draw Calls**
```javascript
console.log('Draw calls:', app.stats.drawCalls.total);
```
- If > 200: Reduce meshes, enable batching

**Step 3: Check Triangles**
```javascript
console.log('Triangles:', app.stats.triangles.total);
```
- If > 500k: Reduce geometry, use LOD

**Step 4: Check Texture Memory**
```javascript
console.log('Texture VRAM:', app.stats.vram.tex / 1024 / 1024, 'MB');
```
- If > 500MB: Compress textures, reduce sizes

**Step 5: Profile Scripts**
```javascript
console.profile('update');
app.on('update', (dt) => {
  // Game logic
});
console.profileEnd('update');
```
- Check DevTools Performance tab

---

## Resources

- **Optimization Tutorial**: https://developer.playcanvas.com/en/tutorials/optimization/
- **Best Practices**: https://developer.playcanvas.com/en/user-manual/optimization/
- **Profiling Guide**: https://developer.playcanvas.com/en/user-manual/optimization/profiling/

---

## Quick Wins

**5-Minute Optimizations**:

1. **Enable texture compression** (Basis Universal)
2. **Disable shadows on mobile**
3. **Reduce shadow resolution** to 1024
4. **Enable frustum culling**
5. **Cache entity lookups**
6. **Use entity pooling** for bullets/particles
7. **Compress textures** to power-of-2 sizes
8. **Batch static geometry**
9. **Disable invisible entities**
10. **Throttle expensive update calls**

---

This guide covers all major optimization strategies. Apply these techniques to achieve 60 FPS on your target platform.
