# Substance 3D Painter Export Presets

Complete catalog of built-in and custom export presets for various game engines and web platforms.

## Table of Contents

- [Built-in Presets](#built-in-presets)
- [Web/glTF Presets](#webgltf-presets)
- [Custom Preset Examples](#custom-preset-examples)
- [Channel Packing Strategies](#channel-packing-strategies)

## Built-in Presets

Substance 3D Painter ships with presets for major engines and renderers.

### PBR Metallic Roughness

**Context:** `starter_assets`
**Name:** `PBR Metallic Roughness`
**Use for:** glTF, Three.js, Babylon.js, generic PBR engines

**Output textures:**
- `$textureSet_baseColor.png` - Base color (RGB)
- `$textureSet_normal.png` - Normal map (RGB, OpenGL format)
- `$textureSet_metallicRoughness.png` - Packed texture:
  - Red: Unused
  - Green: Roughness
  - Blue: Metallic
- `$textureSet_emissive.png` - Emissive (RGB) *if present*

**Usage:**
```python
preset = substance_painter.resource.ResourceID(
    context="starter_assets",
    name="PBR Metallic Roughness"
)
```

**Best for:**
- Web applications (Three.js, Babylon.js)
- glTF/GLB export
- Generic PBR workflows

---

### Unity HDRP (Lit)

**Context:** `starter_assets`
**Name:** `Unity HDRP (Lit)`
**Use for:** Unity High Definition Render Pipeline

**Output textures:**
- `$textureSet_BaseMap.png` - Base color + alpha
- `$textureSet_Normal.png` - Normal map (DirectX format)
- `$textureSet_MaskMap.png` - Packed texture:
  - Red: Metallic
  - Green: Ambient Occlusion
  - Blue: Detail Mask
  - Alpha: Smoothness (1 - roughness)

**Differences from standard PBR:**
- DirectX normal format (Y-flipped)
- Smoothness instead of roughness (inverted)
- Different channel packing

---

### Unity URP (Lit)

**Context:** `starter_assets`
**Name:** `Unity URP (Lit)`
**Use for:** Unity Universal Render Pipeline

**Output textures:**
- `$textureSet_BaseMap.png` - Base color + alpha
- `$textureSet_Normal.png` - Normal map
- `$textureSet_MetallicSmoothness.png` - Packed:
  - RGB: Metallic
  - Alpha: Smoothness

---

### Unreal Engine

**Context:** `starter_assets`
**Name:** `Unreal Engine 4/5 (Packed)`
**Use for:** Unreal Engine 4 and 5

**Output textures:**
- `$textureSet_BaseColor.png` - Base color
- `$textureSet_Normal.png` - Normal map (DirectX)
- `$textureSet_OcclusionRoughnessMetallic.png` - Packed:
  - Red: Ambient Occlusion
  - Green: Roughness
  - Blue: Metallic
- `$textureSet_Emissive.png` - Emissive

**Note:** Unreal's packed ORM format is widely used and efficient.

---

### Arnold (AiStandard)

**Context:** `starter_assets`
**Name:** `Arnold (AiStandard)`
**Use for:** Arnold renderer (Maya, Cinema 4D, Houdini)

**Output textures:**
- `$textureSet_baseColor.exr` - Base color (EXR 32-bit)
- `$textureSet_normal.exr` - Normal map
- `$textureSet_specularRoughness.exr` - Roughness
- `$textureSet_metalness.exr` - Metallic

**Note:** Uses EXR format for high dynamic range.

---

### V-Ray

**Context:** `starter_assets`
**Name:** `V-Ray`
**Use for:** V-Ray renderer

**Output textures:**
- Separate files for each channel
- High bit-depth support (16/32-bit)

## Web/glTF Presets

Optimized presets for web and real-time rendering.

### glTF 2.0 Standard

**Custom preset for glTF 2.0 compliance:**

```python
{
    "exportPresets": [{
        "name": "glTF_Standard",
        "maps": [
            {
                "fileName": "$textureSet_baseColor",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ],
                "parameters": {
                    "fileFormat": "png",
                    "bitDepth": "8",
                    "sizeLog2": 10  # 1024×1024
                }
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_metallicRoughness",
                "channels": [
                    {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                    {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            }
        ]
    }]
}
```

**Matches glTF 2.0 specification:**
- BaseColor in sRGB color space
- MetallicRoughness: Green = Roughness, Blue = Metallic
- Normal in OpenGL format (Y+)

---

### Three.js Optimized

**Preset optimized for Three.js MeshStandardMaterial:**

```python
{
    "exportPresets": [{
        "name": "ThreeJS_Standard",
        "maps": [
            {
                "fileName": "$textureSet_color",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ],
                "parameters": {"fileFormat": "jpeg", "bitDepth": "8", "sizeLog2": 10}  # JPEG for smaller size
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_ao",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_metalness",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_roughness",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            }
        ]
    }]
}
```

**Features:**
- JPEG for baseColor (70-80% quality, 10× smaller)
- PNG for data textures (lossless required)
- Separate metalness and roughness for flexibility
- Separate AO map

**Three.js usage:**
```javascript
const material = new THREE.MeshStandardMaterial({
  map: new THREE.TextureLoader().load('Asset_color.jpg'),
  normalMap: new THREE.TextureLoader().load('Asset_normal.png'),
  aoMap: new THREE.TextureLoader().load('Asset_ao.png'),
  metalnessMap: new THREE.TextureLoader().load('Asset_metalness.png'),
  roughnessMap: new THREE.TextureLoader().load('Asset_roughness.png'),
});
```

---

### Babylon.js PBR

**Preset for Babylon.js PBRMaterial:**

```python
{
    "exportPresets": [{
        "name": "BabylonJS_PBR",
        "maps": [
            {
                "fileName": "$textureSet_albedo",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            },
            {
                "fileName": "$textureSet_metallicRoughness",
                "channels": [
                    {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                    {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
            }
        ]
    }]
}
```

**Babylon.js usage:**
```javascript
const pbr = new BABYLON.PBRMaterial("pbr", scene);
pbr.albedoTexture = new BABYLON.Texture("Asset_albedo.png", scene);
pbr.bumpTexture = new BABYLON.Texture("Asset_normal.png", scene);
pbr.metallicTexture = new BABYLON.Texture("Asset_metallicRoughness.png", scene);
pbr.useRoughnessFromMetallicTextureGreen = true;
pbr.useMetallnessFromMetallicTextureBlue = true;
```

---

### Mobile WebGL (Low Spec)

**Aggressive compression for mobile:**

```python
{
    "exportPresets": [{
        "name": "Mobile_WebGL",
        "maps": [
            {
                "fileName": "$textureSet_color",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ],
                "parameters": {"fileFormat": "jpeg", "bitDepth": "8", "sizeLog2": 9}  # 512×512
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 9}  # Skip blue channel
            },
            {
                "fileName": "$textureSet_packed",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"},
                    {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                    {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 9}
            }
        ]
    }]
}
```

**Optimizations:**
- 512×512 maximum resolution
- JPEG for color (lossy but small)
- RG normal map only (reconstruct Z in shader)
- ORM packing (3 maps → 1 texture)

**Total texture budget:** ~3MB (vs. ~16MB standard)

## Custom Preset Examples

### ORM Packing (Occlusion-Roughness-Metallic)

**Most efficient packing for web:**

```python
orm_preset = {
    "exportPresets": [{
        "name": "Web_ORM",
        "maps": [
            {
                "fileName": "$textureSet_baseColor",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ]
            },
            {
                "fileName": "$textureSet_normal",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"}
                ]
            },
            {
                "fileName": "$textureSet_ORM",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"},
                    {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                    {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ]
            }
        ]
    }]
}
```

**Reduces texture count:** 6 textures → 3 textures
**Shader setup (Three.js):**
```javascript
material.aoMap = ormTexture;
material.roughnessMap = ormTexture;
material.metalnessMap = ormTexture;
// Three.js automatically reads from R/G/B channels
```

---

### Height + Normal Combined

**Pack height into normal alpha channel:**

```python
{
    "fileName": "$textureSet_normalHeight",
    "channels": [
        {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
        {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"},
        {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "normal"},
        {"destChannel": "A", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "height"}
    ]
}
```

**Use case:** Parallax occlusion mapping (height from alpha)

---

### Emissive + Alpha

**Pack emissive RGB + opacity:**

```python
{
    "fileName": "$textureSet_emissiveAlpha",
    "channels": [
        {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive"},
        {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive"},
        {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive"},
        {"destChannel": "A", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "opacity"}
    ]
}
```

---

### Stylized/NPR Export

**Non-photorealistic rendering (toon shading):**

```python
{
    "exportPresets": [{
        "name": "Stylized_Toon",
        "maps": [
            {
                "fileName": "$textureSet_diffuse",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "baseColor"},
                    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "baseColor"}
                ]
            },
            {
                "fileName": "$textureSet_shadowMask",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"}
                ]
            },
            # No metallic/roughness for toon shaders
        ]
    }]
}
```

## Channel Packing Strategies

### Standard PBR Packing

**glTF 2.0 / Khronos Standard:**
- BaseColor: RGB (sRGB)
- Normal: RGB (OpenGL, linear)
- MetallicRoughness:
  - R: Unused
  - G: Roughness (linear)
  - B: Metallic (linear)

**Advantages:**
- Industry standard
- Maximum compatibility
- glTF compliance

---

### Unreal Engine Packing

**Unreal's ORM format:**
- BaseColor: RGB
- Normal: RGB (DirectX)
- ORM:
  - R: Ambient Occlusion
  - G: Roughness
  - B: Metallic

**Advantages:**
- Includes AO without extra texture
- Widely used format
- Efficient for complex materials

---

### Mobile Optimized Packing

**Aggressive compression:**
- BaseColor: JPEG (lossy)
- Normal: RG only (reconstruct Z)
- ORM: RGB (AO + Roughness + Metallic)

**Advantages:**
- Smallest file size
- Reduced texture memory
- Faster loading on mobile

**Disadvantages:**
- Lossy baseColor (visual artifacts)
- RG normal requires shader modification

---

### High Quality / Archival

**Separate channels, high bit depth:**
- BaseColor: PNG-16 or EXR-32
- Normal: PNG-16
- Metallic: PNG-16 (separate)
- Roughness: PNG-16 (separate)
- AO: PNG-16 (separate)
- Height: PNG-16 (separate)

**Advantages:**
- Maximum quality
- Per-channel editability
- HDR support (EXR)

**Disadvantages:**
- Large file sizes
- More texture slots
- Overkill for real-time

## Preset Selection Guide

### By Platform

| Platform | Recommended Preset | Resolution | Format |
|----------|-------------------|------------|---------|
| **Desktop Web** | glTF_Standard / Web_ORM | 1024-2048 | PNG |
| **Mobile Web** | Mobile_WebGL | 512-1024 | JPEG+PNG |
| **Unity HDRP** | Unity HDRP (Lit) | 2048-4096 | PNG |
| **Unreal Engine** | Unreal Engine (Packed) | 2048-4096 | PNG |
| **glTF Export** | PBR Metallic Roughness | 1024-2048 | PNG |
| **Three.js** | ThreeJS_Standard | 1024-2048 | JPEG+PNG |
| **Babylon.js** | BabylonJS_PBR | 1024-2048 | PNG |

### By Use Case

| Use Case | Preset | Notes |
|----------|--------|-------|
| **Quick web export** | PBR Metallic Roughness | Built-in, universal |
| **Smallest file size** | Mobile_WebGL | JPEG color, ORM packing |
| **Maximum compatibility** | glTF_Standard | Strict glTF 2.0 spec |
| **Maximum quality** | High Quality / Archival | 16/32-bit, separate channels |
| **Production pipeline** | Web_ORM | Efficient, industry standard |

### By Texture Count

| Texture Count | Packing Strategy | Maps |
|---------------|------------------|------|
| **3 textures** | ORM packed | BaseColor, Normal, ORM |
| **4 textures** | glTF standard | BaseColor, Normal, MetallicRoughness, Emissive |
| **5+ textures** | Separate channels | Color, Normal, Metallic, Roughness, AO |

## Best Practices

### For Web Platforms

1. **Use ORM packing** - 3 textures instead of 6
2. **JPEG for baseColor** - 70-80% quality, 10× smaller
3. **PNG for data maps** - Normal, ORM require lossless
4. **Start at 1024×1024** - Scale up only when needed
5. **Test file sizes** - Aim for <5MB total per asset

### For Game Engines

1. **Use engine-specific presets** - Proper channel order/format
2. **Match color space** - sRGB for color, linear for data
3. **Check normal format** - DirectX vs. OpenGL (Y-flip)
4. **Consider UDIM** - For large characters (multiple tiles)

### For glTF/GLB

1. **Use "PBR Metallic Roughness"** - Official standard
2. **OpenGL normal maps** - Y+ (green up)
3. **Keep within spec** - Avoid custom channels
4. **Compress with Draco** - gltf-pipeline for final export

## Troubleshooting

**Textures look washed out:**
- BaseColor in wrong color space (should be sRGB)
- Check engine texture settings

**Metallic looks rough / rough looks metallic:**
- Channels swapped (check Green/Blue order)
- Verify MetallicRoughness packing: G=Roughness, B=Metallic

**Normal map inverted:**
- DirectX vs. OpenGL format
- Flip green channel in export or engine

**Seams at UV borders:**
- Use `"paddingAlgorithm": "infinite"` in export parameters
- Increase dilation distance

**File sizes too large:**
- Use JPEG for baseColor
- Reduce resolution (sizeLog2)
- Pack channels (ORM)
- Compress with external tools (pngquant, tinypng)
