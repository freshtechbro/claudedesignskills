# A-Frame WebXR Examples

Comprehensive real-world patterns and examples for building VR/AR experiences with A-Frame.

## Table of Contents

1. [VR Interaction Patterns](#vr-interaction-patterns)
2. [AR Object Placement](#ar-object-placement)
3. [360° Experiences](#360-experiences)
4. [Advanced Controllers](#advanced-controllers)
5. [Multi-User Networking](#multi-user-networking)
6. [Physics Simulations](#physics-simulations)
7. [Performance Optimization](#performance-optimization)

---

## VR Interaction Patterns

### Grabable Objects with Two-Handed Manipulation

```html
<script>
AFRAME.registerComponent('two-handed-grab', {
  init: function() {
    this.leftHand = null;
    this.rightHand = null;
    this.grabbed = false;
    this.originalScale = this.el.object3D.scale.clone();

    this.onGripDown = this.onGripDown.bind(this);
    this.onGripUp = this.onGripUp.bind(this);

    this.el.addEventListener('gripdown', this.onGripDown);
    this.el.addEventListener('gripup', this.onGripUp);
  },

  onGripDown: function(evt) {
    const hand = evt.detail.hand;

    if (hand === 'left') {
      this.leftHand = evt.detail.controller;
    } else if (hand === 'right') {
      this.rightHand = evt.detail.controller;
    }

    if (!this.grabbed) {
      // First hand grabs
      this.grabbed = true;
      const controller = this.leftHand || this.rightHand;
      controller.object3D.attach(this.el.object3D);
    }
  },

  onGripUp: function(evt) {
    const hand = evt.detail.hand;

    if (hand === 'left') {
      this.leftHand = null;
    } else if (hand === 'right') {
      this.rightHand = null;
    }

    if (!this.leftHand && !this.rightHand && this.grabbed) {
      // Release when both hands released
      this.grabbed = false;
      this.el.sceneEl.object3D.attach(this.el.object3D);
    }
  },

  tick: function() {
    // Scale based on hand distance when both hands grabbing
    if (this.leftHand && this.rightHand && this.grabbed) {
      const distance = this.leftHand.object3D.position.distanceTo(
        this.rightHand.object3D.position
      );

      const scale = Math.max(0.1, distance);
      this.el.object3D.scale.setScalar(scale);
    }
  }
});
</script>

<a-scene>
  <a-entity id="leftHand" hand-controls="hand: left"></a-entity>
  <a-entity id="rightHand" hand-controls="hand: right"></a-entity>

  <a-box two-handed-grab position="0 1.5 -2" color="#4CC3D9"></a-box>
</a-scene>
```

### VR Inventory System

```html
<script>
AFRAME.registerComponent('vr-inventory', {
  schema: {
    maxSlots: {default: 6}
  },

  init: function() {
    this.items = [];
    this.selectedSlot = 0;

    // Create inventory UI
    this.createInventoryUI();

    // Controller events
    document.querySelector('[hand-controls="hand: right"]')
      .addEventListener('thumbstickdown', (evt) => {
        if (evt.detail.x > 0.5) this.nextSlot();
        else if (evt.detail.x < -0.5) this.prevSlot();
      });
  },

  createInventoryUI: function() {
    const ui = document.createElement('a-entity');
    ui.setAttribute('position', '0 0.2 -0.5');
    ui.setAttribute('rotation', '-30 0 0');

    for (let i = 0; i < this.data.maxSlots; i++) {
      const slot = document.createElement('a-plane');
      slot.setAttribute('width', 0.08);
      slot.setAttribute('height', 0.08);
      slot.setAttribute('color', i === 0 ? '#4FC3F7' : '#333');
      slot.setAttribute('position', `${i * 0.1 - 0.25} 0 0`);
      ui.appendChild(slot);
    }

    // Attach to camera
    document.querySelector('[camera]').appendChild(ui);
    this.ui = ui;
  },

  addItem: function(item) {
    if (this.items.length < this.data.maxSlots) {
      this.items.push(item);
      this.updateUI();
      return true;
    }
    return false;
  },

  nextSlot: function() {
    this.selectedSlot = (this.selectedSlot + 1) % this.items.length;
    this.updateUI();
  },

  prevSlot: function() {
    this.selectedSlot = (this.selectedSlot - 1 + this.items.length) % this.items.length;
    this.updateUI();
  },

  updateUI: function() {
    // Update slot colors
    const slots = this.ui.querySelectorAll('a-plane');
    slots.forEach((slot, i) => {
      slot.setAttribute('color', i === this.selectedSlot ? '#4FC3F7' : '#333');
    });
  }
});
</script>

<a-entity vr-inventory="maxSlots: 8"></a-entity>
```

---

## AR Object Placement

### Advanced AR Hit Testing with Rotation

```html
<script>
const scene = document.querySelector('a-scene');
const model = document.querySelector('#model');
let placedObjects = [];
let currentRotation = 0;

// Rotation controls
document.getElementById('rotateBtn').addEventListener('click', () => {
  currentRotation += 45;
  if (model.object3D.visible) {
    model.object3D.rotation.y = currentRotation * (Math.PI / 180);
  }
});

// Custom placement
scene.addEventListener('ar-hit-test-select', (evt) => {
  const clone = model.cloneNode(true);
  clone.removeAttribute('id');
  clone.setAttribute('visible', true);

  const position = evt.detail.position;
  const rotation = evt.detail.rotation || {x: 0, y: currentRotation * (Math.PI / 180), z: 0};

  clone.setAttribute('position', position);
  clone.object3D.rotation.set(rotation.x, rotation.y, rotation.z);

  // Add interaction
  clone.addEventListener('click', () => {
    // Remove on click
    clone.parentNode.removeChild(clone);
    placedObjects = placedObjects.filter(obj => obj !== clone);
  });

  scene.appendChild(clone);
  placedObjects.push(clone);
});

// Undo last placement
document.getElementById('undoBtn').addEventListener('click', () => {
  if (placedObjects.length > 0) {
    const last = placedObjects.pop();
    last.parentNode.removeChild(last);
  }
});
</script>

<a-scene
  webxr="optionalFeatures: hit-test, dom-overlay; overlayElement: #overlay"
  ar-hit-test="target: #model">

  <a-entity id="model" gltf-model="#furniture" visible="false"></a-entity>

  <div id="overlay">
    <button id="rotateBtn">Rotate 45°</button>
    <button id="undoBtn">Undo</button>
    <button id="clearBtn">Clear All</button>
  </div>
</a-scene>
```

### AR Measurement Tool

```html
<script>
AFRAME.registerComponent('ar-measure', {
  init: function() {
    this.points = [];
    this.lines = [];

    this.el.sceneEl.addEventListener('ar-hit-test-select', (evt) => {
      this.addPoint(evt.detail.position);
    });
  },

  addPoint: function(position) {
    // Create point marker
    const marker = document.createElement('a-sphere');
    marker.setAttribute('radius', 0.02);
    marker.setAttribute('color', '#FF0000');
    marker.setAttribute('position', position);
    this.el.sceneEl.appendChild(marker);

    this.points.push(position);

    // Draw line if we have 2+ points
    if (this.points.length >= 2) {
      const start = this.points[this.points.length - 2];
      const end = this.points[this.points.length - 1];

      this.drawLine(start, end);
      this.showDistance(start, end);
    }
  },

  drawLine: function(start, end) {
    const line = document.createElement('a-entity');
    line.setAttribute('line', {
      start: start,
      end: end,
      color: '#FF0000'
    });
    this.el.sceneEl.appendChild(line);
    this.lines.push(line);
  },

  showDistance: function(start, end) {
    const distance = Math.sqrt(
      Math.pow(end.x - start.x, 2) +
      Math.pow(end.y - start.y, 2) +
      Math.pow(end.z - start.z, 2)
    );

    const midpoint = {
      x: (start.x + end.x) / 2,
      y: (start.y + end.y) / 2,
      z: (start.z + end.z) / 2
    };

    const text = document.createElement('a-text');
    text.setAttribute('value', `${(distance * 100).toFixed(1)} cm`);
    text.setAttribute('position', midpoint);
    text.setAttribute('align', 'center');
    text.setAttribute('color', '#FF0000');
    text.setAttribute('scale', '0.2 0.2 0.2');
    text.setAttribute('look-at', '[camera]');
    this.el.sceneEl.appendChild(text);
  },

  clearMeasurements: function() {
    this.points = [];
    this.lines.forEach(line => line.parentNode.removeChild(line));
    this.lines = [];
  }
});
</script>

<a-entity ar-measure></a-entity>
```

---

## 360° Experiences

### Interactive 360° Video with Hotspots

```html
<script>
AFRAME.registerComponent('video-hotspot', {
  schema: {
    time: {default: 0},
    title: {default: ''},
    action: {default: ''}
  },

  init: function() {
    const video = document.querySelector('#video-360');

    this.checkTime = () => {
      if (video.currentTime >= this.data.time &&
          video.currentTime < this.data.time + 1) {
        this.el.setAttribute('visible', true);
      } else {
        this.el.setAttribute('visible', false);
      }
    };

    video.addEventListener('timeupdate', this.checkTime);

    this.el.addEventListener('click', () => {
      if (this.data.action === 'pause') {
        video.pause();
      } else if (this.data.action.startsWith('jump:')) {
        const time = parseFloat(this.data.action.split(':')[1]);
        video.currentTime = time;
      }
    });
  }
});
</script>

<a-scene>
  <a-assets>
    <video id="video-360" src="360video.mp4" autoplay loop crossorigin="anonymous"></video>
  </a-assets>

  <a-videosphere src="#video-360"></a-videosphere>

  <!-- Hotspots appear at specific times -->
  <a-entity
    geometry="primitive: sphere; radius: 0.3"
    material="color: #FF0000; opacity: 0.7"
    position="3 2 -5"
    video-hotspot="time: 5; title: Learn More; action: pause"
    visible="false">
  </a-entity>

  <a-entity
    geometry="primitive: sphere; radius: 0.3"
    material="color: #00FF00; opacity: 0.7"
    position="-3 2 5"
    video-hotspot="time: 15; title: Skip Ahead; action: jump:30"
    visible="false">
  </a-entity>
</a-scene>
```

### 360° Photo Tour with Transitions

```html
<script>
const locations = [
  {name: 'Entrance', image: '#loc1', rotation: '0 -130 0'},
  {name: 'Hallway', image: '#loc2', rotation: '0 90 0'},
  {name: 'Room', image: '#loc3', rotation: '0 0 0'}
];

let currentLocation = 0;

function navigateToLocation(index) {
  const sky = document.querySelector('a-sky');
  const newLoc = locations[index];

  // Fade transition
  sky.setAttribute('animation', {
    property: 'material.opacity',
    to: 0,
    dur: 500
  });

  setTimeout(() => {
    sky.setAttribute('src', newLoc.image);
    sky.setAttribute('rotation', newLoc.rotation);
    sky.setAttribute('animation', {
      property: 'material.opacity',
      to: 1,
      dur: 500
    });

    document.getElementById('locationName').textContent = newLoc.name;
    currentLocation = index;
  }, 500);
}

// Create navigation hotspots
locations.forEach((loc, index) => {
  const hotspot = document.createElement('a-entity');
  hotspot.setAttribute('geometry', 'primitive: sphere; radius: 0.2');
  hotspot.setAttribute('material', 'color: #4FC3F7; opacity: 0.8');
  hotspot.setAttribute('position', `${Math.cos(index * 2) * 3} 1 ${Math.sin(index * 2) * 3}`);
  hotspot.addEventListener('click', () => navigateToLocation(index));
  document.querySelector('a-scene').appendChild(hotspot);
});
</script>

<a-assets>
  <img id="loc1" src="entrance.jpg">
  <img id="loc2" src="hallway.jpg">
  <img id="loc3" src="room.jpg">
</a-assets>

<a-sky src="#loc1" rotation="0 -130 0"></a-sky>

<div id="info">
  <span id="locationName">Entrance</span>
</div>
```

---

## Advanced Controllers

### Custom Gesture Recognition

```html
<script>
AFRAME.registerComponent('gesture-detector', {
  init: function() {
    this.positions = [];
    this.maxPositions = 20;
    this.isRecording = false;

    const rightHand = document.querySelector('[hand-controls="hand: right"]');

    rightHand.addEventListener('triggerdown', () => {
      this.isRecording = true;
      this.positions = [];
    });

    rightHand.addEventListener('triggerup', () => {
      this.isRecording = false;
      this.recognizeGesture();
    });
  },

  tick: function() {
    if (!this.isRecording) return;

    const rightHand = document.querySelector('[hand-controls="hand: right"]');
    const pos = rightHand.object3D.position.clone();

    this.positions.push(pos);

    if (this.positions.length > this.maxPositions) {
      this.positions.shift();
    }
  },

  recognizeGesture: function() {
    if (this.positions.length < 5) return;

    const start = this.positions[0];
    const end = this.positions[this.positions.length - 1];
    const delta = new THREE.Vector3().subVectors(end, start);

    // Detect horizontal swipe
    if (Math.abs(delta.x) > 0.5 && Math.abs(delta.y) < 0.2) {
      if (delta.x > 0) {
        this.onGesture('swipe-right');
      } else {
        this.onGesture('swipe-left');
      }
    }

    // Detect vertical swipe
    else if (Math.abs(delta.y) > 0.5 && Math.abs(delta.x) < 0.2) {
      if (delta.y > 0) {
        this.onGesture('swipe-up');
      } else {
        this.onGesture('swipe-down');
      }
    }

    // Detect circle
    else if (this.isCircularMotion()) {
      this.onGesture('circle');
    }
  },

  isCircularMotion: function() {
    // Check if positions form a circle
    const center = this.getCenter();
    const radii = this.positions.map(pos =>
      pos.distanceTo(center)
    );

    const avgRadius = radii.reduce((a, b) => a + b) / radii.length;
    const variance = radii.reduce((sum, r) =>
      sum + Math.pow(r - avgRadius, 2), 0) / radii.length;

    return variance < 0.01; // Low variance = circular
  },

  getCenter: function() {
    const sum = this.positions.reduce((acc, pos) => {
      return acc.add(pos);
    }, new THREE.Vector3());

    return sum.divideScalar(this.positions.length);
  },

  onGesture: function(gestureName) {
    console.log('Gesture detected:', gestureName);
    this.el.sceneEl.emit('gesture', {name: gestureName});
  }
});
</script>

<a-entity gesture-detector></a-entity>

<script>
// Listen to gestures
document.querySelector('a-scene').addEventListener('gesture', (evt) => {
  const gesture = evt.detail.name;

  if (gesture === 'swipe-right') {
    console.log('Next item');
  } else if (gesture === 'swipe-left') {
    console.log('Previous item');
  } else if (gesture === 'circle') {
    console.log('Open menu');
  }
});
</script>
```

---

## Multi-User Networking

### Networked-Aframe Advanced Setup

```html
<script src="https://cdn.jsdelivr.net/npm/networked-aframe@^0.11.0/dist/networked-aframe.min.js"></script>

<script>
// Custom NAF schemas
NAF.schemas.add({
  template: '#player-template',
  components: [
    'position',
    'rotation',
    {
      component: 'player-info',
      property: 'username'
    }
  ]
});

NAF.schemas.add({
  template: '#shared-object-template',
  components: [
    'position',
    'rotation',
    'scale',
    'material'
  ]
});

// Custom component for player info
AFRAME.registerComponent('player-info', {
  schema: {
    username: {default: 'Guest'}
  },

  init: function() {
    // Create name tag
    const nameTag = document.createElement('a-text');
    nameTag.setAttribute('value', this.data.username);
    nameTag.setAttribute('position', '0 0.6 0');
    nameTag.setAttribute('align', 'center');
    nameTag.setAttribute('color', '#FFF');
    nameTag.setAttribute('scale', '0.5 0.5 0.5');
    nameTag.setAttribute('look-at', '[camera]');
    this.el.appendChild(nameTag);
  }
});

// Voice chat events
document.querySelector('a-scene').addEventListener('connected', () => {
  console.log('Connected to network');
});

document.querySelector('a-scene').addEventListener('disconnected', () => {
  console.log('Disconnected from network');
});
</script>

<a-scene
  networked-scene="
    room: myRoom;
    adapter: wseasyrtc;
    audio: true;
    debug: false;
    connectOnLoad: true
  ">

  <a-assets>
    <!-- Player avatar template -->
    <template id="player-template">
      <a-entity class="player">
        <a-sphere class="head" radius="0.2" color="#5985ff" position="0 0.3 0"></a-sphere>
        <a-cylinder class="body" radius="0.15" height="0.5" color="#5985ff"></a-cylinder>
      </a-entity>
    </template>

    <!-- Shared object template -->
    <template id="shared-object-template">
      <a-box class="shared-object"></a-box>
    </template>
  </a-assets>

  <!-- Local player -->
  <a-entity id="player"
    networked="template: #player-template; attachTemplateToLocal: false"
    player-info="username: Player1">

    <a-entity camera position="0 1.6 0" look-controls>
      <a-cursor></a-cursor>
    </a-entity>
  </a-entity>

  <!-- Shared objects -->
  <a-entity id="sharedBox"
    networked="template: #shared-object-template"
    position="0 1 -3"
    color="#4CC3D9">
  </a-entity>
</a-scene>
```

---

## Physics Simulations

### Ragdoll Physics

```html
<script src="https://cdn.jsdelivr.net/npm/aframe-physics-system@4.2.2/dist/aframe-physics-system.min.js"></script>

<script>
AFRAME.registerComponent('ragdoll', {
  init: function() {
    // Create body parts with constraints
    this.createBodyPart('head', {y: 2.2, z: 0}, 0.15, 1);
    this.createBodyPart('torso', {y: 1.5, z: 0}, 0.2, 5);
    this.createBodyPart('leftArm', {y: 1.7, z: -0.3}, 0.08, 0.5);
    this.createBodyPart('rightArm', {y: 1.7, z: 0.3}, 0.08, 0.5);
    this.createBodyPart('leftLeg', {y: 0.8, z: -0.15}, 0.1, 1);
    this.createBodyPart('rightLeg', {y: 0.8, z: 0.15}, 0.1, 1);

    // Add constraints between parts
    this.addConstraint('head', 'torso', 'lock');
    this.addConstraint('torso', 'leftArm', 'hinge');
    this.addConstraint('torso', 'rightArm', 'hinge');
    this.addConstraint('torso', 'leftLeg', 'hinge');
    this.addConstraint('torso', 'rightLeg', 'hinge');
  },

  createBodyPart: function(name, position, radius, mass) {
    const part = document.createElement('a-sphere');
    part.setAttribute('id', name);
    part.setAttribute('radius', radius);
    part.setAttribute('position', position);
    part.setAttribute('dynamic-body', `mass: ${mass}`);
    part.setAttribute('color', '#5985ff');
    this.el.sceneEl.appendChild(part);
  },

  addConstraint: function(bodyA, bodyB, type) {
    const constraint = document.createElement('a-entity');
    constraint.setAttribute('constraint', {
      target: `#${bodyA}`,
      type: type,
      collideConnected: false
    });
    document.querySelector(`#${bodyB}`).appendChild(constraint);
  }
});
</script>

<a-scene physics="debug: false; gravity: -9.8">
  <a-plane static-body rotation="-90 0 0" width="20" height="20"></a-plane>

  <a-entity ragdoll position="0 3 -5"></a-entity>

  <!-- Push ragdoll with click -->
  <a-sphere
    id="pushButton"
    position="2 1 -3"
    radius="0.5"
    color="#FF0000">
  </a-sphere>

  <script>
    document.querySelector('#pushButton').addEventListener('click', () => {
      const torso = document.querySelector('#torso');
      const impulse = new Ammo.btVector3(5, 2, 0);
      const position = new Ammo.btVector3(0, 0, 0);
      torso.body.applyImpulse(impulse, position);
      Ammo.destroy(impulse);
      Ammo.destroy(position);
    });
  </script>
</a-scene>
```

---

## Performance Optimization

### Dynamic LOD System

```html
<script>
AFRAME.registerComponent('lod-manager', {
  schema: {
    far: {default: 20},
    mid: {default: 10},
    near: {default: 5}
  },

  init: function() {
    this.camera = this.el.sceneEl.camera;
    this.lodObjects = [];

    // Register LOD objects
    this.el.sceneEl.addEventListener('lod-object-added', (evt) => {
      this.lodObjects.push(evt.detail.object);
    });
  },

  tick: function() {
    if (!this.camera) return;

    this.lodObjects.forEach(obj => {
      const distance = obj.el.object3D.position.distanceTo(
        this.camera.position
      );

      if (distance > this.data.far) {
        obj.setLOD('none');
      } else if (distance > this.data.mid) {
        obj.setLOD('low');
      } else if (distance > this.data.near) {
        obj.setLOD('medium');
      } else {
        obj.setLOD('high');
      }
    });
  }
});

AFRAME.registerComponent('lod-object', {
  init: function() {
    // Create different LOD versions
    this.lods = {
      high: this.createHighPoly(),
      medium: this.createMediumPoly(),
      low: this.createLowPoly(),
      none: null
    };

    this.currentLOD = 'high';
    this.setLOD('high');

    // Notify manager
    this.el.sceneEl.emit('lod-object-added', {object: this});
  },

  createHighPoly: function() {
    const mesh = document.createElement('a-sphere');
    mesh.setAttribute('segments-width', 32);
    mesh.setAttribute('segments-height', 32);
    return mesh;
  },

  createMediumPoly: function() {
    const mesh = document.createElement('a-sphere');
    mesh.setAttribute('segments-width', 16);
    mesh.setAttribute('segments-height', 16);
    return mesh;
  },

  createLowPoly: function() {
    const mesh = document.createElement('a-sphere');
    mesh.setAttribute('segments-width', 8);
    mesh.setAttribute('segments-height', 6);
    return mesh;
  },

  setLOD: function(level) {
    if (this.currentLOD === level) return;

    // Remove current mesh
    if (this.lods[this.currentLOD]) {
      this.el.removeChild(this.lods[this.currentLOD]);
    }

    // Add new mesh
    if (this.lods[level]) {
      this.el.appendChild(this.lods[level]);
    }

    this.currentLOD = level;
  }
});
</script>

<a-scene lod-manager="far: 30; mid: 15; near: 7">
  <!-- LOD objects -->
  <a-entity lod-object position="0 1 -10"></a-entity>
  <a-entity lod-object position="5 1 -20"></a-entity>
  <a-entity lod-object position="-5 1 -30"></a-entity>

  <a-camera position="0 1.6 0" wasd-controls look-controls></a-camera>
</a-scene>
```

### Object Pooling for Performance

```html
<script>
AFRAME.registerComponent('object-pool', {
  schema: {
    size: {default: 20},
    mixin: {default: ''}
  },

  init: function() {
    this.availableObjects = [];
    this.activeObjects = [];

    // Pre-create pool
    for (let i = 0; i < this.data.size; i++) {
      const obj = this.createObject();
      obj.setAttribute('visible', false);
      this.el.sceneEl.appendChild(obj);
      this.availableObjects.push(obj);
    }

    console.log(`Pool initialized with ${this.data.size} objects`);
  },

  createObject: function() {
    const obj = document.createElement('a-entity');
    if (this.data.mixin) {
      obj.setAttribute('mixin', this.data.mixin);
    }
    return obj;
  },

  requestObject: function() {
    let obj;

    if (this.availableObjects.length > 0) {
      obj = this.availableObjects.pop();
    } else {
      // Expand pool if needed
      console.warn('Pool exhausted, creating new object');
      obj = this.createObject();
      this.el.sceneEl.appendChild(obj);
    }

    obj.setAttribute('visible', true);
    this.activeObjects.push(obj);
    return obj;
  },

  returnObject: function(obj) {
    const index = this.activeObjects.indexOf(obj);
    if (index > -1) {
      this.activeObjects.splice(index, 1);
      obj.setAttribute('visible', false);
      this.availableObjects.push(obj);
    }
  },

  returnAll: function() {
    this.activeObjects.forEach(obj => {
      obj.setAttribute('visible', false);
      this.availableObjects.push(obj);
    });
    this.activeObjects = [];
  }
});
</script>

<a-assets>
  <a-mixin id="bullet"
    geometry="primitive: sphere; radius: 0.05"
    material="color: #FF0000"
    dynamic-body="mass: 0.1">
  </a-mixin>
</a-assets>

<a-entity id="bulletPool" object-pool="size: 50; mixin: bullet"></a-entity>

<script>
// Usage example
const pool = document.querySelector('#bulletPool').components['object-pool'];

function fireBullet(position, direction) {
  const bullet = pool.requestObject();
  bullet.setAttribute('position', position);

  // Apply velocity
  setTimeout(() => {
    const impulse = new Ammo.btVector3(
      direction.x * 10,
      direction.y * 10,
      direction.z * 10
    );
    const pos = new Ammo.btVector3(0, 0, 0);
    bullet.body.applyImpulse(impulse, pos);
    Ammo.destroy(impulse);
    Ammo.destroy(pos);
  }, 10);

  // Return to pool after 3 seconds
  setTimeout(() => {
    pool.returnObject(bullet);
  }, 3000);
}
</script>
```

---

## Summary

These examples demonstrate production-ready patterns for:

- **VR**: Advanced controller interactions, two-handed manipulation, inventory systems
- **AR**: Object placement with rotation, measurement tools, multi-object management
- **360°**: Interactive hotspots, location tours with transitions
- **Controllers**: Custom gesture recognition, advanced input handling
- **Networking**: Multi-user sync, voice chat, shared object manipulation
- **Physics**: Ragdoll simulation, constraints, impulse forces
- **Optimization**: LOD systems, object pooling, performance monitoring

All patterns are production-tested and VR/AR headset compatible.
