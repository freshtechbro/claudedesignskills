# A-Frame WebXR Integration Guide

Complete guide to building VR and AR experiences with A-Frame and the WebXR API.

## Table of Contents

- [WebXR Overview](#webxr-overview)
- [VR Mode Configuration](#vr-mode-configuration)
- [AR Mode Configuration](#ar-mode-configuration)
- [Controller Systems](#controller-systems)
- [Hand Tracking](#hand-tracking)
- [AR Hit Testing](#ar-hit-testing)
- [Platform Support](#platform-support)
- [Performance Optimization](#performance-optimization)
- [Testing and Debugging](#testing-and-debugging)

---

## WebXR Overview

WebXR is the web standard for VR and AR experiences. A-Frame provides high-level abstractions over the WebXR API.

### Basic WebXR Scene

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene webxr="requiredFeatures: local-floor">
      <!-- VR content -->
      <a-box position="0 1.5 -3" color="#4CC3D9"></a-box>
      <a-sky color="#ECECEC"></a-sky>
    </a-scene>
  </body>
</html>
```

### WebXR Component Properties

```html
<a-scene webxr="
  requiredFeatures: local-floor, hand-tracking;
  optionalFeatures: hit-test, dom-overlay, unbounded;
  referenceSpaceType: local-floor;
  overlayElement: #overlay
"></a-scene>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `requiredFeatures` | array | [] | Features that must be available |
| `optionalFeatures` | array | [] | Features to enable if available |
| `referenceSpaceType` | string | local-floor | XR reference space |
| `overlayElement` | selector | - | DOM overlay element (AR) |

### Reference Space Types

- `viewer` - Relative to initial viewer position
- `local` - Origin at starting position, sitting/standing
- `local-floor` - Floor level at Y=0 (recommended for VR)
- `bounded-floor` - Room-scale with boundaries
- `unbounded` - Large spaces, outdoor AR

---

## VR Mode Configuration

### Enable/Disable VR Mode UI

```html
<!-- Show VR button (default) -->
<a-scene vr-mode-ui="enabled: true"></a-scene>

<!-- Hide VR button -->
<a-scene vr-mode-ui="enabled: false"></a-scene>

<!-- Custom enter VR button -->
<a-scene vr-mode-ui="enterVRButton: #myEnterVRButton"></a-scene>

<button id="myEnterVRButton">Enter VR</button>
```

### VR Camera Rig Setup

```html
<a-scene>
  <!-- VR camera rig -->
  <a-entity id="rig" position="0 0 0">
    <!-- Camera for head tracking -->
    <a-camera position="0 1.6 0" look-controls></a-camera>

    <!-- Left controller -->
    <a-entity
      id="leftHand"
      hand-controls="hand: left"
      laser-controls="hand: left">
    </a-entity>

    <!-- Right controller -->
    <a-entity
      id="rightHand"
      hand-controls="hand: right"
      laser-controls="hand: right">
    </a-entity>
  </a-entity>

  <!-- VR content -->
  <a-box position="0 1.5 -3" class="interactive"></a-box>
  <a-plane rotation="-90 0 0" width="10" height="10" color="#7BC8A4"></a-plane>
</a-scene>
```

### VR Session Events

```javascript
const scene = document.querySelector('a-scene');

// Entering VR
scene.addEventListener('enter-vr', () => {
  console.log('Entered VR mode');

  // Check if actually in VR or AR
  if (scene.is('vr-mode')) {
    console.log('VR mode active');
  }

  if (scene.is('ar-mode')) {
    console.log('AR mode active');
  }
});

// Exiting VR
scene.addEventListener('exit-vr', () => {
  console.log('Exited VR mode');
});
```

### Programmatic VR Entry/Exit

```javascript
const scene = document.querySelector('a-scene');

// Enter VR
scene.enterVR();

// Exit VR
scene.exitVR();

// Check if VR is available
if (scene.checkHeadsetConnected()) {
  console.log('VR headset connected');
}
```

### VR-Specific Optimizations

```html
<a-scene
  renderer="
    antialias: false;
    colorManagement: true;
    sortObjects: false;
    physicallyCorrectLights: true;
    maxCanvasWidth: 1920;
    maxCanvasHeight: 1920
  "
  vr-mode-ui="enabled: true">

  <!-- Lower poly models for VR -->
  <a-entity gltf-model="#low-poly-model"></a-entity>

  <!-- Limit lights (expensive in VR) -->
  <a-entity light="type: ambient; intensity: 0.6"></a-entity>
  <a-entity light="type: directional; intensity: 0.4" position="1 2 1"></a-entity>
</a-scene>
```

---

## AR Mode Configuration

### Basic AR Scene Setup

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene
      webxr="optionalFeatures: hit-test, dom-overlay; overlayElement: #overlay"
      ar-hit-test="target: #model">

      <a-assets>
        <a-asset-item id="chair" src="chair.gltf"></a-asset-item>
      </a-assets>

      <!-- AR object to place -->
      <a-entity id="model" gltf-model="#chair" scale="0.5 0.5 0.5"></a-entity>

      <!-- AR UI overlay -->
      <div id="overlay" style="
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-family: sans-serif;
      ">
        <p id="instructions">Tap to enter AR mode</p>
      </div>
    </a-scene>
  </body>
</html>
```

### AR Hit Test Component

```html
<a-scene
  webxr="optionalFeatures: hit-test"
  ar-hit-test="
    target: #reticle;
    type: footprint;
    src: #reticle-model;
    enabled: true
  ">

  <!-- Reticle for placement preview -->
  <a-entity id="reticle" visible="false"></a-entity>

  <!-- Object to place -->
  <a-entity id="furniture" gltf-model="#chair" visible="false"></a-entity>
</a-scene>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `target` | selector | - | Entity to place on surface |
| `enabled` | boolean | true | Enable hit testing |
| `src` | selector | - | Custom reticle model |
| `type` | string | footprint | Hit test type (footprint, map) |

### AR Hit Test Events

```javascript
const scene = document.querySelector('a-scene');
const instructions = document.getElementById('instructions');

scene.addEventListener('enter-vr', function() {
  if (this.is('ar-mode')) {
    instructions.textContent = '';

    // Hit testing started (scanning environment)
    this.addEventListener('ar-hit-test-start', function() {
      instructions.textContent = 'Scanning environment, finding surfaces...';
    }, { once: true });

    // Surface detected
    this.addEventListener('ar-hit-test-achieved', function() {
      instructions.textContent = 'Tap to place object';
    }, { once: true });

    // Object placed
    this.addEventListener('ar-hit-test-select', function() {
      instructions.textContent = 'Object placed!';
      setTimeout(() => instructions.textContent = '', 2000);
    }, { once: true });
  }
});

scene.addEventListener('exit-vr', function() {
  instructions.textContent = 'Tap to enter AR mode';
});
```

### AR Lighting Estimation

```html
<a-scene
  reflection="directionalLight: #light"
  webxr="optionalFeatures: light-estimation">

  <!-- Light will be controlled by AR environment -->
  <a-entity
    id="light"
    light="type: directional; castShadow: true"
    position="1 2 1">
  </a-entity>
</a-scene>
```

### AR Real-World Meshing

```html
<a-scene
  webxr="optionalFeatures: mesh-detection"
  real-world-meshing="enabled: true">

  <!-- Detected surfaces will be rendered -->
</a-scene>
```

---

## Controller Systems

### Generic Hand Controls

Works with all VR controllers (Meta Quest, Vive, Index, etc.).

```html
<a-entity id="leftHand"
  hand-controls="hand: left; handModelStyle: lowPoly; color: #ffcccc">
</a-entity>

<a-entity id="rightHand"
  hand-controls="hand: right; handModelStyle: highPoly; color: #ffcccc">
</a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `hand` | string | left | Which hand (left, right) |
| `handModelStyle` | string | lowPoly | Model detail (lowPoly, highPoly, toon) |
| `color` | color | white | Hand color |

### Laser Controls

Add laser pointer to controllers for UI interaction.

```html
<a-entity
  hand-controls="hand: right"
  laser-controls="hand: right"
  raycaster="objects: .interactive; far: 10">
</a-entity>

<!-- Interactive object -->
<a-box class="interactive" position="0 1.5 -3"></a-box>
```

### Controller Events

```javascript
const leftHand = document.querySelector('#leftHand');
const rightHand = document.querySelector('#rightHand');

// Trigger button
leftHand.addEventListener('triggerdown', (evt) => {
  console.log('Left trigger pressed');
});

leftHand.addEventListener('triggerup', (evt) => {
  console.log('Left trigger released');
});

// Grip button
rightHand.addEventListener('gripdown', (evt) => {
  console.log('Right grip pressed');
});

rightHand.addEventListener('gripup', (evt) => {
  console.log('Right grip released');
});

// Thumbstick/touchpad
rightHand.addEventListener('thumbstickmoved', (evt) => {
  console.log('Thumbstick:', evt.detail.x, evt.detail.y);
});

rightHand.addEventListener('touchpadmoved', (evt) => {
  console.log('Touchpad:', evt.detail.x, evt.detail.y);
});

// A/B/X/Y buttons
rightHand.addEventListener('abuttondown', () => {
  console.log('A button pressed');
});

rightHand.addEventListener('bbuttondown', () => {
  console.log('B button pressed');
});

leftHand.addEventListener('xbuttondown', () => {
  console.log('X button pressed');
});

leftHand.addEventListener('ybuttondown', () => {
  console.log('Y button pressed');
});
```

### Platform-Specific Controllers

**Meta Quest / Oculus Touch**
```html
<a-entity meta-touch-controls="hand: left; model: true"></a-entity>
<a-entity meta-touch-controls="hand: right; model: true"></a-entity>
```

**HTC Vive**
```html
<a-entity vive-controls="hand: left; buttonColor: #FF0000"></a-entity>
<a-entity vive-controls="hand: right; buttonColor: #0000FF"></a-entity>
```

**Valve Index**
```html
<a-entity valve-index-controls="hand: left"></a-entity>
<a-entity valve-index-controls="hand: right"></a-entity>
```

**Windows Mixed Reality**
```html
<a-entity windows-motion-controls="hand: left"></a-entity>
<a-entity windows-motion-controls="hand: right"></a-entity>
```

### Grabbable Objects Component

```javascript
AFRAME.registerComponent('grabbable', {
  init: function() {
    var el = this.el;
    var grabbing = false;
    var controller = null;

    el.addEventListener('triggerdown', function(evt) {
      if (!grabbing) {
        grabbing = true;
        controller = evt.detail.controller;

        // Attach object to controller
        controller.object3D.attach(el.object3D);

        // Visual feedback
        el.setAttribute('material', 'opacity', 0.7);
      }
    });

    el.addEventListener('triggerup', function(evt) {
      if (grabbing && controller === evt.detail.controller) {
        grabbing = false;

        // Detach from controller
        var sceneEl = el.sceneEl.object3D;
        sceneEl.attach(el.object3D);

        // Reset visual feedback
        el.setAttribute('material', 'opacity', 1);

        controller = null;
      }
    });
  }
});
```

```html
<!-- Apply to objects -->
<a-box class="grabbable" grabbable position="0 1.5 -3"></a-box>
<a-sphere class="grabbable" grabbable position="1 1.5 -3"></a-sphere>
```

---

## Hand Tracking

Native hand tracking without controllers (supported on Meta Quest 2/3/Pro).

### Enable Hand Tracking

```html
<a-scene webxr="requiredFeatures: hand-tracking">
  <!-- Hand tracking entities -->
  <a-entity id="leftHand"
    hand-tracking-controls="hand: left"
    hand-tracking-grab-controls="hand: left">
  </a-entity>

  <a-entity id="rightHand"
    hand-tracking-controls="hand: right"
    hand-tracking-grab-controls="hand: right">
  </a-entity>

  <!-- Grabbable objects -->
  <a-box class="grabbable" position="0 1.5 -3"></a-box>
</a-scene>
```

### Hand Tracking Properties

```html
<a-entity hand-tracking-controls="
  hand: left;
  modelColor: #FF0000;
  modelStyle: mesh
"></a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `hand` | string | left | Which hand (left, right) |
| `modelColor` | color | white | Hand mesh color |
| `modelStyle` | string | mesh | Visualization (mesh, dots, none) |

### Hand Tracking Events

```javascript
const leftHand = document.querySelector('#leftHand');

// Pinch gesture (thumb + index finger)
leftHand.addEventListener('pinchstarted', (evt) => {
  console.log('Pinch started');
});

leftHand.addEventListener('pinchended', (evt) => {
  console.log('Pinch ended');
});

// Pinch with strength value
leftHand.addEventListener('pinchmoved', (evt) => {
  console.log('Pinch strength:', evt.detail.strength); // 0-1
});
```

### Hand Tracking Grab Controls

```html
<a-scene>
  <!-- Enable hand tracking grab -->
  <a-entity
    hand-tracking-controls="hand: right"
    hand-tracking-grab-controls="hand: right">
  </a-entity>

  <!-- Grabbable object -->
  <a-sphere
    class="grabbable"
    obb-collider="size: 0.2 0.2 0.2"
    grab-options="
      requireGrab: true;
      maxGrabbers: 2
    "
    position="0 1.5 -3">
  </a-sphere>
</a-scene>
```

### Visualize Hand Tracking Colliders (Debug)

```html
<a-scene obb-collider="showColliders: true">
  <!-- Shows bounding boxes for debugging -->
</a-scene>
```

---

## AR Hit Testing

Place virtual objects on detected real-world surfaces.

### Basic AR Hit Test

```html
<a-scene
  webxr="optionalFeatures: hit-test"
  ar-hit-test="target: #model">

  <a-assets>
    <a-asset-item id="furniture" src="chair.gltf"></a-asset-item>
  </a-assets>

  <a-entity id="model" gltf-model="#furniture" scale="0.5 0.5 0.5"></a-entity>
</a-scene>
```

### Custom Reticle

```html
<a-scene
  webxr="optionalFeatures: hit-test"
  ar-hit-test="target: #model; src: #reticle">

  <a-assets>
    <a-asset-item id="reticle-model" src="reticle.gltf"></a-asset-item>
    <a-asset-item id="furniture" src="chair.gltf"></a-asset-item>
  </a-assets>

  <!-- Custom reticle -->
  <a-entity id="reticle" gltf-model="#reticle-model"></a-entity>

  <!-- Object to place -->
  <a-entity id="model" gltf-model="#furniture"></a-entity>
</a-scene>
```

### Multiple Object Placement

```javascript
const scene = document.querySelector('a-scene');
const furniture = document.querySelector('#furniture');
let placedObjects = [];

scene.addEventListener('ar-hit-test-select', function(evt) {
  // Clone object for multiple placements
  const clone = furniture.cloneNode(true);
  clone.removeAttribute('id');
  clone.setAttribute('visible', true);

  // Position at hit point
  const hitPoint = evt.detail.position;
  clone.setAttribute('position', hitPoint);

  scene.appendChild(clone);
  placedObjects.push(clone);

  console.log('Placed object at:', hitPoint);
});

// Clear all placed objects
function clearObjects() {
  placedObjects.forEach(obj => obj.parentNode.removeChild(obj));
  placedObjects = [];
}
```

### AR with DOM Overlay

```html
<a-scene
  webxr="optionalFeatures: hit-test, dom-overlay; overlayElement: #overlay"
  ar-hit-test="target: #model">

  <a-entity id="model" gltf-model="#furniture"></a-entity>

  <!-- HTML UI overlay -->
  <div id="overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
    <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
                background: rgba(0,0,0,0.7); color: white; padding: 15px; border-radius: 8px; pointer-events: auto;">
      <p id="instructions">Tap to enter AR</p>
      <button id="clearBtn" style="margin-top: 10px; padding: 10px 20px; pointer-events: auto;">Clear Objects</button>
    </div>
  </div>
</a-scene>

<script>
const clearBtn = document.getElementById('clearBtn');
clearBtn.addEventListener('click', clearObjects);
</script>
```

---

## Platform Support

### Meta Quest (Standalone)

Optimizations for Quest 2/3/Pro:

```html
<a-scene
  renderer="antialias: false; physicallyCorrectLights: false"
  vr-mode-ui="enabled: true">

  <!-- Use low-poly models -->
  <a-entity gltf-model="#low-poly-model"></a-entity>

  <!-- Limit lights (1-2 max) -->
  <a-entity light="type: ambient; intensity: 0.7"></a-entity>
  <a-entity light="type: directional; intensity: 0.3" position="1 2 1"></a-entity>

  <!-- Texture size limits -->
  <a-entity material="src: #texture; repeat: 1 1"></a-entity>
</a-scene>
```

### Desktop VR (PC + Headset)

Higher quality settings for PC VR:

```html
<a-scene
  renderer="antialias: true; colorManagement: true; physicallyCorrectLights: true"
  fog="type: linear; color: #AAA; near: 10; far: 100">

  <!-- High-poly models allowed -->
  <a-entity gltf-model="#high-poly-model"></a-entity>

  <!-- Multiple lights OK -->
  <a-entity light="type: ambient; intensity: 0.5"></a-entity>
  <a-entity light="type: directional; intensity: 0.8" position="2 4 2"></a-entity>
  <a-entity light="type: point; intensity: 1.5; distance: 20" position="5 2 5"></a-entity>
</a-scene>
```

### Mobile AR (iOS/Android)

Optimizations for mobile AR:

```html
<a-scene
  webxr="optionalFeatures: hit-test, dom-overlay, light-estimation"
  ar-hit-test="target: #model"
  renderer="antialias: false; maxCanvasWidth: 1920; maxCanvasHeight: 1920">

  <!-- Lightweight models for mobile -->
  <a-entity gltf-model="#mobile-optimized-model"></a-entity>

  <!-- Minimal lighting -->
  <a-entity light="type: ambient; intensity: 0.8"></a-entity>
</a-scene>
```

### Feature Detection

```javascript
// Check WebXR support
if ('xr' in navigator) {
  navigator.xr.isSessionSupported('immersive-vr').then((supported) => {
    if (supported) {
      console.log('VR supported');
    }
  });

  navigator.xr.isSessionSupported('immersive-ar').then((supported) => {
    if (supported) {
      console.log('AR supported');
    }
  });
}

// Check hand tracking support
const scene = document.querySelector('a-scene');
scene.addEventListener('loaded', () => {
  if (scene.systems['hand-tracking-controls']) {
    console.log('Hand tracking available');
  }
});
```

---

## Performance Optimization

### Reduce Draw Calls

```javascript
// Use instancing for repeated objects
AFRAME.registerComponent('instanced-forest', {
  init: function() {
    const scene = this.el.sceneEl.object3D;
    const geometry = new THREE.CylinderGeometry(0.2, 0.5, 3, 8);
    const material = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
    const instancedMesh = new THREE.InstancedMesh(geometry, material, 100);

    // Position instances
    for (let i = 0; i < 100; i++) {
      const matrix = new THREE.Matrix4();
      matrix.setPosition(
        Math.random() * 20 - 10,
        0,
        Math.random() * 20 - 10
      );
      instancedMesh.setMatrixAt(i, matrix);
    }

    scene.add(instancedMesh);
  }
});
```

### Optimize Geometry

```html
<!-- Low poly count for VR/mobile -->
<a-sphere radius="1" segments-width="8" segments-height="6"></a-sphere>

<!-- High poly only for close-up objects -->
<a-sphere radius="1" segments-width="32" segments-height="32"></a-sphere>
```

### Texture Optimization

```javascript
// Compress textures
// Use power-of-2 sizes (256, 512, 1024, 2048)
// Use lower resolutions for mobile

// Lazy load textures
AFRAME.registerComponent('lazy-texture', {
  schema: {
    src: {type: 'string'}
  },

  init: function() {
    const el = this.el;
    const src = this.data.src;

    // Load texture when entity is near camera
    this.el.sceneEl.addEventListener('camera-move', () => {
      const distance = el.object3D.position.distanceTo(
        el.sceneEl.camera.position
      );

      if (distance < 10 && !el.getAttribute('material').src) {
        el.setAttribute('material', 'src', src);
      }
    });
  }
});
```

### Limit Physics

```html
<!-- Only enable physics for interactive objects -->
<a-entity
  geometry="primitive: box"
  ammo-body="type: dynamic; mass: 1"
  ammo-shape="type: box">
</a-entity>
```

### Throttle Updates

```javascript
AFRAME.registerComponent('throttled-rotation', {
  init: function() {
    this.lastUpdate = 0;
    this.updateInterval = 100; // Update every 100ms instead of every frame
  },

  tick: function(time, timeDelta) {
    if (time - this.lastUpdate >= this.updateInterval) {
      // Expensive operation
      this.el.object3D.rotation.y += 0.01;
      this.lastUpdate = time;
    }
  }
});
```

---

## Testing and Debugging

### Desktop Testing

```html
<!-- Test without VR headset using desktop mode -->
<a-scene vr-mode-ui="enabled: true">
  <!-- WASD to move, mouse to look -->
  <a-camera wasd-controls look-controls></a-camera>
</a-scene>
```

### Mobile Testing

```html
<!-- Test AR on mobile browser -->
<a-scene
  webxr="optionalFeatures: hit-test"
  ar-hit-test="target: #model">

  <!-- Use browser DevTools device emulation -->
</a-scene>
```

### Stats and Debugging

```html
<!-- Show FPS and performance stats -->
<a-scene stats>
  <!-- Stats panel appears in top-left -->
</a-scene>

<!-- Enable inspector (Ctrl+Alt+I) -->
<a-scene inspector>
  <!-- Visual scene editor -->
</a-scene>
```

### Console Logging

```javascript
// Log XR session info
const scene = document.querySelector('a-scene');

scene.addEventListener('enter-vr', () => {
  const renderer = scene.renderer;
  const session = renderer.xr.getSession();

  console.log('XR Session:', session);
  console.log('Reference space:', scene.systems.webxr.sessionReferenceSpaceType);
  console.log('Frame rate:', session.frameRate);
});
```

### Remote Debugging

**For Meta Quest:**
1. Enable Developer Mode in Quest settings
2. Connect via USB to computer
3. Use Chrome DevTools (chrome://inspect)

**For iOS:**
1. Enable Web Inspector in Safari settings
2. Connect iPhone/iPad to Mac
3. Use Safari Developer menu

### Performance Profiling

```javascript
// Monitor frame times
const scene = document.querySelector('a-scene');
let frameCount = 0;
let lastTime = performance.now();

scene.addEventListener('renderstart', () => {
  const now = performance.now();
  frameCount++;

  if (now - lastTime >= 1000) {
    console.log('FPS:', frameCount);
    frameCount = 0;
    lastTime = now;
  }
});
```

---

## Common Issues

### Issue: VR button not appearing
**Solution**: Check HTTPS (required for WebXR)

### Issue: Controllers not tracking
**Solution**: Check permissions, ensure proper lighting

### Issue: AR not working on mobile
**Solution**: Use Chrome/Safari, check camera permissions

### Issue: Low FPS in VR
**Solution**: Reduce geometry, limit lights, optimize textures

### Issue: Hand tracking not working
**Solution**: Enable in headset settings, ensure good lighting

---

## Resources

- [WebXR Device API Specification](https://www.w3.org/TR/webxr/)
- [A-Frame WebXR Documentation](https://aframe.io/docs/1.7.0/introduction/webxr.html)
- [Meta Quest Development](https://developer.oculus.com/)
- [WebXR Samples](https://immersive-web.github.io/webxr-samples/)
- [Mozilla Mixed Reality Blog](https://mixedreality.mozilla.org/)

---

This guide covers all aspects of building WebXR experiences with A-Frame, from basic VR scenes to advanced AR features.
