# Three.js Materials Comprehensive Guide

## Material Selection Decision Tree

```
Need lighting?
├─ NO → MeshBasicMaterial
└─ YES → Need PBR realism?
    ├─ NO → Need specular highlights?
    │   ├─ YES → MeshPhongMaterial
    │   └─ NO → MeshLambertMaterial
    └─ YES → Need advanced effects?
        ├─ YES → MeshPhysicalMaterial
        └─ NO → MeshStandardMaterial
```

## Material Comparison Table

| Material | Lighting | PBR | Performance | Use Case |
|----------|----------|-----|-------------|----------|
| MeshBasicMaterial | ✗ | ✗ | Excellent | UI, debugging, unlit scenes |
| MeshLambertMaterial | ✓ | ✗ | Very Good | Mobile, simple diffuse |
| MeshPhongMaterial | ✓ | ✗ | Good | Legacy, specular highlights |
| MeshStandardMaterial | ✓ | ✓ | Moderate | Most realistic scenes |
| MeshPhysicalMaterial | ✓ | ✓✓ | Lower | Advanced materials (glass, car paint) |
| MeshToonMaterial | ✓ | ✗ | Very Good | Cel-shaded / cartoon style |
| ShaderMaterial | Custom | Custom | Varies | Complete custom control |

## MeshBasicMaterial

**Use for:** UI elements, debugging, flat-colored objects, unlit scenes

```javascript
const material = new THREE.MeshBasicMaterial({
  color: 0xff0000,
  wireframe: false,
  transparent: false,
  opacity: 1.0,
  side: THREE.FrontSide,
  map: texture,
  alphaMap: alphaTexture,
  envMap: environmentMap,
  combine: THREE.MultiplyOperation, // For envMap
  reflectivity: 1.0,
  refractionRatio: 0.98
});
```

**Key Features:**
- No lighting calculations (fastest)
- Flat, unshaded appearance
- Always visible regardless of lights
- Good for backgrounds, UI, or stylized looks

**Performance:** ⭐⭐⭐⭐⭐

## MeshLambertMaterial

**Use for:** Mobile devices, simple diffuse surfaces, performance-critical scenes

```javascript
const material = new THREE.MeshLambertMaterial({
  color: 0xff0000,
  emissive: 0x000000,
  emissiveIntensity: 1.0,
  emissiveMap: null,
  map: texture,
  lightMap: lightMapTexture,
  lightMapIntensity: 1.0,
  aoMap: aoTexture,
  aoMapIntensity: 1.0
});
```

**Key Features:**
- Simple diffuse (matte) lighting
- No specular highlights
- Cheaper than Phong/Standard
- Good for organic, non-reflective surfaces

**Performance:** ⭐⭐⭐⭐

## MeshPhongMaterial

**Use for:** Legacy projects, objects with visible specular highlights

```javascript
const material = new THREE.MeshPhongMaterial({
  color: 0xff0000,
  specular: 0x111111,
  shininess: 30,
  emissive: 0x000000,
  emissiveIntensity: 1.0,
  map: texture,
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),
  bumpMap: bumpTexture,
  bumpScale: 1.0,
  specularMap: specTexture
});
```

**Key Features:**
- Diffuse + specular highlights
- Adjustable shininess
- Per-pixel lighting
- Legacy, prefer MeshStandardMaterial for new projects

**Performance:** ⭐⭐⭐

## MeshStandardMaterial (PBR)

