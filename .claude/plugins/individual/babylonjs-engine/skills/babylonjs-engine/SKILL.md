---
name: babylonjs-engine
description: Comprehensive skill for Babylon.js 3D web rendering engine. Use this skill when building real-time 3D experiences, browser-based games, interactive visualizations, or immersive web applications. Triggers on tasks involving Babylon.js, 3D scenes, WebGL/WebGPU rendering, entity-component systems, physics simulations, PBR materials, shadow mapping, or 3D model loading. Alternative to Three.js with built-in editor integration and game engine features.
---

# Babylon.js Engine Skill

## Related Skills
- threejs-webgl: Alternative 3D engine
- react-three-fiber: React integration for 3D
- gsap-scrolltrigger: Animation library
- motion-framer: UI animations

## Core Concepts

### 1. Engine and Scene Initialization

**Basic Setup**
```javascript
// Get canvas element
const canvas = document.getElementById('renderCanvas');

// Create engine
const engine = new BABYLON.Engine(canvas, true, {
  preserveDrawingBuffer: true,
  stencil: true
});

// Create scene
const scene = new BABYLON.Scene(engine);

// Render loop
engine.runRenderLoop(() => {
  scene.render();
});

// Handle resize
window.addEventListener('resize', () => {
  engine.resize();
});
```

**ES6/TypeScript Setup**
```typescript
import { Engine } from '@babylonjs/core/Engines/engine';
import { Scene } from '@babylonjs/core/scene';
import { FreeCamera } from '@babylonjs/core/Cameras/freeCamera';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { HemisphericLight } from '@babylonjs/core/Lights/hemisphericLight';
import { CreateSphere } from '@babylonjs/core/Meshes/Builders/sphereBuilder';

const canvas = document.getElementById('renderCanvas') as HTMLCanvasElement;
const engine = new Engine(canvas);
const scene = new Scene(engine);

// Camera setup
const camera = new FreeCamera('camera1', new Vector3(0, 5, -10), scene);
camera.setTarget(Vector3.Zero());
camera.attachControl(canvas, true);

// Lighting
const light = new HemisphericLight('light1', new Vector3(0, 1, 0), scene);
light.intensity = 0.7;

// Create mesh
const sphere = CreateSphere('sphere1', { segments: 16, diameter: 2 }, scene);
sphere.position.y = 2;

// Render
engine.runRenderLoop(() => {
  scene.render();
});
```

**Scene Configuration Options**
```javascript
const scene = new BABYLON.Scene(engine, {
  // Optimize for large mesh counts
  useGeometryUniqueIdsMap: true,
  useMaterialMeshMap: true,
  useClonedMeshMap: true
});
```

### 2. Camera Systems

**Free Camera (FPS-style)**
```javascript
const camera = new BABYLON.FreeCamera('camera1', new BABYLON.Vector3(0, 5, -10), scene);
camera.setTarget(BABYLON.Vector3.Zero());
camera.attachControl(canvas, true);

// Movement settings
camera.speed = 0.5;
camera.angularSensibility = 2000;
camera.keysUp = [87]; // W
camera.keysDown = [83]; // S
camera.keysLeft = [65]; // A
camera.keysRight = [68]; // D
```

**Arc Rotate Camera (Orbit)**
```javascript
const camera = new BABYLON.ArcRotateCamera(
  'camera',
  -Math.PI / 2,        // alpha (horizontal rotation)
  Math.PI / 2.5,       // beta (vertical rotation)
  15,                  // radius (distance)
  new BABYLON.Vector3(0, 0, 0), // target
  scene
);
camera.attachControl(canvas, true);

// Constraints
camera.lowerRadiusLimit = 5;
camera.upperRadiusLimit = 50;
camera.lowerBetaLimit = 0.1;
camera.upperBetaLimit = Math.PI / 2;
```

**Universal Camera (Advanced)**
```javascript
const camera = new BABYLON.UniversalCamera('camera', new BABYLON.Vector3(0, 5, -10), scene);
camera.setTarget(BABYLON.Vector3.Zero());
camera.attachControl(canvas, true);

// Collision detection
camera.checkCollisions = true;
camera.applyGravity = true;
camera.ellipsoid = new BABYLON.Vector3(1, 1, 1);
```

### 3. Lighting Systems

**Hemispheric Light (Ambient)**
```javascript
const light = new BABYLON.HemisphericLight('light1', new BABYLON.Vector3(0, 1, 0), scene);
light.intensity = 0.7;
light.diffuse = new BABYLON.Color3(1, 1, 1);
light.specular = new BABYLON.Color3(1, 1, 1);
light.groundColor = new BABYLON.Color3(0, 0, 0);
```

