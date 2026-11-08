# Babylon.js Real-World Examples

Comprehensive collection of production-ready Babylon.js patterns and implementations.

## Table of Contents

- [Model Loading & Optimization](#model-loading--optimization)
- [Advanced Materials](#advanced-materials)
- [Physics Simulations](#physics-simulations)
- [Particle Systems](#particle-systems)
- [Post-Processing Effects](#post-processing-effects)
- [GUI & User Interface](#gui--user-interface)
- [WebXR & VR](#webxr--vr)
- [Performance Optimization](#performance-optimization)
- [Camera Systems](#camera-systems)
- [Animation Patterns](#animation-patterns)

---

## Model Loading & Optimization

### GLTF Model Viewer with Progress

```javascript
import { SceneLoader } from '@babylonjs/core/Loading/sceneLoader.js';
import { Texture } from '@babylonjs/core/Materials/Textures/texture.js';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial.js';
import '@babylonjs/loaders/glTF';

async function createModelViewer(scene, modelUrl, fileName) {
  // Show loading progress
  let loadingScreen = document.getElementById('loading');

  BABYLON.SceneLoader.OnPluginActivatedObservable.addOnce((loader) => {
    loader.onProgress = (event) => {
      const progress = event.lengthComputable
        ? (event.loaded / event.total) * 100
        : 0;

      if (loadingScreen) {
        loadingScreen.textContent = `Loading: ${progress.toFixed(0)}%`;
      }
    };
  });

  // Load model
  const result = await SceneLoader.ImportMeshAsync(
    null,
    modelUrl,
    fileName,
    scene
  );

  if (loadingScreen) {
    loadingScreen.style.display = 'none';
  }

  // Center model
  const meshes = result.meshes;
  const boundingBox = meshes[0].getHierarchyBoundingVectors();
  const center = BABYLON.Vector3.Center(boundingBox.min, boundingBox.max);

  meshes.forEach(mesh => {
    mesh.position.subtractInPlace(center);
  });

  // Scale to fit
  const size = boundingBox.max.subtract(boundingBox.min);
  const maxDimension = Math.max(size.x, size.y, size.z);
  const scale = 5 / maxDimension;

  result.meshes[0].scaling.scaleInPlace(scale);

  // Setup environment
  const envTexture = BABYLON.CubeTexture.CreateFromPrefilteredData(
    'https://assets.babylonjs.com/environments/environmentSpecular.env',
    scene
  );
  scene.environmentTexture = envTexture;

  // Apply PBR to all meshes
  meshes.forEach(mesh => {
    if (mesh.material && mesh.material.albedoTexture) {
      // Already has material, enhance it
      mesh.material.environmentIntensity = 1.0;
    } else if (!mesh.material) {
      // No material, create default
      const pbr = new PBRMaterial('defaultPBR', scene);
      pbr.metallic = 0.0;
      pbr.roughness = 0.5;
      pbr.baseColor = new BABYLON.Color3(0.8, 0.8, 0.8);
      mesh.material = pbr;
    }
  });

  return result;
}
```

### Optimized LOD (Level of Detail)

```javascript
async function createLODMesh(scene, highResUrl, medResUrl, lowResUrl) {
  // Load all LOD levels
  const highRes = await SceneLoader.ImportMeshAsync(null, '', highResUrl, scene);
  const medRes = await SceneLoader.ImportMeshAsync(null, '', medResUrl, scene);
  const lowRes = await SceneLoader.ImportMeshAsync(null, '', lowResUrl, scene);

  const mainMesh = highRes.meshes[0];
  const medMesh = medRes.meshes[0];
  const lowMesh = lowRes.meshes[0];

  // Add LOD levels
  mainMesh.addLODLevel(15, medMesh);   // Switch at 15 units
  mainMesh.addLODLevel(30, lowMesh);   // Switch at 30 units
  mainMesh.addLODLevel(50, null);      // Don't render beyond 50 units

  return mainMesh;
}
```

### Mesh Simplification

```javascript
async function simplifyMesh(mesh, quality = 0.5) {
  const simplified = await mesh.simplify(
    [
      { quality: quality, distance: 10 },
      { quality: quality * 0.5, distance: 25 },
      { quality: quality * 0.25, distance: 50 }
    ],
    true,  // parallelProcessing
    BABYLON.SimplificationType.QUADRATIC
  );

  return simplified;
}
```

### Batch Model Loading

```javascript
async function batchLoadModels(scene, models) {
  const assetsManager = new BABYLON.AssetsManager(scene);

  const loadedMeshes = [];

  models.forEach((model, index) => {
    const task = assetsManager.addMeshTask(
      `model${index}`,
      '',
      model.path,
      model.filename
    );

    task.onSuccess = (task) => {
      task.loadedMeshes.forEach(mesh => {
        mesh.position = model.position || BABYLON.Vector3.Zero();
        mesh.scaling = model.scale || new BABYLON.Vector3(1, 1, 1);
      });

      loadedMeshes.push(...task.loadedMeshes);
    };

    task.onError = (task, message, exception) => {
      console.error(`Failed to load ${model.filename}:`, message);
    };
  });

  return new Promise((resolve) => {
    assetsManager.onFinish = (tasks) => {
      resolve(loadedMeshes);
    };

    assetsManager.load();
  });
}

// Usage
const models = [
  { path: '/models/', filename: 'car.glb', position: new BABYLON.Vector3(0, 0, 0) },
  { path: '/models/', filename: 'tree.glb', position: new BABYLON.Vector3(5, 0, 0), scale: new BABYLON.Vector3(2, 2, 2) },
  { path: '/models/', filename: 'building.glb', position: new BABYLON.Vector3(-5, 0, 0) }
];

const meshes = await batchLoadModels(scene, models);
```

---

## Advanced Materials

### PBR Material with All Maps

```javascript
function createAdvancedPBRMaterial(scene) {
  const pbr = new BABYLON.PBRMaterial('advancedPBR', scene);

  // Base color
  pbr.albedoTexture = new BABYLON.Texture('textures/albedo.png', scene);

  // Metallic and roughness (combined in one texture)
  pbr.metallicTexture = new BABYLON.Texture('textures/metallic_roughness.png', scene);
  pbr.useRoughnessFromMetallicTextureAlpha = false;
  pbr.useMetallnessFromMetallicTextureBlue = true;

  // Normal map
  pbr.bumpTexture = new BABYLON.Texture('textures/normal.png', scene);
  pbr.invertNormalMapX = false;
  pbr.invertNormalMapY = false;

  // Ambient occlusion
  pbr.ambientTexture = new BABYLON.Texture('textures/ao.png', scene);
  pbr.useAmbientOcclusionFromMetallicTextureRed = true;
  pbr.ambientTextureStrength = 1.0;

  // Emissive
  pbr.emissiveTexture = new BABYLON.Texture('textures/emissive.png', scene);
  pbr.emissiveColor = new BABYLON.Color3(1, 1, 1);
  pbr.emissiveIntensity = 1.0;

  // Environment
  pbr.environmentIntensity = 1.0;
  pbr.reflectionTexture = scene.environmentTexture;

  // Advanced settings
  pbr.directIntensity = 1.0;
  pbr.specularIntensity = 1.0;
  pbr.usePhysicalLightFalloff = true;
  pbr.useRadianceOverAlpha = true;

  return pbr;
}
```

### Glass Material

```javascript
function createGlassMaterial(scene) {
  const glass = new BABYLON.PBRMaterial('glass', scene);

  glass.metallic = 0.0;
  glass.roughness = 0.0;
  glass.alpha = 0.3;
  glass.alphaCutOff = 0.0;

  glass.indexOfRefraction = 1.52; // Glass IOR

  glass.reflectionTexture = scene.environmentTexture;
  glass.refractionTexture = scene.environmentTexture;
  glass.refractionTexture.refractionDepth = 0.8;

  glass.linkRefractionWithTransparency = true;

  glass.baseColor = new BABYLON.Color3(0.95, 0.95, 1.0);

  glass.environmentIntensity = 1.0;

  return glass;
}
```

### Water Material

```javascript
import { WaterMaterial } from '@babylonjs/materials/water/waterMaterial.js';

function createWaterMaterial(scene) {
  const water = new WaterMaterial('water', scene, new BABYLON.Vector2(512, 512));

  water.bumpTexture = new BABYLON.Texture('textures/waterbump.png', scene);
  water.windForce = -5;
  water.waveHeight = 0.3;
  water.bumpHeight = 0.1;
  water.windDirection = new BABYLON.Vector2(1, 1);

  water.waterColor = new BABYLON.Color3(0.1, 0.3, 0.5);
  water.colorBlendFactor = 0.3;

  water.waveLength = 0.1;

  // Add meshes to reflect/refract
  water.addToRenderList(skybox);
  water.addToRenderList(terrain);
  water.addToRenderList(buildings);

  return water;
}
```

### Node Material (Visual Shader)

```javascript
async function createNodeMaterial(scene) {
  // Load from snippet
  const nodeMaterial = await BABYLON.NodeMaterial.ParseFromSnippetAsync(
    '#SNIPPET_ID',
    scene
  );

  // Or create programmatically
  const nodeMaterial2 = new BABYLON.NodeMaterial('node', scene);

  // Input blocks
  const position = new BABYLON.InputBlock('position');
  position.setAsAttribute('position');

  const worldPos = new BABYLON.TransformBlock('worldPos');
  const worldViewProjection = new BABYLON.InputBlock('worldViewProjection');
  worldViewProjection.setAsSystemValue(BABYLON.NodeMaterialSystemValues.WorldViewProjection);

  const worldPosMult = new BABYLON.MultiplyBlock('worldPosMult');
  worldPosMult.left.connectTo(worldViewProjection.output);
  worldPosMult.right.connectTo(worldPos.output);

  // Fragment output
  const fragmentOutput = new BABYLON.FragmentOutputBlock('fragmentOutput');
  const color = new BABYLON.ColorBlock('color');
  color.value = new BABYLON.Color3(1, 0, 0);

  fragmentOutput.rgb.connectTo(color.output);

  nodeMaterial2.addOutputNode(fragmentOutput);

  nodeMaterial2.build();

  return nodeMaterial2;
}
```

### Dynamic Material Switching

```javascript
class MaterialSwitcher {
  constructor(mesh, materials) {
    this.mesh = mesh;
    this.materials = materials;
    this.currentIndex = 0;
  }

  switchMaterial() {
    this.currentIndex = (this.currentIndex + 1) % this.materials.length;
    this.mesh.material = this.materials[this.currentIndex];
  }

  setMaterial(index) {
    if (index >= 0 && index < this.materials.length) {
      this.currentIndex = index;
      this.mesh.material = this.materials[index];
    }
  }

  getCurrentMaterial() {
    return this.materials[this.currentIndex];
  }
}

// Usage
const materials = [
  createPBRMaterial(scene),
  createGlassMaterial(scene),
  createMetallicMaterial(scene)
];

const switcher = new MaterialSwitcher(mesh, materials);

// Switch on click
scene.onPointerDown = () => {
  switcher.switchMaterial();
};
```

---

## Physics Simulations

### Ragdoll Physics

```javascript
async function createRagdoll(scene, mesh) {
  const havokInstance = await HavokPhysics();
  const havokPlugin = new BABYLON.HavokPlugin(true, havokInstance);
  scene.enablePhysics(new BABYLON.Vector3(0, -9.8, 0), havokPlugin);

  // Create physics bodies for each bone
  const skeleton = mesh.skeleton;

  const bonePhysics = [];

  skeleton.bones.forEach((bone, index) => {
    const boneMatrix = bone.getTransformNode();

    if (boneMatrix) {
      // Create capsule for bone
      const capsule = BABYLON.MeshBuilder.CreateCapsule(
        `bone_${index}`,
        {
          radius: 0.05,
          height: 0.3
        },
        scene
      );

      capsule.position = boneMatrix.position.clone();
      capsule.rotation = boneMatrix.rotation.clone();

      // Add physics
      const aggregate = new BABYLON.PhysicsAggregate(
        capsule,
        BABYLON.PhysicsShapeType.CAPSULE,
        { mass: 0.5, friction: 0.5 },
        scene
      );

      bonePhysics.push({ bone, capsule, aggregate });
    }
  });

  // Add constraints between bones
  for (let i = 0; i < bonePhysics.length - 1; i++) {
    const current = bonePhysics[i];
    const next = bonePhysics[i + 1];

    // Create joint
    const constraint = new BABYLON.PhysicsConstraint(
      BABYLON.PhysicsConstraintType.HINGE,
      {
        pivotA: new BABYLON.Vector3(0, 0.15, 0),
        pivotB: new BABYLON.Vector3(0, -0.15, 0),
        axisA: new BABYLON.Vector3(1, 0, 0),
        axisB: new BABYLON.Vector3(1, 0, 0)
      },
      [
        { body: current.aggregate.body },
        { body: next.aggregate.body }
      ],
      scene
    );
  }

  return bonePhysics;
}
```

### Cloth Simulation

```javascript
function createCloth(scene, width = 10, height = 10, segments = 20) {
  const cloth = BABYLON.MeshBuilder.CreateGround(
    'cloth',
    { width, height, subdivisions: segments },
    scene
  );

  // Make updatable
  cloth.convertToFlatShadedMesh();

  const positions = cloth.getVerticesData(BABYLON.VertexBuffer.PositionKind);
  const indices = cloth.getIndices();

  // Create particles for each vertex
  const particles = [];
  for (let i = 0; i < positions.length; i += 3) {
    particles.push({
      position: new BABYLON.Vector3(positions[i], positions[i + 1], positions[i + 2]),
      previous: new BABYLON.Vector3(positions[i], positions[i + 1], positions[i + 2]),
      pinned: positions[i + 1] >= height / 2 - 0.1 // Pin top row
    });
  }

  // Update function
  const gravity = new BABYLON.Vector3(0, -9.8, 0);
  const damping = 0.99;
  const timestep = 1 / 60;

  scene.onBeforeRenderObservable.add(() => {
    // Verlet integration
    particles.forEach(particle => {
      if (particle.pinned) return;

      const velocity = particle.position.subtract(particle.previous);
      particle.previous.copyFrom(particle.position);

      const acceleration = gravity.scale(timestep * timestep);
      particle.position.addInPlace(velocity.scale(damping)).addInPlace(acceleration);
    });

    // Constrain distances
    for (let iteration = 0; iteration < 5; iteration++) {
      for (let i = 0; i < indices.length; i += 3) {
        const p1 = particles[indices[i]];
        const p2 = particles[indices[i + 1]];

        if (p1.pinned && p2.pinned) continue;

        const diff = p1.position.subtract(p2.position);
        const distance = diff.length();
        const restDistance = width / segments;

        const correction = diff.scale((distance - restDistance) / distance * 0.5);

        if (!p1.pinned) p1.position.subtractInPlace(correction);
        if (!p2.pinned) p2.position.addInPlace(correction);
      }
    }

    // Update mesh
    const newPositions = [];
    particles.forEach(p => {
      newPositions.push(p.position.x, p.position.y, p.position.z);
    });

    cloth.updateVerticesData(BABYLON.VertexBuffer.PositionKind, newPositions);
    cloth.refreshBoundingInfo();
  });

  return cloth;
}
```

### Vehicle Physics

```javascript
class Vehicle {
  constructor(scene, position) {
    this.scene = scene;

    // Create chassis
    this.chassis = BABYLON.MeshBuilder.CreateBox(
      'chassis',
      { width: 2, height: 0.5, depth: 4 },
      scene
    );
    this.chassis.position = position;

    const chassisAggregate = new BABYLON.PhysicsAggregate(
      this.chassis,
      BABYLON.PhysicsShapeType.BOX,
      { mass: 1000, friction: 0.5 },
      scene
    );

    this.body = chassisAggregate.body;

    // Create wheels
    this.wheels = [];
    const wheelPositions = [
      new BABYLON.Vector3(-0.8, -0.5, 1.5),   // Front left
      new BABYLON.Vector3(0.8, -0.5, 1.5),    // Front right
      new BABYLON.Vector3(-0.8, -0.5, -1.5),  // Rear left
      new BABYLON.Vector3(0.8, -0.5, -1.5)    // Rear right
    ];

    wheelPositions.forEach((pos, index) => {
      const wheel = BABYLON.MeshBuilder.CreateCylinder(
        `wheel${index}`,
        { diameter: 0.8, height: 0.3, tessellation: 16 },
        scene
      );
      wheel.rotation.z = Math.PI / 2;
      wheel.parent = this.chassis;
      wheel.position = pos;

      this.wheels.push(wheel);
    });

    // Controls
    this.throttle = 0;
    this.steering = 0;
    this.maxSpeed = 50;
    this.acceleration = 10;
    this.turnSpeed = 2;

    this.setupControls();
  }

  setupControls() {
    const keys = {};

    window.addEventListener('keydown', (e) => {
      keys[e.code] = true;
    });

    window.addEventListener('keyup', (e) => {
      keys[e.code] = false;
    });

    this.scene.onBeforeRenderObservable.add(() => {
      // Throttle
      if (keys['KeyW']) {
        this.throttle = Math.min(this.throttle + 0.1, 1);
      } else if (keys['KeyS']) {
        this.throttle = Math.max(this.throttle - 0.1, -0.5);
      } else {
        this.throttle *= 0.95; // Decay
      }

      // Steering
      if (keys['KeyA']) {
        this.steering = Math.max(this.steering - 0.1, -1);
      } else if (keys['KeyD']) {
        this.steering = Math.min(this.steering + 0.1, 1);
      } else {
        this.steering *= 0.9; // Center
      }

      // Apply forces
      const forward = this.chassis.forward;
      const force = forward.scale(this.throttle * this.acceleration * 1000);

      this.body.applyForce(
        force,
        this.chassis.position
      );

      // Apply turning torque
      const torque = new BABYLON.Vector3(0, this.steering * this.turnSpeed * 100, 0);
      this.body.setAngularVelocity(torque);

      // Rotate wheels
      this.wheels.forEach((wheel, index) => {
        wheel.rotation.x += this.throttle * 0.2;

        // Steer front wheels
        if (index < 2) {
          wheel.rotation.y = this.steering * 0.5;
        }
      });
    });
  }
}

// Usage
const vehicle = new Vehicle(scene, new BABYLON.Vector3(0, 5, 0));
```

---

## Particle Systems

### Fire Effect

```javascript
function createFireEffect(scene, position) {
  const fire = new BABYLON.ParticleSystem('fire', 2000, scene);

  fire.particleTexture = new BABYLON.Texture(
    'https://assets.babylonjs.com/textures/flare.png',
    scene
  );

  fire.emitter = position;
  fire.minEmitBox = new BABYLON.Vector3(-0.5, 0, -0.5);
  fire.maxEmitBox = new BABYLON.Vector3(0.5, 0, 0.5);

  // Colors
  fire.color1 = new BABYLON.Color4(1, 0.5, 0, 1.0);
  fire.color2 = new BABYLON.Color4(1, 0.2, 0, 1.0);
  fire.colorDead = new BABYLON.Color4(0, 0, 0, 0.0);

  // Size
  fire.minSize = 0.3;
  fire.maxSize = 1.0;

  // Life time
  fire.minLifeTime = 0.2;
  fire.maxLifeTime = 0.4;

  // Emission
  fire.emitRate = 600;

  // Blend mode
  fire.blendMode = BABYLON.ParticleSystem.BLENDMODE_ONEONE;

  // Direction
  fire.direction1 = new BABYLON.Vector3(-0.5, 4, -0.5);
  fire.direction2 = new BABYLON.Vector3(0.5, 8, 0.5);

  // Angular speed
  fire.minAngularSpeed = 0;
  fire.maxAngularSpeed = Math.PI;

  // Speed
  fire.minEmitPower = 1;
  fire.maxEmitPower = 3;
  fire.updateSpeed = 0.01;

  // Gravity
  fire.gravity = new BABYLON.Vector3(0, 0, 0);

  fire.start();

  return fire;
}
```

### Smoke Effect

```javascript
function createSmokeEffect(scene, position) {
  const smoke = new BABYLON.ParticleSystem('smoke', 1000, scene);

  smoke.particleTexture = new BABYLON.Texture(
    'https://assets.babylonjs.com/textures/cloud.png',
    scene
  );

  smoke.emitter = position;
  smoke.minEmitBox = new BABYLON.Vector3(-0.3, 0, -0.3);
  smoke.maxEmitBox = new BABYLON.Vector3(0.3, 0, 0.3);

  // Colors - gray smoke
  smoke.color1 = new BABYLON.Color4(0.3, 0.3, 0.3, 1.0);
  smoke.color2 = new BABYLON.Color4(0.6, 0.6, 0.6, 1.0);
  smoke.colorDead = new BABYLON.Color4(0, 0, 0, 0.0);

  // Size - grows over time
  smoke.minSize = 0.5;
  smoke.maxSize = 1.5;
  smoke.minScaleX = 0.5;
  smoke.maxScaleX = 2.0;
  smoke.minScaleY = 0.5;
  smoke.maxScaleY = 2.0;

  // Life time
  smoke.minLifeTime = 2.0;
  smoke.maxLifeTime = 4.0;

  // Emission
  smoke.emitRate = 200;

  // Blend mode - additive for glow
  smoke.blendMode = BABYLON.ParticleSystem.BLENDMODE_STANDARD;

  // Direction - upwards
  smoke.direction1 = new BABYLON.Vector3(-1, 3, -1);
  smoke.direction2 = new BABYLON.Vector3(1, 5, 1);

  // Speed
  smoke.minEmitPower = 0.5;
  smoke.maxEmitPower = 1.5;

  // Gravity - slight upward float
  smoke.gravity = new BABYLON.Vector3(0, -0.5, 0);

  smoke.start();

  return smoke;
}
```

### GPU Particle System (Performance)

```javascript
function createGPUParticles(scene, position) {
  const gpu = new BABYLON.GPUParticleSystem('gpu', { capacity: 50000 }, scene);

  gpu.particleTexture = new BABYLON.Texture(
    'https://assets.babylonjs.com/textures/flare.png',
    scene
  );

  gpu.emitter = position;
  gpu.minEmitBox = new BABYLON.Vector3(-2, 0, -2);
  gpu.maxEmitBox = new BABYLON.Vector3(2, 0, 2);

  // Colors - rainbow
  gpu.addColorGradient(0, new BABYLON.Color4(1, 0, 0, 1));
  gpu.addColorGradient(0.3, new BABYLON.Color4(1, 1, 0, 1));
  gpu.addColorGradient(0.6, new BABYLON.Color4(0, 1, 0, 1));
  gpu.addColorGradient(1.0, new BABYLON.Color4(0, 0, 1, 0));

  // Size over lifetime
  gpu.addSizeGradient(0, 0.5);
  gpu.addSizeGradient(0.5, 1.0);
  gpu.addSizeGradient(1.0, 0.1);

  // Life time
  gpu.minLifeTime = 1.0;
  gpu.maxLifeTime = 2.0;

  // Emission
  gpu.emitRate = 10000;

  // Direction
  gpu.direction1 = new BABYLON.Vector3(-1, 1, -1);
  gpu.direction2 = new BABYLON.Vector3(1, 3, 1);

  // Speed
  gpu.minEmitPower = 2;
  gpu.maxEmitPower = 4;

  // Gravity
  gpu.gravity = new BABYLON.Vector3(0, -9.8, 0);

  gpu.start();

  return gpu;
}
```

---

## Post-Processing Effects

### Bloom + DOF + Color Grading

```javascript
function createCinematicPipeline(scene, camera) {
  const pipeline = new BABYLON.DefaultRenderingPipeline(
    'cinematic',
    true, // HDR
    scene,
    [camera]
  );

  // Enable features
  pipeline.samples = 4; // MSAA

  // FXAA anti-aliasing
  pipeline.fxaaEnabled = true;

  // Bloom
  pipeline.bloomEnabled = true;
  pipeline.bloomThreshold = 0.8;
  pipeline.bloomWeight = 0.5;
  pipeline.bloomKernel = 64;
  pipeline.bloomScale = 0.5;

  // Depth of field
  pipeline.depthOfFieldEnabled = true;
  pipeline.depthOfFieldBlurLevel = BABYLON.DepthOfFieldEffectBlurLevel.Medium;
  pipeline.depthOfField.focusDistance = 5000;
  pipeline.depthOfField.focalLength = 100;
  pipeline.depthOfField.fStop = 2.0;

  // Image processing
  pipeline.imageProcessingEnabled = true;

  // Tone mapping
  pipeline.imageProcessing.toneMappingEnabled = true;
  pipeline.imageProcessing.toneMappingType = BABYLON.ImageProcessingConfiguration.TONEMAPPING_ACES;

  // Color grading
  pipeline.imageProcessing.contrast = 1.2;
  pipeline.imageProcessing.exposure = 1.0;

  // Vignette
  pipeline.imageProcessing.vignetteEnabled = true;
  pipeline.imageProcessing.vignetteWeight = 2.0;
  pipeline.imageProcessing.vignetteStretch = 0.5;
  pipeline.imageProcessing.vignetteCameraFov = 0.8;
  pipeline.imageProcessing.vignetteColor = new BABYLON.Color4(0, 0, 0, 0);

  // Chromatic aberration
  pipeline.chromaticAberrationEnabled = true;
  pipeline.chromaticAberration.aberrationAmount = 30;

  // Grain
  pipeline.grainEnabled = true;
  pipeline.grain.intensity = 10;
  pipeline.grain.animated = true;

  return pipeline;
}
```

### Outline/Glow Effect

```javascript
function createOutlineEffect(scene, meshes) {
  const highlightLayer = new BABYLON.HighlightLayer('highlight', scene);

  meshes.forEach(mesh => {
    highlightLayer.addMesh(mesh, BABYLON.Color3.Green());
  });

  // Glow layer for emissive
  const glowLayer = new BABYLON.GlowLayer('glow', scene);
  glowLayer.intensity = 0.5;

  return { highlightLayer, glowLayer };
}
```

### Custom Post-Process

```javascript
function createCustomPostProcess(camera) {
  const postProcess = new BABYLON.PostProcess(
    'customPP',
    './shaders/custom', // Path to shader files
    ['time'], // Uniforms
    ['textureSampler'], // Samplers
    1.0, // Sampling ratio
    camera
  );

  postProcess.onApply = (effect) => {
    effect.setFloat('time', performance.now() / 1000);
  };

  return postProcess;
}

// Custom shader (shaders/custom.fragment.fx)
// precision highp float;
// uniform sampler2D textureSampler;
// uniform float time;
// varying vec2 vUV;
//
// void main(void) {
//   vec2 uv = vUV;
//   uv.x += sin(uv.y * 10.0 + time) * 0.01;
//   gl_FragColor = texture2D(textureSampler, uv);
// }
```

---

## GUI & User Interface

### 3D Menu System

```javascript
import { AdvancedDynamicTexture } from '@babylonjs/gui/2D/advancedDynamicTexture.js';
import { StackPanel } from '@babylonjs/gui/2D/controls/stackPanel.js';
import { Button } from '@babylonjs/gui/2D/controls/button.js';
import { TextBlock } from '@babylonjs/gui/2D/controls/textBlock.js';

function create3DMenu(scene) {
  // Create plane for menu
  const plane = BABYLON.MeshBuilder.CreatePlane('menuPlane', { size: 4 }, scene);
  plane.position = new BABYLON.Vector3(0, 2, 0);

  // Create texture for plane
  const advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateForMesh(
    plane,
    1024,
    1024
  );

  // Create panel
  const panel = new BABYLON.GUI.StackPanel();
  panel.width = '600px';
  panel.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_CENTER;
  panel.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_CENTER;
  advancedTexture.addControl(panel);

  // Title
  const title = new BABYLON.GUI.TextBlock();
  title.text = 'Main Menu';
  title.height = '80px';
  title.color = 'white';
  title.fontSize = 48;
  title.fontWeight = 'bold';
  panel.addControl(title);

  // Buttons
  const buttonData = [
    { text: 'Start Game', action: () => console.log('Start') },
    { text: 'Options', action: () => console.log('Options') },
    { text: 'Exit', action: () => console.log('Exit') }
  ];

  buttonData.forEach(data => {
    const button = BABYLON.GUI.Button.CreateSimpleButton('button', data.text);
    button.width = '400px';
    button.height = '60px';
    button.color = 'white';
    button.background = '#4fc3f7';
    button.cornerRadius = 8;
    button.thickness = 0;
    button.fontSize = 24;
    button.paddingTop = '10px';
    button.paddingBottom = '10px';

    button.onPointerEnterObservable.add(() => {
      button.background = '#29b6f6';
    });

    button.onPointerOutObservable.add(() => {
      button.background = '#4fc3f7';
    });

    button.onPointerUpObservable.add(data.action);

    panel.addControl(button);
  });

  return { plane, advancedTexture };
}
```

### HUD with Stats

```javascript
function createHUD(scene, engine) {
  const advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI('HUD');

  // FPS counter
  const fpsText = new BABYLON.GUI.TextBlock();
  fpsText.text = 'FPS: 60';
  fpsText.color = 'white';
  fpsText.fontSize = 18;
  fpsText.textHorizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_RIGHT;
  fpsText.textVerticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
  fpsText.paddingTop = '10px';
  fpsText.paddingRight = '10px';
  advancedTexture.addControl(fpsText);

  // Health bar
  const healthContainer = new BABYLON.GUI.Rectangle();
  healthContainer.width = '200px';
  healthContainer.height = '30px';
  healthContainer.cornerRadius = 4;
  healthContainer.color = 'white';
  healthContainer.thickness = 2;
  healthContainer.background = 'rgba(0, 0, 0, 0.5)';
  healthContainer.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
  healthContainer.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
  healthContainer.left = 10;
  healthContainer.top = 10;
  advancedTexture.addControl(healthContainer);

  const healthBar = new BABYLON.GUI.Rectangle();
  healthBar.width = '100%';
  healthBar.height = '100%';
  healthBar.background = '#4caf50';
  healthBar.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;
  healthContainer.addControl(healthBar);

  // Update FPS
  scene.onBeforeRenderObservable.add(() => {
    fpsText.text = `FPS: ${engine.getFps().toFixed(0)}`;
  });

  return { advancedTexture, healthBar };
}
```

---

## WebXR & VR

### VR Scene Setup

```javascript
async function createVRScene(scene) {
  // Create environment
  const env = scene.createDefaultEnvironment({
    createGround: true,
    createSkybox: true
  });

  // Enable WebXR
  const xrHelper = await scene.createDefaultXRExperienceAsync({
    floorMeshes: [env.ground],
    disableTeleportation: false
  });

  // Controller input
  xrHelper.input.onControllerAddedObservable.add((controller) => {
    controller.onMotionControllerInitObservable.add((motionController) => {
      // Get components
      const trigger = motionController.getMainComponent();
      const squeeze = motionController.getComponent('squeeze');
      const thumbstick = motionController.getComponent('thumbstick');

      // Trigger press
      trigger.onButtonStateChangedObservable.add((component) => {
        if (component.pressed) {
          console.log('Trigger pressed');
          // Perform raycast
          const ray = controller.getWorldPointerRayToRef(new BABYLON.Ray());
          const hit = scene.pickWithRay(ray);

          if (hit.pickedMesh) {
            console.log('Hit:', hit.pickedMesh.name);
          }
        }
      });

      // Squeeze (grip) press
      if (squeeze) {
        squeeze.onButtonStateChangedObservable.add((component) => {
          if (component.pressed) {
            console.log('Grip pressed');
          }
        });
      }

      // Thumbstick
      if (thumbstick) {
        thumbstick.onAxisValueChangedObservable.add((axes) => {
          console.log('Thumbstick:', axes.x, axes.y);
        });
      }
    });
  });

  return xrHelper;
}
```

### VR Teleportation

```javascript
function setupVRTeleportation(xrHelper, validTargets) {
  xrHelper.teleportation.addFloorMesh(validTargets[0]);

  // Custom teleportation behavior
  xrHelper.teleportation.onTargetMeshSelectedObservable.add((mesh) => {
    console.log('Teleporting to:', mesh.name);
  });

  // Change teleportation arc color
  xrHelper.teleportation.defaultTargetMeshOptions.teleportationFillColor = '#4fc3f7';
  xrHelper.teleportation.defaultTargetMeshOptions.teleportationBorderColor = '#29b6f6';
}
```

---

## Performance Optimization

### Octree Scene Optimization

```javascript
function optimizeWithOctree(scene) {
  const octree = scene.createOrUpdateSelectionOctree(32, 2);

  // Enable octree for all meshes
  scene.meshes.forEach(mesh => {
    mesh.alwaysSelectAsActiveMesh = false;
  });

  return octree;
}
```

### Mesh Instancing

```javascript
function createInstancedMeshes(scene, template, count) {
  const instances = [];

  for (let i = 0; i < count; i++) {
    const instance = template.createInstance(`instance${i}`);
    instance.position = new BABYLON.Vector3(
      Math.random() * 50 - 25,
      0,
      Math.random() * 50 - 25
    );
    instance.rotation.y = Math.random() * Math.PI * 2;

    instances.push(instance);
  }

  return instances;
}
```

### Thin Instances (Best Performance)

```javascript
function createThinInstances(mesh, count) {
  const matrices = [];

  for (let i = 0; i < count; i++) {
    const matrix = BABYLON.Matrix.Translation(
      Math.random() * 50 - 25,
      0,
      Math.random() * 50 - 25
    );

    matrices.push(matrix);
  }

  const buffer = new Float32Array(matrices.length * 16);

  matrices.forEach((matrix, index) => {
    matrix.copyToArray(buffer, index * 16);
  });

  mesh.thinInstanceSetBuffer('matrix', buffer, 16);
}
```

This comprehensive examples documentation provides production-ready patterns for advanced Babylon.js development. Each example is complete and can be integrated into real projects.
