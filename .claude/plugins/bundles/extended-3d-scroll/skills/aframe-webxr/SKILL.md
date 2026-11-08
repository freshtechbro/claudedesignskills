---
name: aframe-webxr
description: Declarative web framework for building browser-based 3D, VR, and AR experiences using HTML and entity-component architecture. Use this skill when creating WebXR applications, VR experiences, AR experiences, 360-degree media viewers, or immersive web content with minimal JavaScript. Triggers on tasks involving A-Frame, WebXR, VR development, AR development, entity-component-system, declarative 3D, or HTML-based 3D scenes. Built on Three.js with accessible HTML-first approach.
---

# A-Frame WebXR Skill

## When to Use This Skill
- Build VR/AR experiences with minimal JavaScript
- Create cross-platform WebXR applications (desktop, mobile, headset)
- Prototype 3D scenes quickly with HTML primitives
- Implement VR controller interactions
- Add 3D content to web pages declaratively
- Build 360° image/video experiences
- Develop AR experiences with hit testing

## Core Concepts

### 1. Entity-Component-System (ECS)

A-Frame uses an entity-component-system architecture where:
- **Entities** are containers (like `<div>` in HTML)
- **Components** add functionality/appearance to entities
- **Systems** provide global functionality

```html
<!-- Entity with components -->
<a-entity
  geometry="primitive: box; width: 2"
  material="color: red; metalness: 0.5"
  position="0 1.5 -3"
  rotation="0 45 0">
</a-entity>
```

**Primitives** are shortcuts for common entity + component combinations:

```html
<!-- Primitive (shorthand) -->
<a-box color="red" position="0 1.5 -3" rotation="0 45 0" width="2"></a-box>

<!-- Equivalent entity-component form -->
<a-entity
  geometry="primitive: box; width: 2"
  material="color: red"
  position="0 1.5 -3"
  rotation="0 45 0">
</a-entity>
```

### 2. Scene Setup

Every A-Frame app starts with `<a-scene>`:

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <!-- Entities go here -->
      <a-box position="-1 0.5 -3" color="#4CC3D9"></a-box>
      <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
      <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D"></a-cylinder>
      <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></a-plane>
      <a-sky color="#ECECEC"></a-sky>
    </a-scene>
  </body>
</html>
```

The scene automatically injects:
- Default camera (position: `0 1.6 0`)
- Look controls (mouse drag)
- WASD controls (keyboard movement)

### 3. Camera Systems

**Default Camera** (auto-injected if none specified):

```html
<a-entity camera="active: true" look-controls wasd-controls position="0 1.6 0"></a-entity>
```

**Custom Camera**:

```html
<a-camera position="0 2 5" look-controls wasd-controls="acceleration: 50"></a-camera>
```

**Camera Rig** (for independent movement and rotation):

```html
<a-entity id="rig" position="0 0 0">
  <!-- Camera for head tracking -->
  <a-camera look-controls></a-camera>

  <!-- Movement applied to rig, not camera -->
</a-entity>
```

**VR Camera Rig with Controllers**:

```html
<a-entity id="rig" position="0 0 0">
  <!-- Camera at eye level -->
  <a-camera position="0 1.6 0"></a-camera>

  <!-- Left hand controller -->
  <a-entity
    hand-controls="hand: left"
    laser-controls="hand: left">
  </a-entity>

  <!-- Right hand controller -->
  <a-entity
    hand-controls="hand: right"
    laser-controls="hand: right">
  </a-entity>
</a-entity>
```

### 4. Lighting

**Ambient Light** (global illumination):

```html
<a-entity light="type: ambient; color: #BBB; intensity: 0.5"></a-entity>
```

**Directional Light** (like sunlight):

```html
<a-entity light="type: directional; color: #FFF; intensity: 0.8" position="1 2 1"></a-entity>
```

**Point Light** (radiates in all directions):

```html
<a-entity light="type: point; color: #F00; intensity: 2; distance: 50" position="0 3 0"></a-entity>
```

**Spot Light** (cone-shaped beam):

```html
<a-entity light="type: spot; angle: 45; intensity: 1.5" position="0 5 0" rotation="-90 0 0"></a-entity>
```

### 5. Materials and Textures

**Standard Material**:

```html
<a-sphere
  material="color: #FF0000; metalness: 0.5; roughness: 0.3"
  position="0 1 -3">