**Directional Light (Sun-like)**
```javascript
const light = new BABYLON.DirectionalLight('dirLight', new BABYLON.Vector3(-1, -2, -1), scene);
light.position = new BABYLON.Vector3(20, 40, 20);
light.intensity = 0.5;

// Shadow setup
const shadowGenerator = new BABYLON.ShadowGenerator(1024, light);
shadowGenerator.useExponentialShadowMap = true;
```

**Point Light (Omni-directional)**
```javascript
const light = new BABYLON.PointLight('pointLight', new BABYLON.Vector3(0, 10, 0), scene);
light.intensity = 0.7;
light.diffuse = new BABYLON.Color3(1, 0, 0);
light.specular = new BABYLON.Color3(0, 1, 0);

// Range and falloff
light.range = 100;
light.radius = 0.1;
```

**Spot Light (Focused)**
```javascript
const light = new BABYLON.SpotLight(
  'spotLight',
  new BABYLON.Vector3(0, 10, 0),      // position
  new BABYLON.Vector3(0, -1, 0),      // direction
  Math.PI / 3,                        // angle
  2,                                  // exponent
  scene
);
light.intensity = 0.8;
```

**Light Optimization (Include Only Specific Meshes)**
```javascript
// Only affect specific meshes
light.includedOnlyMeshes = [mesh1, mesh2, mesh3];

// Or exclude specific meshes
light.excludedMeshes = [mesh4, mesh5];
```

### 4. Mesh Creation

**Built-in Shapes**
```javascript
// Box
const box = BABYLON.MeshBuilder.CreateBox('box', {
  size: 2,
  width: 2,
  height: 2,
  depth: 2
}, scene);

// Sphere
const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {
  diameter: 2,
  segments: 32,
  diameterX: 2,
  diameterY: 2,
  diameterZ: 2,
  arc: 1,
  slice: 1
}, scene);

// Cylinder
const cylinder = BABYLON.MeshBuilder.CreateCylinder('cylinder', {
  height: 3,
  diameter: 2,
  tessellation: 24
}, scene);

// Plane
const plane = BABYLON.MeshBuilder.CreatePlane('plane', {
  size: 5,
  width: 5,
  height: 5
}, scene);

// Ground
const ground = BABYLON.MeshBuilder.CreateGround('ground', {
  width: 10,
  height: 10,
  subdivisions: 2
}, scene);

// Ground from heightmap
const ground = BABYLON.MeshBuilder.CreateGroundFromHeightMap('ground', 'heightmap.png', {
  width: 100,
  height: 100,
  subdivisions: 100,
  minHeight: 0,
  maxHeight: 10
}, scene);

// Torus
const torus = BABYLON.MeshBuilder.CreateTorus('torus', {
  diameter: 3,
  thickness: 1,
  tessellation: 16
}, scene);

// TorusKnot
const torusKnot = BABYLON.MeshBuilder.CreateTorusKnot('torusKnot', {
  radius: 2,
  tube: 0.6,
  radialSegments: 64,
  tubularSegments: 8,
  p: 2,
  q: 3
}, scene);
```

**Mesh Transformations**
```javascript
// Position
mesh.position = new BABYLON.Vector3(0, 5, 10);
mesh.position.x = 5;
mesh.position.y = 2;

// Rotation (radians)
mesh.rotation = new BABYLON.Vector3(0, Math.PI / 2, 0);
mesh.rotation.y = Math.PI / 4;

// Scaling
mesh.scaling = new BABYLON.Vector3(2, 2, 2);
mesh.scaling.x = 1.5;

// Look at
mesh.lookAt(new BABYLON.Vector3(0, 0, 0));

// Parent-child relationships
childMesh.parent = parentMesh;
```

**Mesh Properties**
```javascript
// Visibility
mesh.isVisible = true;
mesh.visibility = 0.5; // 0 = invisible, 1 = fully visible

// Picking
mesh.isPickable = true;
mesh.checkCollisions = true;

// Culling
mesh.cullingStrategy = BABYLON.AbstractMesh.CULLINGSTRATEGY_BOUNDINGSPHERE_ONLY;

// Receive shadows
mesh.receiveShadows = true;
```

### 5. Materials

