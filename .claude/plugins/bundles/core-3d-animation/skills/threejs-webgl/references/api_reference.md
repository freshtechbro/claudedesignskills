# Three.js API Quick Reference

## Core Classes

### Scene
```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);
scene.fog = new THREE.Fog(0xffffff, 10, 100);
scene.add(object);
scene.remove(object);
scene.getObjectByName('name');
```

### Camera

#### PerspectiveCamera
```javascript
new THREE.PerspectiveCamera(fov, aspect, near, far);
camera.position.set(x, y, z);
camera.lookAt(target);
camera.updateProjectionMatrix(); // Call after changing properties
```

**Common FOVs:**
- 45° - Natural perspective
- 50° - Default for many apps
- 75° - Wide, immersive feel

#### OrthographicCamera
```javascript
new THREE.OrthographicCamera(left, right, top, bottom, near, far);
// Useful for 2D/isometric views
```

### Renderer

#### WebGLRenderer
```javascript
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true,
  powerPreference: "high-performance"
});
renderer.setSize(width, height);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
```

#### WebGPURenderer
```javascript
const renderer = new THREE.WebGPURenderer({ antialias: true });
renderer.setAnimationLoop(animate);
```

## Geometry

### Built-in Geometries
```javascript
new THREE.BoxGeometry(width, height, depth);
new THREE.SphereGeometry(radius, widthSegments, heightSegments);
new THREE.PlaneGeometry(width, height);
new THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments);
new THREE.TorusGeometry(radius, tube, radialSegments, tubularSegments);
```

### BufferGeometry (Custom)
```javascript
const geometry = new THREE.BufferGeometry();
const vertices = new Float32Array([...]);
geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
geometry.computeVertexNormals();
geometry.computeBoundingSphere();
```

### Geometry Operations
```javascript
geometry.dispose(); // Free memory
geometry.center(); // Center geometry at origin
geometry.scale(x, y, z);
geometry.rotateX(angle);
geometry.translate(x, y, z);
```

## Materials

### Common Properties
```javascript
{
  color: 0xff0000,
  transparent: true,
  opacity: 0.5,
  side: THREE.DoubleSide, // FrontSide, BackSide, DoubleSide
  depthWrite: true,
  depthTest: true,
  wireframe: false
}
```

### Material Types
```javascript
new THREE.MeshBasicMaterial({}); // Unlit
new THREE.MeshLambertMaterial({}); // Simple diffuse
new THREE.MeshPhongMaterial({ shininess: 30 }); // Specular
new THREE.MeshStandardMaterial({ roughness: 0.5, metalness: 0.5 }); // PBR
new THREE.MeshPhysicalMaterial({ // Advanced PBR
  roughness: 0.0,
  metalness: 0.0,
  clearcoat: 1.0,
  clearcoatRoughness: 0.1,
  transmission: 1.0,
  ior: 1.5
});
```

## Lights

### AmbientLight
```javascript
new THREE.AmbientLight(0xffffff, 0.5);
// Illuminates all objects equally
```

### DirectionalLight
```javascript
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 7.5);
light.castShadow = true;
// Parallel rays (like sunlight)
```

### PointLight
```javascript
const light = new THREE.PointLight(0xffffff, 1, distance, decay);
light.castShadow = true;
// Radiates in all directions
```

### SpotLight
```javascript
const light = new THREE.SpotLight(0xffffff, 1, distance, angle, penumbra, decay);
light.target.position.set(x, y, z);
light.castShadow = true;
```

### HemisphereLight
```javascript
new THREE.HemisphereLight(skyColor, groundColor, intensity);
// Sky and ground hemisphere lighting
```

### Light Properties
```javascript
light.intensity = 1.0;
light.color.set(0xff0000);
light.power = 1700; // Lumens (for PointLight)
light.visible = false;
```

## Textures

### TextureLoader
```javascript
const loader = new THREE.TextureLoader();
const texture = loader.load('texture.jpg', onLoad, onProgress, onError);

texture.colorSpace = THREE.SRGBColorSpace;
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
texture.repeat.set(2, 2);
texture.offset.set(0.5, 0.5);
texture.rotation = Math.PI / 4;
texture.minFilter = THREE.LinearMipmapLinearFilter;
texture.magFilter = THREE.LinearFilter;
texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
```

### Texture Types
```javascript
material.map = diffuseTexture;
material.normalMap = normalTexture;
material.roughnessMap = roughnessTexture;
material.metalnessMap = metalnessTexture;
material.emissiveMap = emissiveTexture;
material.aoMap = aoTexture;
material.bumpMap = bumpTexture;
material.displacementMap = displacementTexture;
material.alphaMap = alphaTexture;
```

## Mesh

### Creation
```javascript
const mesh = new THREE.Mesh(geometry, material);
mesh.position.set(x, y, z);
mesh.rotation.set(x, y, z); // Radians
mesh.scale.set(x, y, z);
mesh.castShadow = true;
mesh.receiveShadow = true;
mesh.visible = true;
mesh.name = 'my-mesh';
```

### Transformations
```javascript
mesh.translateX(distance);
mesh.translateY(distance);
mesh.translateZ(distance);
mesh.rotateX(angle);
mesh.rotateY(angle);
mesh.rotateZ(angle);
mesh.lookAt(targetVector);
```

