# PlayCanvas Engine API Reference

Complete API documentation for the PlayCanvas WebGL/WebGPU engine.

**Version**: 1.70+
**License**: MIT
**Official Docs**: https://api.playcanvas.com/

---

## Table of Contents

1. [Application](#application)
2. [Entity](#entity)
3. [Components](#components)
4. [Assets](#assets)
5. [Graphics](#graphics)
6. [Input](#input)
7. [Physics](#physics)
8. [Audio](#audio)

---

## Application

### pc.Application

The root application managing the rendering loop, scene, and systems.

#### Constructor

```javascript
const app = new pc.Application(canvas, options);
```

**Parameters**:
- `canvas` (HTMLCanvasElement): Canvas element for rendering
- `options` (Object): Configuration options
  - `keyboard` (pc.Keyboard): Keyboard device
  - `mouse` (pc.Mouse): Mouse device
  - `touch` (pc.TouchDevice): Touch device
  - `gamepads` (pc.GamePads): Gamepad devices
  - `graphicsDeviceOptions` (Object): WebGL/WebGPU settings

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `root` | pc.Entity | Root entity of scene hierarchy |
| `scene` | pc.Scene | Scene settings |
| `assets` | pc.AssetRegistry | Asset management |
| `graphicsDevice` | pc.GraphicsDevice | Rendering device |
| `systems` | pc.ComponentSystemRegistry | Component systems |
| `keyboard` | pc.Keyboard | Keyboard input |
| `mouse` | pc.Mouse | Mouse input |
| `touch` | pc.TouchDevice | Touch input |
| `gamepads` | pc.GamePads | Gamepad input |
| `timeScale` | Number | Global time scale (default: 1) |

#### Methods

**setCanvasFillMode(mode)**
```javascript
app.setCanvasFillMode(pc.FILLMODE_FILL_WINDOW);
```

Modes:
- `pc.FILLMODE_NONE`: No auto-resize
- `pc.FILLMODE_FILL_WINDOW`: Fill entire window
- `pc.FILLMODE_KEEP_ASPECT`: Maintain aspect ratio

**setCanvasResolution(mode)**
```javascript
app.setCanvasResolution(pc.RESOLUTION_AUTO);
```

Modes:
- `pc.RESOLUTION_AUTO`: Match window device pixel ratio
- `pc.RESOLUTION_FIXED`: Use canvas width/height

**resizeCanvas()**
```javascript
app.resizeCanvas();
// Manually trigger resize
```

**start()**
```javascript
app.start();
// Start the application update loop
```

**destroy()**
```javascript
app.destroy();
// Clean up application resources
```

#### Events

```javascript
app.on('update', (dt) => {
  // Called every frame
  // dt = delta time in seconds
});

app.on('postUpdate', (dt) => {
  // Called after update
});

app.on('prerender', () => {
  // Before rendering
});

app.on('postrender', () => {
  // After rendering
});

app.on('start', () => {
  // Application started
});

app.on('destroy', () => {
  // Application destroyed
});
```

---

## Entity

### pc.Entity

Nodes in the scene hierarchy with components.

#### Constructor

```javascript
const entity = new pc.Entity(name);
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | String | Entity name |
| `enabled` | Boolean | Render and update enabled |
| `children` | Array | Child entities |
| `parent` | pc.Entity | Parent entity |
| `tags` | pc.Tags | Tag list for searching |

**Component Accessors**:
- `entity.model` - Model component
- `entity.camera` - Camera component
- `entity.light` - Light component
- `entity.script` - Script component
- `entity.rigidbody` - Rigidbody component
- `entity.collision` - Collision component
- `entity.animation` - Animation component
- `entity.sound` - Sound component

#### Transform Methods

**Position**:
```javascript
entity.setPosition(x, y, z);
entity.setPosition(new pc.Vec3(x, y, z));
entity.setLocalPosition(x, y, z);

const pos = entity.getPosition();  // World position
const localPos = entity.getLocalPosition();  // Local position

entity.translate(x, y, z);  // Move relative
entity.translateLocal(x, y, z);  // Move in local space
```

**Rotation**:
```javascript
entity.setEulerAngles(x, y, z);  // Degrees
entity.setLocalEulerAngles(x, y, z);

const angles = entity.getEulerAngles();
const localAngles = entity.getLocalEulerAngles();

entity.rotate(x, y, z);  // Rotate relative (degrees)
entity.rotateLocal(x, y, z);

// Quaternion rotation
entity.setRotation(quat);
const quat = entity.getRotation();

// Look at target
entity.lookAt(target);  // target is Vec3 or Entity
entity.lookAt(x, y, z);
```

**Scale**:
```javascript
entity.setLocalScale(x, y, z);
entity.setLocalScale(new pc.Vec3(x, y, z));

const scale = entity.getLocalScale();
```

**Forward/Right/Up Vectors**:
```javascript
const forward = entity.forward;  // pc.Vec3
const right = entity.right;
const up = entity.up;
```

#### Hierarchy Methods

**addChild(entity)**
```javascript
parent.addChild(child);
```

**removeChild(entity)**
```javascript
parent.removeChild(child);
```

**insertChild(entity, index)**
```javascript
parent.insertChild(child, 0);  // Insert at start
```

**reparent(parent)**
```javascript
entity.reparent(newParent);
```

**find()**
```javascript
// Find by name
const child = entity.find(name => name === 'PlayerModel');

// Find all
const allChildren = entity.find(() => true);
```

**findByName(name)**
```javascript
const player = app.root.findByName('Player');
```

**findByTag(tag)**
```javascript
const enemies = app.root.findByTag('enemy');
// Returns array of entities
```

#### Component Methods

**addComponent(type, data)**
```javascript
entity.addComponent('model', {
  type: 'box'
});
```

**removeComponent(type)**
```javascript
entity.removeComponent('model');
```

**hasComponent(type)**
```javascript
if (entity.hasComponent('rigidbody')) {
  // Has physics
}
```

#### Entity Methods

**clone()**
```javascript
const clone = entity.clone();
app.root.addChild(clone);
```

**destroy()**
```javascript
entity.destroy();
// Removes from parent and cleans up
```

**enable()**/**disable()**
```javascript
entity.enabled = false;  // Disable
entity.enabled = true;   // Enable
```

---

## Components

### Model Component

Renders 3D meshes.

```javascript
entity.addComponent('model', {
  type: 'box',               // Primitive type
  asset: assetId,            // Model asset
  castShadows: true,
  receiveShadows: true,
  castShadowsLightmap: false,
  lightmapped: false,
  isStatic: false,
  layers: [pc.LAYERID_WORLD]
});
```

**Primitive Types**:
- `'box'`, `'capsule'`, `'cone'`, `'cylinder'`, `'plane'`, `'sphere'`

**Properties**:
```javascript
entity.model.meshInstances;  // Array of MeshInstance
entity.model.material = material;
entity.model.asset = assetId;
```

---

### Camera Component

Renders the scene from a viewpoint.

```javascript
entity.addComponent('camera', {
  clearColor: new pc.Color(0, 0, 0, 1),
  fov: 45,
  aspectRatio: 16/9,  // Auto-calculated if null
  nearClip: 0.1,
  farClip: 1000,
  projection: pc.PROJECTION_PERSPECTIVE,
  priority: 0,
  frustumCulling: true,
  rect: new pc.Vec4(0, 0, 1, 1),  // Viewport
  layers: [pc.LAYERID_WORLD, pc.LAYERID_UI]
});
```

**Projection Types**:
- `pc.PROJECTION_PERSPECTIVE`
- `pc.PROJECTION_ORTHOGRAPHIC`

**Methods**:
```javascript
// Screen to world conversion
const worldPos = camera.camera.screenToWorld(screenX, screenY, depth);

// World to screen
const screenPos = camera.camera.worldToScreen(worldPos);

// Ray from screen point
const ray = camera.camera.screenToWorld(screenX, screenY, camera.camera.nearClip);
```

---

### Light Component

Illuminates the scene.

```javascript
entity.addComponent('light', {
  type: pc.LIGHTTYPE_DIRECTIONAL,
  color: new pc.Color(1, 1, 1),
  intensity: 1,
  castShadows: true,
  shadowDistance: 40,
  shadowResolution: 2048,
  shadowBias: 0.05,
  normalOffsetBias: 0.05,
  range: 10,              // Point/Spot only
  innerConeAngle: 40,     // Spot only
  outerConeAngle: 45,     // Spot only
  falloffMode: pc.LIGHTFALLOFF_INVERSESQUARED,
  layers: [pc.LAYERID_WORLD]
});
```

**Light Types**:
- `pc.LIGHTTYPE_DIRECTIONAL`: Sun-like, parallel rays
- `pc.LIGHTTYPE_POINT`: Omnidirectional, like a bulb
- `pc.LIGHTTYPE_SPOT`: Cone-shaped, like a flashlight

**Shadow Types**:
```javascript
entity.light.shadowType = pc.SHADOW_PCF3;
```
- `pc.SHADOW_PCF3`: 3x3 PCF (good quality)
- `pc.SHADOW_PCF5`: 5x5 PCF (better quality, slower)
- `pc.SHADOW_VSM8`: Variance shadow maps (softer)

---

### Rigidbody Component

Adds physics simulation.

```javascript
entity.addComponent('rigidbody', {
  type: pc.BODYTYPE_DYNAMIC,
  mass: 1,
  linearDamping: 0,
  angularDamping: 0,
  linearFactor: new pc.Vec3(1, 1, 1),
  angularFactor: new pc.Vec3(1, 1, 1),
  friction: 0.5,
  restitution: 0,
  group: pc.BODYGROUP_DYNAMIC,
  mask: pc.BODYMASK_ALL
});
```

**Body Types**:
- `pc.BODYTYPE_STATIC`: Immovable (terrain, buildings)
- `pc.BODYTYPE_DYNAMIC`: Affected by forces
- `pc.BODYTYPE_KINEMATIC`: Moved by script, not physics

**Methods**:
```javascript
// Apply force
entity.rigidbody.applyForce(x, y, z);
entity.rigidbody.applyForce(new pc.Vec3(x, y, z));

// Apply force at point
entity.rigidbody.applyForce(force, point);

// Apply impulse (instant velocity change)
entity.rigidbody.applyImpulse(x, y, z);
entity.rigidbody.applyImpulse(impulse, point);

// Apply torque
entity.rigidbody.applyTorque(x, y, z);

// Apply torque impulse
entity.rigidbody.applyTorqueImpulse(x, y, z);

// Velocity
entity.rigidbody.linearVelocity = new pc.Vec3(x, y, z);
entity.rigidbody.angularVelocity = new pc.Vec3(x, y, z);

// Teleport
entity.rigidbody.teleport(x, y, z);
entity.rigidbody.teleport(position, rotation);
```

---

### Collision Component

Defines physics collision shape.

```javascript
entity.addComponent('collision', {
  type: 'box',
  halfExtents: new pc.Vec3(0.5, 0.5, 0.5),
  radius: 0.5,           // Sphere/Capsule
  axis: pc.AXIS_Y,       // Capsule/Cylinder
  height: 2,             // Capsule/Cylinder
  asset: assetId,        // Mesh collision
  renderAsset: assetId   // Mesh collision (render)
});
```

**Collision Types**:
- `'box'`: Box shape
- `'sphere'`: Sphere shape
- `'capsule'`: Capsule shape
- `'cylinder'`: Cylinder shape
- `'cone'`: Cone shape
- `'mesh'`: Triangle mesh (static only)
- `'compound'`: Multiple shapes

**Events**:
```javascript
entity.collision.on('collisionstart', (result) => {
  console.log('Collision with:', result.other.name);
  console.log('Contact point:', result.contacts[0].point);
});

entity.collision.on('collisionend', (other) => {
  console.log('Collision ended with:', other.name);
});

entity.collision.on('contact', (result) => {
  // Contact maintained
});
```

---

### Script Component

Runs custom JavaScript code.

```javascript
entity.addComponent('script');
entity.script.create('scriptName', {
  attributes: {
    speed: 10,
    target: targetEntity
  }
});
```

**Script Definition**:
```javascript
const MyScript = pc.createScript('myScript');

MyScript.attributes.add('speed', {
  type: 'number',
  default: 10,
  title: 'Movement Speed',
  description: 'Units per second'
});

MyScript.attributes.add('target', {
  type: 'entity',
  title: 'Target Entity'
});

MyScript.prototype.initialize = function() {
  // Called once
};

MyScript.prototype.update = function(dt) {
  // Called every frame
  this.entity.translate(0, 0, this.speed * dt);
};

MyScript.prototype.postUpdate = function(dt) {
  // After all updates
};

MyScript.prototype.destroy = function() {
  // Cleanup
};
```

**Attribute Types**:
- `'boolean'`, `'number'`, `'string'`
- `'entity'`, `'asset'`, `'rgb'`, `'rgba'`
- `'vec2'`, `'vec3'`, `'vec4'`
- `'curve'`, `'colorcurve'`
- `'json'`

---

### Animation Component

Plays skeletal animations.

```javascript
entity.addComponent('animation', {
  assets: [animAsset],
  speed: 1.0,
  loop: true,
  activate: true
});
```

**Methods**:
```javascript
// Play animation
entity.animation.play('Run', 0.2);  // 0.2s blend time

// Get current animations
const anims = entity.animation.animations;

// Animation events
entity.animation.on('animationend', (name) => {
  console.log('Animation ended:', name);
});
```

---

### Sound Component

3D positional audio.

```javascript
entity.addComponent('sound', {
  positional: true,
  refDistance: 1,
  maxDistance: 10000,
  rollOffFactor: 1,
  distanceModel: pc.DISTANCE_LINEAR,
  slots: {
    'music': {
      asset: musicAsset,
      autoPlay: true,
      loop: true,
      volume: 0.5,
      pitch: 1.0
    }
  }
});
```

**Methods**:
```javascript
entity.sound.play('slotName');
entity.sound.pause('slotName');
entity.sound.stop('slotName');

entity.sound.volume = 0.8;  // Global volume
```

---

## Assets

### pc.AssetRegistry

Manages loading and caching of assets.

**add(asset)**
```javascript
const asset = new pc.Asset('name', 'texture', { url: '/texture.jpg' });
app.assets.add(asset);
```

**load(asset)**
```javascript
app.assets.load(asset);
```

**remove(asset)**
```javascript
app.assets.remove(asset);
```

**find()**
```javascript
// Find by name
const asset = app.assets.find('PlayerModel');

// Find by type
const textures = app.assets.findAll('texture');

// Find by tag
const tagged = app.assets.findByTag('environment');
```

**Events**:
```javascript
asset.ready((loadedAsset) => {
  // Asset loaded
  console.log('Loaded:', loadedAsset.resource);
});

asset.on('load', (asset) => {
  // Asset loaded
});

asset.on('error', (err) => {
  // Loading failed
});

asset.on('remove', () => {
  // Asset removed from registry
});
```

---

### Asset Types

**Texture**:
```javascript
const texture = new pc.Asset('diffuse', 'texture', {
  url: '/textures/diffuse.jpg'
});
```

**Model (Container)**:
```javascript
const model = new pc.Asset('character', 'container', {
  url: '/models/character.glb'
});

model.ready((asset) => {
  const entity = asset.resource.instantiateRenderEntity();
  app.root.addChild(entity);
});
```

**Material**:
```javascript
const material = new pc.Asset('custom', 'material');
```

**Audio**:
```javascript
const audio = new pc.Asset('music', 'audio', {
  url: '/audio/music.mp3'
});
```

**Script**:
```javascript
const script = new pc.Asset('playerController', 'script', {
  url: '/scripts/player-controller.js'
});
```

---

## Graphics

### pc.StandardMaterial

PBR material for rendering.

```javascript
const material = new pc.StandardMaterial();

// Diffuse (albedo)
material.diffuse = new pc.Color(1, 0, 0);  // Red
material.diffuseMap = texture;

// Metalness
material.metalness = 0.5;
material.metalnessMap = metalnessTexture;

// Gloss (inverse of roughness)
material.gloss = 0.8;
material.glossMap = roughnessTexture;

// Normal map
material.normalMap = normalTexture;
material.bumpiness = 1.0;

// Emissive
material.emissive = new pc.Color(1, 1, 0);
material.emissiveMap = emissiveTexture;
material.emissiveIntensity = 1.0;

// Ambient occlusion
material.aoMap = aoTexture;

// Opacity
material.opacity = 0.5;
material.opacityMap = opacityTexture;
material.blendType = pc.BLEND_NORMAL;

// Update material
material.update();
```

**Blend Types**:
- `pc.BLEND_NONE`: Opaque
- `pc.BLEND_NORMAL`: Alpha blending
- `pc.BLEND_ADDITIVE`: Additive blending
- `pc.BLEND_MULTIPLICATIVE`: Multiply blending

---

### pc.Texture

2D texture resource.

```javascript
const texture = new pc.Texture(app.graphicsDevice, {
  width: 512,
  height: 512,
  format: pc.PIXELFORMAT_RGBA8,
  minFilter: pc.FILTER_LINEAR_MIPMAP_LINEAR,
  magFilter: pc.FILTER_LINEAR,
  addressU: pc.ADDRESS_REPEAT,
  addressV: pc.ADDRESS_REPEAT,
  mipmaps: true,
  anisotropy: 16
});
```

**Pixel Formats**:
- `pc.PIXELFORMAT_RGBA8`: Standard 8-bit RGBA
- `pc.PIXELFORMAT_RGB8`: 8-bit RGB
- `pc.PIXELFORMAT_DXT5`: GPU-compressed
- `pc.PIXELFORMAT_ETC2_RGBA`: Mobile compression

**Filters**:
- `pc.FILTER_NEAREST`: Pixelated
- `pc.FILTER_LINEAR`: Smooth
- `pc.FILTER_LINEAR_MIPMAP_LINEAR`: Trilinear (best quality)

**Address Modes**:
- `pc.ADDRESS_REPEAT`: Tile texture
- `pc.ADDRESS_CLAMP`: Clamp to edge
- `pc.ADDRESS_MIRRORED_REPEAT`: Mirror tiling

---

## Input

### pc.Keyboard

Keyboard input handling.

```javascript
const keyboard = new pc.Keyboard(window);

// Check if key is currently pressed
if (keyboard.isPressed(pc.KEY_W)) {
  player.translate(0, 0, -speed * dt);
}

// Check if key was just pressed this frame
if (keyboard.wasPressed(pc.KEY_SPACE)) {
  player.jump();
}

// Check if key was just released
if (keyboard.wasReleased(pc.KEY_SHIFT)) {
  player.stopSprinting();
}

// Events
keyboard.on(pc.EVENT_KEYDOWN, (event) => {
  console.log('Key down:', event.key);
});

keyboard.on(pc.EVENT_KEYUP, (event) => {
  console.log('Key up:', event.key);
});
```

**Key Constants**:
- `pc.KEY_W`, `pc.KEY_A`, `pc.KEY_S`, `pc.KEY_D`
- `pc.KEY_SPACE`, `pc.KEY_SHIFT`, `pc.KEY_CONTROL`
- `pc.KEY_ENTER`, `pc.KEY_ESCAPE`
- `pc.KEY_UP`, `pc.KEY_DOWN`, `pc.KEY_LEFT`, `pc.KEY_RIGHT`
- `pc.KEY_0` through `pc.KEY_9`
- `pc.KEY_A` through `pc.KEY_Z`

---

### pc.Mouse

Mouse input handling.

```javascript
const mouse = new pc.Mouse(canvas);

// Events
mouse.on(pc.EVENT_MOUSEDOWN, (event) => {
  if (event.button === pc.MOUSEBUTTON_LEFT) {
    console.log('Left click at:', event.x, event.y);
  }
});

mouse.on(pc.EVENT_MOUSEUP, (event) => {
  console.log('Mouse up');
});

mouse.on(pc.EVENT_MOUSEMOVE, (event) => {
  const dx = event.dx;  // Delta movement
  const dy = event.dy;

  camera.rotate(-dy * 0.2, -dx * 0.2, 0);
});

mouse.on(pc.EVENT_MOUSEWHEEL, (event) => {
  zoom += event.wheelDelta * 0.1;
});
```

**Mouse Buttons**:
- `pc.MOUSEBUTTON_LEFT`: Left button
- `pc.MOUSEBUTTON_MIDDLE`: Middle button
- `pc.MOUSEBUTTON_RIGHT`: Right button

**Properties**:
```javascript
mouse.isPressed(pc.MOUSEBUTTON_LEFT);  // Check if button pressed
```

---

### pc.TouchDevice

Touch input for mobile.

```javascript
const touch = new pc.TouchDevice(canvas);

touch.on(pc.EVENT_TOUCHSTART, (event) => {
  event.touches.forEach((touch, index) => {
    console.log(`Touch ${index} at:`, touch.x, touch.y);
  });
});

touch.on(pc.EVENT_TOUCHEND, (event) => {
  // Touches ended
});

touch.on(pc.EVENT_TOUCHMOVE, (event) => {
  const touch = event.touches[0];
  const dx = touch.dx;
  const dy = touch.dy;
});
```

---

## Physics

### Raycasting

Cast rays to detect collisions.

```javascript
// Raycast from camera through mouse
const camera = app.root.findByName('Camera');
const from = camera.camera.screenToWorld(mouseX, mouseY, camera.camera.nearClip);
const to = camera.camera.screenToWorld(mouseX, mouseY, camera.camera.farClip);

const result = app.systems.rigidbody.raycastFirst(from, to);

if (result) {
  console.log('Hit entity:', result.entity.name);
  console.log('Hit point:', result.point);
  console.log('Hit normal:', result.normal);
}

// Raycast all
const results = app.systems.rigidbody.raycastAll(from, to);
results.forEach(result => {
  console.log('Hit:', result.entity.name);
});
```

---

## Audio

### pc.SoundComponent

3D positional audio.

```javascript
entity.addComponent('sound');

// Add sound slot
entity.sound.addSlot('footstep', {
  asset: footstepAsset,
  autoPlay: false,
  loop: false,
  volume: 0.8,
  pitch: 1.0,
  positional: true,
  refDistance: 1,
  maxDistance: 20
});

// Play sound
entity.sound.play('footstep');

// Stop sound
entity.sound.stop('footstep');

// Pause sound
entity.sound.pause('footstep');

// Resume
entity.sound.resume('footstep');
```

---

## Utilities

### pc.Vec3

3D vector.

```javascript
const v = new pc.Vec3(x, y, z);

// Operations
v.add(other);
v.sub(other);
v.mul(scalar);
v.div(scalar);
v.dot(other);
v.cross(other);
v.normalize();
v.length();
v.distance(other);
v.lerp(a, b, t);
```

### pc.Color

RGBA color.

```javascript
const color = new pc.Color(r, g, b, a);  // 0-1 range

// Conversion
const hex = color.toString();  // "#RRGGBB"
```

### pc.Quat

Quaternion rotation.

```javascript
const quat = new pc.Quat();
quat.setFromEulerAngles(x, y, z);
quat.slerp(a, b, t);  // Spherical interpolation
```

---

## Constants Reference

**Fill Modes**:
- `pc.FILLMODE_NONE`
- `pc.FILLMODE_FILL_WINDOW`
- `pc.FILLMODE_KEEP_ASPECT`

**Resolution Modes**:
- `pc.RESOLUTION_AUTO`
- `pc.RESOLUTION_FIXED`

**Projection Types**:
- `pc.PROJECTION_PERSPECTIVE`
- `pc.PROJECTION_ORTHOGRAPHIC`

**Light Types**:
- `pc.LIGHTTYPE_DIRECTIONAL`
- `pc.LIGHTTYPE_POINT`
- `pc.LIGHTTYPE_SPOT`

**Body Types**:
- `pc.BODYTYPE_STATIC`
- `pc.BODYTYPE_DYNAMIC`
- `pc.BODYTYPE_KINEMATIC`

**Blend Types**:
- `pc.BLEND_NONE`
- `pc.BLEND_NORMAL`
- `pc.BLEND_ADDITIVE`
- `pc.BLEND_MULTIPLICATIVE`

---

## License

MIT - Free for commercial and personal use.