**Standard Material**
```javascript
const material = new BABYLON.StandardMaterial('material', scene);

// Colors
material.diffuseColor = new BABYLON.Color3(1, 0, 1);
material.specularColor = new BABYLON.Color3(0.5, 0.6, 0.87);
material.emissiveColor = new BABYLON.Color3(0, 0, 0);
material.ambientColor = new BABYLON.Color3(0.23, 0.98, 0.53);

// Textures
material.diffuseTexture = new BABYLON.Texture('diffuse.png', scene);
material.specularTexture = new BABYLON.Texture('specular.png', scene);
material.emissiveTexture = new BABYLON.Texture('emissive.png', scene);
material.ambientTexture = new BABYLON.Texture('ambient.png', scene);
material.bumpTexture = new BABYLON.Texture('normal.png', scene);
material.opacityTexture = new BABYLON.Texture('opacity.png', scene);

// Properties
material.alpha = 0.8;
material.backFaceCulling = true;
material.wireframe = false;
material.specularPower = 64;

// Apply to mesh
mesh.material = material;
```

**PBR Material (Physically Based Rendering)**
```javascript
const pbr = new BABYLON.PBRMaterial('pbr', scene);

// Metallic workflow
pbr.albedoColor = new BABYLON.Color3(1, 1, 1);
pbr.albedoTexture = new BABYLON.Texture('albedo.png', scene);
pbr.metallic = 1.0;
pbr.roughness = 0.5;
pbr.metallicTexture = new BABYLON.Texture('metallic.png', scene);

// Or specular workflow
pbr.albedoTexture = new BABYLON.Texture('albedo.png', scene);
pbr.reflectivityTexture = new BABYLON.Texture('reflectivity.png', scene);

// Environment
pbr.environmentTexture = BABYLON.CubeTexture.CreateFromPrefilteredData('environment.dds', scene);

// Other maps
pbr.bumpTexture = new BABYLON.Texture('normal.png', scene);
pbr.ambientTexture = new BABYLON.Texture('ao.png', scene);
pbr.emissiveTexture = new BABYLON.Texture('emissive.png', scene);

mesh.material = pbr;
```

**Multi-Materials**
```javascript
const multiMat = new BABYLON.MultiMaterial('multiMat', scene);
multiMat.subMaterials.push(material1);
multiMat.subMaterials.push(material2);
multiMat.subMaterials.push(material3);

mesh.material = multiMat;
mesh.subMeshes = [];
mesh.subMeshes.push(new BABYLON.SubMesh(0, 0, verticesCount, 0, indicesCount1, mesh));
mesh.subMeshes.push(new BABYLON.SubMesh(1, 0, verticesCount, indicesCount1, indicesCount2, mesh));
```

### 6. Model Loading

**GLTF/GLB Import**
```javascript
// Append to scene
BABYLON.SceneLoader.Append('path/to/', 'model.gltf', scene, function(scene) {
  console.log('Model loaded');
});

// Import mesh
BABYLON.SceneLoader.ImportMesh('', 'path/to/', 'model.gltf', scene, function(meshes) {
  const mesh = meshes[0];
  mesh.position.y = 5;
});

// Async version
const result = await BABYLON.SceneLoader.ImportMeshAsync(
  null,  // all meshes
  'https://assets.babylonjs.com/meshes/',
  'village.glb',
  scene
);
console.log('Loaded meshes:', result.meshes);

// Load from binary
const result = await BABYLON.SceneLoader.AppendAsync(
  '',
  'data:' + arrayBuffer,
  scene
);
```

**Asset Manager (Batch Loading)**
```javascript
const assetsManager = new BABYLON.AssetsManager(scene);

// Add mesh task
const meshTask = assetsManager.addMeshTask('model', '', 'path/to/', 'model.gltf');
meshTask.onSuccess = function(task) {
  task.loadedMeshes[0].position = new BABYLON.Vector3(0, 0, 0);
};

// Add texture task
const textureTask = assetsManager.addTextureTask('texture', 'texture.png');
textureTask.onSuccess = function(task) {
  material.diffuseTexture = task.texture;
};

// Load all
assetsManager.onFinish = function(tasks) {
  console.log('All assets loaded');
  engine.runRenderLoop(() => scene.render());
};

assetsManager.load();
```

### 7. Physics Engine