**Use for:** Realistic materials, production-quality scenes, modern workflows

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5, // 0 = mirror, 1 = matte
  metalness: 0.5, // 0 = dielectric, 1 = metal
  map: diffuseTexture,
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture,
  aoMap: aoTexture,
  aoMapIntensity: 1.0,
  emissive: 0x000000,
  emissiveMap: emissiveTexture,
  emissiveIntensity: 1.0,
  envMap: environmentMap,
  envMapIntensity: 1.0,
  bumpMap: bumpTexture,
  bumpScale: 1.0,
  displacementMap: dispTexture,
  displacementScale: 1.0,
  displacementBias: 0.0,
  alphaMap: alphaTexture,
  flatShading: false
});
```

**Key Features:**
- Physically Based Rendering (PBR)
- Energy-conserving reflections
- Works with HDR environment maps
- Industry-standard workflow (glTF)

**Roughness Guide:**
- 0.0 - Perfect mirror (chrome, polished metal)
- 0.2 - Very glossy (wet surfaces, varnished wood)
- 0.5 - Moderate (painted metal, plastic)
- 0.8 - Matte (fabric, unpolished wood)
- 1.0 - Completely diffuse (clay, concrete)

**Metalness Guide:**
- 0.0 - Non-metal (wood, plastic, skin, fabric)
- 1.0 - Metal (gold, silver, copper, iron)
- Avoid values between 0-1 (physically incorrect)

**Performance:** ⭐⭐⭐

## MeshPhysicalMaterial (Advanced PBR)

**Use for:** Glass, car paint, clearcoat, transmission, iridescence

```javascript
const material = new THREE.MeshPhysicalMaterial({
  // All MeshStandardMaterial properties, plus:

  clearcoat: 1.0, // 0-1, adds glossy layer on top
  clearcoatRoughness: 0.1,
  clearcoatMap: clearcoatTexture,
  clearcoatRoughnessMap: clearcoatRoughnessTexture,
  clearcoatNormalMap: clearcoatNormalTexture,
  clearcoatNormalScale: new THREE.Vector2(1, 1),

  transmission: 1.0, // 0-1, for glass/transparency
  thickness: 1.0, // Subsurface thickness
  thicknessMap: thicknessTexture,

  ior: 1.5, // Index of refraction (glass ~1.5, water ~1.33, diamond ~2.4)

  sheen: 1.0, // Fabric-like sheen
  sheenRoughness: 0.5,
  sheenColor: new THREE.Color(0xffffff),

  iridescence: 1.0, // Soap bubble, oil slick effect
  iridescenceIOR: 1.3,
  iridescenceThicknessRange: [100, 400]
});
```

**Use Cases:**

### Glass
```javascript
{
  roughness: 0.0,
  metalness: 0.0,
  transmission: 1.0,
  thickness: 1.0,
  ior: 1.5
}
```

### Car Paint
```javascript
{
  roughness: 0.4,
  metalness: 0.8,
  clearcoat: 1.0,
  clearcoatRoughness: 0.1,
  color: 0xff0000
}
```

### Fabric (Velvet, Satin)
```javascript
{
  roughness: 0.8,
  metalness: 0.0,
  sheen: 1.0,
  sheenRoughness: 0.5,
  sheenColor: new THREE.Color(0xffffff)
}
```

### Soap Bubble
```javascript
{
  roughness: 0.0,
  metalness: 0.0,
  transmission: 1.0,
  thickness: 0.5,
  iridescence: 1.0,
  iridescenceIOR: 1.3
}
```

**Performance:** ⭐⭐

## MeshToonMaterial

**Use for:** Cel-shaded, cartoon, or stylized looks

```javascript
const material = new THREE.MeshToonMaterial({
  color: 0xff0000,
  map: texture,
  gradientMap: gradientTexture, // Controls toon shading steps
  emissive: 0x000000
});
```

**Key Features:**
- Discrete shading levels (cel-shaded)
- Stylized, non-realistic look
- Good performance

**Performance:** ⭐⭐⭐⭐

## Material Properties Deep Dive

### Common Properties (All Materials)

```javascript
{
  // Visibility
  visible: true,
  transparent: false,
  opacity: 1.0,
  alphaTest: 0.5, // Discard pixels below this alpha

  // Rendering
  side: THREE.FrontSide, // FrontSide, BackSide, DoubleSide
  depthTest: true,
  depthWrite: true,
  blending: THREE.NormalBlending,

  // Color
  color: 0xffffff,
  vertexColors: false,

  // Wireframe
  wireframe: false,
  wireframeLinewidth: 1, // Not all platforms support

  // Clipping
  clipShadows: false,
  clipIntersection: false,
  clippingPlanes: [],

  // Precision
  precision: "highp", // "lowp", "mediump", "highp"

  // Fog
  fog: true
}
```

### Texture Properties

```javascript
const texture = loader.load('texture.jpg');

// Color space (IMPORTANT!)
texture.colorSpace = THREE.SRGBColorSpace; // For diffuse/color maps
texture.colorSpace = THREE.LinearSRGBColorSpace; // For data maps (normal, roughness)

// Wrapping
texture.wrapS = THREE.RepeatWrapping; // ClampToEdgeWrapping, MirroredRepeatWrapping
texture.wrapT = THREE.RepeatWrapping;

