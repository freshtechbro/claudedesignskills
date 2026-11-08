# Three.js Performance Optimization Checklist

## Quick Wins (High Impact, Low Effort)

### ✅ Geometry Optimization

- [ ] **Reuse geometries** across multiple meshes
  ```javascript
  const sharedGeometry = new THREE.BoxGeometry(1, 1, 1);
  // Use for all boxes instead of creating new geometry each time
  ```

- [ ] **Use InstancedMesh** for repeated objects (>50 identical objects)
  ```javascript
  const mesh = new THREE.InstancedMesh(geometry, material, 1000);
  ```

- [ ] **Reduce polygon count** where not visible
  - Use simpler geometries for distant objects
  - Implement LOD (Level of Detail)

- [ ] **Dispose unused geometries**
  ```javascript
  geometry.dispose();
  ```

### ✅ Material Optimization

- [ ] **Share materials** across meshes when possible
- [ ] **Use simpler materials**:
  - MeshBasicMaterial for unlit objects
  - MeshLambertMaterial for mobile
  - MeshStandardMaterial only when PBR needed
- [ ] **Dispose unused materials**
  ```javascript
  material.dispose();
  ```

### ✅ Texture Optimization

- [ ] **Use power-of-two dimensions** (512, 1024, 2048)
- [ ] **Compress textures**:
  - JPEG for photos (smaller file size)
  - PNG for transparency
  - Consider KTX2/Basis Universal for web
- [ ] **Set correct color space**:
  ```javascript
  diffuseTexture.colorSpace = THREE.SRGBColorSpace;
  normalMap.colorSpace = THREE.LinearSRGBColorSpace;
  ```
- [ ] **Limit texture resolution**:
  - 2048x2048 max for most cases
  - 1024x1024 for mobile
  - 512x512 for background/UI elements
- [ ] **Enable mipmaps and anisotropy**:
  ```javascript
  texture.generateMipmaps = true;
  texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
  ```
- [ ] **Dispose unused textures**:
  ```javascript
  texture.dispose();
  ```

### ✅ Rendering Optimization

- [ ] **Set pixel ratio appropriately**:
  ```javascript
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  // Don't use full devicePixelRatio on high-DPI displays
  ```
- [ ] **Disable antialiasing on mobile**
- [ ] **Use render-on-demand** when scene is static:
  ```javascript
  function render() {
    renderer.render(scene, camera);
  }
  // Call only when needed, not in requestAnimationFrame loop
  ```

### ✅ Shadow Optimization

- [ ] **Limit number of shadow-casting lights** (2-3 max)
- [ ] **Reduce shadow map size**:
  ```javascript
  light.shadow.mapSize.width = 1024; // Lower for mobile
  light.shadow.mapSize.height = 1024;
  ```
- [ ] **Optimize shadow camera frustum**:
  ```javascript
  light.shadow.camera.near = 1;
  light.shadow.camera.far = 20; // Only as far as needed
  light.shadow.camera.left = -10;
  light.shadow.camera.right = 10;
  // ... etc - Tight bounds around scene
  ```
- [ ] **Disable shadow updates** when static:
  ```javascript
  renderer.shadowMap.autoUpdate = false;
  renderer.shadowMap.needsUpdate = true; // Only when changed
  ```

## Medium Effort Optimizations

### 🔧 Culling & Visibility

- [ ] **Enable frustum culling** (enabled by default):
  ```javascript
  mesh.frustumCulled = true;
  ```
- [ ] **Compute bounding spheres** for custom geometries:
  ```javascript
  geometry.computeBoundingSphere();
  ```
- [ ] **Hide offscreen objects**:
  ```javascript
  if (distanceToCamera > threshold) {
    mesh.visible = false;
  }
  ```
- [ ] **Use layers** for selective rendering:
  ```javascript
  mesh.layers.set(1);
  camera.layers.enable(1);
  ```

### 🔧 Level of Detail (LOD)

- [ ] **Implement LOD** for complex objects:
  ```javascript
  const lod = new THREE.LOD();
  lod.addLevel(highDetailMesh, 0);
  lod.addLevel(mediumDetailMesh, 50);
  lod.addLevel(lowDetailMesh, 100);
  scene.add(lod);
  ```

### 🔧 Draw Call Reduction

- [ ] **Merge static geometries**:
  ```javascript
  import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils.js';
  const merged = mergeGeometries([geo1, geo2, geo3]);
  ```
- [ ] **Use texture atlases** to combine multiple textures
- [ ] **Batch similar materials** together

### 🔧 Animation Optimization

- [ ] **Use Clock.getDelta()** for frame-independent animations:
  ```javascript
  const delta = clock.getDelta();
  mixer.update(delta);
  ```
- [ ] **Pause animations** when offscreen:
  ```javascript
  if (!mesh.visible) {
    mixer.stop();
  }
  ```
- [ ] **Limit AnimationMixer updates** to visible objects

### 🔧 Post-Processing Optimization

- [ ] **Reduce effect quality** on mobile
- [ ] **Limit bloom/blur passes**
- [ ] **Use lower resolution render targets**:
  ```javascript
  const renderTarget = new THREE.WebGLRenderTarget(
    window.innerWidth * 0.5,
    window.innerHeight * 0.5
  );
  ```

## Advanced Optimizations

### ⚙️ Memory Management