</a-sphere>
```

**Textured Material**:

```html
<a-assets>
  <img id="woodTexture" src="wood.jpg">
</a-assets>

<a-box material="src: #woodTexture" position="0 1 -3"></a-box>
```

**Flat Shading** (no lighting):

```html
<a-plane material="shader: flat; color: #4CC3D9"></a-plane>
```

### 6. Animations

**Property Animation**:

```html
<a-box
  position="0 1 -3"
  animation="property: rotation; to: 0 360 0; loop: true; dur: 5000">
</a-box>
```

**Multiple Animations** (use `animation__*` naming):

```html
<a-sphere
  position="0 1 -3"
  animation__position="property: position; to: 0 3 -3; dir: alternate; loop: true; dur: 2000"
  animation__rotation="property: rotation; to: 360 360 0; loop: true; dur: 4000"
  animation__scale="property: scale; to: 1.5 1.5 1.5; dir: alternate; loop: true; dur: 1000">
</a-sphere>
```

**Event-Based Animation**:

```html
<a-box
  color="blue"
  animation__mouseenter="property: scale; to: 1.2 1.2 1.2; startEvents: mouseenter"
  animation__mouseleave="property: scale; to: 1 1 1; startEvents: mouseleave"
  animation__click="property: rotation; from: 0 0 0; to: 0 360 0; startEvents: click">
</a-box>
```

### 7. Assets Management

Preload assets for better performance:

```html
<a-scene>
  <a-assets>
    <!-- Images -->
    <img id="texture1" src="texture.jpg">
    <img id="skyTexture" src="sky.jpg">

    <!-- Videos -->
    <video id="video360" src="360video.mp4" autoplay loop></video>

    <!-- Audio -->
    <audio id="bgMusic" src="music.mp3" preload="auto"></audio>

    <!-- Models -->
    <a-asset-item id="tree" src="tree.gltf"></a-asset-item>

    <!-- Mixins (reusable component sets) -->
    <a-mixin id="redMaterial" material="color: red; metalness: 0.7"></a-mixin>
  </a-assets>

  <!-- Use assets -->
  <a-entity gltf-model="#tree" position="2 0 -5"></a-entity>
  <a-sphere mixin="redMaterial" position="0 1 -3"></a-sphere>
  <a-sky src="#skyTexture"></a-sky>
</a-scene>
```

### 8. Custom Components

Register custom components to encapsulate logic:

```javascript
AFRAME.registerComponent('rotate-on-click', {
  // Component schema (configuration)
  schema: {
    speed: {type: 'number', default: 1}
  },

  // Lifecycle: called once when component attached
  init: function() {
    this.el.addEventListener('click', () => {
      this.rotating = !this.rotating;
    });
  },

  // Lifecycle: called every frame
  tick: function(time, timeDelta) {
    if (this.rotating) {
      var rotation = this.el.getAttribute('rotation');
      rotation.y += this.data.speed;
      this.el.setAttribute('rotation', rotation);
    }
  }
});
```

```html
<a-box rotate-on-click="speed: 2" position="0 1 -3"></a-box>
```

## Common Patterns

### Pattern 1: VR Controller Interactions

**Problem**: Enable object grabbing and manipulation in VR

**Solution**: Use hand-controls and custom grab component

```html
<a-scene>
  <!-- VR Camera Rig -->
  <a-entity id="rig">
    <a-camera position="0 1.6 0"></a-camera>

    <a-entity
      id="leftHand"
      hand-controls="hand: left"
      laser-controls="hand: left">
    </a-entity>

    <a-entity
      id="rightHand"
      hand-controls="hand: right"
      laser-controls="hand: right">
    </a-entity>
  </a-entity>

  <!-- Grabbable objects -->
  <a-box class="grabbable" position="-1 1.5 -3" color="#4CC3D9"></a-box>
  <a-sphere class="grabbable" position="1 1.5 -3" color="#EF2D5E"></a-sphere>
</a-scene>