**Havok Physics Setup**
```javascript
// Import Havok
import HavokPhysics from '@babylonjs/havok';

// Initialize
const havokInstance = await HavokPhysics();
const havokPlugin = new BABYLON.HavokPlugin(true, havokInstance);

// Enable physics
scene.enablePhysics(new BABYLON.Vector3(0, -9.8, 0), havokPlugin);

// Create physics aggregate for mesh
const sphereAggregate = new BABYLON.PhysicsAggregate(
  sphere,
  BABYLON.PhysicsShapeType.SPHERE,
  { mass: 1, restitution: 0.75 },
  scene
);

// Ground (static)
const groundAggregate = new BABYLON.PhysicsAggregate(
  ground,
  BABYLON.PhysicsShapeType.BOX,
  { mass: 0 }, // mass 0 = static
  scene
);
```

**Physics Shapes**
```javascript
// Available shapes
BABYLON.PhysicsShapeType.SPHERE
BABYLON.PhysicsShapeType.BOX
BABYLON.PhysicsShapeType.CAPSULE
BABYLON.PhysicsShapeType.CYLINDER
BABYLON.PhysicsShapeType.CONVEX_HULL
BABYLON.PhysicsShapeType.MESH
BABYLON.PhysicsShapeType.HEIGHTFIELD
```

**Physics Body Control**
```javascript
// Get body
const body = aggregate.body;

// Apply force
body.applyForce(
  new BABYLON.Vector3(0, 10, 0),    // force
  new BABYLON.Vector3(0, 0, 0)      // point of application
);

// Apply impulse
body.applyImpulse(
  new BABYLON.Vector3(0, 5, 0),
  new BABYLON.Vector3(0, 0, 0)
);

// Set velocity
body.setLinearVelocity(new BABYLON.Vector3(0, 5, 0));
body.setAngularVelocity(new BABYLON.Vector3(0, 1, 0));

// Properties
body.setMassProperties({ mass: 2 });
body.setCollisionCallbackEnabled(true);
```

### 8. Animations

**Direct Animation**
```javascript
// Animate property
BABYLON.Animation.CreateAndStartAnimation(
  'anim',
  mesh,
  'position.y',
  30,                    // FPS
  120,                   // total frames
  mesh.position.y,       // from
  10,                    // to
  BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
);
```

**Animation Class**
```javascript
const animation = new BABYLON.Animation(
  'myAnimation',
  'position.x',
  30,
  BABYLON.Animation.ANIMATIONTYPE_FLOAT,
  BABYLON.Animation.ANIMATIONLOOPMODE_CYCLE
);

// Keyframes
const keys = [
  { frame: 0, value: 0 },
  { frame: 30, value: 10 },
  { frame: 60, value: 0 }
];
animation.setKeys(keys);

// Attach to mesh
mesh.animations.push(animation);

// Start
scene.beginAnimation(mesh, 0, 60, true);
```

**Animation Groups**
```javascript
const animationGroup = new BABYLON.AnimationGroup('group', scene);
animationGroup.addTargetedAnimation(animation1, mesh1);
animationGroup.addTargetedAnimation(animation2, mesh2);

// Control
animationGroup.play();
animationGroup.pause();
animationGroup.stop();
animationGroup.speedRatio = 2.0;

// Events
animationGroup.onAnimationEndObservable.add(() => {
  console.log('Animation complete');
});
```

**Skeleton Animations (from imported models)**
```javascript
// Get skeleton from imported model
const skeleton = result.skeletons[0];

// Get animation ranges
const ranges = skeleton.getAnimationRanges();

// Play animation range
scene.beginAnimation(skeleton, 0, 100, true);

// Or use animation groups
result.animationGroups[0].play();
result.animationGroups[0].setWeightForAllAnimatables(0.5);
```

## Common Patterns

### Pattern 1: Scene Setup with Default Environment

```javascript
const createScene = function() {
  const scene = new BABYLON.Scene(engine);

  // Quick setup
  scene.createDefaultCameraOrLight(true, true, true);
  const env = scene.createDefaultEnvironment({
    createGround: true,
    createSkybox: true,
    skyboxSize: 150,
    groundSize: 50
  });

  // Your meshes
  const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {diameter: 2}, scene);
  sphere.position.y = 1;

  return scene;
};
```

### Pattern 2: Async Scene Loading

```javascript
const createScene = async function() {
  const scene = new BABYLON.Scene(engine);

  const camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 10, BABYLON.Vector3.Zero(), scene);
  camera.attachControl(canvas, true);

  const light = new BABYLON.HemisphericLight('light', new BABYLON.Vector3(0, 1, 0), scene);

  // Load model
  const result = await BABYLON.SceneLoader.ImportMeshAsync(
    null,
    'https://assets.babylonjs.com/meshes/',
    'village.glb',
    scene
  );

  // Setup physics
  const havokInstance = await HavokPhysics();
  const havokPlugin = new BABYLON.HavokPlugin(true, havokInstance);
  scene.enablePhysics(new BABYLON.Vector3(0, -9.8, 0), havokPlugin);

  return scene;
};

createScene().then(scene => {
  engine.runRenderLoop(() => scene.render());
});
```

