# PlayCanvas Examples

Comprehensive collection of PlayCanvas examples, patterns, and use cases.

---

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [3D Graphics](#3d-graphics)
3. [Physics & Interaction](#physics--interaction)
4. [Animation](#animation)
5. [User Interface](#user-interface)
6. [Audio](#audio)
7. [Performance](#performance)
8. [Integration Patterns](#integration-patterns)

---

## Basic Examples

### 1. Hello Cube

Minimal PlayCanvas scene with rotating cube:

```javascript
const canvas = document.getElementById('canvas');
const app = new pc.Application(canvas);

app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
app.setCanvasResolution(pc.RESOLUTION_AUTO);

// Camera
const camera = new pc.Entity('camera');
camera.addComponent('camera', {
    clearColor: new pc.Color(0.2, 0.3, 0.4)
});
camera.setPosition(0, 0, 5);
app.root.addChild(camera);

// Light
const light = new pc.Entity('light');
light.addComponent('light');
light.setEulerAngles(45, 45, 0);
app.root.addChild(light);

// Cube
const cube = new pc.Entity('cube');
cube.addComponent('model', { type: 'box' });
app.root.addChild(cube);

// Rotate cube
app.on('update', (dt) => {
    cube.rotate(10 * dt, 20 * dt, 30 * dt);
});

app.start();
```

---

### 2. Multiple Objects

Creating multiple objects in a scene:

```javascript
const shapes = ['box', 'sphere', 'cylinder', 'cone', 'capsule'];
const colors = [
    new pc.Color(1, 0, 0),  // Red
    new pc.Color(0, 1, 0),  // Green
    new pc.Color(0, 0, 1),  // Blue
    new pc.Color(1, 1, 0),  // Yellow
    new pc.Color(1, 0, 1)   // Magenta
];

shapes.forEach((shape, i) => {
    const entity = new pc.Entity(shape);
    entity.addComponent('model', { type: shape });

    // Position in grid
    entity.setPosition((i - 2) * 2, 0, 0);

    // Create material
    const material = new pc.StandardMaterial();
    material.diffuse = colors[i];
    material.update();
    entity.model.material = material;

    app.root.addChild(entity);
});
```

---

### 3. Loading 3D Models

Load GLTF/GLB models:

```javascript
// Create asset for model
const asset = new pc.Asset('model', 'container', {
    url: 'path/to/model.glb'
});

app.assets.add(asset);

// Load asset
app.assets.load(asset);

asset.ready((asset) => {
    const entity = asset.resource.instantiateRenderEntity();
    entity.setPosition(0, 0, 0);
    app.root.addChild(entity);
});

asset.on('error', (err) => {
    console.error('Failed to load model:', err);
});
```

---

## 3D Graphics

### 1. Materials & Textures

PBR material with textures:

```javascript
// Create material
const material = new pc.StandardMaterial();

// Diffuse (albedo) texture
const diffuseAsset = new pc.Asset('diffuse', 'texture', {
    url: 'textures/albedo.jpg'
});
app.assets.add(diffuseAsset);
app.assets.load(diffuseAsset);

diffuseAsset.ready(() => {
    material.diffuseMap = diffuseAsset.resource;
    material.update();
});

// Normal map
const normalAsset = new pc.Asset('normal', 'texture', {
    url: 'textures/normal.jpg'
});
app.assets.add(normalAsset);
app.assets.load(normalAsset);

normalAsset.ready(() => {
    material.normalMap = normalAsset.resource;
    material.update();
});

// Metalness
material.metalness = 0.7;
material.gloss = 0.8;

// Apply to entity
entity.model.material = material;
```

---

### 2. Dynamic Lighting

Multiple light types:

```javascript
// Directional Light (Sun)
const sun = new pc.Entity('sun');
sun.addComponent('light', {
    type: 'directional',
    color: new pc.Color(1, 1, 0.9),
    intensity: 1.5,
    castShadows: true,
    shadowBias: 0.2,
    shadowDistance: 40
});
sun.setEulerAngles(45, 30, 0);
app.root.addChild(sun);

// Point Light
const pointLight = new pc.Entity('pointLight');
pointLight.addComponent('light', {
    type: 'point',
    color: new pc.Color(1, 0, 0),
    intensity: 1,
    range: 10,
    castShadows: false
});
pointLight.setPosition(0, 2, 0);
app.root.addChild(pointLight);

// Spot Light
const spotLight = new pc.Entity('spotLight');
spotLight.addComponent('light', {
    type: 'spot',
    color: new pc.Color(0, 1, 0),
    intensity: 1,
    range: 15,
    innerConeAngle: 20,
    outerConeAngle: 30,
    castShadows: true
});
spotLight.setPosition(5, 5, 0);
spotLight.lookAt(0, 0, 0);
app.root.addChild(spotLight);
```

---

### 3. Camera Effects

Post-processing and camera effects:

```javascript
// Depth of Field
camera.camera.enablePostEffects = true;

// Create depth of field effect (requires custom script)
const dofScript = camera.script.create('depthOfField', {
    attributes: {
        focusDistance: 10,
        aperture: 0.5,
        maxBlur: 1.0
    }
});

// Camera shake effect
function cameraShake(intensity, duration) {
    const startTime = Date.now();
    const originalPos = camera.getPosition().clone();

    const shakeInterval = setInterval(() => {
        const elapsed = (Date.now() - startTime) / 1000;

        if (elapsed >= duration) {
            camera.setPosition(originalPos);
            clearInterval(shakeInterval);
            return;
        }

        const shakeAmount = intensity * (1 - elapsed / duration);
        const x = originalPos.x + (Math.random() - 0.5) * shakeAmount;
        const y = originalPos.y + (Math.random() - 0.5) * shakeAmount;
        const z = originalPos.z + (Math.random() - 0.5) * shakeAmount;

        camera.setPosition(x, y, z);
    }, 16);
}

// Usage
cameraShake(0.5, 0.5);  // intensity, duration
```

---

## Physics & Interaction

### 1. Basic Physics

Rigidbody and collision setup:

```javascript
// Dynamic rigidbody (falls with gravity)
const dynamicBox = new pc.Entity('dynamicBox');
dynamicBox.addComponent('model', { type: 'box' });
dynamicBox.addComponent('rigidbody', {
    type: 'dynamic',
    mass: 1,
    friction: 0.5,
    restitution: 0.5  // Bounciness
});
dynamicBox.addComponent('collision', {
    type: 'box',
    halfExtents: new pc.Vec3(0.5, 0.5, 0.5)
});
dynamicBox.setPosition(0, 5, 0);
app.root.addChild(dynamicBox);

// Static ground
const ground = new pc.Entity('ground');
ground.addComponent('model', { type: 'plane' });
ground.addComponent('rigidbody', {
    type: 'static'
});
ground.addComponent('collision', {
    type: 'box',
    halfExtents: new pc.Vec3(10, 0.1, 10)
});
ground.setLocalScale(20, 1, 20);
app.root.addChild(ground);
```

---

### 2. Raycasting & Object Picking

Pick objects with mouse:

```javascript
function pickObject(screenX, screenY) {
    const camera = app.root.findByName('Camera');

    // Convert screen to world coordinates
    const worldPos = camera.camera.screenToWorld(
        screenX,
        screenY,
        camera.camera.farClip
    );

    const from = camera.getPosition();
    const to = worldPos;

    // Raycast
    const result = app.systems.rigidbody.raycastFirst(from, to);

    if (result) {
        console.log('Hit:', result.entity.name);
        return result.entity;
    }

    return null;
}

// Mouse click handler
app.mouse.on(pc.EVENT_MOUSEDOWN, (event) => {
    const picked = pickObject(event.x, event.y);
    if (picked) {
        // Do something with picked entity
        picked.rigidbody.applyImpulse(0, 5, 0);
    }
});
```

---

### 3. Character Controller

WASD character movement:

```javascript
var CharacterController = pc.createScript('characterController');

CharacterController.attributes.add('speed', {
    type: 'number',
    default: 5.0
});

CharacterController.prototype.initialize = function() {
    this.moveDirection = new pc.Vec3();
};

CharacterController.prototype.update = function(dt) {
    const keyboard = this.app.keyboard;

    // Get camera direction
    const camera = this.app.root.findByName('Camera');
    const forward = camera.forward.clone();
    const right = camera.right.clone();

    // Flatten to horizontal
    forward.y = 0;
    forward.normalize();
    right.y = 0;
    right.normalize();

    // Calculate movement
    this.moveDirection.set(0, 0, 0);

    if (keyboard.isPressed(pc.KEY_W)) {
        this.moveDirection.add(forward);
    }
    if (keyboard.isPressed(pc.KEY_S)) {
        this.moveDirection.sub(forward);
    }
    if (keyboard.isPressed(pc.KEY_A)) {
        this.moveDirection.sub(right);
    }
    if (keyboard.isPressed(pc.KEY_D)) {
        this.moveDirection.add(right);
    }

    // Apply movement
    if (this.moveDirection.length() > 0) {
        this.moveDirection.normalize();
        this.moveDirection.scale(this.speed * dt);

        const pos = this.entity.getPosition();
        pos.add(this.moveDirection);
        this.entity.setPosition(pos);

        // Rotate to face movement direction
        const angle = Math.atan2(this.moveDirection.x, this.moveDirection.z) * pc.math.RAD_TO_DEG;
        this.entity.setEulerAngles(0, angle, 0);
    }
};
```

---

## Animation

### 1. Property Animation (Tween)

Animate entity properties:

```javascript
// Tween helper
function tween(entity, property, from, to, duration, easing = 'linear') {
    const startTime = Date.now();

    const easingFuncs = {
        linear: t => t,
        easeIn: t => t * t,
        easeOut: t => t * (2 - t),
        easeInOut: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
    };

    const easingFunc = easingFuncs[easing] || easingFuncs.linear;

    const animate = () => {
        const elapsed = (Date.now() - startTime) / 1000;
        const t = Math.min(elapsed / duration, 1);
        const eased = easingFunc(t);

        const value = from + (to - from) * eased;

        if (property === 'x' || property === 'y' || property === 'z') {
            const pos = entity.getPosition();
            pos[property] = value;
            entity.setPosition(pos);
        }

        if (t < 1) {
            requestAnimationFrame(animate);
        }
    };

    animate();
}

// Usage
tween(entity, 'y', 0, 5, 2, 'easeInOut');  // Move up over 2 seconds
```

---

### 2. Skeletal Animation

Animate 3D character models:

```javascript
// Load model with animations
const modelAsset = new pc.Asset('character', 'container', {
    url: 'models/character.glb'
});

app.assets.add(modelAsset);
app.assets.load(modelAsset);

modelAsset.ready((asset) => {
    const entity = asset.resource.instantiateRenderEntity();

    // Add animation component
    entity.addComponent('anim', {
        activate: true
    });

    // Get animation clips
    const animations = asset.resource.animations;

    // Create animation state graph
    const animStateGraph = {
        layers: [
            {
                name: 'locomotion',
                states: [
                    { name: 'idle', speed: 1.0 },
                    { name: 'walk', speed: 1.0 },
                    { name: 'run', speed: 1.0 }
                ],
                transitions: [
                    { from: 'idle', to: 'walk', duration: 0.2 },
                    { from: 'walk', to: 'run', duration: 0.2 },
                    { from: 'run', to: 'idle', duration: 0.3 }
                ]
            }
        ]
    };

    // Load animation clips
    animations.forEach(anim => {
        entity.anim.assignAnimation(anim.name, anim.resource);
    });

    // Play animation
    entity.anim.setBoolean('walk', true);

    app.root.addChild(entity);
});
```

---

### 3. Particle Systems

Create particle effects:

```javascript
// Particle system entity
const particles = new pc.Entity('particles');

// Add particle system component
particles.addComponent('particlesystem', {
    numParticles: 100,
    lifetime: 2,
    rate: 0.05,
    emitterShape: pc.EMITTERSHAPE_SPHERE,
    emitterRadius: 0.5,

    // Velocity
    velocityGraph: new pc.CurveSet([
        [0, 0.1],
        [1, 0.5]
    ]),

    // Size
    scaleGraph: new pc.CurveSet([
        [0, 0.1],
        [0.5, 0.5],
        [1, 0.1]
    ]),

    // Color
    colorGraph: new pc.CurveSet([
        [0, 1, 1, 0, 0],  // Red at start
        [0.5, 1, 0.5, 0, 0],  // Orange
        [1, 0.2, 0, 0, 0]  // Dark at end
    ]),

    // Alpha
    alphaGraph: new pc.CurveSet([
        [0, 0],
        [0.2, 1],
        [0.8, 1],
        [1, 0]
    ]),

    blendType: pc.BLEND_ADDITIVE,
    depthWrite: false,
    lighting: false
});

particles.setPosition(0, 2, 0);
app.root.addChild(particles);
```

---

## User Interface

### 1. 2D UI Elements

Create screen-space UI:

```javascript
// Create screen entity (UI root)
const screen = new pc.Entity('screen');
screen.addComponent('screen', {
    referenceResolution: new pc.Vec2(1280, 720),
    scaleBlend: 0.5,
    scaleMode: pc.SCALEMODE_BLEND,
    screenSpace: true
});
app.root.addChild(screen);

// Create button
const button = new pc.Entity('button');
button.addComponent('element', {
    anchor: new pc.Vec4(0.5, 0.5, 0.5, 0.5),
    pivot: new pc.Vec2(0.5, 0.5),
    width: 200,
    height: 50,
    type: pc.ELEMENTTYPE_IMAGE,
    color: new pc.Color(0.2, 0.6, 1),
    useInput: true
});

// Button text
const buttonText = new pc.Entity('buttonText');
buttonText.addComponent('element', {
    anchor: new pc.Vec4(0.5, 0.5, 0.5, 0.5),
    pivot: new pc.Vec2(0.5, 0.5),
    fontSize: 24,
    text: 'Click Me',
    type: pc.ELEMENTTYPE_TEXT,
    color: new pc.Color(1, 1, 1)
});

button.addChild(buttonText);
screen.addChild(button);

// Button click handler
button.element.on('click', () => {
    console.log('Button clicked!');
});
```

---

### 2. Health Bar

Dynamic UI health bar:

```javascript
// Health bar background
const healthBg = new pc.Entity('healthBg');
healthBg.addComponent('element', {
    anchor: new pc.Vec4(0, 1, 0, 1),
    pivot: new pc.Vec2(0, 1),
    margin: new pc.Vec4(20, 20, 0, 0),
    width: 200,
    height: 20,
    type: pc.ELEMENTTYPE_IMAGE,
    color: new pc.Color(0.2, 0.2, 0.2)
});

// Health bar fill
const healthFill = new pc.Entity('healthFill');
healthFill.addComponent('element', {
    anchor: new pc.Vec4(0, 0, 0, 1),
    pivot: new pc.Vec2(0, 0.5),
    width: 200,
    height: 16,
    type: pc.ELEMENTTYPE_IMAGE,
    color: new pc.Color(0, 1, 0)
});

healthBg.addChild(healthFill);
screen.addChild(healthBg);

// Update health
function setHealth(percent) {
    healthFill.element.width = 200 * (percent / 100);

    // Color based on health
    if (percent > 50) {
        healthFill.element.color = new pc.Color(0, 1, 0);  // Green
    } else if (percent > 25) {
        healthFill.element.color = new pc.Color(1, 1, 0);  // Yellow
    } else {
        healthFill.element.color = new pc.Color(1, 0, 0);  // Red
    }
}

// Usage
setHealth(75);
```

---

## Audio

### 1. Background Music

Load and play audio:

```javascript
// Create audio asset
const musicAsset = new pc.Asset('music', 'audio', {
    url: 'audio/music.mp3'
});

app.assets.add(musicAsset);
app.assets.load(musicAsset);

// Create audio entity
const music = new pc.Entity('music');
music.addComponent('sound');

musicAsset.ready(() => {
    music.sound.addSlot('music', {
        asset: musicAsset,
        autoPlay: true,
        loop: true,
        volume: 0.5
    });
});

app.root.addChild(music);

// Control playback
music.sound.play('music');
music.sound.pause('music');
music.sound.stop('music');
music.sound.slot('music').volume = 0.7;
```

---

### 2. 3D Positional Audio

Spatial audio effects:

```javascript
// 3D sound effect
const soundEntity = new pc.Entity('sound');
soundEntity.addComponent('sound', {
    positional: true,
    distanceModel: pc.DISTANCE_INVERSE,
    refDistance: 1,
    maxDistance: 20,
    rollOffFactor: 1
});

soundEntity.setPosition(5, 0, 0);

const soundAsset = new pc.Asset('effect', 'audio', {
    url: 'audio/explosion.mp3'
});

app.assets.add(soundAsset);
app.assets.load(soundAsset);

soundAsset.ready(() => {
    soundEntity.sound.addSlot('effect', {
        asset: soundAsset,
        autoPlay: false,
        loop: false,
        volume: 1.0
    });
});

app.root.addChild(soundEntity);

// Play sound at position
soundEntity.sound.play('effect');
```

---

## Performance

### 1. Object Pooling

Reuse objects instead of creating/destroying:

```javascript
class ObjectPool {
    constructor(app, template, initialSize = 10) {
        this.app = app;
        this.template = template;
        this.available = [];
        this.active = [];

        // Pre-create objects
        for (let i = 0; i < initialSize; i++) {
            this.createObject();
        }
    }

    createObject() {
        const obj = this.template.clone();
        obj.enabled = false;
        this.app.root.addChild(obj);
        this.available.push(obj);
        return obj;
    }

    spawn(position) {
        let obj = this.available.pop();

        if (!obj) {
            obj = this.createObject();
        }

        obj.enabled = true;
        obj.setPosition(position);
        this.active.push(obj);

        return obj;
    }

    despawn(obj) {
        obj.enabled = false;
        const index = this.active.indexOf(obj);
        if (index > -1) {
            this.active.splice(index, 1);
            this.available.push(obj);
        }
    }

    reset() {
        this.active.forEach(obj => {
            obj.enabled = false;
            this.available.push(obj);
        });
        this.active = [];
    }
}

// Usage
const bulletTemplate = new pc.Entity('bullet');
bulletTemplate.addComponent('model', { type: 'sphere' });
bulletTemplate.setLocalScale(0.2, 0.2, 0.2);

const bulletPool = new ObjectPool(app, bulletTemplate, 50);

// Spawn bullet
const bullet = bulletPool.spawn(new pc.Vec3(0, 1, 0));

// Despawn after 2 seconds
setTimeout(() => {
    bulletPool.despawn(bullet);
}, 2000);
```

---

### 2. LOD (Level of Detail)

Optimize rendering with LOD:

```javascript
// Create entity with multiple LOD levels
const entity = new pc.Entity('lodEntity');
entity.addComponent('model', { type: 'asset', asset: highPolyModel });

// Setup LOD levels
const meshInstances = entity.model.meshInstances;

meshInstances.forEach(meshInstance => {
    // Define LOD levels
    meshInstance.lodDistances = [10, 50, 100];

    // High detail (< 10 units)
    meshInstance.lod0 = highPolyMesh;

    // Medium detail (10-50 units)
    meshInstance.lod1 = mediumPolyMesh;

    // Low detail (50-100 units)
    meshInstance.lod2 = lowPolyMesh;

    // Very low detail (> 100 units)
    meshInstance.lod3 = veryLowPolyMesh;
});
```

---

## Integration Patterns

### 1. React Integration

Use PlayCanvas in React:

```javascript
import React, { useEffect, useRef } from 'react';
import * as pc from 'playcanvas';

function PlayCanvasComponent() {
    const canvasRef = useRef(null);
    const appRef = useRef(null);

    useEffect(() => {
        // Initialize PlayCanvas
        const app = new pc.Application(canvasRef.current);
        app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
        app.setCanvasResolution(pc.RESOLUTION_AUTO);

        // Setup scene
        setupScene(app);

        app.start();
        appRef.current = app;

        // Cleanup
        return () => {
            app.destroy();
        };
    }, []);

    return <canvas ref={canvasRef} />;
}

function setupScene(app) {
    // Add camera, lights, objects...
}

export default PlayCanvasComponent;
```

---

### 2. Three.js Migration

Migrate from Three.js concepts:

```javascript
// Three.js
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// PlayCanvas equivalent
const entity = new pc.Entity('box');
entity.addComponent('model', { type: 'box' });

const material = new pc.StandardMaterial();
material.diffuse = new pc.Color(1, 0, 0);
material.update();
entity.model.material = material;

app.root.addChild(entity);
```

---

### 3. WebXR Integration

VR/AR with WebXR:

```javascript
// Enable XR
if (app.xr.supported) {
    // VR mode
    const enterVRButton = document.getElementById('enterVR');

    enterVRButton.addEventListener('click', () => {
        camera.camera.startXr(pc.XRTYPE_VR, pc.XRSPACE_LOCAL);
    });

    // AR mode
    const enterARButton = document.getElementById('enterAR');

    enterARButton.addEventListener('click', () => {
        camera.camera.startXr(pc.XRTYPE_AR, pc.XRSPACE_LOCALFLOOR);
    });

    // XR input
    app.xr.input.on('select', (inputSource) => {
        console.log('XR input selected');
    });
}
```

---

## Resources

- **Official Examples**: https://playcanvas.github.io
- **API Docs**: https://api.playcanvas.com
- **Tutorials**: https://developer.playcanvas.com/tutorials
- **Forum**: https://forum.playcanvas.com

---

## License

Examples provided for educational purposes. PlayCanvas Engine is MIT licensed.
