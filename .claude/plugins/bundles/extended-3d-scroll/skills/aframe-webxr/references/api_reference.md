# A-Frame API Reference

Complete reference for A-Frame 1.7.x core components, primitives, and systems.

## Table of Contents

- [Scene](#scene)
- [Entity](#entity)
- [Core Components](#core-components)
  - [Camera](#camera)
  - [Geometry](#geometry)
  - [Material](#material)
  - [Light](#light)
  - [Position, Rotation, Scale](#position-rotation-scale)
  - [Animation](#animation)
  - [Sound](#sound)
- [Primitives](#primitives)
- [Controls](#controls)
- [VR/XR Components](#vrxr-components)
- [Systems](#systems)
- [Component API](#component-api)
- [JavaScript API](#javascript-api)

---

## Scene

The `<a-scene>` element represents the 3D scene and contains all entities.

### HTML Usage

```html
<a-scene
  background="color: #ECECEC"
  fog="type: linear; color: #AAA; near: 1; far: 100"
  stats
  inspector
  embedded
  vr-mode-ui="enabled: true"
  loading-screen="enabled: true"
  renderer="antialias: true; colorManagement: true"
  webxr="requiredFeatures: hit-test; optionalFeatures: dom-overlay">
</a-scene>
```

### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `background` | color | - | Scene background color |
| `fog` | object | - | Fog settings |
| `stats` | boolean | false | Show performance stats |
| `inspector` | boolean | false | Enable inspector (Ctrl+Alt+I) |
| `embedded` | boolean | false | Embed in page (no fullscreen) |
| `vr-mode-ui` | object | - | VR mode button config |
| `loading-screen` | object | - | Loading screen config |
| `renderer` | object | - | Three.js renderer settings |
| `webxr` | object | - | WebXR configuration |

### Events

- `loaded`: Scene loaded and ready
- `enter-vr`: Entered VR/AR mode
- `exit-vr`: Exited VR/AR mode
- `renderstart`: First render tick
- `componentchanged`: Component updated

### JavaScript API

```javascript
const scene = document.querySelector('a-scene');

// Check if scene is loaded
if (scene.hasLoaded) {
  console.log('Scene ready');
}

// Check VR/AR mode
if (scene.is('vr-mode')) {
  console.log('In VR mode');
}

if (scene.is('ar-mode')) {
  console.log('In AR mode');
}

// Enter/exit VR
scene.enterVR();
scene.exitVR();

// Access Three.js scene
const threeScene = scene.object3D;

// Access camera
const camera = scene.camera;

// Access renderer
const renderer = scene.renderer;

// Access systems
const geometrySystem = scene.systems.geometry;
```

---

## Entity

The `<a-entity>` is the base building block. All objects are entities with attached components.

### HTML Usage

```html
<a-entity
  id="myEntity"
  class="interactive"
  geometry="primitive: box; width: 2"
  material="color: red; metalness: 0.5"
  position="0 1.5 -3"
  rotation="0 45 0"
  scale="1 1 1"
  visible="true"
  mixin="baseEntity">
</a-entity>
```

### Core Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | string | - | Unique identifier |
| `class` | string | - | CSS-like class names |
| `mixin` | string | - | Space-separated mixin IDs |
| `visible` | boolean | true | Visibility |

### JavaScript API

```javascript
const entity = document.querySelector('#myEntity');

// Set attribute
entity.setAttribute('position', '1 2 3');
entity.setAttribute('position', {x: 1, y: 2, z: 3});

// Get attribute
const position = entity.getAttribute('position');
console.log(position.x, position.y, position.z);

// Add/remove class
entity.classList.add('interactive');
entity.classList.remove('interactive');

// Component methods
entity.setAttribute('my-component', 'value: 5');
entity.removeAttribute('my-component');
entity.hasAttribute('my-component');

// States
entity.addState('selected');
entity.removeState('selected');
entity.is('selected'); // Check state

// Events
entity.emit('hit', {damage: 10});
entity.addEventListener('hit', (evt) => {
  console.log('Damage:', evt.detail.damage);
});

// Access Three.js object
const object3D = entity.object3D;
object3D.position.set(1, 2, 3);
object3D.rotation.y = Math.PI / 4;

// Parent/child
const parent = entity.parentNode;
const children = entity.children;
entity.appendChild(childEntity);
entity.removeChild(childEntity);

// Play/pause
entity.play();
entity.pause();

// Component access
const material = entity.components.material;
```

---

## Core Components

### Camera

Defines the view into the 3D scene.

#### Properties

```html
<a-entity camera="
  active: true;
  far: 10000;
  fov: 80;
  near: 0.1;
  spectator: false;
  zoom: 1
"></a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `active` | boolean | true | Whether camera is active |
| `far` | number | 10000 | Far clipping plane |
| `fov` | number | 80 | Field of view (degrees) |
| `near` | number | 0.005 | Near clipping plane |
| `spectator` | boolean | false | Spectator mode (desktop only) |
| `zoom` | number | 1 | Zoom level |

#### Example

```html
<a-entity
  camera="fov: 60; near: 0.1; far: 1000"
  look-controls
  wasd-controls
  position="0 1.6 0">
</a-entity>
```

### Geometry

Defines the shape of an entity.

#### Properties

```html
<a-entity geometry="
  primitive: box;
  width: 1;
  height: 1;
  depth: 1
"></a-entity>
```

#### Primitives

**Box**
```html
<a-entity geometry="primitive: box; width: 1; height: 1; depth: 1"></a-entity>
```

**Sphere**
```html
<a-entity geometry="primitive: sphere; radius: 1; segmentsWidth: 32; segmentsHeight: 32"></a-entity>
```

**Plane**
```html
<a-entity geometry="primitive: plane; width: 1; height: 1"></a-entity>
```

**Cylinder**
```html
<a-entity geometry="primitive: cylinder; radius: 0.5; height: 1; segmentsRadial: 36"></a-entity>
```

**Cone**
```html
<a-entity geometry="primitive: cone; radiusBottom: 0.5; radiusTop: 0; height: 1"></a-entity>
```

**Circle**
```html
<a-entity geometry="primitive: circle; radius: 1; segments: 32; thetaStart: 0; thetaLength: 360"></a-entity>
```

**Ring**
```html
<a-entity geometry="primitive: ring; radiusInner: 0.5; radiusOuter: 1"></a-entity>
```

**Torus**
```html
<a-entity geometry="primitive: torus; radius: 1; radiusTubular: 0.2; segmentsRadial: 36; segmentsTubular: 32"></a-entity>
```

**Torus Knot**
```html
<a-entity geometry="primitive: torusKnot; radius: 1; radiusTubular: 0.2; p: 2; q: 3"></a-entity>
```

**Triangle**
```html
<a-entity geometry="primitive: triangle; vertexA: 0 0.5 0; vertexB: -0.5 -0.5 0; vertexC: 0.5 -0.5 0"></a-entity>
```

### Material

Defines the appearance of the geometry.

#### Standard Material Properties

```html
<a-entity material="
  color: #FFF;
  metalness: 0;
  opacity: 1;
  roughness: 0.5;
  shader: standard;
  side: front;
  transparent: false;
  vertexColors: none;
  visible: true
"></a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `color` | color | #FFF | Base color |
| `metalness` | number | 0 | Metallic property (0-1) |
| `opacity` | number | 1 | Opacity (0-1, requires transparent: true) |
| `roughness` | number | 0.5 | Surface roughness (0-1) |
| `shader` | string | standard | Shader type (standard, flat) |
| `side` | string | front | Which sides to render (front, back, double) |
| `transparent` | boolean | false | Enable transparency |
| `src` | selector | - | Texture image/video |
| `repeat` | vec2 | 1 1 | Texture repeat |
| `normalMap` | selector | - | Normal map texture |
| `emissive` | color | #000 | Emissive color |
| `emissiveIntensity` | number | 1 | Emissive intensity |

#### Flat Shader

```html
<a-entity material="shader: flat; color: #4CC3D9"></a-entity>
```

#### Textured Material

```html
<a-assets>
  <img id="texture" src="texture.jpg">
</a-assets>

<a-entity material="src: #texture; repeat: 2 2; normalMap: #normalTexture"></a-entity>
```

### Light

Illuminates the scene.

#### Types

**Ambient Light**
```html
<a-entity light="type: ambient; color: #BBB; intensity: 0.5"></a-entity>
```

**Directional Light**
```html
<a-entity light="
  type: directional;
  color: #FFF;
  intensity: 0.8;
  castShadow: true;
  shadowCameraLeft: -5;
  shadowCameraRight: 5;
  shadowCameraTop: 5;
  shadowCameraBottom: -5
" position="1 2 1"></a-entity>
```

**Point Light**
```html
<a-entity light="
  type: point;
  color: #F00;
  intensity: 2;
  distance: 50;
  decay: 1
" position="0 3 0"></a-entity>
```

**Spot Light**
```html
<a-entity light="
  type: spot;
  color: #FFF;
  intensity: 1.5;
  angle: 45;
  penumbra: 0.1;
  distance: 100;
  decay: 1;
  castShadow: true
" position="0 5 0" rotation="-90 0 0"></a-entity>
```

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `type` | string | directional | Light type |
| `color` | color | #FFF | Light color |
| `intensity` | number | 1 | Light intensity |
| `castShadow` | boolean | false | Cast shadows |
| `distance` | number | 0 | Max distance (point/spot) |
| `decay` | number | 1 | Light decay (point/spot) |
| `angle` | number | 60 | Spot cone angle (degrees) |
| `penumbra` | number | 0 | Spot edge softness (0-1) |

### Position, Rotation, Scale

Transform components control entity placement and orientation.

#### Position

```html
<a-entity position="0 1.5 -3"></a-entity>
<a-entity position="x: 0; y: 1.5; z: -3"></a-entity>
```

```javascript
entity.setAttribute('position', '1 2 3');
entity.setAttribute('position', {x: 1, y: 2, z: 3});
entity.object3D.position.set(1, 2, 3);
```

#### Rotation

```html
<!-- Degrees -->
<a-entity rotation="0 45 0"></a-entity>
<a-entity rotation="x: 0; y: 45; z: 0"></a-entity>
```

```javascript
// Degrees
entity.setAttribute('rotation', '0 90 0');
entity.setAttribute('rotation', {x: 0, y: 90, z: 0});

// Radians (Three.js)
entity.object3D.rotation.y = Math.PI / 2;
```

#### Scale

```html
<a-entity scale="2 2 2"></a-entity>
<a-entity scale="x: 2; y: 1; z: 2"></a-entity>
```

```javascript
entity.setAttribute('scale', '2 2 2');
entity.setAttribute('scale', {x: 2, y: 1, z: 2});
entity.object3D.scale.set(2, 1, 2);
```

### Animation

Animate entity properties over time.

#### Properties

```html
<a-entity animation="
  property: rotation;
  to: 0 360 0;
  dur: 2000;
  easing: linear;
  loop: true;
  dir: normal;
  delay: 0;
  startEvents: click;
  pauseEvents: pause;
  resumeEvents: resume
"></a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `property` | string | - | Property to animate |
| `from` | - | current | Starting value |
| `to` | - | - | Target value |
| `dur` | number | 1000 | Duration (ms) |
| `delay` | number | 0 | Delay before start (ms) |
| `easing` | string | easeInQuad | Easing function |
| `loop` | boolean/number | false | Loop (true, false, or count) |
| `dir` | string | normal | Direction (normal, alternate, reverse) |
| `startEvents` | array | [] | Events that start animation |
| `pauseEvents` | array | [] | Events that pause animation |
| `resumeEvents` | array | [] | Events that resume animation |

#### Easing Functions

`linear`, `easeInQuad`, `easeOutQuad`, `easeInOutQuad`, `easeInCubic`, `easeOutCubic`, `easeInOutCubic`, `easeInQuart`, `easeOutQuart`, `easeInOutQuart`, `easeInQuint`, `easeOutQuint`, `easeInOutQuint`, `easeInSine`, `easeOutSine`, `easeInOutSine`, `easeInExpo`, `easeOutExpo`, `easeInOutExpo`, `easeInCirc`, `easeOutCirc`, `easeInOutCirc`, `easeInElastic`, `easeOutElastic`, `easeInOutElastic`, `easeInBack`, `easeOutBack`, `easeInOutBack`, `easeInBounce`, `easeOutBounce`, `easeInOutBounce`

#### Examples

```html
<!-- Continuous rotation -->
<a-box animation="property: rotation; to: 0 360 0; loop: true; dur: 5000"></a-box>

<!-- Multiple animations -->
<a-sphere
  animation__rotate="property: rotation; to: 360 360 0; loop: true; dur: 10000"
  animation__scale="property: scale; to: 1.5 1.5 1.5; dir: alternate; loop: true; dur: 2000">
</a-sphere>

<!-- Event-triggered -->
<a-box
  animation__click="property: position; to: 0 5 0; startEvents: click"
  animation__mouseenter="property: scale; to: 1.2 1.2 1.2; startEvents: mouseenter"
  animation__mouseleave="property: scale; to: 1 1 1; startEvents: mouseleave">
</a-box>
```

### Sound

Audio playback component.

#### Properties

```html
<a-entity sound="
  src: #sound1;
  autoplay: false;
  loop: false;
  on: click;
  poolSize: 1;
  volume: 1
"></a-entity>
```

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `src` | selector | - | Audio asset |
| `autoplay` | boolean | false | Play on load |
| `loop` | boolean | false | Loop audio |
| `on` | string | - | Event to play on |
| `poolSize` | number | 1 | Audio buffer pool size |
| `volume` | number | 1 | Volume (0-1) |
| `positional` | boolean | true | 3D positional audio |
| `refDistance` | number | 1 | Reference distance for falloff |
| `rolloffFactor` | number | 1 | Rolloff rate |

#### Example

```html
<a-assets>
  <audio id="click-sound" src="click.mp3"></audio>
  <audio id="bg-music" src="music.mp3"></audio>
</a-assets>

<!-- Play on click -->
<a-box sound="src: #click-sound; on: click" position="0 1 -3"></a-box>

<!-- Background music -->
<a-entity sound="src: #bg-music; autoplay: true; loop: true; volume: 0.5"></a-entity>

<!-- Positional audio -->
<a-entity sound="src: #ambient; autoplay: true; loop: true; positional: true" position="5 0 0"></a-entity>
```

---

## Primitives

Primitives are shortcuts for entity + common components.

### a-box

```html
<a-box
  color="#4CC3D9"
  depth="1"
  height="1"
  width="1"
  position="0 1 -3"
  rotation="0 45 0"
  scale="2 2 2"
  src="#texture"
  metalness="0.5"
  roughness="0.3">
</a-box>
```

Equivalent to:
```html
<a-entity
  geometry="primitive: box; width: 1; height: 1; depth: 1"
  material="color: #4CC3D9; metalness: 0.5; roughness: 0.3; src: #texture"
  position="0 1 -3"
  rotation="0 45 0"
  scale="2 2 2">
</a-entity>
```

### a-sphere

```html
<a-sphere
  color="#EF2D5E"
  radius="1.25"
  segments-width="32"
  segments-height="32"
  phi-start="0"
  phi-length="360"
  theta-start="0"
  theta-length="180"
  position="0 1.25 -5">
</a-sphere>
```

### a-cylinder

```html
<a-cylinder
  color="#FFC65D"
  height="1.5"
  radius="0.5"
  radius-bottom="0.5"
  radius-top="0.5"
  segments-radial="36"
  segments-height="1"
  open-ended="false"
  position="1 0.75 -3">
</a-cylinder>
```

### a-plane

```html
<a-plane
  color="#7BC8A4"
  width="4"
  height="4"
  segments-width="1"
  segments-height="1"
  position="0 0 -4"
  rotation="-90 0 0"
  src="#ground-texture">
</a-plane>
```

### a-sky

```html
<!-- Solid color -->
<a-sky color="#ECECEC"></a-sky>

<!-- 360 image -->
<a-assets>
  <img id="sky-texture" src="sky.jpg">
</a-assets>
<a-sky src="#sky-texture" rotation="0 -130 0"></a-sky>

<!-- 360 video -->
<a-assets>
  <video id="sky-video" src="360video.mp4" autoplay loop></video>
</a-assets>
<a-sky src="#sky-video"></a-sky>
```

### a-camera

```html
<a-camera
  active="true"
  far="10000"
  fov="80"
  look-controls-enabled="true"
  near="0.1"
  position="0 1.6 0"
  reverse-mouse-drag="false"
  wasd-controls-enabled="true">
  <a-cursor></a-cursor>
</a-camera>
```

### a-cursor

```html
<a-cursor
  fuse="false"
  fuse-timeout="1500"
  max-distance="1000"
  raycaster="objects: .interactive">
</a-cursor>
```

### a-light

```html
<a-light type="ambient" color="#BBB" intensity="0.5"></a-light>
<a-light type="directional" color="#FFF" intensity="0.8" position="1 2 1"></a-light>
<a-light type="point" color="#F00" intensity="2" distance="50" position="0 3 0"></a-light>
<a-light type="spot" color="#FFF" intensity="1.5" angle="45" position="0 5 0" rotation="-90 0 0"></a-light>
```

### a-text

```html
<a-text
  value="Hello World"
  color="#FFF"
  width="4"
  align="center"
  anchor="center"
  baseline="center"
  font="roboto"
  letter-spacing="0"
  line-height="1"
  opacity="1"
  side="front"
  wrap-count="40"
  position="0 2 -3">
</a-text>
```

### a-gltf-model

```html
<a-assets>
  <a-asset-item id="tree" src="tree.gltf"></a-asset-item>
</a-assets>

<a-gltf-model
  src="#tree"
  position="0 0 -5"
  scale="0.5 0.5 0.5"
  rotation="0 45 0">
</a-gltf-model>
```

---

## Controls

### look-controls

Enable mouse/touch drag to look around.

```html
<a-entity camera look-controls="
  enabled: true;
  hmdEnabled: true;
  reverseMouseDrag: false;
  reverseTouchDrag: false;
  touchEnabled: true;
  mouseEnabled: true;
  pointerLockEnabled: false
"></a-entity>
```

### wasd-controls

Keyboard movement (W/A/S/D).

```html
<a-entity camera wasd-controls="
  enabled: true;
  acceleration: 65;
  easing: 20;
  fly: false
"></a-entity>
```

### cursor

Raycaster-based pointer for interactions.

```html
<a-cursor
  raycaster="objects: .interactive; far: 1000"
  fuse="false"
  fuse-timeout="1500">
</a-cursor>
```

---

## VR/XR Components

### hand-controls

VR controller hands visualization and tracking.

```html
<a-entity hand-controls="hand: left; handModelStyle: lowPoly; color: #ffcccc"></a-entity>
<a-entity hand-controls="hand: right; handModelStyle: highPoly; color: #ffcccc"></a-entity>
```

### laser-controls

Laser pointer for VR controllers.

```html
<a-entity
  laser-controls="hand: right"
  raycaster="objects: .interactive; far: 10">
</a-entity>
```

### vive-controls

HTC Vive controller support.

```html
<a-entity vive-controls="hand: left; buttonColor: #FF0000; buttonHighlightColor: #FFFF00"></a-entity>
<a-entity vive-controls="hand: right"></a-entity>
```

### meta-touch-controls

Meta Quest/Oculus Touch controller support.

```html
<a-entity meta-touch-controls="hand: left; model: true"></a-entity>
<a-entity meta-touch-controls="hand: right; model: true"></a-entity>
```

### webxr

Configure WebXR features and settings.

```html
<a-scene webxr="
  requiredFeatures: hit-test, local-floor;
  optionalFeatures: dom-overlay, unbounded;
  overlayElement: #overlay;
  referenceSpaceType: local-floor
"></a-scene>
```

### ar-hit-test

AR surface detection and object placement.

```html
<a-scene
  webxr="optionalFeatures: hit-test"
  ar-hit-test="target: #furniture; type: footprint">

  <a-entity id="furniture" gltf-model="#chair"></a-entity>
</a-scene>
```

Events:
- `ar-hit-test-start`: Hit testing started
- `ar-hit-test-achieved`: Surface detected
- `ar-hit-test-select`: User selected placement location

---

## Systems

Systems provide global scene-level functionality.

### Geometry System

```javascript
const geometrySystem = document.querySelector('a-scene').systems.geometry;
```

### Material System

```javascript
const materialSystem = document.querySelector('a-scene').systems.material;
```

### Accessing Systems

```javascript
AFRAME.registerComponent('my-component', {
  init: function() {
    const geometrySystem = this.el.sceneEl.systems.geometry;
    const materialSystem = this.el.sceneEl.systems.material;
  }
});
```

---

## Component API

Register custom components to extend A-Frame.

### Basic Component

```javascript
AFRAME.registerComponent('my-component', {
  // Component schema (configuration)
  schema: {
    color: {type: 'color', default: '#FFF'},
    size: {type: 'number', default: 1},
    enabled: {type: 'boolean', default: true}
  },

  // Initialize (called once)
  init: function() {
    console.log('Component initialized');
    // this.el = entity element
    // this.data = component data
    // this.el.sceneEl = scene element
  },

  // Update (called when properties change)
  update: function(oldData) {
    console.log('Component updated');
    // this.data = new data
    // oldData = previous data
  },

  // Remove (called when component removed)
  remove: function() {
    console.log('Component removed');
  },

  // Tick (called every frame)
  tick: function(time, timeDelta) {
    // time = total elapsed time (ms)
    // timeDelta = time since last tick (ms)
  },

  // Pause (called when entity/scene pauses)
  pause: function() {
    console.log('Component paused');
  },

  // Play (called when entity/scene plays)
  play: function() {
    console.log('Component playing');
  }
});
```

### Schema Types

```javascript
schema: {
  // Basic types
  boolean: {type: 'boolean', default: false},
  number: {type: 'number', default: 0},
  string: {type: 'string', default: ''},

  // Color
  color: {type: 'color', default: '#FFF'},

  // Vectors
  vec2: {type: 'vec2', default: {x: 0, y: 0}},
  vec3: {type: 'vec3', default: {x: 0, y: 0, z: 0}},
  vec4: {type: 'vec4', default: {x: 0, y: 0, z: 0, w: 1}},

  // Selectors
  selector: {type: 'selector'}, // CSS selector
  selectorAll: {type: 'selectorAll'}, // Multiple elements

  // Assets
  audio: {type: 'audio'},
  map: {type: 'map'},
  model: {type: 'model'},

  // Arrays
  array: {type: 'array', default: []},

  // Objects
  object: {type: 'object', default: {}}
}
```

### Multi-Property Components

```javascript
AFRAME.registerComponent('light', {
  schema: {
    type: {default: 'directional', oneOf: ['ambient', 'directional', 'point', 'spot']},
    color: {type: 'color', default: '#FFF'},
    intensity: {type: 'number', default: 1}
  },

  init: function() {
    // Access individual properties
    console.log(this.data.type);
    console.log(this.data.color);
    console.log(this.data.intensity);
  }
});
```

Usage:
```html
<a-entity light="type: point; color: #F00; intensity: 2"></a-entity>
```

### Single-Property Components

```javascript
AFRAME.registerComponent('visible', {
  schema: {type: 'boolean', default: true},

  update: function() {
    // this.data is the boolean value directly
    this.el.object3D.visible = this.data;
  }
});
```

Usage:
```html
<a-entity visible="false"></a-entity>
```

---

## JavaScript API

### Creating Entities

```javascript
const scene = document.querySelector('a-scene');

// Create entity
const entity = document.createElement('a-entity');

// Set attributes
entity.setAttribute('geometry', {primitive: 'box', width: 2});
entity.setAttribute('material', {color: 'red'});
entity.setAttribute('position', {x: 0, y: 1, z: -3});

// Append to scene
scene.appendChild(entity);
```

### Removing Entities

```javascript
const entity = document.querySelector('#myEntity');
entity.parentNode.removeChild(entity);
```

### Event Handling

```javascript
const box = document.querySelector('a-box');

// Listen to events
box.addEventListener('click', (evt) => {
  console.log('Clicked at:', evt.detail.intersection.point);
});

box.addEventListener('mouseenter', () => {
  box.setAttribute('color', 'yellow');
});

box.addEventListener('mouseleave', () => {
  box.setAttribute('color', 'blue');
});

// Emit custom events
box.emit('hit', {damage: 10});

box.addEventListener('hit', (evt) => {
  console.log('Damage:', evt.detail.damage);
});
```

### Accessing Components

```javascript
const entity = document.querySelector('#myEntity');

// Get component instance
const material = entity.components.material;
const geometry = entity.components.geometry;

// Access component data
console.log(material.data.color);

// Call component methods
material.update();
```

### Three.js Integration

```javascript
const entity = document.querySelector('a-box');

// Access Three.js Object3D
const object3D = entity.object3D;

// Manipulate directly
object3D.position.set(1, 2, 3);
object3D.rotation.y = Math.PI / 4;
object3D.scale.set(2, 2, 2);

// Access Three.js mesh
const mesh = entity.getObject3D('mesh');
console.log(mesh.geometry);
console.log(mesh.material);

// Add custom Three.js objects
const scene = document.querySelector('a-scene').object3D;
const customMesh = new THREE.Mesh(geometry, material);
scene.add(customMesh);
```

### Wait for Scene Load

```javascript
const scene = document.querySelector('a-scene');

if (scene.hasLoaded) {
  run();
} else {
  scene.addEventListener('loaded', run);
}

function run() {
  console.log('Scene is ready');
}
```

### Animation Control

```javascript
const entity = document.querySelector('#animated');

// Start animation
entity.emit('startAnimation');

// Pause animation
entity.components.animation.pauseAnimation();

// Resume animation
entity.components.animation.resumeAnimation();
```

### States

```javascript
const enemy = document.querySelector('#enemy');

// Add state
enemy.addState('attacking');
enemy.addState('angry');

// Check state
if (enemy.is('attacking')) {
  console.log('Enemy is attacking');
}

// Remove state
enemy.removeState('attacking');

// Listen to state changes
enemy.addEventListener('stateadded', (evt) => {
  console.log('State added:', evt.detail);
});

enemy.addEventListener('stateremoved', (evt) => {
  console.log('State removed:', evt.detail);
});
```

---

## Constants

### Key Codes

Use with keyboard events:

```javascript
document.addEventListener('keydown', (evt) => {
  if (evt.key === 'w' || evt.key === 'W') {
    console.log('W pressed');
  }
});
```

Common keys:
- `'w'`, `'a'`, `'s'`, `'d'` - Movement
- `' '` - Spacebar
- `'Escape'` - Escape
- `'Enter'` - Enter
- `'ArrowUp'`, `'ArrowDown'`, `'ArrowLeft'`, `'ArrowRight'` - Arrow keys

### Side Constants

```javascript
// Material side
'front' // THREE.FrontSide
'back'  // THREE.BackSide
'double' // THREE.DoubleSide
```

### Easing Functions

See Animation component for full list of easing functions.

---

## Examples

### Complete Scene

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <a-assets>
        <img id="ground-texture" src="ground.jpg">
        <img id="sky-texture" src="sky.jpg">
        <a-asset-item id="tree" src="tree.gltf"></a-asset-item>
      </a-assets>

      <!-- Environment -->
      <a-sky src="#sky-texture"></a-sky>
      <a-plane src="#ground-texture" rotation="-90 0 0" width="100" height="100"></a-plane>

      <!-- Lighting -->
      <a-entity light="type: ambient; color: #888; intensity: 0.5"></a-entity>
      <a-entity light="type: directional; color: #FFF; intensity: 0.8" position="2 4 2"></a-entity>

      <!-- Objects -->
      <a-box position="-1 0.5 -3" color="#4CC3D9"></a-box>
      <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
      <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></a-cylinder>
      <a-gltf-model src="#tree" position="3 0 -5" scale="0.5 0.5 0.5"></a-gltf-model>

      <!-- Camera -->
      <a-camera position="0 1.6 0">
        <a-cursor></a-cursor>
      </a-camera>
    </a-scene>
  </body>
</html>
```

This API reference covers the core A-Frame components and patterns for building VR/AR experiences.