<script>
AFRAME.registerComponent('grabbable', {
  init: function() {
    var el = this.el;

    el.addEventListener('triggerdown', function(evt) {
      console.log('Grabbed by', evt.detail.hand);
      el.setAttribute('color', 'green');
    });

    el.addEventListener('triggerup', function(evt) {
      el.setAttribute('color', 'blue');
    });

    el.addEventListener('gripdown', function(evt) {
      // Attach object to controller
      var controllerEl = evt.detail.controller;
      controllerEl.object3D.attach(el.object3D);
    });

    el.addEventListener('gripup', function(evt) {
      // Detach from controller
      var sceneEl = el.sceneEl.object3D;
      sceneEl.attach(el.object3D);
    });
  }
});

// Apply grabbable component
document.querySelectorAll('.grabbable').forEach(el => {
  el.setAttribute('grabbable', '');
});
</script>
```

### Pattern 2: 360° Image Gallery

**Problem**: Create an interactive 360° photo viewer

**Solution**: Use sky primitive and clickable thumbnails

```html
<a-scene>
  <a-assets>
    <img id="city" src="city.jpg">
    <img id="forest" src="forest.jpg">
    <img id="beach" src="beach.jpg">
    <img id="city-thumb" src="city-thumb.jpg">
    <img id="forest-thumb" src="forest-thumb.jpg">
    <img id="beach-thumb" src="beach-thumb.jpg">
    <audio id="click-sound" src="click.mp3"></audio>
  </a-assets>

  <!-- 360 image sphere -->
  <a-sky id="image-360" src="#city" rotation="0 -130 0"></a-sky>

  <!-- Thumbnail menu -->
  <a-entity id="menu" position="0 1.6 -2">
    <a-entity class="link"
      geometry="primitive: plane; width: 0.7; height: 0.7"
      material="shader: flat; src: #city-thumb"
      position="-1 0 0"
      sound="on: click; src: #click-sound"
      event-set__mouseenter="scale: 1.2 1.2 1"
      event-set__mouseleave="scale: 1 1 1"
      event-set__click="_target: #image-360; material.src: #city">
    </a-entity>

    <a-entity class="link"
      geometry="primitive: plane; width: 0.7; height: 0.7"
      material="shader: flat; src: #forest-thumb"
      position="0 0 0"
      sound="on: click; src: #click-sound"
      event-set__mouseenter="scale: 1.2 1.2 1"
      event-set__mouseleave="scale: 1 1 1"
      event-set__click="_target: #image-360; material.src: #forest">
    </a-entity>

    <a-entity class="link"
      geometry="primitive: plane; width: 0.7; height: 0.7"
      material="shader: flat; src: #beach-thumb"
      position="1 0 0"
      sound="on: click; src: #click-sound"
      event-set__mouseenter="scale: 1.2 1.2 1"
      event-set__mouseleave="scale: 1 1 1"
      event-set__click="_target: #image-360; material.src: #beach">
    </a-entity>
  </a-entity>

  <!-- Camera with cursor for gaze interaction -->
  <a-camera>
    <a-cursor raycaster="objects: .link"></a-cursor>
  </a-camera>
</a-scene>
```

### Pattern 3: AR Hit Testing (Place Objects in Real World)

**Problem**: Place virtual objects on detected real-world surfaces

**Solution**: Use ar-hit-test component

```html
<a-scene
  webxr="optionalFeatures: hit-test, dom-overlay; overlayElement: #overlay"
  ar-hit-test="target: #furniture; type: footprint">

  <a-assets>
    <a-asset-item id="chair" src="chair.gltf"></a-asset-item>
  </a-assets>

  <!-- Object to place -->
  <a-entity id="furniture" gltf-model="#chair" scale="0.5 0.5 0.5"></a-entity>

  <!-- AR instructions overlay -->
  <div id="overlay" style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
                           background: rgba(0,0,0,0.7); color: white; padding: 15px;
                           border-radius: 8px; font-family: sans-serif;">
    <p id="message">Tap to enter AR mode</p>
  </div>
</a-scene>

<script>
const sceneEl = document.querySelector('a-scene');
const message = document.getElementById('message');

