# PBR Texture Channel Guide

Deep dive into Physically Based Rendering (PBR) texture channels, their purpose, authoring best practices, and technical specifications.

## Table of Contents

- [PBR Fundamentals](#pbr-fundamentals)
- [Core Channels](#core-channels)
- [Additional Channels](#additional-channels)
- [Channel Best Practices](#channel-best-practices)
- [Common Material Types](#common-material-types)

## PBR Fundamentals

### What is PBR?

Physically Based Rendering (PBR) is a shading model that aims to accurately simulate how light interacts with surfaces in the real world. PBR workflows ensure materials look consistent under different lighting conditions.

**Key principles:**
1. **Energy conservation** - Reflected light never exceeds incoming light
2. **Fresnel reflectance** - Reflection intensity varies with viewing angle
3. **Microsurface detail** - Surface roughness affects light scattering

### Metallic/Roughness vs. Specular/Glossiness

Substance 3D Painter uses the **metallic/roughness** workflow (also called metal/rough or met/rough).

**Metallic/Roughness:**
- `baseColor` = Albedo color for dielectrics, reflectance tint for metals
- `metallic` = 0 for non-metals, 1 for metals
- `roughness` = Surface roughness (0 = glossy, 1 = rough)

**Advantages:**
- Simpler (fewer maps)
- More physically accurate
- Industry standard (glTF, PBR games)

**Alternative (Specular/Glossiness):**
- `diffuse` = Albedo color
- `specular` = RGB specular reflectance
- `glossiness` = Surface smoothness (1 - roughness)

Note: Substance supports both, but metallic/roughness is recommended for web.

## Core Channels

### Base Color (Albedo)

**What it is:**
The intrinsic color of the surface, without any lighting information.

**Technical specs:**
- **Format:** RGB, 8-bit per channel (24-bit total)
- **Color space:** sRGB (gamma ~2.2)
- **Value range:** 0-255 per channel
- **File format:** PNG or JPEG

**Authoring guidelines:**

**For non-metals (dielectrics):**
- Typical value range: sRGB 50-240 (linear 0.02-0.8)
- Dark materials: Charcoal ~50, Rubber ~60
- Mid-tone materials: Wood ~120, Leather ~100
- Light materials: Snow ~240, Paper ~200
- **Never pure black** (30 minimum for black materials)
- **Never pure white** (240 maximum for white materials)

**For metals:**
- Use actual metal reflectance values:
  - Iron: sRGB(196, 198, 200)
  - Gold: sRGB(255, 195, 86)
  - Copper: sRGB(250, 155, 110)
  - Aluminum: sRGB(245, 246, 246)
  - Silver: sRGB(252, 250, 245)
- Bright, saturated colors for colored metals (gold, copper)

**Common mistakes:**
- ❌ **Lighting baked in** - Shadows or highlights in albedo
- ❌ **Too dark** - Black baseColor = no light reflection
- ❌ **Too bright** - Unrealistic energy conservation
- ❌ **Specular details** - Reflections should come from roughness, not albedo

**Validation:**
Use the "no lighting" shader in Substance to check:
- Does the material look correct without lights?
- Are there any baked shadows or highlights?
- Are values within physically plausible ranges?

---

### Normal Map

**What it is:**
Encodes surface detail by perturbing surface normals, creating the illusion of depth without additional geometry.

**Technical specs:**
- **Format:** RGB, 8-bit per channel
- **Color space:** Linear (not sRGB!)
- **Value range:** 0-255 → maps to -1 to +1 normals
- **File format:** PNG (lossless required)
- **Coordinate system:** Tangent space

**Normal format standards:**

**OpenGL (Y+) - Used by:**
- glTF/GLB
- Three.js
- Babylon.js
- Substance 3D Painter (default export)
- WebGL/WebGPU

**DirectX (Y-) - Used by:**
- Unity
- Unreal Engine
- Direct3D engines

**Visual difference:**
- OpenGL: Green channel points "up" on the texture
- DirectX: Green channel points "down" (inverted Y)

**Converting between formats:**
- OpenGL → DirectX: Invert green channel (255 - G)
- DirectX → OpenGL: Invert green channel (255 - G)

**Authoring guidelines:**

**Do:**
- ✅ Bake high-poly details to normal map
- ✅ Use for micro-surface detail (scratches, dents, pores)
- ✅ Keep intensity realistic (don't over-exaggerate)
- ✅ Use 8-bit PNG (16-bit unnecessary for real-time)

**Don't:**
- ❌ Use JPEG (compression artifacts create shading errors)
- ❌ Apply to low-poly silhouettes (causes artifacts)
- ❌ Extreme details (creates aliasing/shimmering)

**Validation:**
- Flat surface = RGB(128, 128, 255) or #8080FF
- No black or white pixels (except extreme cases)
- Blue channel dominant (~255) for most pixels

---

### Metallic

**What it is:**
Defines whether a surface is metallic (conductor) or non-metallic (dielectric/insulator).

**Technical specs:**
- **Format:** Grayscale, 8-bit
- **Color space:** Linear
- **Value range:** 0-255 (0 = non-metal, 255 = metal)
- **File format:** PNG

**Physical meaning:**
- **0 (black)** - Dielectric materials:
  - Wood, plastic, fabric, skin, ceramic, stone
  - Specular reflection ~4% (Fresnel F0 ≈ 0.04)
  - BaseColor = diffuse color
- **255 (white)** - Metallic materials:
  - Iron, gold, copper, aluminum, silver, chrome
  - Specular reflection ~60-100% (Fresnel F0 ≈ 0.6-1.0)
  - BaseColor = specular tint (no diffuse)

**Authoring guidelines:**

**Binary choice:**
- Use **only 0 or 255** (fully non-metal or fully metal)
- **Avoid gray values** (0-254) - not physically accurate
- Exception: Corroded/oxidized metals can have transition zones

**Material examples:**
- **Metallic = 0:** Wood, leather, cloth, rubber, plastic, glass, skin, concrete
- **Metallic = 255:** Iron, steel, aluminum, gold, silver, copper, brass, chrome

**Common mistakes:**
- ❌ Gradient metallic (0-255) - Not realistic
- ❌ Metallic = 255 with dark baseColor - Metals are reflective
- ❌ Metallic = 0 with bright baseColor + low roughness - Creates plastic look

**Special cases:**

**Painted metal:**
- Metallic = 0 (paint is dielectric)
- Only exposed metal areas = 255

**Rusty metal:**
- Clean metal = 255
- Rust (iron oxide) = 0 (rust is dielectric)

**Validation:**
- Histogram should show two spikes: at 0 and 255
- Very few pixels in 1-254 range

---

### Roughness

**What it is:**
Defines the microsurface roughness, controlling how light scatters when reflected.

**Technical specs:**
- **Format:** Grayscale, 8-bit
- **Color space:** Linear
- **Value range:** 0-255 (0 = smooth/glossy, 255 = rough/matte)
- **File format:** PNG

**Physical meaning:**
- **0 (black)** - Mirror smooth:
  - Perfect specular reflections
  - Sharp, focused highlights
  - Examples: Polished chrome, water, glass
- **255 (white)** - Completely rough:
  - Diffuse specular reflections
  - Large, blurred highlights
  - Examples: Concrete, fabric, unfinished wood

**Authoring guidelines:**

**Typical value ranges:**
- Mirror/chrome: 0-20
- Polished metal: 20-50
- Glossy plastic: 30-70
- Painted surfaces: 50-100
- Unfinished wood: 150-200
- Concrete/fabric: 200-255

**Do:**
- ✅ Use full range (0-255) across different materials
- ✅ Add variation (dirt, fingerprints, wear in crevices)
- ✅ Consider surface finish (polished vs. brushed vs. rough)

**Don't:**
- ❌ Uniform roughness across entire surface (boring, unrealistic)
- ❌ Pure white (255) for hard surfaces (leaves no specular)
- ❌ Pure black (0) for organic materials (too perfect)

**Roughness variation examples:**

**Metal object:**
- Base roughness: 40 (semi-polished)
- Scratches: 80 (exposed rough metal)
- Fingerprints: 30 (oil reduces roughness)
- Edges: 60 (worn from handling)

**Wooden table:**
- Base roughness: 100 (sanded wood)
- Glossy finish: 40 (varnish/polish)
- Worn areas: 150 (exposed grain)

**Validation:**
- Histogram should show variation (not single spike)
- Check for breakup in specular highlights (not uniform)
- Test under different lighting (rotating HDRI)

---

## Additional Channels

### Ambient Occlusion (AO)

**What it is:**
Approximates how ambient light reaches each point on the surface. Darkens crevices and contact areas.

**Technical specs:**
- **Format:** Grayscale, 8-bit
- **Color space:** Linear
- **Value range:** 0-255 (0 = fully occluded, 255 = fully lit)
- **File format:** PNG

**Purpose:**
- Enhance depth perception
- Darken crevices, corners, contact points
- Fake indirect lighting occlusion

**Authoring guidelines:**

**Do:**
- ✅ Bake from high-poly mesh
- ✅ Subtle intensity (avoid pure black)
- ✅ Use for cavity detail (screws, seams, panel gaps)

**Don't:**
- ❌ Bake directional lighting (AO should be omnidirectional)
- ❌ Over-darken (reduces albedo contrast)

**Web implementation:**

**Three.js:**
```javascript
material.aoMap = aoTexture;
material.aoMapIntensity = 1.0; // Adjust strength
geometry.attributes.uv2 = geometry.attributes.uv; // AO requires second UV channel
```

**Note:** Many engines require a second UV channel for AO. Consider baking AO into baseColor as an alternative for simpler setups.

---

### Height (Displacement)

**What it is:**
Grayscale map encoding surface height, used for displacement mapping or parallax effects.

**Technical specs:**
- **Format:** Grayscale, 8-16 bit
- **Color space:** Linear
- **Value range:** 0-255 (0 = low, 255 = high)
- **File format:** PNG

**Use cases:**
1. **Displacement mapping** - Actual geometry modification (not common in real-time)
2. **Parallax occlusion mapping (POM)** - Shader-based fake depth
3. **Normal map generation** - Convert height → normal in Substance

**Authoring guidelines:**
- Smooth gradients (avoid sharp steps)
- Sufficient contrast for visible effect
- Usually lower resolution than other maps (512-1024)

**Web usage:**
Limited support in real-time engines. Height is usually converted to normal maps in Substance before export.

---

### Emissive (Self-Illumination)

**What it is:**
RGB map defining areas that emit light (glow).

**Technical specs:**
- **Format:** RGB, 8-bit or 16-bit
- **Color space:** Linear (for HDR) or sRGB (for LDR)
- **Value range:** 0-255 (8-bit) or 0-65535 (16-bit)
- **File format:** PNG or EXR

**Use cases:**
- Glowing screens, LEDs, neon signs
- Bioluminescence
- Hot metal/lava
- Energy effects

**Authoring guidelines:**

**LDR emissive (8-bit):**
- Black (0,0,0) = no emission
- White (255,255,255) = full brightness
- Use `emissiveIntensity` in engine to control brightness

**HDR emissive (16/32-bit EXR):**
- Values can exceed 1.0 for bloom effects
- Physically accurate for bright lights

**Web implementation:**

**Three.js:**
```javascript
material.emissive = new THREE.Color(0xffffff);
material.emissiveMap = emissiveTexture;
material.emissiveIntensity = 2.0; // Boost for bloom
```

**Common mistake:**
❌ Using emissive for ambient occlusion (emissive should glow, not darken)

---

### Opacity (Alpha)

**What it is:**
Grayscale map controlling surface transparency.

**Technical specs:**
- **Format:** Grayscale, 8-bit
- **Color space:** Linear
- **Value range:** 0-255 (0 = transparent, 255 = opaque)
- **File format:** PNG (with alpha channel support)

**Use cases:**
- Glass, water, smoke
- Vegetation (leaves, grass)
- Decals, stickers
- Fading effects

**Authoring guidelines:**

**Binary alpha (cutout):**
- Use only 0 or 255 (fully transparent or opaque)
- Efficient for vegetation (no alpha blending)
- Set `alphaTest` threshold in engine

**Gradient alpha (blended):**
- Full 0-255 range for smooth transparency
- More expensive (requires alpha blending, sorting)

**Web implementation:**

**Three.js:**
```javascript
material.transparent = true;
material.alphaMap = opacityTexture;
material.alphaTest = 0.5; // For binary alpha (cutout)
material.opacity = 1.0; // Overall opacity multiplier
```

**Performance notes:**
- Alpha blending is expensive (disable backface culling, requires sorting)
- Use `alphaTest` (cutout) instead of `transparent` when possible

## Channel Best Practices

### Color Space Management

**sRGB (Gamma ~2.2):**
- BaseColor
- Emissive (8-bit)

**Linear (No Gamma):**
- Normal
- Metallic
- Roughness
- AO
- Height
- Opacity

**Why it matters:**
Incorrect color space causes incorrect lighting calculations. Always ensure:
- BaseColor textures have sRGB flag in engine
- Data textures (normal, roughness, etc.) use linear

**Three.js example:**
```javascript
baseColorTexture.colorSpace = THREE.SRGBColorSpace; // ✅ Correct
normalTexture.colorSpace = THREE.NoColorSpace;     // ✅ Correct (linear)
```

---

### Resolution Guidelines

**By channel importance:**

**Highest detail (1024-2048):**
- BaseColor (most visible)
- Normal (defines micro-detail)

**Medium detail (512-1024):**
- Roughness (specular breakup)
- Metallic (usually binary, less detail)

**Lower detail (512-1024):**
- AO (subtle effect)
- Emissive (often solid colors)

**Lowest detail (256-512):**
- Height (usually converted to normal)

**Web optimization:**
All channels can share the same resolution (1024×1024) for simplicity, but consider per-channel resizing for advanced optimization.

---

### File Format Selection

| Channel | Recommended Format | Reason |
|---------|-------------------|--------|
| **BaseColor** | JPEG (70-80%) or PNG-8 | Large file, compression acceptable |
| **Normal** | PNG-8 | Lossless required, compression breaks lighting |
| **Metallic** | PNG-8 | Binary data, lossless required |
| **Roughness** | PNG-8 | Subtle details, lossless preferred |
| **AO** | PNG-8 or JPEG (80%) | Subtle, can tolerate some compression |
| **Height** | PNG-16 | Benefits from higher bit depth |
| **Emissive** | PNG-8 (LDR) or EXR-32 (HDR) | HDR for bloom effects |
| **Opacity** | PNG-8 (with alpha) | Requires alpha channel |

---

### Texture Streaming & LOD

**Mipmaps:**
Always generate mipmaps for all textures. Engines generate automatically, but you can bake custom mipmaps in Substance for specific filtering.

**LOD strategy:**
Export multiple resolution sets:
- **LOD0** (close-up): 2048×2048
- **LOD1** (medium): 1024×1024
- **LOD2** (distant): 512×512

**Implementation (Three.js):**
```javascript
const lod = new THREE.LOD();
lod.addLevel(mesh_high_res, 0);    // 0-10 units
lod.addLevel(mesh_med_res, 10);    // 10-30 units
lod.addLevel(mesh_low_res, 30);    // 30+ units
```

## Common Material Types

### Plastic

**BaseColor:**
- Saturated colors (RGB 180, 60, 40 for red plastic)
- Consistent across surface

**Metallic:** 0 (non-metal)

**Roughness:**
- Glossy plastic: 30-50
- Matte plastic: 150-200

**Example (Three.js):**
```javascript
material.color = new THREE.Color(0xb43c28); // Orange plastic
material.metalness = 0.0;
material.roughness = 0.3; // Glossy
```

---

### Brushed Metal

**BaseColor:**
- Metal reflectance value (e.g., Aluminum: #F5F6F6)

**Metallic:** 255 (full metal)

**Roughness:**
- Directional variation (brush lines)
- 40-80 depending on finish

**Special:** Add anisotropic roughness for realistic brushed look (advanced shaders)

---

### Wood

**BaseColor:**
- Natural wood colors (browns, tans)
- Wood grain texture
- RGB 90-150 range

**Metallic:** 0 (non-metal)

**Roughness:**
- Unfinished: 150-200
- Varnished: 40-80
- Add variation (grain roughness differs)

**AO:** Cavity detail in grain

---

### Glass

**BaseColor:**
- Slight tint (RGB 245, 245, 245 for clear)

**Metallic:** 0

**Roughness:**
- Clean glass: 0-10
- Frosted glass: 100-200

**Opacity:** 20-50 (mostly transparent)

**Special:** Use refraction in engine (`transmission` in Three.js)

---

### Fabric

**BaseColor:**
- Fabric color with weave detail
- Medium values (RGB 80-180)

**Metallic:** 0

**Roughness:** 180-220 (very rough)

**Normal:** Weave/fiber details

**Special:** Consider subsurface scattering for translucent fabrics

---

### Rusty Metal

**BaseColor:**
- Clean metal: Metal reflectance
- Rust: Orange-brown (RGB 150, 80, 40)
- Use mask to blend

**Metallic:**
- Clean metal: 255
- Rust (iron oxide): 0
- Use same mask as baseColor

**Roughness:**
- Clean metal: 30-50
- Rust: 180-220

**Example mask-based blend:**
```python
# In Substance, use rust mask to drive:
# - BaseColor: Metal color → Rust color
# - Metallic: 255 → 0
# - Roughness: 40 → 200
```

## Validation Checklist

Before exporting, verify:

**BaseColor:**
- [ ] No baked lighting/shadows
- [ ] Values within plausible range (30-240 for most materials)
- [ ] Metals use actual metal reflectance colors

**Normal:**
- [ ] Correct format (OpenGL vs. DirectX)
- [ ] No compression artifacts (PNG only)
- [ ] Blue channel dominant

**Metallic:**
- [ ] Binary values (0 or 255 only)
- [ ] Matches material type (0 for dielectrics)

**Roughness:**
- [ ] Has surface variation (not uniform)
- [ ] Within realistic range for material

**All Maps:**
- [ ] Correct color space (sRGB vs. linear)
- [ ] Appropriate resolution (not oversized)
- [ ] Proper file format (lossless for data, JPEG for color)
- [ ] Padding set to "infinite" (no seams)

## Resources

- **PBR Guide:** https://academy.substance3d.com/courses/the-pbr-guide-part-1
- **Material Values:** https://docs.unrealengine.com/en-US/Resources/ContentExamples/MaterialProperties/
- **Texture Naming:** glTF 2.0 specification