### Pattern 3: Interactive Picking

```javascript
scene.onPointerDown = function(evt, pickResult) {
  if (pickResult.hit) {
    console.log('Picked mesh:', pickResult.pickedMesh.name);
    console.log('Pick point:', pickResult.pickedPoint);

    // Highlight picked mesh
    pickResult.pickedMesh.material.emissiveColor = new BABYLON.Color3(1, 0, 0);
  }
};

// Or use action manager
mesh.actionManager = new BABYLON.ActionManager(scene);
mesh.actionManager.registerAction(
  new BABYLON.ExecuteCodeAction(
    BABYLON.ActionManager.OnPickTrigger,
    function() {
      console.log('Mesh clicked');
    }
  )
);
```

### Pattern 4: Post-Processing Effects

```javascript
// Default pipeline
const pipeline = new BABYLON.DefaultRenderingPipeline('pipeline', true, scene, [camera]);
pipeline.samples = 4;
pipeline.fxaaEnabled = true;
pipeline.bloomEnabled = true;
pipeline.bloomThreshold = 0.8;
pipeline.bloomWeight = 0.5;
pipeline.bloomKernel = 64;

// Depth of field
pipeline.depthOfFieldEnabled = true;
pipeline.depthOfFieldBlurLevel = BABYLON.DepthOfFieldEffectBlurLevel.Low;
pipeline.depthOfField.focusDistance = 2000;
pipeline.depthOfField.focalLength = 50;

// Glow layer
const glowLayer = new BABYLON.GlowLayer('glow', scene);
glowLayer.intensity = 0.5;

// Highlight layer
const highlightLayer = new BABYLON.HighlightLayer('highlight', scene);
highlightLayer.addMesh(mesh, BABYLON.Color3.Green());
```

### Pattern 5: GUI (2D UI)

```javascript
import { AdvancedDynamicTexture, Button, TextBlock, Rectangle } from '@babylonjs/gui';

// Fullscreen UI
const advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI('UI');

// Button
const button = BABYLON.GUI.Button.CreateSimpleButton('button', 'Click Me');
button.width = '150px';
button.height = '40px';
button.color = 'white';
button.background = 'green';
button.onPointerUpObservable.add(() => {
  console.log('Button clicked');
});
advancedTexture.addControl(button);

// Text
const text = new BABYLON.GUI.TextBlock();
text.text = 'Hello World';
text.color = 'white';
text.fontSize = 24;
advancedTexture.addControl(text);

// 3D mesh UI
const plane = BABYLON.MeshBuilder.CreatePlane('plane', {size: 2}, scene);
const advancedTexture3D = BABYLON.GUI.AdvancedDynamicTexture.CreateForMesh(plane);
const button3D = BABYLON.GUI.Button.CreateSimpleButton('button3D', 'Click Me');
advancedTexture3D.addControl(button3D);
```

### Pattern 6: Shadow Mapping

```javascript
const light = new BABYLON.DirectionalLight('light', new BABYLON.Vector3(-1, -2, -1), scene);
light.position = new BABYLON.Vector3(20, 40, 20);

// Create shadow generator
const shadowGenerator = new BABYLON.ShadowGenerator(1024, light);
shadowGenerator.useExponentialShadowMap = true;
shadowGenerator.usePoissonSampling = true;

// Add shadow casters
shadowGenerator.addShadowCaster(sphere);
shadowGenerator.addShadowCaster(box);

// Enable shadow receiving
ground.receiveShadows = true;
```

### Pattern 7: Particle Systems

