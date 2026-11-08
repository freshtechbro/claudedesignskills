# Babylon.js API Reference

Complete API reference for Babylon.js 7.x covering core classes, methods, and properties.

## Table of Contents

- [Engine](#engine)
- [Scene](#scene)
- [Cameras](#cameras)
- [Lights](#lights)
- [Meshes](#meshes)
- [Materials](#materials)
- [Textures](#textures)
- [Physics](#physics)
- [Animations](#animations)
- [GUI](#gui)
- [Post-Processing](#post-processing)

---

## Engine

### BABYLON.Engine

Main rendering engine that manages the WebGL context and rendering loop.

#### Constructor

```typescript
new Engine(
  canvasOrContext: HTMLCanvasElement | WebGLRenderingContext,
  antialias?: boolean,
  options?: EngineOptions,
  adaptToDeviceRatio?: boolean
): Engine
```

**Parameters:**
- `canvasOrContext`: HTML canvas element or WebGL context
- `antialias`: Enable anti-aliasing (default: false)
- `options`: Engine configuration options
- `adaptToDeviceRatio`: Adapt to device pixel ratio (default: false)

**EngineOptions:**
```typescript
interface EngineOptions {
  preserveDrawingBuffer?: boolean;     // Keep buffer for screenshots
  stencil?: boolean;                   // Enable stencil buffer
  disableWebGL2Support?: boolean;      // Force WebGL 1
  powerPreference?: string;            // "high-performance" | "low-power"
  failIfMajorPerformanceCaveat?: boolean;
  deterministicLockstep?: boolean;     // Fixed timestep
  lockstepMaxSteps?: number;           // Max steps per frame
}
```

#### Properties

```typescript
engine.isFullscreen: boolean                    // Current fullscreen state
engine.isPointerLock: boolean                   // Pointer lock state
engine.scenes: Scene[]                          // All scenes
engine.renderEvenInBackground: boolean          // Continue rendering when tab hidden
engine.enableOfflineSupport: boolean            // Enable IndexedDB caching
engine.doNotHandleContextLost: boolean          // Disable context lost recovery
```

#### Methods

**Rendering**
```typescript
engine.runRenderLoop(renderFunction: () => void): void
engine.stopRenderLoop(renderFunction?: () => void): void
engine.resize(forceResize?: boolean): void
engine.setHardwareScalingLevel(level: number): void    // 1 = native, 2 = half resolution
engine.getHardwareScalingLevel(): number
engine.setSize(width: number, height: number, forceSetSize?: boolean): void
```

**Frame Info**
```typescript
engine.getFps(): number
engine.getDeltaTime(): number                   // Milliseconds since last frame
engine.getTimeStep(): number                    // Time step in ms
```

**State Management**
```typescript
engine.wipeCaches(bruteForce?: boolean): void
engine.dispose(): void
engine.clear(color: Color4, backBuffer: boolean, depth: boolean, stencil?: boolean): void
```

**Screenshots**
```typescript
engine.createScreenshot(
  camera: Camera,
  size: number | { width: number, height: number },
  successCallback: (data: string) => void,
  mimeType?: string,
  forceDownload?: boolean
): void

engine.createScreenshotUsingRenderTarget(
  camera: Camera,
  size: number | { width: number, height: number },
  successCallback: (data: string) => void,
  mimeType?: string,
  samples?: number,
  antialiasing?: boolean,
  fileName?: string
): void
```

---

## Scene

### BABYLON.Scene

Container for all 3D objects, cameras, lights, and materials.

#### Constructor

```typescript
new Scene(
  engine: Engine,
  options?: SceneOptions
): Scene
```

**SceneOptions:**
```typescript
interface SceneOptions {
  useGeometryUniqueIdsMap?: boolean;      // Faster geometry operations
  useMaterialMeshMap?: boolean;           // Faster material operations
  useClonedMeshMap?: boolean;             // Faster clone operations
  virtual?: boolean;                      // Don't render automatically
}
```

#### Properties

**Core**
```typescript
scene.activeCamera: Camera | null               // Current rendering camera
scene.activeCameras: Camera[]                   // For multi-viewport
scene.meshes: AbstractMesh[]                    // All meshes
scene.lights: Light[]                           // All lights
scene.cameras: Camera[]                         // All cameras
scene.materials: Material[]                     // All materials
scene.textures: BaseTexture[]                   // All textures
scene.transformNodes: TransformNode[]           // Transform-only nodes
```

**Rendering**
```typescript
scene.autoClear: boolean                        // Auto-clear buffers
scene.autoClearDepthAndStencil: boolean         // Auto-clear depth/stencil
scene.clearColor: Color4                        // Background color
scene.ambientColor: Color3                      // Ambient lighting color
scene.fogEnabled: boolean                       // Enable fog
scene.fogMode: number                           // Scene.FOGMODE_*
scene.fogDensity: number                        // Fog density
scene.fogStart: number                          // Linear fog start
scene.fogEnd: number                            // Linear fog end
scene.fogColor: Color3                          // Fog color
```

**Optimization**
```typescript
scene.blockMaterialDirtyMechanism: boolean      // Prevent material updates
scene.useDelayedTextureLoading: boolean         // Lazy texture loading
scene.skipPointerMovePicking: boolean           // Disable pointer move picking
scene.forceShowBoundingBoxes: boolean           // Debug bounding boxes
scene.skipFrustumClipping: boolean              // Disable frustum culling
```

**Animation**
```typescript
scene.animationsEnabled: boolean                // Enable animations
scene.useConstantAnimationDeltaTime: boolean    // Fixed timestep
scene.constantlyUpdateMeshUnderPointer: boolean // Continuous picking
```

#### Methods

**Rendering**
```typescript
scene.render(updateCameras?: boolean, ignoreAnimations?: boolean): void
scene.enableDepthRenderer(camera?: Camera, useFloat?: boolean): DepthRenderer
scene.enableGeometryBufferRenderer(ratio?: number): GeometryBufferRenderer
```

**Mesh Management**
```typescript
scene.getMeshByName(name: string): AbstractMesh | null
scene.getMeshById(id: string): AbstractMesh | null
scene.getMeshesByTags(tagsQuery: string): Mesh[]
scene.removeMesh(mesh: AbstractMesh): number
```

**Camera Management**
```typescript
scene.getCameraByName(name: string): Camera | null
scene.getCameraById(id: string): Camera | null
scene.removeCamera(camera: Camera): number
```

**Light Management**
```typescript
scene.getLightByName(name: string): Light | null
scene.getLightById(id: string): Light | null
scene.removeLight(light: Light): number
```

**Material Management**
```typescript
scene.getMaterialByName(name: string): Material | null
scene.getMaterialById(id: string): Material | null
scene.removeMaterial(material: Material): number
```

**Animation**
```typescript
scene.beginAnimation(
  target: any,
  from: number,
  to: number,
  loop?: boolean,
  speedRatio?: number,
  onAnimationEnd?: () => void,
  animatable?: Animatable,
  stopCurrent?: boolean,
  targetMask?: (target: any) => boolean
): Animatable

scene.stopAnimation(target: any, animationName?: string): void
scene.stopAllAnimations(): void
scene.getAnimatableByTarget(target: any): Animatable | null
```

**Picking**
```typescript
scene.pick(
  x: number,
  y: number,
  predicate?: (mesh: AbstractMesh) => boolean,
  fastCheck?: boolean,
  camera?: Camera
): PickingInfo

scene.pickWithRay(
  ray: Ray,
  predicate?: (mesh: AbstractMesh) => boolean,
  fastCheck?: boolean
): PickingInfo

scene.multiPick(
  x: number,
  y: number,
  predicate?: (mesh: AbstractMesh) => boolean,
  camera?: Camera
): PickingInfo[]
```

**Environment**
```typescript
scene.createDefaultEnvironment(options?: IEnvironmentHelperOptions): EnvironmentHelper | null
scene.createDefaultCameraOrLight(
  createArcRotateCamera?: boolean,
  replace?: boolean,
  attachCameraControls?: boolean
): void
scene.createDefaultSkybox(
  environmentTexture?: BaseTexture,
  pbr?: boolean,
  scale?: number,
  blur?: number,
  setGlobalEnvTexture?: boolean
): Mesh | null
```

**Optimization**
```typescript
scene.createOrUpdateSelectionOctree(
  maxCapacity?: number,
  maxDepth?: number
): Octree<AbstractMesh>

scene.freezeActiveMeshes(frustumCullingEnabled?: boolean): Scene
scene.unfreezeActiveMeshes(): Scene
```

**Cleanup**
```typescript
scene.dispose(): void
scene.disposeSounds(): void
```

#### Events (Observables)

```typescript
scene.onBeforeRenderObservable: Observable<Scene>
scene.onAfterRenderObservable: Observable<Scene>
scene.onBeforeAnimationsObservable: Observable<Scene>
scene.onAfterAnimationsObservable: Observable<Scene>
scene.onBeforePhysicsObservable: Observable<Scene>
scene.onAfterPhysicsObservable: Observable<Scene>
scene.onBeforeCameraRenderObservable: Observable<Camera>
scene.onAfterCameraRenderObservable: Observable<Camera>
scene.onReadyObservable: Observable<Scene>
scene.onDataLoadedObservable: Observable<Scene>
scene.onDispose: () => void
scene.onPointerDown: (evt: PointerEvent, pickInfo: PickingInfo) => void
scene.onPointerUp: (evt: PointerEvent, pickInfo: PickingInfo) => void
scene.onPointerMove: (evt: PointerEvent, pickInfo: PickingInfo) => void
scene.onPointerPick: (evt: PointerEvent, pickInfo: PickingInfo) => void
```

---

## Cameras

### Base Camera Properties

```typescript
camera.position: Vector3                        // Camera position
camera.rotation: Vector3                        // Camera rotation (Euler)
camera.fov: number                              // Field of view (radians)
camera.minZ: number                             // Near clipping plane
camera.maxZ: number                             // Far clipping plane
camera.inertia: number                          // Movement smoothing (0-1)
camera.speed: number                            // Movement speed
camera.angularSensibility: number               // Mouse sensitivity
camera.layerMask: number                        // Rendering layers
camera.fovMode: number                          // Camera.FOVMODE_*
```

### BABYLON.FreeCamera

First-person camera with WASD controls.

```typescript
new FreeCamera(
  name: string,
  position: Vector3,
  scene: Scene
): FreeCamera
```

**Properties:**
```typescript
camera.ellipsoid: Vector3                       // Collision ellipsoid
camera.checkCollisions: boolean                 // Enable collisions
camera.applyGravity: boolean                    // Enable gravity
camera.keysUp: number[]                         // Key codes for forward
camera.keysDown: number[]                       // Key codes for backward
camera.keysLeft: number[]                       // Key codes for left
camera.keysRight: number[]                      // Key codes for right
camera.keysUpward: number[]                     // Key codes for up (fly mode)
camera.keysDownward: number[]                   // Key codes for down (fly mode)
```

**Methods:**
```typescript
camera.attachControl(noPreventDefault?: boolean): void
camera.detachControl(): void
camera.setTarget(target: Vector3): void
```

### BABYLON.ArcRotateCamera

Orbital camera that rotates around a target.

```typescript
new ArcRotateCamera(
  name: string,
  alpha: number,        // Horizontal rotation (radians)
  beta: number,         // Vertical rotation (radians)
  radius: number,       // Distance from target
  target: Vector3,      // Look-at point
  scene: Scene
): ArcRotateCamera
```

**Properties:**
```typescript
camera.alpha: number                            // Horizontal angle
camera.beta: number                             // Vertical angle
camera.radius: number                           // Distance
camera.target: Vector3                          // Target position
camera.inertialAlphaOffset: number              // Horizontal momentum
camera.inertialBetaOffset: number               // Vertical momentum
camera.inertialRadiusOffset: number             // Zoom momentum
camera.lowerAlphaLimit: number | null           // Min horizontal
camera.upperAlphaLimit: number | null           // Max horizontal
camera.lowerBetaLimit: number                   // Min vertical (0.01)
camera.upperBetaLimit: number                   // Max vertical (Math.PI - 0.01)
camera.lowerRadiusLimit: number | null          // Min distance
camera.upperRadiusLimit: number | null          // Max distance
camera.panningAxis: Vector3                     // Panning direction
camera.panningInertia: number                   // Panning smoothing
camera.zoomOnFactor: number                     // Zoom speed
camera.wheelPrecision: number                   // Wheel sensitivity
camera.panningSensibility: number               // Pan sensitivity
```

**Methods:**
```typescript
camera.setPosition(position: Vector3): void
camera.setTarget(target: Vector3): void
camera.focusOn(meshesOrMinMaxVectorAndDistance: any, doNotUpdateMaxZ?: boolean): void
camera.zoomOn(meshes?: AbstractMesh[], doNotUpdateMaxZ?: boolean): void
```

### BABYLON.UniversalCamera

Combination of FreeCamera and TouchCamera.

```typescript
new UniversalCamera(
  name: string,
  position: Vector3,
  scene: Scene
): UniversalCamera
```

Inherits all FreeCamera properties and adds touch support.

### BABYLON.FollowCamera

Camera that follows a target mesh.

```typescript
new FollowCamera(
  name: string,
  position: Vector3,
  scene: Scene
): FollowCamera
```

**Properties:**
```typescript
camera.lockedTarget: AbstractMesh               // Mesh to follow
camera.radius: number                           // Distance from target
camera.heightOffset: number                     // Height above target
camera.rotationOffset: number                   // Horizontal offset
camera.cameraAcceleration: number               // Movement speed
camera.maxCameraSpeed: number                   // Max speed
```

---

## Lights

### Base Light Properties

```typescript
light.diffuse: Color3                           // Diffuse color
light.specular: Color3                          // Specular color
light.intensity: number                         // Light intensity (0-1)
light.range: number                             // Effective range
light.includeOnlyMeshes: AbstractMesh[]         // Only affect these
light.includedOnlyMeshes: AbstractMesh[]        // Same as above
light.excludedMeshes: AbstractMesh[]            // Don't affect these
light.excludeWithLayerMask: number              // Layer mask exclusion
light.includeOnlyWithLayerMask: number          // Layer mask inclusion
light.lightmapMode: number                      // Light.LIGHTMAP_*
```

### BABYLON.HemisphericLight

Ambient light with ground color.

```typescript
new HemisphericLight(
  name: string,
  direction: Vector3,
  scene: Scene
): HemisphericLight
```

**Properties:**
```typescript
light.groundColor: Color3                       // Color from below
light.direction: Vector3                        // Light direction
```

### BABYLON.DirectionalLight

Parallel light (sun-like).

```typescript
new DirectionalLight(
  name: string,
  direction: Vector3,
  scene: Scene
): DirectionalLight
```

**Properties:**
```typescript
light.direction: Vector3                        // Light direction
light.position: Vector3                         // For shadow calculation
light.shadowMinZ: number                        // Shadow near plane
light.shadowMaxZ: number                        // Shadow far plane
light.autoUpdateExtends: boolean                // Auto-calculate shadow bounds
light.autoCalcShadowZBounds: boolean            // Auto Z bounds
light.orthoLeft: number                         // Orthographic left
light.orthoRight: number                        // Orthographic right
light.orthoTop: number                          // Orthographic top
light.orthoBottom: number                       // Orthographic bottom
```

### BABYLON.PointLight

Omni-directional point light.

```typescript
new PointLight(
  name: string,
  position: Vector3,
  scene: Scene
): PointLight
```

**Properties:**
```typescript
light.position: Vector3                         // Light position
light.shadowMinZ: number                        // Shadow near plane
light.shadowMaxZ: number                        // Shadow far plane
```

### BABYLON.SpotLight

Focused cone light.

```typescript
new SpotLight(
  name: string,
  position: Vector3,
  direction: Vector3,
  angle: number,
  exponent: number,
  scene: Scene
): SpotLight
```

**Properties:**
```typescript
light.position: Vector3                         // Light position
light.direction: Vector3                        // Light direction
light.angle: number                             // Cone angle (radians)
light.exponent: number                          // Light falloff
light.shadowAngleScale: number                  // Shadow angle scale
light.innerAngle: number                        // Inner cone angle
```

---

## Meshes

### BABYLON.Mesh

Basic 3D mesh object.

#### Constructor

```typescript
new Mesh(
  name: string,
  scene: Scene | null,
  parent?: Node,
  source?: Mesh,
  doNotCloneChildren?: boolean,
  clonePhysicsImpostor?: boolean
): Mesh
```

#### Properties

**Transform**
```typescript
mesh.position: Vector3                          // World position
mesh.rotation: Vector3                          // Euler rotation
mesh.rotationQuaternion: Quaternion | null      // Quaternion rotation
mesh.scaling: Vector3                           // Scale factors
mesh.parent: Node | null                        // Parent node
mesh.billboardMode: number                      // Mesh.BILLBOARDMODE_*
```

**Visibility**
```typescript
mesh.isVisible: boolean                         // Render visibility
mesh.visibility: number                         // Transparency (0-1)
mesh.alphaIndex: number                         // Render order
mesh.infiniteDistance: boolean                  // Always render at distance
mesh.isPickable: boolean                        // Can be picked
mesh.showBoundingBox: boolean                   // Debug bounds
```

**Rendering**
```typescript
mesh.material: Material | null                  // Applied material
mesh.receiveShadows: boolean                    // Receive shadows
mesh.renderingGroupId: number                   // Rendering order group
mesh.layerMask: number                          // Camera layer mask
mesh.alwaysSelectAsActiveMesh: boolean          // Skip frustum culling
mesh.doNotSyncBoundingInfo: boolean             // Skip bounds sync
mesh.isOccluded: boolean                        // Occlusion query result
mesh.isOcclusionQueryInProgress: boolean        // Query in progress
```

**Collisions**
```typescript
mesh.checkCollisions: boolean                   // Enable collision detection
mesh.ellipsoid: Vector3                         // Collision shape
mesh.ellipsoidOffset: Vector3                   // Collision offset
```

**LOD**
```typescript
mesh.useLODScreenCoverage: boolean              // Use screen coverage for LOD
```

#### Methods

**Transform**
```typescript
mesh.setAbsolutePosition(absolutePosition: Vector3): Mesh
mesh.getAbsolutePosition(): Vector3
mesh.setPivotMatrix(matrix: Matrix, postMultiplyPivotMatrix?: boolean): Mesh
mesh.getPivotMatrix(): Matrix
mesh.setPreTransformMatrix(matrix: Matrix): Mesh
mesh.lookAt(targetPoint: Vector3, yawCor?: number, pitchCor?: number, rollCor?: number): Mesh
mesh.translate(axis: Vector3, distance: number, space?: Space): Mesh
mesh.rotate(axis: Vector3, amount: number, space?: Space): Mesh
mesh.rotateAround(point: Vector3, axis: Vector3, amount: number): Mesh
```

**Geometry**
```typescript
mesh.getBoundingInfo(): BoundingInfo
mesh.refreshBoundingInfo(applySkeleton?: boolean): Mesh
mesh.updateVerticesData(kind: string, data: FloatArray, updateExtends?: boolean, makeItUnique?: boolean): Mesh
mesh.getVerticesData(kind: string, copyWhenShared?: boolean, forceCopy?: boolean): FloatArray | null
mesh.getIndices(copyWhenShared?: boolean, forceCopy?: boolean): IndicesArray | null
mesh.getTotalVertices(): number
mesh.getTotalIndices(): number
```

**Cloning**
```typescript
mesh.clone(name: string, newParent?: Node | null, doNotCloneChildren?: boolean): Mesh
mesh.createInstance(name: string): InstancedMesh
```

**LOD**
```typescript
mesh.addLODLevel(distanceOrScreenCoverage: number, mesh: Mesh | null): Mesh
mesh.removeLODLevel(mesh: Mesh): Mesh
mesh.getLODLevelAtDistance(distance: number): Mesh | null
```

**Optimization**
```typescript
mesh.convertToFlatShadedMesh(): Mesh
mesh.convertToUnIndexedMesh(): Mesh
mesh.flipFaces(flipNormals?: boolean): Mesh
mesh.increaseVertices(numberPerEdge: number): void
mesh.forceSharedVertices(): void
mesh.freezeWorldMatrix(newWorldMatrix?: Matrix | null, stopRecursion?: boolean): Mesh
mesh.unfreezeWorldMatrix(): Mesh
```

**Disposal**
```typescript
mesh.dispose(doNotRecurse?: boolean, disposeMaterialAndTextures?: boolean): void
```

### MeshBuilder

Static class for creating built-in shapes.

```typescript
// Box
BABYLON.MeshBuilder.CreateBox(name: string, options: {
  size?: number;
  width?: number;
  height?: number;
  depth?: number;
  faceUV?: Vector4[];
  faceColors?: Color4[];
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  wrap?: boolean;
  topBaseAt?: number;
  bottomBaseAt?: number;
  updatable?: boolean;
}, scene?: Scene): Mesh

// Sphere
BABYLON.MeshBuilder.CreateSphere(name: string, options: {
  segments?: number;
  diameter?: number;
  diameterX?: number;
  diameterY?: number;
  diameterZ?: number;
  arc?: number;
  slice?: number;
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  updatable?: boolean;
}, scene?: Scene): Mesh

// Cylinder
BABYLON.MeshBuilder.CreateCylinder(name: string, options: {
  height?: number;
  diameterTop?: number;
  diameterBottom?: number;
  diameter?: number;
  tessellation?: number;
  subdivisions?: number;
  arc?: number;
  faceColors?: Color4[];
  faceUV?: Vector4[];
  hasRings?: boolean;
  enclose?: boolean;
  cap?: number;
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  updatable?: boolean;
}, scene?: Scene): Mesh

// Plane
BABYLON.MeshBuilder.CreatePlane(name: string, options: {
  size?: number;
  width?: number;
  height?: number;
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  updatable?: boolean;
  sourcePlane?: Plane;
}, scene?: Scene): Mesh

// Ground
BABYLON.MeshBuilder.CreateGround(name: string, options: {
  width?: number;
  height?: number;
  subdivisions?: number;
  subdivisionsX?: number;
  subdivisionsY?: number;
  updatable?: boolean;
}, scene?: Scene): Mesh

// Ground from heightmap
BABYLON.MeshBuilder.CreateGroundFromHeightMap(name: string, url: string, options: {
  width?: number;
  height?: number;
  subdivisions?: number;
  minHeight?: number;
  maxHeight?: number;
  colorFilter?: Color3;
  alphaFilter?: number;
  updatable?: boolean;
  onReady?: (mesh: GroundMesh) => void;
}, scene?: Scene): GroundMesh

// Torus
BABYLON.MeshBuilder.CreateTorus(name: string, options: {
  diameter?: number;
  thickness?: number;
  tessellation?: number;
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  updatable?: boolean;
}, scene?: Scene): Mesh

// Lines
BABYLON.MeshBuilder.CreateLines(name: string, options: {
  points: Vector3[];
  updatable?: boolean;
  instance?: LinesMesh;
  colors?: Color4[];
  useVertexAlpha?: boolean;
}, scene?: Scene): LinesMesh

// Ribbon
BABYLON.MeshBuilder.CreateRibbon(name: string, options: {
  pathArray: Vector3[][];
  closeArray?: boolean;
  closePath?: boolean;
  offset?: number;
  updatable?: boolean;
  sideOrientation?: number;
  frontUVs?: Vector4;
  backUVs?: Vector4;
  instance?: Mesh;
  invertUV?: boolean;
  uvs?: Vector2[];
  colors?: Color4[];
}, scene?: Scene): Mesh
```

---

## Materials

### BABYLON.StandardMaterial

Basic Phong-based material.

#### Constructor

```typescript
new StandardMaterial(
  name: string,
  scene: Scene
): StandardMaterial
```

#### Properties

**Colors**
```typescript
material.diffuseColor: Color3                   // Main color
material.specularColor: Color3                  // Highlight color
material.emissiveColor: Color3                  // Self-illumination
material.ambientColor: Color3                   // Ambient contribution
material.specularPower: number                  // Shininess (1-128)
```

**Textures**
```typescript
material.diffuseTexture: BaseTexture | null     // Albedo map
material.ambientTexture: BaseTexture | null     // Ambient occlusion
material.opacityTexture: BaseTexture | null     // Transparency map
material.reflectionTexture: BaseTexture | null  // Environment/reflection
material.emissiveTexture: BaseTexture | null    // Emission map
material.specularTexture: BaseTexture | null    // Specular map
material.bumpTexture: BaseTexture | null        // Normal/bump map
material.lightmapTexture: BaseTexture | null    // Baked lighting
material.refractionTexture: BaseTexture | null  // Refraction map
```

**Rendering**
```typescript
material.alpha: number                          // Opacity (0-1)
material.backFaceCulling: boolean               // Cull back faces
material.cullBackFaces: boolean                 // Same as above
material.sideOrientation: number                // Material.SIDE_*
material.alphaMode: number                      // Material.ALPHA_*
material.transparencyMode: number | null        // Material.MATERIAL_*
material.wireframe: boolean                     // Render as wireframe
material.pointsCloud: boolean                   // Render as points
material.fillMode: number                       // Material.FILLMODE_*
```

**Lighting**
```typescript
material.useEmissiveAsIllumination: boolean     // Emissive as light
material.linkEmissiveWithDiffuse: boolean       // Tie colors
material.useSpecularOverAlpha: boolean          // Spec on transparent
material.useReflectionOverAlpha: boolean        // Refl on transparent
material.useAlphaFromDiffuseTexture: boolean    // Alpha from diffuse
material.useParallax: boolean                   // Parallax mapping
material.useParallaxOcclusion: boolean          // Parallax occlusion
material.parallaxScaleBias: number              // Parallax strength
material.roughness: number                      // Surface roughness
material.useLightmapAsShadowmap: boolean        // Lightmap = shadows
material.useGlossinessFromSpecularMapAlpha: boolean  // Glossiness source
```

**Fresnel**
```typescript
material.diffuseFresnelParameters: FresnelParameters | null
material.opacityFresnelParameters: FresnelParameters | null
material.reflectionFresnelParameters: FresnelParameters | null
material.emissiveFresnelParameters: FresnelParameters | null
material.refractionFresnelParameters: FresnelParameters | null
```

#### Methods

```typescript
material.clone(name: string): StandardMaterial
material.dispose(forceDisposeEffect?: boolean, forceDisposeTextures?: boolean): void
material.freeze(): void
material.unfreeze(): void
material.needAlphaBlending(): boolean
material.needAlphaTesting(): boolean
```

### BABYLON.PBRMaterial

Physically based rendering material.

#### Constructor

```typescript
new PBRMaterial(
  name: string,
  scene: Scene
): PBRMaterial
```

#### Properties

**Metallic-Roughness Workflow**
```typescript
material.metallic: number | null                // Metalness (0-1)
material.roughness: number | null               // Roughness (0-1)
material.metallicTexture: BaseTexture | null    // Metallic map
material.roughnessTexture: BaseTexture | null   // Roughness map (if separate)
material.metallicRoughnessTexture: BaseTexture | null  // Combined MR map
material.baseColor: Color3                      // Base color
material.baseTexture: BaseTexture | null        // Base color map
material.albedoColor: Color3                    // Same as baseColor
material.albedoTexture: BaseTexture | null      // Same as baseTexture
```

**Specular-Glossiness Workflow**
```typescript
material.reflectivityColor: Color3              // Specular color
material.reflectivityTexture: BaseTexture | null  // Specular map
material.microSurface: number                   // Glossiness (0-1)
material.microSurfaceTexture: BaseTexture | null  // Glossiness map
material.useMicroSurfaceFromReflectivityMapAlpha: boolean
```

**Other Maps**
```typescript
material.bumpTexture: BaseTexture | null        // Normal map
material.ambientTexture: BaseTexture | null     // Ambient occlusion
material.ambientTextureStrength: number         // AO strength
material.emissiveTexture: BaseTexture | null    // Emission map
material.emissiveColor: Color3                  // Emission color
material.emissiveIntensity: number              // Emission strength
material.lightmapTexture: BaseTexture | null    // Lightmap
material.opacityTexture: BaseTexture | null     // Opacity map
```

**Environment**
```typescript
material.environmentTexture: BaseTexture | null  // IBL/reflection
material.environmentIntensity: number           // Environment strength
material.useRadianceOverAlpha: boolean          // Refl over alpha
material.useSpecularOverAlpha: boolean          // Spec over alpha
```

**Rendering**
```typescript
material.alpha: number                          // Opacity (0-1)
material.transparencyMode: number | null        // PBRMaterial.PBRMATERIAL_*
material.alphaCutOff: number                    // Alpha test threshold
material.directIntensity: number                // Direct light multiplier
material.emissiveIntensity: number              // Emissive multiplier
material.environmentIntensity: number           // Environment multiplier
material.specularIntensity: number              // Specular multiplier
material.disableLighting: boolean               // Unlit mode
material.unlit: boolean                         // Same as above
```

**Advanced**
```typescript
material.usePhysicalLightFalloff: boolean       // Inverse square falloff
material.useRadianceOcclusion: boolean          // Radiance AO
material.useHorizonOcclusion: boolean           // Horizon AO
material.useAlphaFromAlbedoTexture: boolean     // Alpha from albedo
material.forceIrradianceInFragment: boolean     // Force fragment irradiance
material.realTimeFiltering: boolean             // Real-time filtering
material.realTimeFilteringQuality: number       // Filtering quality
```

---

## Textures

### BABYLON.Texture

2D texture from image file.

#### Constructor

```typescript
new Texture(
  url: string | null,
  sceneOrEngine: Scene | ThinEngine,
  noMipmap?: boolean,
  invertY?: boolean,
  samplingMode?: number,
  onLoad?: (() => void) | null,
  onError?: ((message?: string, exception?: any) => void) | null,
  buffer?: string | ArrayBuffer | ArrayBufferView | HTMLImageElement | Blob | ImageBitmap | null,
  deleteBuffer?: boolean,
  format?: number,
  mimeType?: string
): Texture
```

#### Properties

```typescript
texture.url: string | null                      // Texture URL
texture.uOffset: number                         // U offset
texture.vOffset: number                         // V offset
texture.uScale: number                          // U scale
texture.vScale: number                          // V scale
texture.uAng: number                            // U rotation
texture.vAng: number                            // V rotation
texture.wAng: number                            // W rotation
texture.wrapU: number                           // Texture.WRAP_*
texture.wrapV: number                           // Texture.WRAP_*
texture.coordinatesMode: number                 // Texture.MODE_*
texture.coordinatesIndex: number                // UV channel
texture.level: number                           // Texture level
texture.hasAlpha: boolean                       // Has alpha channel
texture.getAlphaFromRGB: boolean                // Alpha from luminance
texture.invertZ: boolean                        // Invert Z (for normal maps)
texture.isBlocking: boolean                     // Block until loaded
```

#### Methods

```typescript
texture.clone(): Texture
texture.dispose(): void
texture.updateURL(url: string, buffer?: string | ArrayBuffer | ArrayBufferView | HTMLImageElement | Blob, onLoad?: () => void): void
texture.updateSamplingMode(samplingMode: number): void
```

### BABYLON.CubeTexture

Cubemap texture for reflections/environment.

```typescript
new CubeTexture(
  rootUrl: string,
  sceneOrEngine: Scene | ThinEngine,
  extensions?: string[] | null,
  noMipmap?: boolean,
  files?: string[] | null,
  onLoad?: (() => void) | null,
  onError?: ((message?: string, exception?: any) => void) | null,
  format?: number,
  prefiltered?: boolean,
  forcedExtension?: string | null
): CubeTexture

// Create from prefiltered DDS
CubeTexture.CreateFromPrefilteredData(url: string, scene: Scene, forcedExtension?: string): CubeTexture
```

### BABYLON.RenderTargetTexture

Render-to-texture for effects.

```typescript
new RenderTargetTexture(
  name: string,
  size: number | { width: number, height: number } | { ratio: number },
  scene?: Scene,
  generateMipMaps?: boolean,
  doNotChangeAspectRatio?: boolean,
  type?: number,
  isCube?: boolean,
  samplingMode?: number,
  generateDepthBuffer?: boolean,
  generateStencilBuffer?: boolean,
  isMulti?: boolean,
  format?: number,
  delayAllocation?: boolean
): RenderTargetTexture
```

**Properties:**
```typescript
renderTarget.renderList: AbstractMesh[] | null  // Meshes to render
renderTarget.activeCamera: Camera | null        // Render camera
renderTarget.refreshRate: number                // Update frequency
renderTarget.clearColor: Color4                 // Clear color
```

---

## Physics

### Physics Engine Setup

```typescript
// Enable physics
scene.enablePhysics(
  gravity?: Vector3,
  plugin?: IPhysicsEnginePlugin
): boolean

// Default gravity
const gravity = new BABYLON.Vector3(0, -9.8, 0);

// Havok plugin
const havokInstance = await HavokPhysics();
const havokPlugin = new BABYLON.HavokPlugin(true, havokInstance);

scene.enablePhysics(gravity, havokPlugin);
```

### BABYLON.PhysicsAggregate

Physics body for a mesh (Havok v2).

```typescript
new PhysicsAggregate(
  transformNode: TransformNode,
  type: PhysicsShapeType,
  options?: PhysicsAggregateParameters,
  scene?: Scene
): PhysicsAggregate
```

**PhysicsShapeType:**
```typescript
BABYLON.PhysicsShapeType.SPHERE
BABYLON.PhysicsShapeType.BOX
BABYLON.PhysicsShapeType.CAPSULE
BABYLON.PhysicsShapeType.CYLINDER
BABYLON.PhysicsShapeType.CONVEX_HULL
BABYLON.PhysicsShapeType.MESH
BABYLON.PhysicsShapeType.HEIGHTFIELD
BABYLON.PhysicsShapeType.CONTAINER
```

**PhysicsAggregateParameters:**
```typescript
interface PhysicsAggregateParameters {
  mass?: number;                                // 0 = static
  restitution?: number;                         // Bounciness (0-1)
  friction?: number;                            // Surface friction
  startAsleep?: boolean;                        // Start inactive
  ignoreChildren?: boolean;                     // Ignore child meshes
  disableBidirectionalTransformation?: boolean;
  pressure?: number;                            // For soft bodies
  stiffness?: number;                           // For soft bodies
  velocityIterations?: number;
  positionIterations?: number;
}
```

**Properties:**
```typescript
aggregate.body: PhysicsBody                     // Physics body
aggregate.shape: PhysicsShape                   // Collision shape
aggregate.transformNode: TransformNode          // Associated node
```

**Methods:**
```typescript
aggregate.dispose(): void
```

### BABYLON.PhysicsBody

Physics body control.

```typescript
body.setMassProperties(props: { mass?: number, inertia?: Vector3, centerOfMass?: Vector3 }): void
body.getMass(): number
body.setLinearVelocity(velocity: Vector3): void
body.getLinearVelocity(): Vector3
body.setAngularVelocity(velocity: Vector3): void
body.getAngularVelocity(): Vector3
body.applyForce(force: Vector3, location: Vector3): void
body.applyImpulse(impulse: Vector3, location: Vector3): void
body.setMotionType(motionType: PhysicsMotionType): void
body.getMotionType(): PhysicsMotionType
body.setLinearDamping(damping: number): void
body.setAngularDamping(damping: number): void
body.setCollisionCallbackEnabled(enabled: boolean): void
```

### BABYLON.PhysicsRaycastResult

Raycast result.

```typescript
scene.physicsEngine?.raycast(from: Vector3, to: Vector3): PhysicsRaycastResult

interface PhysicsRaycastResult {
  hasHit: boolean;
  hitPointWorld: Vector3;
  hitNormalWorld: Vector3;
  hitFraction: number;
  body?: PhysicsBody;
}
```

---

## Animations

### BABYLON.Animation

Property animation.

#### Constructor

```typescript
new Animation(
  name: string,
  targetProperty: string,
  framePerSecond: number,
  dataType: number,
  loopMode?: number,
  enableBlending?: boolean
): Animation
```

**Data Types:**
```typescript
Animation.ANIMATIONTYPE_FLOAT
Animation.ANIMATIONTYPE_VECTOR2
Animation.ANIMATIONTYPE_VECTOR3
Animation.ANIMATIONTYPE_QUATERNION
Animation.ANIMATIONTYPE_MATRIX
Animation.ANIMATIONTYPE_COLOR3
Animation.ANIMATIONTYPE_COLOR4
Animation.ANIMATIONTYPE_SIZE
```

**Loop Modes:**
```typescript
Animation.ANIMATIONLOOPMODE_RELATIVE  // Continue from current
Animation.ANIMATIONLOOPMODE_CYCLE     // Loop
Animation.ANIMATIONLOOPMODE_CONSTANT  // Stop at end
Animation.ANIMATIONLOOPMODE_YOYO      // Ping-pong
```

#### Methods

```typescript
animation.setKeys(keys: IAnimationKey[]): void

interface IAnimationKey {
  frame: number;
  value: any;
  inTangent?: any;
  outTangent?: any;
  interpolation?: AnimationKeyInterpolation;
}

// Helper
Animation.CreateAndStartAnimation(
  name: string,
  node: Node,
  targetProperty: string,
  framePerSecond: number,
  totalFrame: number,
  from: any,
  to: any,
  loopMode?: number,
  easingFunction?: EasingFunction,
  onAnimationEnd?: () => void
): Animatable
```

### BABYLON.AnimationGroup

Group of synchronized animations.

```typescript
const animationGroup = new BABYLON.AnimationGroup('group', scene);
animationGroup.addTargetedAnimation(animation: Animation, target: any): TargetedAnimation;

// Control
animationGroup.play(loop?: boolean): void
animationGroup.pause(): void
animationGroup.stop(): void
animationGroup.reset(): void
animationGroup.goToFrame(frame: number): void
animationGroup.speedRatio = 2.0;  // 2x speed
```

---

## GUI

### BABYLON.GUI.AdvancedDynamicTexture

2D UI container.

```typescript
// Fullscreen UI
const advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI('UI', true, scene);

// Mesh UI
const plane = BABYLON.MeshBuilder.CreatePlane('plane', {size: 2}, scene);
const advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateForMesh(plane, 1024, 1024);

// Add controls
advancedTexture.addControl(control);
```

### Common Controls

```typescript
// Button
const button = BABYLON.GUI.Button.CreateSimpleButton('button', 'Click Me');
button.width = '150px';
button.height = '40px';
button.color = 'white';
button.background = 'green';
button.onPointerUpObservable.add(() => console.log('Clicked'));

// TextBlock
const text = new BABYLON.GUI.TextBlock();
text.text = 'Hello';
text.color = 'white';
text.fontSize = 24;

// Rectangle
const rect = new BABYLON.GUI.Rectangle();
rect.width = '400px';
rect.height = '200px';
rect.background = 'red';

// Image
const image = new BABYLON.GUI.Image('image', 'url');
image.width = '100px';
image.height = '100px';

// Slider
const slider = new BABYLON.GUI.Slider();
slider.minimum = 0;
slider.maximum = 100;
slider.value = 50;
slider.onValueChangedObservable.add((value) => console.log(value));
```

---

## Post-Processing

### BABYLON.DefaultRenderingPipeline

All-in-one post-processing.

```typescript
const pipeline = new BABYLON.DefaultRenderingPipeline(
  'pipeline',
  true,      // HDR
  scene,
  [camera]   // cameras
);

// FXAA
pipeline.fxaaEnabled = true;

// Bloom
pipeline.bloomEnabled = true;
pipeline.bloomThreshold = 0.8;
pipeline.bloomWeight = 0.5;
pipeline.bloomKernel = 64;

// Image processing
pipeline.imageProcessingEnabled = true;
pipeline.imageProcessing.contrast = 1.5;
pipeline.imageProcessing.exposure = 1.0;
pipeline.imageProcessing.toneMappingEnabled = true;

// Depth of field
pipeline.depthOfFieldEnabled = true;
pipeline.depthOfField.focusDistance = 2000;
pipeline.depthOfField.focalLength = 50;

// Chromatic aberration
pipeline.chromaticAberrationEnabled = true;
pipeline.chromaticAberration.aberrationAmount = 30;

// Grain
pipeline.grainEnabled = true;
pipeline.grain.intensity = 10;

// Sharpen
pipeline.sharpenEnabled = true;
pipeline.sharpen.edgeAmount = 0.3;
```

---

## Constants Reference

### Texture Constants

```typescript
// Wrap modes
Texture.CLAMP_ADDRESSMODE
Texture.WRAP_ADDRESSMODE
Texture.MIRROR_ADDRESSMODE

// Sampling modes
Texture.NEAREST_SAMPLINGMODE
Texture.BILINEAR_SAMPLINGMODE
Texture.TRILINEAR_SAMPLINGMODE

// Coordinate modes
Texture.EXPLICIT_MODE
Texture.SPHERICAL_MODE
Texture.PLANAR_MODE
Texture.CUBIC_MODE
Texture.PROJECTION_MODE
Texture.SKYBOX_MODE
Texture.INVCUBIC_MODE
Texture.EQUIRECTANGULAR_MODE
Texture.FIXED_EQUIRECTANGULAR_MODE
```

### Material Constants

```typescript
// Side orientation
Material.ClockWiseSideOrientation
Material.CounterClockWiseSideOrientation

// Fill modes
Material.PointFillMode
Material.WireFrameFillMode
Material.TriangleFillMode

// Alpha modes
Material.ALPHA_DISABLE
Material.ALPHA_ADD
Material.ALPHA_COMBINE
Material.ALPHA_SUBTRACT
Material.ALPHA_MULTIPLY
Material.ALPHA_MAXIMIZED
Material.ALPHA_ONEONE
Material.ALPHA_PREMULTIPLIED
Material.ALPHA_INTERPOLATE
```

---

This reference covers the most commonly used Babylon.js APIs. For complete documentation, visit: https://doc.babylonjs.com/