### Matrix Operations
```javascript
mesh.updateMatrix();
mesh.updateMatrixWorld(force);
mesh.applyMatrix4(matrix);
```

## Groups
```javascript
const group = new THREE.Group();
group.add(mesh1, mesh2, mesh3);
group.position.set(x, y, z);
scene.add(group);
```

## Animation

### AnimationMixer
```javascript
const mixer = new THREE.AnimationMixer(model);
const action = mixer.clipAction(gltf.animations[0]);
action.play();

// In animation loop:
const delta = clock.getDelta();
mixer.update(delta);
```

### AnimationAction Methods
```javascript
action.play();
action.stop();
action.pause();
action.reset();
action.setLoop(THREE.LoopRepeat, Infinity);
action.setDuration(seconds);
action.clampWhenFinished = true;
action.fadeIn(duration);
action.fadeOut(duration);
action.crossFadeTo(otherAction, duration);
```

## Loaders

### GLTFLoader
```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  scene.add(gltf.scene);
}, onProgress, onError);
```

### DRACOLoader
```javascript
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');
gltfLoader.setDRACOLoader(dracoLoader);
```

### OBJLoader, FBXLoader
```javascript
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
```

## Controls

### OrbitControls
```javascript
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2;
controls.target.set(0, 0, 0);
controls.update(); // Call in animation loop if damping enabled
```

### MapControls, TrackballControls, FlyControls
```javascript
import { MapControls } from 'three/addons/controls/MapControls.js';
import { TrackballControls } from 'three/addons/controls/TrackballControls.js';
import { FlyControls } from 'three/addons/controls/FlyControls.js';
```

## Raycaster
```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
}

raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(scene.children, true);

if (intersects.length > 0) {
  const object = intersects[0].object;
  const point = intersects[0].point; // Intersection point
  const face = intersects[0].face; // Intersected face
  const distance = intersects[0].distance;
}
```

## Math Utilities

### Vector3
```javascript
const v = new THREE.Vector3(x, y, z);
v.set(x, y, z);
v.add(otherVector);
v.sub(otherVector);
v.multiply(otherVector);
v.multiplyScalar(scalar);
v.normalize();
v.length();
v.distanceTo(otherVector);
v.lerp(otherVector, alpha);
v.cross(otherVector);
v.dot(otherVector);
```

### Quaternion
```javascript
const q = new THREE.Quaternion();
q.setFromEuler(euler);
q.setFromAxisAngle(axis, angle);
mesh.quaternion.copy(q);
```

### Clock
```javascript
const clock = new THREE.Clock();
const delta = clock.getDelta(); // Time since last call
const elapsed = clock.getElapsedTime(); // Total time
clock.start();
clock.stop();
```

## Post-Processing

### EffectComposer
```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.render();
```

### Common Passes
```javascript
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { SMAAPass } from 'three/addons/postprocessing/SMAAPass.js';
import { OutlinePass } from 'three/addons/postprocessing/OutlinePass.js';
```

## Helpers

```javascript
new THREE.AxesHelper(size);
new THREE.GridHelper(size, divisions);
new THREE.CameraHelper(camera);
new THREE.DirectionalLightHelper(light, size);
new THREE.SpotLightHelper(light);
new THREE.BoxHelper(object, color);
```

## Constants

### Side
- `THREE.FrontSide` (default)
- `THREE.BackSide`
- `THREE.DoubleSide`

### Blending Modes
- `THREE.NormalBlending` (default)
- `THREE.AdditiveBlending`
- `THREE.SubtractiveBlending`
- `THREE.MultiplyBlending`

### Shadow Map Types
- `THREE.BasicShadowMap`
- `THREE.PCFShadowMap`
- `THREE.PCFSoftShadowMap`
- `THREE.VSMShadowMap`

### Tone Mapping
- `THREE.NoToneMapping`
- `THREE.LinearToneMapping`
- `THREE.ReinhardToneMapping`
- `THREE.CineonToneMapping`
- `THREE.ACESFilmicToneMapping`

### Color Spaces
- `THREE.SRGBColorSpace`
- `THREE.LinearSRGBColorSpace`

## Performance Tips

```javascript
// Dispose resources
geometry.dispose();
material.dispose();
texture.dispose();
renderer.dispose();

// Frustum culling (automatic)
mesh.frustumCulled = true;

// Matrix updates
mesh.matrixAutoUpdate = false; // Manual control
mesh.updateMatrix();

// Render on demand
function render() {
  renderer.render(scene, camera);
}
// Call render() only when needed

// Use InstancedMesh for repeated objects
const instancedMesh = new THREE.InstancedMesh(geometry, material, count);
```

## Common Gotchas

1. **Always update projection matrix after changing camera properties**
2. **Set texture.colorSpace = THREE.SRGBColorSpace for diffuse textures**
3. **Enable shadows on renderer, lights, and objects**
4. **Dispose geometries, materials, and textures to prevent memory leaks**
5. **Use Clock.getDelta() for frame-independent animations**
6. **Call controls.update() in animation loop if damping is enabled**
