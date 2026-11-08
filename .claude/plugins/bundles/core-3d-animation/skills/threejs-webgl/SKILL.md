---
name: threejs-webgl
description: Comprehensive skill for Three.js 3D web development. Use this skill when building interactive 3D scenes, WebGL/WebGPU applications, product configurators, 3D visualizations, or immersive web experiences. Triggers on tasks involving Three.js, 3D rendering, scenes, cameras, meshes, materials, lights, animations, textures, or WebGL/WebGPU rendering.
---

# Three.js WebGL/WebGPU Development

## Overview

Three.js is the industry-standard JavaScript library for creating 3D graphics in web browsers using WebGL and WebGPU. This skill provides comprehensive guidance for building performant, interactive 3D experiences including scenes, cameras, renderers, geometries, materials, lights, textures, and animations.

## Core Concepts

### Scene Graph Architecture

Three.js uses a hierarchical scene graph where all 3D objects are organized in a tree structure:

```javascript
Scene
├── Camera
├── Lights
│   ├── AmbientLight
│   ├── DirectionalLight
│   └── PointLight
├── Meshes
│   ├── Mesh (Geometry + Material)
│   └── InstancedMesh
└── Groups
```

### Essential Components

Every Three.js application requires these core elements:

1. **Scene**: Container for all 3D objects
2. **Camera**: Defines the viewing perspective
3. **Renderer**: Draws the scene to canvas (WebGL or WebGPU)
4. **Geometry**: Defines the shape of objects
5. **Material**: Defines the surface appearance
6. **Mesh**: Combines geometry and material

## Quick Start Pattern

### Basic Scene Setup

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x333333);

const camera = new THREE.PerspectiveCamera(
  75, // FOV
  window.innerWidth / window.innerHeight, // Aspect ratio
  0.1, // Near clipping plane
  1000 // Far clipping plane
);
camera.position.set(0, 2, 5);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Animation Loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();

// Handle Resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

### WebGPU Setup (Modern Alternative)

```javascript
import * as THREE from 'three/webgpu';

const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setAnimationLoop(animate);
renderer.toneMapping = THREE.LinearToneMapping;
renderer.toneMappingExposure = 1;
document.body.appendChild(renderer.domElement);
```

## Common Patterns

### 1. Creating Meshes with Materials

```javascript
// Basic Mesh
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({
  color: 0x00ff00,
  roughness: 0.5,
  metalness: 0.5
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Textured Mesh
const loader = new THREE.TextureLoader();
const texture = loader.load('texture.jpg');
texture.colorSpace = THREE.SRGBColorSpace;

const texturedMaterial = new THREE.MeshStandardMaterial({
  map: texture
});
const mesh = new THREE.Mesh(geometry, texturedMaterial);
scene.add(mesh);
```

### 2. Lighting Strategies

```javascript
// Three-Point Lighting Setup
function setupThreePointLight(scene) {
  // Key Light (Main)
  const keyLight = new THREE.DirectionalLight(0xffffff, 3);
  keyLight.position.set(5, 10, 7.5);
  keyLight.castShadow = true;
  scene.add(keyLight);

  // Fill Light (Softens shadows)
  const fillLight = new THREE.DirectionalLight(0xffffff, 1);
  fillLight.position.set(-5, 5, -5);
  scene.add(fillLight);

  // Rim Light (Edge definition)
  const rimLight = new THREE.DirectionalLight(0xffffff, 0.5);
  rimLight.position.set(0, 5, -10);
  scene.add(rimLight);

  // Ambient (Base illumination)
  const ambient = new THREE.AmbientLight(0x404040, 0.5);
  scene.add(ambient);
}

// Physical Light (Realistic)
const bulbLight = new THREE.PointLight(0xffee88, 1, 100, 2);
bulbLight.power = 1700; // Lumens (100W bulb equivalent)
bulbLight.castShadow = true;
scene.add(bulbLight);

// Hemisphere Light (Sky + Ground)
const hemiLight = new THREE.HemisphereLight(
  0xddeeff, // Sky color
  0x0f0e0d, // Ground color
  0.02
);
scene.add(hemiLight);
```

### 3. Instanced Geometry (Performance)