```javascript
const particleSystem = new BABYLON.ParticleSystem('particles', 2000, scene);
particleSystem.particleTexture = new BABYLON.Texture('particle.png', scene);

// Emitter
particleSystem.emitter = new BABYLON.Vector3(0, 5, 0);
particleSystem.minEmitBox = new BABYLON.Vector3(-1, 0, 0);
particleSystem.maxEmitBox = new BABYLON.Vector3(1, 0, 0);

// Colors
particleSystem.color1 = new BABYLON.Color4(0.7, 0.8, 1.0, 1.0);
particleSystem.color2 = new BABYLON.Color4(0.2, 0.5, 1.0, 1.0);
particleSystem.colorDead = new BABYLON.Color4(0, 0, 0.2, 0.0);

// Size
particleSystem.minSize = 0.1;
particleSystem.maxSize = 0.5;

// Life time
particleSystem.minLifeTime = 0.3;
particleSystem.maxLifeTime = 1.5;

// Emission rate
particleSystem.emitRate = 1500;

// Direction
particleSystem.direction1 = new BABYLON.Vector3(-1, 8, 1);
particleSystem.direction2 = new BABYLON.Vector3(1, 8, -1);

// Gravity
particleSystem.gravity = new BABYLON.Vector3(0, -9.81, 0);

// Start
particleSystem.start();
```

## Integration Patterns

### Pattern 1: React Integration

```jsx
import { useEffect, useRef } from 'react';
import * as BABYLON from '@babylonjs/core';

function BabylonScene() {
  const canvasRef = useRef(null);
  const engineRef = useRef(null);
  const sceneRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Initialize
    const engine = new BABYLON.Engine(canvasRef.current, true);
    engineRef.current = engine;

    const scene = new BABYLON.Scene(engine);
    sceneRef.current = scene;

    // Setup scene
    const camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 10, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvasRef.current, true);

    const light = new BABYLON.HemisphericLight('light', new BABYLON.Vector3(0, 1, 0), scene);

    const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {diameter: 2}, scene);

    // Render loop
    engine.runRenderLoop(() => {
      scene.render();
    });

    // Resize handler
    const handleResize = () => engine.resize();
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      scene.dispose();
      engine.dispose();
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{ width: '100%', height: '100vh' }}
    />
  );
}
```

### Pattern 2: WebXR (VR/AR)

```javascript
const createScene = async function() {
  const scene = new BABYLON.Scene(engine);

  const camera = new BABYLON.FreeCamera('camera', new BABYLON.Vector3(0, 5, -10), scene);
  camera.attachControl(canvas, true);

  const light = new BABYLON.HemisphericLight('light', new BABYLON.Vector3(0, 1, 0), scene);

  const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {diameter: 2}, scene);
  sphere.position.y = 1;

  const env = scene.createDefaultEnvironment();

  // Enable WebXR
  const xrHelper = await scene.createDefaultXRExperienceAsync({
    floorMeshes: [env.ground],
    disableTeleportation: false
  });

  // XR controller input
  xrHelper.input.onControllerAddedObservable.add((controller) => {
    controller.onMotionControllerInitObservable.add((motionController) => {
      const trigger = motionController.getMainComponent();
      trigger.onButtonStateChangedObservable.add(() => {
        if (trigger.pressed) {
          console.log('Trigger pressed');
        }
      });
    });
  });

  return scene;
};
```

### Pattern 3: Node Material (Visual Shader Editor)

```javascript
// Create from snippet
const nodeMaterial = await BABYLON.NodeMaterial.ParseFromSnippetAsync('#SNIPPET_ID', scene);

// Apply to mesh
nodeMaterial.build();
mesh.material = nodeMaterial;

// Or create programmatically
const nodeMaterial = new BABYLON.NodeMaterial('node', scene);

const positionInput = new BABYLON.InputBlock('position');
positionInput.setAsAttribute('position');

const worldPos = new BABYLON.TransformBlock('worldPos');
nodeMaterial.addOutputNode(worldPos);
```

## Performance Optimization

### 1. Mesh Optimization

```javascript
// Merge meshes with same material
const merged = BABYLON.Mesh.MergeMeshes(
  [mesh1, mesh2, mesh3],
  true,  // disposeSource
  true,  // allow32BitsIndices
  undefined,
  false, // multiMultiMaterials
  true   // preserveSerializationHelper
);

// Instances (for repeated meshes)
const instance1 = mesh.createInstance('instance1');
const instance2 = mesh.createInstance('instance2');
instance1.position.x = 5;
instance2.position.x = -5;

// Thin instances (even more efficient)
const buffer = new Float32Array(16 * count); // 16 floats per matrix
mesh.thinInstanceSetBuffer('matrix', buffer, 16);

// Freeze meshes (static meshes)
mesh.freezeWorldMatrix();

// Freeze materials
material.freeze();

// Simplify meshes (LOD)
const simplified = mesh.simplify(
  [
    { quality: 0.8, distance: 10 },
    { quality: 0.4, distance: 50 },
    { quality: 0.2, distance: 100 }
  ],
  true,  // parallelProcessing
  BABYLON.SimplificationType.QUADRATIC
);
```