- [ ] **Dispose all resources** when removing from scene:
  ```javascript
  function disposeObject(obj) {
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      if (Array.isArray(obj.material)) {
        obj.material.forEach(m => m.dispose());
      } else {
        obj.material.dispose();
      }
    }
    if (obj.dispose) obj.dispose();
  }

  scene.traverse(disposeObject);
  ```

- [ ] **Clear render targets** when done:
  ```javascript
  renderTarget.dispose();
  ```

- [ ] **Monitor memory usage**:
  ```javascript
  console.log(renderer.info.memory);
  console.log(renderer.info.render);
  ```

### ⚙️ Matrix Optimization

- [ ] **Disable auto-update** for static objects:
  ```javascript
  mesh.matrixAutoUpdate = false;
  mesh.updateMatrix();
  ```

- [ ] **Update world matrix** manually when needed:
  ```javascript
  mesh.matrixWorldNeedsUpdate = true;
  ```

### ⚙️ Custom Shaders

- [ ] **Use low precision** where possible:
  ```glsl
  precision mediump float; // Instead of highp
  ```

- [ ] **Minimize texture samples** in fragment shader
- [ ] **Move calculations** to vertex shader when possible
- [ ] **Use built-in GLSL functions** (faster than custom)

### ⚙️ Lighting Optimization

- [ ] **Limit number of real-time lights** (3-5 max)
- [ ] **Use baked lighting** for static scenes:
  - Lightmaps
  - AO maps
  - Environment maps
- [ ] **Combine directional lights** where possible
- [ ] **Use AmbientLight + DirectionalLight** as base setup

### ⚙️ Model Optimization

- [ ] **Use glTF with Draco compression**:
  ```javascript
  const dracoLoader = new DRACOLoader();
  dracoLoader.setDecoderPath('/draco/');
  gltfLoader.setDRACOLoader(dracoLoader);
  ```

- [ ] **Remove unused data** from models:
  - Multiple UV sets
  - Unused vertex colors
  - Unused morph targets

- [ ] **Optimize mesh topology**:
  - Remove hidden faces
  - Reduce triangle count
  - Use instancing for repeated elements

## Mobile-Specific Optimizations

### 📱 Mobile Best Practices

- [ ] **Lower pixel ratio**:
  ```javascript
  renderer.setPixelRatio(1);
  ```

- [ ] **Disable antialiasing**
- [ ] **Use simpler materials** (MeshLambertMaterial)
- [ ] **Reduce texture resolution** (512-1024px max)
- [ ] **Limit particle count** (<1000)
- [ ] **Disable shadows** or use lower resolution
- [ ] **Reduce geometry complexity** by 50%
- [ ] **Disable post-processing** or use minimal effects
- [ ] **Implement aggressive LOD**
- [ ] **Pause rendering** when tab is hidden:
  ```javascript
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      // Stop animation loop
    } else {
      // Resume animation loop
    }
  });
  ```

## Profiling & Debugging

### 🔍 Performance Monitoring

- [ ] **Use Stats.js**:
  ```javascript
  import Stats from 'three/examples/jsm/libs/stats.module.js';
  const stats = new Stats();
  document.body.appendChild(stats.dom);
  ```

- [ ] **Monitor renderer info**:
  ```javascript
  console.log('Geometries:', renderer.info.memory.geometries);
  console.log('Textures:', renderer.info.memory.textures);
  console.log('Draw Calls:', renderer.info.render.calls);
  console.log('Triangles:', renderer.info.render.triangles);
  ```

- [ ] **Use browser DevTools**:
  - Performance tab (frame rate)
  - Memory tab (heap snapshots)
  - Rendering tab (FPS meter, paint flashing)

- [ ] **WebGL Performance Tools**:
  - Spector.js (WebGL inspector)
  - Chrome GPU Profiler

### 🔍 Common Performance Bottlenecks

1. **Too many draw calls** → Merge geometries, use instancing
2. **Too many triangles** → Reduce geometry complexity, use LOD
3. **Large textures** → Compress, reduce resolution
4. **Too many lights** → Limit lights, use baked lighting
5. **Complex shaders** → Simplify materials
6. **Memory leaks** → Dispose resources properly
7. **Expensive post-processing** → Reduce effects, lower resolution

## Performance Targets

### 🎯 Desktop
- **60 FPS** (16.67ms per frame)
- **Draw calls**: <100
- **Triangles**: <1M visible
- **Texture memory**: <500MB
- **Pixel ratio**: 1-2

### 🎯 Mobile
- **30-60 FPS** (16.67-33ms per frame)
- **Draw calls**: <50
- **Triangles**: <100K visible
- **Texture memory**: <200MB
- **Pixel ratio**: 1

## Optimization Workflow

1. **Profile first** - Identify actual bottlenecks
2. **Optimize bottlenecks** - Focus on highest impact
3. **Measure improvement** - Verify gains
4. **Iterate** - Repeat process

**Remember:** Premature optimization is the root of all evil. Profile before optimizing!

## Quick Optimization Checklist Summary

```
✅ Reuse geometries and materials
✅ Use InstancedMesh for repeated objects
✅ Optimize texture size and format
✅ Set pixel ratio to max 2
✅ Limit shadow-casting lights
✅ Dispose unused resources
✅ Implement LOD for complex objects
✅ Reduce draw calls via merging
✅ Profile with Stats.js
✅ Test on target devices (mobile!)
```