```javascript
// For rendering thousands of similar objects efficiently
const geometry = new THREE.SphereGeometry(0.1, 16, 16);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const instancedMesh = new THREE.InstancedMesh(geometry, material, 1000);

const matrix = new THREE.Matrix4();
const color = new THREE.Color();

for (let i = 0; i < 1000; i++) {
  matrix.setPosition(
    Math.random() * 10 - 5,
    Math.random() * 10 - 5,
    Math.random() * 10 - 5
  );
  instancedMesh.setMatrixAt(i, matrix);
  instancedMesh.setColorAt(i, color.setHex(Math.random() * 0xffffff));
}

instancedMesh.instanceMatrix.needsUpdate = true;
scene.add(instancedMesh);
```

### 4. Loading 3D Models (glTF)

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

// Setup loaders
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

// Load model
gltfLoader.load('model.glb', (gltf) => {
  const model = gltf.scene;

  // Enable shadows
  model.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  scene.add(model);

  // Handle animations
  if (gltf.animations.length > 0) {
    const mixer = new THREE.AnimationMixer(model);
    const action = mixer.clipAction(gltf.animations[0]);
    action.play();

    // In animation loop:
    // mixer.update(deltaTime);
  }
});
```

### 5. Shadow Configuration

```javascript
// Enable shadows on renderer
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // or VSMShadowMap

// Configure light shadows
directionalLight.castShadow = true;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
directionalLight.shadow.camera.near = 0.5;
directionalLight.shadow.camera.far = 50;
directionalLight.shadow.camera.left = -10;
directionalLight.shadow.camera.right = 10;
directionalLight.shadow.camera.top = 10;
directionalLight.shadow.camera.bottom = -10;
directionalLight.shadow.radius = 4;
directionalLight.shadow.blurSamples = 8;

// Objects casting/receiving shadows
mesh.castShadow = true;
mesh.receiveShadow = true;
```

### 6. Raycasting (Interaction)

```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0) {
    const object = intersects[0].object;
    object.material.color.set(0xff0000);
  }
}

window.addEventListener('click', onMouseClick);
```

## Integration Patterns

### With GSAP for Animation

```javascript
import gsap from 'gsap';

// Animate camera
gsap.to(camera.position, {
  x: 5,
  y: 3,
  z: 10,
  duration: 2,
  ease: "power2.inOut",
  onUpdate: () => {
    camera.lookAt(scene.position);
  }
});

// Animate mesh properties
gsap.to(mesh.rotation, {
  y: Math.PI * 2,
  duration: 3,
  repeat: -1,
  ease: "none"
});
```

### With React (see react-three-fiber skill)

```javascript
// Three.js integrates naturally with React Three Fiber
// Use the react-three-fiber skill for React integration patterns
```

### With Post-Processing

```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5, // strength
  0.4, // radius
  0.85 // threshold
);
composer.addPass(bloomPass);

// In animation loop:
composer.render();
```

## Performance Optimization

### 1. Geometry Reuse
```javascript
// Bad: Creates new geometry for each mesh
for (let i = 0; i < 100; i++) {
  const geometry = new THREE.BoxGeometry(1, 1, 1);
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
}

// Good: Reuse geometry
const sharedGeometry = new THREE.BoxGeometry(1, 1, 1);
for (let i = 0; i < 100; i++) {
  const mesh = new THREE.Mesh(sharedGeometry, material);
  scene.add(mesh);
}
```

### 2. Use InstancedMesh for Repeated Objects
For hundreds/thousands of identical objects, use `InstancedMesh` (see pattern above).

### 3. Texture Optimization
```javascript
// Compress textures
texture.generateMipmaps = true;
texture.minFilter = THREE.LinearMipmapLinearFilter;
texture.magFilter = THREE.LinearFilter;

// Use power-of-two dimensions (512, 1024, 2048)
// Consider texture atlases for multiple small textures
```

### 4. Level of Detail (LOD)
```javascript
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);    // 0-50 units
lod.addLevel(mediumDetailMesh, 50);  // 50-100 units
lod.addLevel(lowDetailMesh, 100);    // 100+ units
scene.add(lod);
```

### 5. Frustum Culling
Three.js automatically culls objects outside the camera's view. Ensure objects have correct bounding spheres:

```javascript
mesh.geometry.computeBoundingSphere();
```

### 6. Dispose Resources
```javascript
function disposeScene() {
  scene.traverse((object) => {
    if (object.geometry) object.geometry.dispose();
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach(material => material.dispose());
      } else {
        object.material.dispose();
      }
    }
  });
  renderer.dispose();
}
```

## Best Practices

### 1. Use Animation Clocks for Consistent Timing
```javascript
const clock = new THREE.Clock();