### 2. Scene Optimization

```javascript
// Scene optimizer
const options = new BABYLON.SceneOptimizerOptions();
options.addOptimization(new BABYLON.HardwareScalingOptimization(0, 1));
options.addOptimization(new BABYLON.ShadowsOptimization(1));
options.addOptimization(new BABYLON.PostProcessesOptimization(2));
options.addOptimization(new BABYLON.LensFlaresOptimization(3));
options.addOptimization(new BABYLON.ParticlesOptimization(4));
options.addOptimization(new BABYLON.TextureOptimization(5, 512));
options.addOptimization(new BABYLON.RenderTargetsOptimization(6));
options.addOptimization(new BABYLON.MergeMeshesOptimization(7));

const optimizer = new BABYLON.SceneOptimizer(scene, options);
optimizer.start();

// Octree (spatial partitioning)
const octree = scene.createOrUpdateSelectionOctree();

// Frustum culling
scene.blockMaterialDirtyMechanism = true;

// Skip pointer move picking
scene.skipPointerMovePicking = true;

// Freeze active meshes
scene.freezeActiveMeshes();
```

### 3. Rendering Optimization

```javascript
// Hardware scaling
engine.setHardwareScalingLevel(0.5); // Render at half resolution

// Adaptive quality
scene.onBeforeRenderObservable.add(() => {
  const fps = engine.getFps();
  if (fps < 30) {
    // Reduce quality
    engine.setHardwareScalingLevel(2);
  } else if (fps > 55) {
    // Increase quality
    engine.setHardwareScalingLevel(1);
  }
});

// Incremental loading
scene.useDelayedTextureLoading = true;

// Culling strategy
mesh.cullingStrategy = BABYLON.AbstractMesh.CULLINGSTRATEGY_BOUNDINGSPHERE_ONLY;
```

### 4. Texture Optimization

```javascript
// Compressed textures
const texture = new BABYLON.Texture('texture.dds', scene);

// Mipmaps
texture.updateSamplingMode(BABYLON.Texture.TRILINEAR_SAMPLINGMODE);

// Anisotropic filtering
texture.anisotropicFilteringLevel = 4;

// KTX2 compression
const texture = new BABYLON.Texture('texture.ktx2', scene);
```

## Common Pitfalls

### Pitfall 1: Memory Leaks

**Problem**: Not disposing resources
```javascript
// ❌ Bad - memory leak
function createAndRemoveMesh() {
  const mesh = BABYLON.MeshBuilder.CreateBox('box', {}, scene);
  scene.removeMesh(mesh);
}
```

**Solution**: Properly dispose
```javascript
// ✅ Good
function createAndRemoveMesh() {
  const mesh = BABYLON.MeshBuilder.CreateBox('box', {}, scene);
  mesh.dispose();
}

// Dispose entire scene
scene.dispose();

// Dispose engine
engine.dispose();
```

### Pitfall 2: Performance Issues with Too Many Draw Calls

**Problem**: Each mesh = one draw call
```javascript
// ❌ Bad - 1000 draw calls
for (let i = 0; i < 1000; i++) {
  const box = BABYLON.MeshBuilder.CreateBox('box' + i, {}, scene);
  box.position.x = i;
}
```

**Solution**: Use instances or merge
```javascript
// ✅ Good - 1 draw call
const box = BABYLON.MeshBuilder.CreateBox('box', {}, scene);
for (let i = 0; i < 1000; i++) {
  const instance = box.createInstance('instance' + i);
  instance.position.x = i;
}
```

### Pitfall 3: Blocking the Main Thread

**Problem**: Heavy computations blocking render
```javascript
// ❌ Bad - blocks rendering
function createManyMeshes() {
  for (let i = 0; i < 10000; i++) {
    const mesh = BABYLON.MeshBuilder.CreateSphere('sphere' + i, {}, scene);
  }
}
```

**Solution**: Use async/incremental loading
```javascript
// ✅ Good - incremental
async function createManyMeshes() {
  for (let i = 0; i < 10000; i++) {
    const mesh = BABYLON.MeshBuilder.CreateSphere('sphere' + i, {}, scene);

    if (i % 100 === 0) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}
```

### Pitfall 4: Incorrect Camera Controls

**Problem**: Camera not responding
```javascript
// ❌ Bad - forgot attachControl
const camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 10, BABYLON.Vector3.Zero(), scene);
```