sceneEl.addEventListener('enter-vr', function() {
  if (this.is('ar-mode')) {
    message.textContent = '';

    this.addEventListener('ar-hit-test-start', function() {
      message.innerHTML = 'Scanning environment, finding surface.';
    }, { once: true });

    this.addEventListener('ar-hit-test-achieved', function() {
      message.innerHTML = 'Tap on the screen to place the object.';
    }, { once: true });

    this.addEventListener('ar-hit-test-select', function() {
      message.textContent = 'Object placed!';
      setTimeout(() => message.textContent = '', 2000);
    }, { once: true });
  }
});

sceneEl.addEventListener('exit-vr', function() {
  message.textContent = 'Tap to enter AR mode';
});
</script>
```

### Pattern 4: Mouse/Gaze Interactions

**Problem**: Enable click interactions with desktop mouse or VR gaze

**Solution**: Use cursor component and raycaster

```html
<a-scene>
  <!-- Interactive objects -->
  <a-box
    class="interactive"
    position="-1 1.5 -3"
    color="#4CC3D9"
    event-set__mouseenter="color: yellow"
    event-set__mouseleave="color: #4CC3D9"
    event-set__click="scale: 1.5 1.5 1.5">
  </a-box>

  <a-sphere
    class="interactive"
    position="1 1.5 -3"
    color="#EF2D5E"
    event-set__click="color: orange; scale: 2 2 2">
  </a-sphere>

  <a-plane position="0 0 -4" rotation="-90 0 0" width="10" height="10" color="#7BC8A4"></a-plane>

  <!-- Camera with cursor -->
  <a-camera position="0 1.6 0">
    <!-- Raycaster targets .interactive class -->
    <a-cursor
      raycaster="objects: .interactive"
      fuse="true"
      fuse-timeout="1500">
    </a-cursor>
  </a-camera>
</a-scene>

<script>
// Advanced click handling with JavaScript
document.querySelectorAll('.interactive').forEach(el => {
  el.addEventListener('click', function(evt) {
    console.log('Clicked:', this.id || this.tagName);
    console.log('Intersection point:', evt.detail.intersection.point);
  });
});
</script>
```

### Pattern 5: Dynamic Scene Generation

**Problem**: Programmatically create and manipulate entities

**Solution**: Use JavaScript DOM manipulation

```html
<a-scene>
  <a-camera position="0 1.6 5"></a-camera>
  <a-entity light="type: ambient; color: #888"></a-entity>
  <a-entity light="type: directional; color: #FFF" position="1 2 1"></a-entity>
</a-scene>

<script>
const scene = document.querySelector('a-scene');

// Create sphere
function createSphere(x, y, z, color) {
  const entity = document.createElement('a-entity');

  entity.setAttribute('geometry', {
    primitive: 'sphere',
    radius: 0.5
  });

  entity.setAttribute('material', {
    color: color,
    metalness: 0.5,
    roughness: 0.3
  });

  entity.setAttribute('position', {x, y, z});

  // Add animation
  entity.setAttribute('animation', {
    property: 'position',
    to: `${x} ${y + 1} ${z}`,
    dir: 'alternate',
    loop: true,
    dur: 2000
  });

  scene.appendChild(entity);
  return entity;
}

// Generate grid of spheres
for (let x = -3; x <= 3; x += 1.5) {
  for (let z = -5; z <= -2; z += 1.5) {
    const color = `#${Math.floor(Math.random()*16777215).toString(16)}`;
    createSphere(x, 1, z, color);
  }
}

// Listen to component changes
scene.addEventListener('componentchanged', function(evt) {
  console.log('Component changed:', evt.detail.name);
});