function animate() {
  const deltaTime = clock.getDelta();
  const elapsedTime = clock.getElapsedTime();

  // Use deltaTime for frame-independent animations
  mesh.rotation.y += deltaTime * Math.PI * 0.5; // 90° per second

  renderer.render(scene, camera);
}
```

### 2. Camera Setup Guidelines
- **FOV**: 45-75° for most applications
- **Near plane**: As far as possible (avoid z-fighting)
- **Far plane**: As close as possible (precision)
- **Aspect ratio**: Always match canvas dimensions

### 3. Material Selection
- **MeshBasicMaterial**: Unlit, flat colors (debugging, UI)
- **MeshLambertMaterial**: Cheap diffuse lighting (mobile)
- **MeshPhongMaterial**: Specular highlights (older standard)
- **MeshStandardMaterial**: PBR, realistic (recommended)
- **MeshPhysicalMaterial**: Advanced PBR (clearcoat, transmission)

### 4. Coordinate System
- Three.js uses right-handed coordinate system
- +Y is up, +Z is toward camera, +X is right
- Rotations use radians (Math.PI = 180°)

### 5. Scene Organization
```javascript
// Group related objects
const building = new THREE.Group();
building.add(walls, roof, windows);
scene.add(building);

// Use meaningful names
mesh.name = 'player-character';
const found = scene.getObjectByName('player-character');
```

## Common Pitfalls

### 1. Not Updating Aspect Ratio on Resize
Always update camera aspect ratio and projection matrix when window resizes.

### 2. Creating New Objects in Animation Loop
```javascript
// Bad: Memory leak
function animate() {
  const geometry = new THREE.BoxGeometry(); // Created every frame!
  // ...
}

// Good: Create once outside loop
const geometry = new THREE.BoxGeometry();
function animate() {
  // Reuse geometry
}
```

### 3. Forgetting to Enable Shadows
Remember to enable shadows on renderer, lights, and objects.

### 4. Z-Fighting (Flickering)
- Increase near plane distance
- Decrease far plane distance
- Avoid overlapping coplanar surfaces
- Use `material.polygonOffset = true` with `material.polygonOffsetFactor`

### 5. Color Space Issues
```javascript
// Always set color space for textures
texture.colorSpace = THREE.SRGBColorSpace;

// Set renderer output encoding
renderer.outputColorSpace = THREE.SRGBColorSpace;
```

### 6. Not Disposing Resources
Always call `.dispose()` on geometries, materials, textures, and renderers when no longer needed.

## Resources

This skill includes bundled resources to accelerate Three.js development:

### references/
- `api_reference.md`: Quick API reference for core classes (Scene, Camera, Renderer, etc.)
- `materials_guide.md`: Comprehensive material types and properties
- `optimization_checklist.md`: Performance optimization strategies

### scripts/
- `setup_scene.py`: Generate boilerplate Three.js scene setup code
- `texture_optimizer.py`: Batch optimize textures for web (resize, compress)
- `gltf_validator.py`: Validate glTF models before use

### assets/
- `starter_scene/`: Complete HTML/JS boilerplate project
- `shaders/`: Custom GLSL shader examples (vertex, fragment)
- `hdri/`: Environment maps for PBR lighting
- `draco/`: DRACO decoder for compressed models

## Advanced Topics

### Custom Shaders (GLSL)
```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 },
    uColor: { value: new THREE.Color(0x00ff00) }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(uColor * vUv.x, 1.0);
    }
  `
});
```

### Render Targets (Render-to-Texture)
```javascript
const renderTarget = new THREE.WebGLRenderTarget(512, 512);

// Render scene to texture
renderer.setRenderTarget(renderTarget);
renderer.render(scene, camera);
renderer.setRenderTarget(null);

// Use texture
const material = new THREE.MeshBasicMaterial({
  map: renderTarget.texture
});
```

### GPU Computation (GPGPU)
Use `GPUComputationRenderer` for particle simulations, cloth physics, etc.

## When to Use This Skill

Use this skill when:
- Building interactive 3D web experiences
- Creating product configurators or visualizers
- Implementing WebGL/WebGPU rendering
- Working with 3D models, scenes, or animations
- Optimizing Three.js performance
- Integrating Three.js with other libraries (GSAP, React, etc.)
- Debugging Three.js rendering issues

For React integration, use the **react-three-fiber** skill.
For animation, combine with the **gsap-scrolltrigger** skill.
For UI animations, use the **motion-framer** skill.
