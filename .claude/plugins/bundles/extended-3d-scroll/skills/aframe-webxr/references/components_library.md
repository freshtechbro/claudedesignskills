# A-Frame Community Components Library

Curated collection of popular A-Frame community components for extending functionality.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Environment & Effects](#environment--effects)
- [Physics](#physics)
- [Locomotion](#locomotion)
- [Models & Loaders](#models--loaders)
- [User Interface](#user-interface)
- [Particles](#particles)
- [Audio & Video](#audio--video)
- [Input & Interaction](#input--interaction)
- [Networking](#networking)
- [Utilities](#utilities)

---

## Installation Methods

### CDN (Recommended)

```html
<script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-extras@7.5.0/dist/aframe-extras.min.js"></script>
```

### npm

```bash
npm install aframe-extras
```

```javascript
import 'aframe-extras';
```

### Local Download

Download component `.js` file and include in HTML:

```html
<script src="path/to/component.js"></script>
```

---

## Environment & Effects

### aframe-environment-component

Generate procedural 3D environments with presets.

**GitHub**: https://github.com/supermedium/aframe-environment-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-environment-component@1.3.3/dist/aframe-environment-component.min.js"></script>
```

**Usage**:
```html
<!-- Preset environment -->
<a-entity environment="preset: forest"></a-entity>

<!-- Custom environment -->
<a-entity environment="
  preset: default;
  seed: 42;
  skyType: gradient;
  skyColor: #4A90E2;
  horizonColor: #87CEEB;
  lighting: distant;
  lightPosition: 1 1 -2;
  fog: 0.8;
  ground: hills;
  groundColor: #5A7F32;
  groundColor2: #3D5E1F;
  dressing: trees;
  dressingAmount: 50;
  dressingColor: #228B22;
  dressingScale: 5;
  grid: none
"></a-entity>
```

**Presets**:
- `default`, `contact`, `egypt`, `checkerboard`, `forest`, `goaland`, `yavapai`, `goldmine`, `threetowers`, `poison`, `arches`, `tron`, `japan`, `dream`, `volcano`, `starry`, `osiris`

**Properties**:
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `preset` | string | default | Environment preset |
| `seed` | number | 1 | Random seed |
| `skyType` | string | gradient | Sky type (color, gradient, atmosphere) |
| `lighting` | string | distant | Lighting type (none, distant, point) |
| `ground` | string | flat | Ground type (none, flat, hills, canyon, spikes, noise) |
| `dressing` | string | none | Objects on ground (none, cubes, pyramids, cylinders, towers, mushrooms, trees, apparatus, torii) |
| `dressingAmount` | number | 10 | Number of dressing objects |

### aframe-particle-system-component

GPU particle systems for effects.

**GitHub**: https://github.com/IdeaSpaceVR/aframe-particle-system-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/gh/IdeaSpaceVR/aframe-particle-system-component@1.2.x/dist/aframe-particle-system-component.min.js"></script>
```

**Usage**:
```html
<!-- Preset particles -->
<a-entity particle-system="preset: default"></a-entity>
<a-entity particle-system="preset: dust"></a-entity>
<a-entity particle-system="preset: snow"></a-entity>
<a-entity particle-system="preset: rain"></a-entity>

<!-- Custom particles -->
<a-entity particle-system="
  preset: default;
  particleCount: 2000;
  color: #FF0000, #FFFF00;
  size: 0.5, 1;
  velocity: 0 10 0;
  velocitySpread: 1 5 1;
  accelerationValue: 0 -10 0;
  maxAge: 2;
  blending: additive;
  texture: https://cdn.aframe.io/examples/particle/images/star.png
"></a-entity>
```

**Presets**: `default`, `dust`, `snow`, `rain`

### aframe-effects

Post-processing effects (bloom, film grain, etc.).

**GitHub**: https://github.com/wizgrav/aframe-effects

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-effects@2.0.3/dist/aframe-effects.min.js"></script>
```

**Usage**:
```html
<a-scene effects="
  bloom: 1.5;
  fxaa: true;
  filmgrain: 0.35
">
  <!-- Scene content -->
</a-scene>
```

**Effects**:
- `bloom`: Bloom intensity (0-5)
- `fxaa`: Anti-aliasing (boolean)
- `filmgrain`: Film grain amount (0-1)
- `godrays`: God rays intensity (0-1)

---

## Physics

### aframe-physics-system (Ammo.js)

Physics simulation using Ammo.js (Bullet physics).

**GitHub**: https://github.com/c-frame/aframe-physics-system

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-physics-system@4.2.2/dist/aframe-physics-system.min.js"></script>
```

**Usage**:
```html
<a-scene physics="debug: false; gravity: -9.8">
  <!-- Static ground -->
  <a-plane
    static-body
    position="0 0 0"
    rotation="-90 0 0"
    width="10"
    height="10">
  </a-plane>

  <!-- Dynamic box -->
  <a-box
    dynamic-body
    position="0 5 0"
    width="1"
    height="1"
    depth="1">
  </a-box>

  <!-- Kinematic sphere (non-reactive but affects others) -->
  <a-sphere
    kinematic-body
    position="2 3 0"
    radius="0.5">
  </a-sphere>
</a-scene>
```

**Components**:
- `static-body`: Immovable objects (walls, ground)
- `dynamic-body`: Movable objects affected by forces
- `kinematic-body`: Movable by code, affects dynamic bodies

**Properties**:
```html
<a-box dynamic-body="
  mass: 5;
  linearDamping: 0.01;
  angularDamping: 0.01;
  shape: box;
  sphereRadius: 1
"></a-box>
```

### aframe-physics-extras

Physics helpers and constraints.

**GitHub**: https://github.com/c-frame/aframe-physics-system

**Usage**:
```html
<!-- Constraint between two bodies -->
<a-entity
  constraint="
    target: #bodyA;
    type: lock;
    collideConnected: false
  ">
</a-entity>

<!-- Spring -->
<a-entity
  spring="
    target: #box;
    restLength: 2;
    stiffness: 50;
    damping: 1
  ">
</a-entity>
```

---

## Locomotion

### aframe-extras (Movement Components)

Includes movement, controls, and model utilities.

**GitHub**: https://github.com/c-frame/aframe-extras

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-extras@7.5.0/dist/aframe-extras.min.js"></script>
```

**Components Included**:

**movement-controls** (FPS-style movement):
```html
<a-entity movement-controls="
  speed: 0.3;
  fly: false;
  constrainToNavMesh: true;
  camera: #camera
" position="0 0 0">
  <a-entity id="camera" camera position="0 1.6 0"></a-entity>
</a-entity>
```

**checkpoint-controls** (Teleport between waypoints):
```html
<!-- Player -->
<a-entity checkpoint-controls="mode: teleport"></a-entity>

<!-- Waypoints -->
<a-cylinder checkpoint position="0 0 -5" radius="0.5" height="0.1"></a-cylinder>
<a-cylinder checkpoint position="5 0 -5" radius="0.5" height="0.1"></a-cylinder>
```

**Animation Mixer** (GLTF animations):
```html
<a-entity
  gltf-model="#character"
  animation-mixer="clip: walk; loop: repeat">
</a-entity>
```

### aframe-blink-controls

Teleportation locomotion for VR.

**GitHub**: https://github.com/jure/aframe-blink-controls

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-blink-controls/dist/aframe-blink-controls.min.js"></script>
```

**Usage**:
```html
<a-entity
  hand-controls="hand: left"
  blink-controls="
    cameraRig: #rig;
    teleportOrigin: #camera;
    collisionEntities: .ground
  ">
</a-entity>

<a-entity id="rig" position="0 0 0">
  <a-entity id="camera" camera position="0 1.6 0"></a-entity>
</a-entity>

<a-plane class="ground" rotation="-90 0 0" width="20" height="20"></a-plane>
```

---

## Models & Loaders

### gltf-model (Built-in)

Load GLTF/GLB 3D models.

```html
<a-assets>
  <a-asset-item id="tree" src="tree.gltf"></a-asset-item>
</a-assets>

<a-entity gltf-model="#tree" position="0 0 -5"></a-entity>
```

### obj-model (Built-in)

Load OBJ + MTL models.

```html
<a-assets>
  <a-asset-item id="tree-obj" src="tree.obj"></a-asset-item>
  <a-asset-item id="tree-mtl" src="tree.mtl"></a-asset-item>
</a-assets>

<a-entity obj-model="obj: #tree-obj; mtl: #tree-mtl"></a-entity>
```

### aframe-extras (Model Extensions)

Included in aframe-extras:

**animation-mixer**: Play GLTF animations
```html
<a-entity
  gltf-model="#character"
  animation-mixer="clip: walk; loop: repeat; clampWhenFinished: true">
</a-entity>
```

### aframe-simple-sun-sky

Realistic sky with sun position.

**GitHub**: https://github.com/c-frame/aframe-simple-sun-sky

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-simple-sun-sky@^1.2.2/simple-sun-sky.js"></script>
```

**Usage**:
```html
<a-simple-sun-sky sun-position="1 0.4 0"></a-simple-sun-sky>

<!-- Or with parameters -->
<a-simple-sun-sky
  sun-position="1 1 -1"
  rayleigh="1"
  turbidity="10"
  luminance="1"
  mie-coefficient="0.005"
  mie-directional-g="0.8">
</a-simple-sun-sky>
```

---

## User Interface

### aframe-html-shader

Display HTML content on meshes.

**GitHub**: https://github.com/mayognaise/aframe-html-shader

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-html-shader@0.2.0/dist/aframe-html-shader.min.js"></script>
```

**Usage**:
```html
<a-entity geometry="primitive: plane; width: 2; height: 1"
          material="shader: html; target: #html-content; ratio: width"
          position="0 1.5 -3">
</a-entity>

<div id="html-content" style="width: 400px; height: 200px; background: white;">
  <h1>HTML Content</h1>
  <p>This is rendered on a 3D surface!</p>
</div>
```

### aframe-gui

VR GUI components (buttons, sliders, panels).

**GitHub**: https://github.com/rdub80/aframe-gui

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-gui/dist/aframe-gui.min.js"></script>
```

**Usage**:
```html
<!-- Button -->
<a-gui-button
  width="2.5"
  height="0.75"
  value="Click Me"
  onclick="alert('Clicked!')"
  position="0 1.5 -3">
</a-gui-button>

<!-- Slider -->
<a-gui-slider
  width="2.5"
  height="0.75"
  percent="0.5"
  position="0 2.5 -3">
</a-gui-slider>

<!-- Toggle -->
<a-gui-toggle
  width="2.5"
  height="0.75"
  value="Sound: On"
  position="0 3.5 -3">
</a-gui-toggle>
```

### aframe-troika-text

High-quality text rendering.

**GitHub**: https://github.com/lojjic/aframe-troika-text

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/troika-three-text@0.46.4/dist/troika-three-text.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/aframe-troika-text@1.0.0/dist/aframe-troika-text.min.js"></script>
```

**Usage**:
```html
<a-entity troika-text="
  value: High Quality Text;
  align: center;
  anchor: center;
  baseline: center;
  color: #FFF;
  fontSize: 0.2;
  maxWidth: 3;
  outlineWidth: 0.01;
  outlineColor: #000
" position="0 2 -3">
</a-entity>
```

---

## Particles

### aframe-spe-particles

Shader Particle Engine for advanced particle effects.

**GitHub**: https://github.com/harlyq/aframe-spe-particles-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-spe-particles-component/dist/aframe-spe-particles-component.min.js"></script>
```

**Usage**:
```html
<!-- Fire effect -->
<a-entity spe-particles="
  texture: https://cdn.rawgit.com/IdeaSpaceVR/aframe-particle-system-component/master/dist/images/star.png;
  color: #ff0000, #ffff00;
  particleCount: 1000;
  maxAge: 1;
  velocity: 0 4 0;
  velocitySpread: 2 0 2;
  acceleration: 0 -1 0;
  size: 1, 0;
  opacity: 1, 0;
  blending: additive
" position="0 0 -5">
</a-entity>
```

---

## Audio & Video

### aframe-stereo-component

Stereo/spatial audio controls.

**GitHub**: https://github.com/oscarmarinmiro/aframe-stereo-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-stereo-component/dist/aframe-stereo-component.min.js"></script>
```

**Usage**:
```html
<a-assets>
  <audio id="ambience" src="forest.mp3" stereo></audio>
</a-assets>

<a-entity sound="src: #ambience; autoplay: true; loop: true" position="0 0 0"></a-entity>
```

### aframe-video-controls

Video playback controls for 360° and flat videos.

**Usage**:
```html
<a-assets>
  <video id="video360" src="360video.mp4" preload="auto"></video>
</a-assets>

<a-videosphere src="#video360"></a-videosphere>

<!-- Or flat video -->
<a-video src="#video360" width="4" height="2.25" position="0 2 -5"></a-video>
```

---

## Input & Interaction

### aframe-event-set-component (Built-in)

Set component properties on events.

**Usage**:
```html
<a-box
  event-set__mouseenter="scale: 1.2 1.2 1.2; material.color: yellow"
  event-set__mouseleave="scale: 1 1 1; material.color: blue"
  event-set__click="rotation: 0 360 0">
</a-box>
```

### aframe-super-hands-component

Advanced hand interaction (grab, stretch, hover).

**GitHub**: https://github.com/c-frame/aframe-super-hands-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/super-hands/dist/super-hands.min.js"></script>
```

**Usage**:
```html
<!-- Hands with super-hands -->
<a-entity
  hand-controls="hand: left"
  super-hands>
</a-entity>

<!-- Interactive object -->
<a-box
  hoverable
  grabbable
  stretchable
  draggable
  position="0 1.5 -3">
</a-box>
```

### aframe-input-mapping-component

Map VR controller buttons to actions.

**GitHub**: https://github.com/c-frame/aframe-input-mapping-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-input-mapping-component/dist/aframe-input-mapping-component.min.js"></script>
```

**Usage**:
```html
<a-entity
  hand-controls="hand: right"
  input-mapping="
    keyboard: wasd;
    controller: sixdof;
    mapping: {
      'triggerdown': 'shoot',
      'gripdown': 'grab',
      'abuttondown': 'jump'
    }
  ">
</a-entity>
```

---

## Networking

### networked-aframe (NAF)

Multiplayer WebRTC networking.

**GitHub**: https://github.com/networked-aframe/networked-aframe

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/networked-aframe@^0.11.0/dist/networked-aframe.min.js"></script>
```

**Usage**:
```html
<a-scene networked-scene="
  room: myRoom;
  adapter: wseasyrtc;
  audio: true
">
  <!-- Networked entity (synced across clients) -->
  <a-entity
    networked="template: #avatar-template; attachTemplateToLocal: false"
    position="0 0 0">
  </a-entity>
</a-scene>

<script>
// Template for networked entities
NAF.schemas.add({
  template: '#avatar-template',
  components: [
    'position',
    'rotation'
  ]
});
</script>
```

---

## Utilities

### aframe-look-at-component (Built-in)

Make entity face another entity or position.

**Usage**:
```html
<!-- Look at camera -->
<a-text value="Look at me!" look-at="#camera"></a-text>

<!-- Look at position -->
<a-box look-at="0 0 0"></a-box>

<!-- Look at position vector -->
<a-sphere look-at="[camera]"></a-sphere>
```

### aframe-orbit-controls

Orbit camera around scene.

**GitHub**: https://github.com/tizzle/aframe-orbit-controls-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-orbit-controls@1.3.2/dist/aframe-orbit-controls.min.js"></script>
```

**Usage**:
```html
<a-camera orbit-controls="
  target: 0 1.5 -3;
  minDistance: 2;
  maxDistance: 100;
  initialPosition: 0 2 5
">
</a-camera>
```

### aframe-alongpath-component

Animate entities along a path.

**GitHub**: https://github.com/protyze/aframe-alongpath-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-alongpath-component/dist/aframe-alongpath-component.min.js"></script>
```

**Usage**:
```html
<a-curve id="track">
  <a-curve-point position="0 0 0"></a-curve-point>
  <a-curve-point position="5 5 0"></a-curve-point>
  <a-curve-point position="10 0 0"></a-curve-point>
</a-curve>

<a-entity alongpath="
  path: #track;
  dur: 10000;
  loop: true
">
  <a-box></a-box>
</a-entity>
```

### aframe-click-drag-component

Drag entities with mouse/gaze.

**GitHub**: https://github.com/jesstelford/aframe-click-drag-component

**Installation**:
```html
<script src="https://cdn.jsdelivr.net/npm/aframe-click-drag-component/dist/aframe-click-drag-component.min.js"></script>
```

**Usage**:
```html
<a-camera>
  <a-cursor click-drag></a-cursor>
</a-camera>

<a-box click-drag position="0 1 -3"></a-box>
```

### aframe-teleport-controls (Built-in for Quest)

Teleportation for VR.

**Usage**:
```html
<a-entity
  hand-controls="hand: left"
  teleport-controls="
    cameraRig: #rig;
    teleportOrigin: #camera;
    type: parabolic;
    collisionEntities: [mixin='navmesh']
  ">
</a-entity>
```

---

## Component Registry

Browse thousands of community components:

**A-Frame Registry**: https://aframe.io/registry/

Search components by category:
- Animation
- Audio
- Camera
- Controls
- Cursor
- Effects
- Geometry
- Layout
- Lighting
- Material
- Model
- Physics
- Shaders
- UI
- Utilities

---

## Creating Custom Components

Template for creating reusable components:

```javascript
AFRAME.registerComponent('my-custom-component', {
  schema: {
    speed: {type: 'number', default: 1},
    enabled: {type: 'boolean', default: true}
  },

  init: function() {
    // Setup
  },

  update: function(oldData) {
    // When properties change
  },

  tick: function(time, timeDelta) {
    // Every frame
  },

  remove: function() {
    // Cleanup
  }
});
```

**Share your component**:
1. Publish to npm
2. Submit to A-Frame Registry
3. Add GitHub topic: `aframe-component`

---

This components library provides a solid foundation for extending A-Frame with community-created functionality.