// Access Three.js objects directly
setTimeout(() => {
  const entities = document.querySelectorAll('a-entity[geometry]');
  entities.forEach(el => {
    el.object3D.visible = true; // Direct Three.js manipulation
  });
}, 1000);
</script>
```

### Pattern 6: Environment and Skybox

**Problem**: Create immersive environments quickly

**Solution**: Use community components and 360 images

```html
<html>
  <head>
    <script src="https://aframe.io/releases/1.7.1/aframe.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@fern-solutions/aframe-sky-background/dist/sky-background.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/c-frame/aframe-extras@7.5.0/dist/aframe-extras.min.js"></script>
  </head>
  <body>
    <a-scene>
      <!-- Gradient sky -->
      <a-sky-background
        top-color="#4A90E2"
        bottom-color="#87CEEB">
      </a-sky-background>

      <!-- Or textured sky -->
      <!-- <a-sky src="sky.jpg" rotation="0 -130 0"></a-sky> -->

      <!-- Ocean -->
      <a-entity
        ocean="density: 20; width: 50; depth: 50; speed: 4"
        material="color: #9CE3F9; opacity: 0.75; metalness: 0; roughness: 1"
        rotation="-90 0 0">
      </a-entity>

      <!-- Particle system for atmosphere -->
      <a-entity
        particle-system="preset: snow; particleCount: 2000; color: #FFF">
      </a-entity>

      <a-entity light="type: ambient; color: #888"></a-entity>
      <a-entity light="type: directional; color: #FFF; intensity: 0.7" position="1 2 1"></a-entity>
    </a-scene>
  </body>
</html>
```

### Pattern 7: GLTF Model Loading

**Problem**: Load and display 3D models

**Solution**: Use gltf-model component with asset management

```html
<a-scene>
  <a-assets>
    <a-asset-item id="robot" src="robot.gltf"></a-asset-item>
    <a-asset-item id="building" src="building.glb"></a-asset-item>
  </a-assets>

  <!-- Load model -->
  <a-entity
    gltf-model="#robot"
    position="0 0 -3"
    scale="0.5 0.5 0.5"
    animation="property: rotation; to: 0 360 0; loop: true; dur: 10000">
  </a-entity>

  <!-- Load with extras (animations) -->
  <a-entity
    gltf-model="#building"
    position="5 0 -10"
    animation-mixer="clip: *; loop: repeat">
  </a-entity>

  <a-camera position="0 1.6 5"></a-camera>
  <a-entity light="type: ambient; intensity: 0.5"></a-entity>
  <a-entity light="type: directional; intensity: 0.8" position="2 4 2"></a-entity>
</a-scene>

<script>
// Handle model loading events
document.querySelector('[gltf-model="#robot"]').addEventListener('model-loaded', (evt) => {
  console.log('Model loaded:', evt.detail.model);

  // Access Three.js object
  const model = evt.detail.model;
  model.traverse(node => {
    if (node.isMesh) {
      console.log('Mesh found:', node.name);
    }
  });
});

document.querySelector('[gltf-model="#robot"]').addEventListener('model-error', (evt) => {
  console.error('Model loading error:', evt.detail);
});
</script>
```

## Integration Patterns

### With Three.js

Access underlying Three.js objects:

```javascript
// Get Three.js scene
const scene = document.querySelector('a-scene').object3D;

// Get entity's Three.js object
const box = document.querySelector('a-box');
const threeObject = box.object3D;

// Direct Three.js manipulation
threeObject.position.set(1, 2, 3);
threeObject.rotation.y = Math.PI / 4;

// Add custom Three.js objects
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
```

### With GSAP (Animation)

Animate A-Frame entities with GSAP:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script>
const box = document.querySelector('a-box');

// Animate position
gsap.to(box.object3D.position, {
  x: 3,
  y: 2,
  z: -5,
  duration: 2,
  ease: 'power2.inOut'
});

// Animate rotation
gsap.to(box.object3D.rotation, {
  y: Math.PI * 2,
  duration: 3,
  repeat: -1,
  ease: 'none'
});

// Animate attributes
gsap.to(box.components.material.material, {
  opacity: 0.5,
  duration: 1
});
</script>
```

### With React

Integrate A-Frame in React components:

```jsx
import React, { useEffect, useRef } from 'react';
import 'aframe';

function VRScene() {
  const sceneRef = useRef(null);

  useEffect(() => {
    const scene = sceneRef.current;

    // Create entities dynamically
    const entity = document.createElement('a-sphere');
    entity.setAttribute('position', '0 1.5 -3');
    entity.setAttribute('color', '#EF2D5E');
    scene.appendChild(entity);

    // Listen to events
    scene.addEventListener('enter-vr', () => {
      console.log('Entered VR mode');
    });
  }, []);

  return (
    <a-scene ref={sceneRef}>
      <a-box position="-1 0.5 -3" rotation="0 45 0" color="#4CC3D9" />
      <a-sphere position="0 1.25 -5" radius="1.25" color="#EF2D5E" />
      <a-cylinder position="1 0.75 -3" radius="0.5" height="1.5" color="#FFC65D" />
      <a-plane position="0 0 -4" rotation="-90 0 0" width="4" height="4" color="#7BC8A4" />
      <a-sky color="#ECECEC" />
    </a-scene>
  );
}

export default VRScene;
```