**Solution**: Always attach controls
```javascript
// ✅ Good
const camera = new BABYLON.ArcRotateCamera('camera', 0, 0, 10, BABYLON.Vector3.Zero(), scene);
camera.attachControl(canvas, true);
```

### Pitfall 5: Not Handling Async Operations

**Problem**: Using scene before it's ready
```javascript
// ❌ Bad
BABYLON.SceneLoader.ImportMesh('', 'path/', 'model.gltf', scene);
const mesh = scene.getMeshByName('meshName'); // null!
```

**Solution**: Use callbacks or async/await
```javascript
// ✅ Good
const result = await BABYLON.SceneLoader.ImportMeshAsync('', 'path/', 'model.gltf', scene);
const mesh = scene.getMeshByName('meshName');

// Or with callback
BABYLON.SceneLoader.ImportMesh('', 'path/', 'model.gltf', scene, function(meshes) {
  const mesh = meshes[0];
});
```

### Pitfall 6: Physics Not Working

**Problem**: Forgot to enable physics or create aggregates
```javascript
// ❌ Bad
const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {}, scene);
sphere.physicsImpostor = new BABYLON.PhysicsImpostor(sphere, BABYLON.PhysicsImpostor.SphereImpostor, {mass: 1}, scene);
// Error: Physics not enabled!
```

**Solution**: Enable physics first, use aggregates
```javascript
// ✅ Good
const havokInstance = await HavokPhysics();
const havokPlugin = new BABYLON.HavokPlugin(true, havokInstance);
scene.enablePhysics(new BABYLON.Vector3(0, -9.8, 0), havokPlugin);

const sphere = BABYLON.MeshBuilder.CreateSphere('sphere', {}, scene);
const aggregate = new BABYLON.PhysicsAggregate(
  sphere,
  BABYLON.PhysicsShapeType.SPHERE,
  {mass: 1},
  scene
);
```

## Advanced Topics

### 1. Custom Shaders

```javascript
BABYLON.Effect.ShadersStore['customVertexShader'] = `
  precision highp float;
  attribute vec3 position;
  attribute vec2 uv;
  uniform mat4 worldViewProjection;
  varying vec2 vUV;

  void main(void) {
    gl_Position = worldViewProjection * vec4(position, 1.0);
    vUV = uv;
  }
`;

BABYLON.Effect.ShadersStore['customFragmentShader'] = `
  precision highp float;
  varying vec2 vUV;
  uniform sampler2D textureSampler;

  void main(void) {
    gl_FragColor = texture2D(textureSampler, vUV);
  }
`;

const shaderMaterial = new BABYLON.ShaderMaterial('shader', scene, {
  vertex: 'custom',
  fragment: 'custom'
}, {
  attributes: ['position', 'uv'],
  uniforms: ['worldViewProjection']
});
```

### 2. Compute Shaders

```javascript
const computeShader = new BABYLON.ComputeShader('compute', engine, {
  computeSource: `
    #version 450
    layout (local_size_x = 8, local_size_y = 8, local_size_z = 1) in;
    layout(std430, binding = 0) buffer OutputBuffer { vec4 data[]; } outputBuffer;

    void main() {
      uint index = gl_GlobalInvocationID.x + gl_GlobalInvocationID.y * 8u;
      outputBuffer.data[index] = vec4(1.0, 0.0, 0.0, 1.0);
    }
  `
});
```

### 3. Procedural Textures

```javascript
const noiseTexture = new BABYLON.NoiseProceduralTexture('noise', 256, scene);
noiseTexture.octaves = 4;
noiseTexture.persistence = 0.8;
noiseTexture.animationSpeedFactor = 5;

material.emissiveTexture = noiseTexture;
```

## Debugging

```javascript
// Show inspector
scene.debugLayer.show();

// Show bounding boxes
scene.forceShowBoundingBoxes = true;

// Show wireframes
material.wireframe = true;

// Log FPS
setInterval(() => {
  console.log('FPS:', engine.getFps());
}, 1000);

// Instrumentation
const instrumentation = new BABYLON.SceneInstrumentation(scene);
instrumentation.captureFrameTime = true;
console.log('Frame time:', instrumentation.frameTimeCounter.average);
```

## Resources

- [Official Documentation](https://doc.babylonjs.com/)
- [Playground](https://playground.babylonjs.com/)
- [Forum](https://forum.babylonjs.com/)
- [Examples](https://doc.babylonjs.com/examples/)
- [NPM Package](https://www.npmjs.com/package/@babylonjs/core)

## Version Notes

This skill is based on Babylon.js 7.x. For latest features, consult the official documentation.