// Repeat & Offset
texture.repeat.set(2, 2); // Tile 2x2
texture.offset.set(0.5, 0.5);
texture.rotation = Math.PI / 4;
texture.center.set(0.5, 0.5); // Rotation center

// Filtering
texture.minFilter = THREE.LinearMipmapLinearFilter; // Minification
texture.magFilter = THREE.LinearFilter; // Magnification
texture.anisotropy = renderer.capabilities.getMaxAnisotropy(); // Reduce blur at angles

// Mipmaps
texture.generateMipmaps = true;
```

### Texture Types & Color Spaces

| Texture Type | Color Space | Purpose |
|--------------|-------------|---------|
| map (diffuse) | SRGB | Base color |
| normalMap | Linear | Surface detail |
| roughnessMap | Linear | Surface roughness |
| metalnessMap | Linear | Metallic areas |
| aoMap | Linear | Ambient occlusion |
| emissiveMap | SRGB | Glow |
| bumpMap | Linear | Height data |
| displacementMap | Linear | Vertex displacement |
| alphaMap | Linear | Transparency mask |

## Material Optimization Tips

### 1. Texture Atlas
Combine multiple textures into one to reduce draw calls.

### 2. Share Materials
```javascript
// Good: Share material across meshes
const sharedMaterial = new THREE.MeshStandardMaterial({...});
const mesh1 = new THREE.Mesh(geo1, sharedMaterial);
const mesh2 = new THREE.Mesh(geo2, sharedMaterial);

// Bad: New material per mesh
const mesh1 = new THREE.Mesh(geo1, new THREE.MeshStandardMaterial({...}));
```

### 3. Texture Size
- Use power-of-two dimensions (512, 1024, 2048)
- Compress textures (JPEG for photos, PNG for alpha)
- Consider KTX2/Basis Universal for web

### 4. Disable Unnecessary Features
```javascript
material.needsUpdate = false; // After initial setup
renderer.shadowMap.autoUpdate = false; // If shadows don't change
```

### 5. Use InstancedMesh with Materials
For identical objects with the same material.

## Custom Shaders (ShaderMaterial)

**Use for:** Complete custom control, special effects, optimizations

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0.0 },
    uColor: { value: new THREE.Color(0xff0000) },
    uTexture: { value: texture }
  },
  vertexShader: `
    uniform float uTime;
    varying vec2 vUv;
    varying vec3 vNormal;

    void main() {
      vUv = uv;
      vNormal = normal;

      vec3 pos = position;
      pos.z += sin(pos.x * 10.0 + uTime) * 0.1;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 uColor;
    uniform sampler2D uTexture;
    varying vec2 vUv;
    varying vec3 vNormal;

    void main() {
      vec4 texColor = texture2D(uTexture, vUv);
      gl_FragColor = vec4(uColor * texColor.rgb, 1.0);
    }
  `,
  transparent: false,
  side: THREE.DoubleSide
});

// Update uniforms in animation loop
material.uniforms.uTime.value = elapsedTime;
```

## Material Disposal

Always dispose materials when no longer needed:

```javascript
material.dispose();

// Dispose textures too
if (material.map) material.map.dispose();
if (material.normalMap) material.normalMap.dispose();
if (material.roughnessMap) material.roughnessMap.dispose();
// ... etc
```

## Troubleshooting

### Material Appears Black
- No lights in scene (for Lambert/Phong/Standard)
- Normals inverted
- Material side setting incorrect

### Material Too Shiny
- Reduce roughness (Standard/Physical)
- Reduce shininess (Phong)
- Check roughnessMap is loaded

### Material Not Transparent
```javascript
material.transparent = true;
material.opacity = 0.5;
material.depthWrite = false; // For glass-like materials
```

### Texture Not Showing
- Check texture.colorSpace (SRGB for diffuse)
- Ensure geometry has UV coordinates
- Verify texture loaded successfully

### Z-Fighting / Flickering
- Adjust material.polygonOffset
```javascript
material.polygonOffset = true;
material.polygonOffsetFactor = -1;
material.polygonOffsetUnits = -1;
```

## Material Performance Ranking

1. **MeshBasicMaterial** - Fastest
2. **MeshToonMaterial** - Very Fast
3. **MeshLambertMaterial** - Fast
4. **MeshPhongMaterial** - Moderate
5. **MeshStandardMaterial** - Moderate-Slow
6. **MeshPhysicalMaterial** - Slowest

Use the simplest material that achieves your visual goals.