## Performance Best Practices

### 1. Use Asset Management

Preload assets to avoid blocking:

```html
<a-assets>
  <img id="texture1" src="large-texture.jpg">
  <video id="video360" src="360video.mp4" preload="auto"></video>
  <a-asset-item id="model" src="complex-model.gltf"></a-asset-item>
</a-assets>
```

### 2. Pool Entities

Reuse entities instead of creating/destroying:

```javascript
AFRAME.registerComponent('bullet-pool', {
  init: function() {
    this.pool = [];
    this.used = [];

    // Pre-create bullets
    for (let i = 0; i < 20; i++) {
      const bullet = document.createElement('a-sphere');
      bullet.setAttribute('radius', 0.1);
      bullet.setAttribute('visible', false);
      this.el.sceneEl.appendChild(bullet);
      this.pool.push(bullet);
    }
  },

  getBullet: function() {
    if (this.pool.length > 0) {
      const bullet = this.pool.pop();
      bullet.setAttribute('visible', true);
      this.used.push(bullet);
      return bullet;
    }
  },

  returnBullet: function(bullet) {
    bullet.setAttribute('visible', false);
    const index = this.used.indexOf(bullet);
    if (index > -1) {
      this.used.splice(index, 1);
      this.pool.push(bullet);
    }
  }
});
```

### 3. Optimize Geometry

Use low-poly models and LOD:

```html
<!-- Low-poly for distant objects -->
<a-sphere radius="1" segments-width="8" segments-height="6"></a-sphere>

<!-- High-poly for close objects -->
<a-sphere radius="1" segments-width="32" segments-height="32"></a-sphere>
```

### 4. Limit Draw Calls

Use instancing for repeated objects:

```javascript
AFRAME.registerComponent('instanced-trees', {
  init: function() {
    // Use Three.js InstancedMesh for repeated geometry
    const scene = this.el.sceneEl.object3D;
    const geometry = new THREE.ConeGeometry(0.5, 2, 8);
    const material = new THREE.MeshStandardMaterial({ color: 0x228B22 });
    const mesh = new THREE.InstancedMesh(geometry, material, 100);

    // Position instances
    for (let i = 0; i < 100; i++) {
      const matrix = new THREE.Matrix4();
      matrix.setPosition(
        Math.random() * 20 - 10,
        0,
        Math.random() * 20 - 10
      );
      mesh.setMatrixAt(i, matrix);
    }

    scene.add(mesh);
  }
});
```

### 5. Throttle tick() Functions

Don't update every frame if unnecessary:

```javascript
AFRAME.registerComponent('throttled-update', {
  init: function() {
    this.lastUpdate = 0;
    this.updateInterval = 100; // ms
  },

  tick: function(time, timeDelta) {
    if (time - this.lastUpdate >= this.updateInterval) {
      // Expensive operation here
      this.lastUpdate = time;
    }
  }
});
```

### 6. Use Stats Component for Monitoring

```html
<a-scene stats>
  <!-- Shows FPS and performance metrics -->
</a-scene>
```

## Common Pitfalls and Solutions

### Pitfall 1: Entities Not Appearing

**Problem**: Entity added but not visible

**Causes**:
- Entity positioned behind camera
- Scale is 0 or very small
- Material opacity is 0
- Entity outside camera frustum

**Solution**:

```javascript
// Wait for scene to load
const scene = document.querySelector('a-scene');
scene.addEventListener('loaded', () => {
  const entity = document.createElement('a-box');
  entity.setAttribute('position', '0 1.5 -3'); // In front of camera
  entity.setAttribute('color', 'red');
  scene.appendChild(entity);
});

// Debug: Check entity position
console.log(entity.getAttribute('position'));

// Debug: Check if entity is in scene
console.log(entity.parentNode); // Should be <a-scene>
```

### Pitfall 2: Events Not Firing

**Problem**: Click/mouseenter events don't trigger

**Cause**: Missing raycaster or cursor

**Solution**:

```html
<!-- Add cursor to camera -->
<a-camera>
  <a-cursor raycaster="objects: .interactive"></a-cursor>
</a-camera>

<!-- Add class to interactive objects -->
<a-box class="interactive" position="0 1 -3"></a-box>

<!-- Or use raycaster directly -->
<a-entity raycaster="objects: [geometry]" cursor></a-entity>
```

### Pitfall 3: Performance Degradation

**Problem**: Low FPS with many entities

**Causes**:
- Too many draw calls
- Complex geometries
- Unoptimized textures
- Too many tick() updates

**Solutions**:

```javascript
// 1. Use object pooling (see Performance section)
// 2. Simplify geometry
// 3. Optimize textures (reduce size, use compression)
// 4. Throttle updates

AFRAME.registerComponent('optimize-far-entities', {
  tick: function() {
    const camera = this.el.sceneEl.camera;
    const entities = document.querySelectorAll('[geometry]');

    entities.forEach(el => {
      const distance = el.object3D.position.distanceTo(camera.position);

      // Hide distant entities
      el.object3D.visible = distance < 50;
    });
  }
});
```

### Pitfall 4: Z-Fighting (Overlapping Surfaces)

**Problem**: Flickering when surfaces overlap

**Cause**: Two surfaces at same position

**Solution**:

```html
<!-- Offset surfaces slightly -->
<a-plane position="0 0.01 0" rotation="-90 0 0"></a-plane>
<a-plane position="0 0.02 0" rotation="-90 0 0"></a-plane>

<!-- Or use renderOrder -->
<a-entity
  geometry="primitive: plane"
  material="src: #texture1; transparent: true"
  class="has-render-order">
</a-entity>

<script>
document.querySelector('.has-render-order').object3D.renderOrder = 1;
</script>
```

### Pitfall 5: Mobile VR Performance

**Problem**: Low performance on mobile VR

**Solutions**:

```html
<!-- Reduce renderer max canvas size -->
<a-scene renderer="maxCanvasWidth: 1920; maxCanvasHeight: 1920">

<!-- Use low-poly models -->
<a-sphere radius="1" segments-width="8" segments-height="6"></a-sphere>

<!-- Limit lights (expensive on mobile) -->
<a-entity light="type: ambient; intensity: 0.6"></a-entity>
<a-entity light="type: directional; intensity: 0.4" position="1 2 1"></a-entity>

<!-- Disable antialiasing if needed -->
<a-scene renderer="antialias: false">
</a-scene>
```

### Pitfall 6: Asset Loading Issues

**Problem**: Assets not loading or CORS errors

**Solutions**:

```html
<!-- Use crossorigin attribute -->
<a-assets>
  <img id="texture" src="https://example.com/texture.jpg" crossorigin="anonymous">
</a-assets>

<!-- Wait for assets to load -->
<script>
const assets = document.querySelector('a-assets');
assets.addEventListener('loaded', () => {
  console.log('All assets loaded');
  // Safe to use assets now
});

assets.addEventListener('timeout', () => {
  console.error('Asset loading timeout');
});
</script>

<!-- Handle loading errors -->
<script>
const img = document.querySelector('img#texture');
img.addEventListener('error', () => {
  console.error('Failed to load texture');
  // Use fallback
  img.src = 'fallback-texture.jpg';
});
</script>
```

## Resources

- [A-Frame Documentation](https://aframe.io/docs/)
- [A-Frame GitHub](https://github.com/aframevr/aframe)
- [A-Frame School](https://aframe.io/school/)
- [A-Frame Community Components](https://github.com/c-frame)
- [WebXR Device API](https://www.w3.org/TR/webxr/)
- [Three.js Documentation](https://threejs.org/docs/) (A-Frame built on Three.js)

## Related Skills

- **threejs-webgl**: For advanced Three.js control beyond A-Frame's declarative API
- **babylonjs-engine**: Alternative 3D engine with different architecture
- **gsap-scrolltrigger**: For animating A-Frame entities with GSAP
- **react-three-fiber**: React approach to Three.js (compare with A-Frame's HTML approach)
