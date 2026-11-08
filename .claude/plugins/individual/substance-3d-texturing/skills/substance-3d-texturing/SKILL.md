---
name: substance-3d-texturing
description: Comprehensive skill for Adobe Substance 3D Painter texturing and material creation workflow. Use this skill when creating PBR materials, exporting textures for web/game engines, optimizing 3D assets for real-time rendering, or automating texture workflows. Triggers on tasks involving Substance 3D Painter, PBR texturing, material creation, texture export for Three.js, Babylon.js, Unity, Unreal, glTF optimization, or Python API automation. Creates optimized textures for threejs-webgl, react-three-fiber, and babylonjs-engine materials.
---

# Substance 3D Texturing

## Overview

Master PBR (Physically Based Rendering) texture creation and export workflows for web and real-time engines. This skill covers Substance 3D Painter workflows from material creation through web-optimized texture export, with Python automation for batch processing and integration with WebGL/WebGPU engines.

**Key capabilities:**
- PBR material authoring (metallic/roughness workflow)
- Web-optimized texture export (glTF, Three.js, Babylon.js)
- Python API automation for batch export
- Texture compression and optimization for real-time rendering

## Core Concepts

### PBR Workflow

Substance 3D Painter uses the **metallic/roughness** PBR workflow with these core channels:

**Base Texture Maps:**
- `baseColor` (Albedo) - RGB diffuse color, no lighting information
- `normal` - RGB normal map (tangent space)
- `metallic` - Grayscale metalness (0 = dielectric, 1 = metal)
- `roughness` - Grayscale surface roughness (0 = smooth/glossy, 1 = rough/matte)

**Additional Maps:**
- `ambientOcclusion` (AO) - Grayscale cavity/occlusion
- `height` - Grayscale displacement/height
- `emissive` - RGB self-illumination
- `opacity` - Grayscale transparency

### Export Presets

Substance 3D Painter includes built-in export presets for common engines:
- **PBR Metallic Roughness** - Standard glTF/WebGL format
- **Unity HDRP/URP** - Unity pipelines
- **Unreal Engine** - UE4/UE5 format
- **Arnold (AiStandard)** - Renderer-specific

For web engines, **PBR Metallic Roughness** is the universal standard.

### Texture Resolution

Common resolutions for web (powers of 2):
- 512×512 - Low detail props, mobile
- 1024×1024 - Standard props, characters
- 2048×2048 - Hero assets, close-ups
- 4096×4096 - Showcase quality (use sparingly)

**Web optimization rule:** Start at 1024×1024, scale up only when texture detail is visible.

## Common Patterns

### 1. Basic Web Export (Three.js/Babylon.js)

Manual export workflow for single texture set:

**Steps:**
1. **File → Export Textures**
2. **Select preset:** "PBR Metallic Roughness"
3. **Configure export:**
   - Output directory: Choose target folder
   - File format: PNG (8-bit) for web
   - Padding: "Infinite" (prevents seams)
   - Resolution: 1024×1024 (adjust per asset)
4. **Export**

**Result files:**
```
MyAsset_baseColor.png
MyAsset_normal.png
MyAsset_metallicRoughness.png  // Packed: R=nothing, G=roughness, B=metallic
MyAsset_emissive.png           // Optional
```

**Three.js usage:**
```javascript
import * as THREE from 'three';

const textureLoader = new THREE.TextureLoader();

const material = new THREE.MeshStandardMaterial({
  map: textureLoader.load('MyAsset_baseColor.png'),
  normalMap: textureLoader.load('MyAsset_normal.png'),
  metalnessMap: textureLoader.load('MyAsset_metallicRoughness.png'),
  roughnessMap: textureLoader.load('MyAsset_metallicRoughness.png'),
  aoMap: textureLoader.load('MyAsset_ambientOcclusion.png'),
});
```

### 2. Batch Export with Python API

Automate export for multiple texture sets:

```python
import substance_painter.export
import substance_painter.resource
import substance_painter.textureset

# Define export preset
export_preset = substance_painter.resource.ResourceID(
    context="starter_assets",
    name="PBR Metallic Roughness"
)

# Configure export for all texture sets
config = {
    "exportShaderParams": False,
    "exportPath": "C:/export/web_textures",
    "defaultExportPreset": export_preset.url(),
    "exportList": [],
    "exportParameters": [{
        "parameters": {
            "fileFormat": "png",
            "bitDepth": "8",
            "dithering": True,
            "paddingAlgorithm": "infinite",
            "sizeLog2": 10  // 1024×1024
        }
    }]
}

# Add all texture sets to export list
for texture_set in substance_painter.textureset.all_texture_sets():
    config["exportList"].append({
        "rootPath": texture_set.name()
    })

# Execute export
result = substance_painter.export.export_project_textures(config)

if result.status == substance_painter.export.ExportStatus.Success:
    for stack, files in result.textures.items():
        print(f"Exported {stack}: {len(files)} textures")
else:
    print(f"Export failed: {result.message}")
```

### 3. Resolution Override per Asset

Export different resolutions for different assets (e.g., hero vs. background):

```python
config = {
    "exportPath": "C:/export",
    "defaultExportPreset": export_preset.url(),
    "exportList": [
        {"rootPath": "HeroCharacter"},   # Will use 2048 (override below)
        {"rootPath": "BackgroundProp"}   # Will use 512 (override below)
    ],
    "exportParameters": [
        {
            "filter": {"dataPaths": ["HeroCharacter"]},
            "parameters": {"sizeLog2": 11}  # 2048×2048
        },
        {
            "filter": {"dataPaths": ["BackgroundProp"]},
            "parameters": {"sizeLog2": 9}   # 512×512
        }
    ]
}
```

### 4. Custom Export Preset (Separate Channels)

Create custom preset to export metallic and roughness as separate files:

```python
custom_preset = {
    "exportPresets": [{
        "name": "WebGL_Separated",
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
                "fileName": "$textureSet_metallic",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8"}
            },
            {
                "fileName": "$textureSet_roughness",
                "channels": [
                    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"}
                ],
                "parameters": {"fileFormat": "png", "bitDepth": "8"}
            }
        ]
    }]
}

config = {
    "exportPath": "C:/export",
    "exportPresets": custom_preset["exportPresets"],
    "exportList": [{"rootPath": "MyAsset", "exportPreset": "WebGL_Separated"}]
}
```

### 5. Mobile-Optimized Export

Aggressive compression for mobile WebGL:

```python
mobile_config = {
    "exportPath": "C:/export/mobile",
    "defaultExportPreset": export_preset.url(),
    "exportList": [{"rootPath": texture_set.name()}],
    "exportParameters": [{
        "parameters": {
            "fileFormat": "jpeg",        # JPEG for baseColor (lossy but smaller)
            "bitDepth": "8",
            "sizeLog2": 9,               # 512×512 maximum
            "paddingAlgorithm": "infinite"
        }
    }, {
        "filter": {"outputMaps": ["$textureSet_normal", "$textureSet_metallicRoughness"]},
        "parameters": {
            "fileFormat": "png"          # PNG for data maps (need lossless)
        }
    }]
}
```

**Post-export:** Use tools like `pngquant` or `tinypng` for further compression.

### 6. glTF/GLB Integration

Export textures for glTF 2.0 format:

```python
gltf_config = {
    "exportPath": "C:/export/gltf",
    "defaultExportPreset": substance_painter.resource.ResourceID(
        context="starter_assets",
        name="PBR Metallic Roughness"
    ).url(),
    "exportList": [{"rootPath": texture_set.name()}],
    "exportParameters": [{
        "parameters": {
            "fileFormat": "png",
            "bitDepth": "8",
            "sizeLog2": 10,              # 1024×1024
            "paddingAlgorithm": "infinite"
        }
    }]
}

# After export, reference in glTF:
# {
#   "materials": [{
#     "name": "Material",
#     "pbrMetallicRoughness": {
#       "baseColorTexture": {"index": 0},
#       "metallicRoughnessTexture": {"index": 1}
#     },
#     "normalTexture": {"index": 2}
#   }]
# }
```

### 7. Event-Driven Export Plugin

Auto-export on save using Python plugin:

```python
import substance_painter.event
import substance_painter.export
import substance_painter.project

def auto_export(e):
    if not substance_painter.project.is_open():
        return

    config = {
        "exportPath": substance_painter.project.file_path().replace('.spp', '_textures'),
        "defaultExportPreset": substance_painter.resource.ResourceID(
            context="starter_assets", name="PBR Metallic Roughness"
        ).url(),
        "exportList": [{"rootPath": ts.name()} for ts in substance_painter.textureset.all_texture_sets()],
        "exportParameters": [{
            "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
        }]
    }

    substance_painter.export.export_project_textures(config)
    print("Auto-export completed")

# Register event
substance_painter.event.DISPATCHER.connect(
    substance_painter.event.ProjectSaved,
    auto_export
)
```

## Integration Patterns

### Three.js + React Three Fiber

Use exported textures in R3F:

```jsx
import { useTexture } from '@react-three/drei';

function TexturedMesh() {
  const [baseColor, normal, metallicRoughness, ao] = useTexture([
    '/textures/Asset_baseColor.png',
    '/textures/Asset_normal.png',
    '/textures/Asset_metallicRoughness.png',
    '/textures/Asset_ambientOcclusion.png',
  ]);

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial
        map={baseColor}
        normalMap={normal}
        metalnessMap={metallicRoughness}
        roughnessMap={metallicRoughness}
        aoMap={ao}
      />
    </mesh>
  );
}
```

See **react-three-fiber** skill for advanced R3F material workflows.

### Babylon.js PBR Materials

```javascript
import { PBRMaterial, Texture } from '@babylonjs/core';

const pbr = new PBRMaterial("pbr", scene);
pbr.albedoTexture = new Texture("/textures/Asset_baseColor.png", scene);
pbr.bumpTexture = new Texture("/textures/Asset_normal.png", scene);
pbr.metallicTexture = new Texture("/textures/Asset_metallicRoughness.png", scene);
pbr.useRoughnessFromMetallicTextureAlpha = false;
pbr.useRoughnessFromMetallicTextureGreen = true;
pbr.useMetallnessFromMetallicTextureBlue = true;
```

See **babylonjs-engine** skill for advanced PBR workflows.

### GLTF Export Pipeline

1. Export textures from Substance (as above)
2. Export model from Blender with glTF exporter
3. Reference Substance textures in `.gltf` JSON
4. Use `gltf-pipeline` for Draco compression:

```bash
gltf-pipeline -i model.gltf -o model.glb -d
```

See **blender-web-pipeline** skill for complete 3D asset pipeline.

## Performance Optimization

### Texture Size Budget

**Desktop WebGL:** ~100-150MB total texture memory
**Mobile WebGL:** ~30-50MB total texture memory

**Budget per asset:**
- Background/props: 512×512 (1MB per texture × 4 maps = 4MB)
- Standard assets: 1024×1024 (4MB per texture × 4 maps = 16MB)
- Hero assets: 2048×2048 (16MB per texture × 4 maps = 64MB)

### Compression Strategies

1. **JPEG for baseColor** (70-80% quality) - 10× smaller than PNG
2. **PNG-8 for data maps** (normal, metallic, roughness) - lossless required
3. **Basis Universal** (`.basis`) - GPU texture compression (90% smaller)
4. **Texture atlasing** - Combine multiple assets into single texture

### Channel Packing

Pack grayscale maps into RGB channels to reduce texture count:

**Packed ORM (Occlusion-Roughness-Metallic):**
- Red: Ambient Occlusion
- Green: Roughness
- Blue: Metallic

Export in Substance:
```python
orm_map = {
    "fileName": "$textureSet_ORM",
    "channels": [
        {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"},
        {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
        {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
    ]
}
```

### Mipmaps

Always enable mipmaps in engine for textures viewed at distance:

```javascript
// Three.js (automatic)
texture.generateMipmaps = true;

// Babylon.js
texture.updateSamplingMode(Texture.TRILINEAR_SAMPLINGMODE);
```

## Common Pitfalls

### 1. Wrong Color Space for BaseColor

**Problem:** BaseColor exported in linear space looks washed out.

**Solution:** Substance exports baseColor in sRGB by default (correct). Ensure engine uses sRGB:

```javascript
// Three.js
baseColorTexture.colorSpace = THREE.SRGBColorSpace;

// Babylon.js (automatic for albedoTexture)
```

### 2. Normal Map Baking Issues

**Problem:** Normal maps show inverted or incorrect shading.

**Solution:**
- Verify tangent space normal format (DirectX vs. OpenGL Y-flip)
- Substance uses OpenGL (Y+), same as glTF standard
- If using DirectX engine, flip green channel in export

### 3. Metallic/Roughness Channel Order

**Problem:** Metallic/roughness texture has swapped channels.

**Solution:** Default Substance export:
- Blue channel = Metallic
- Green channel = Roughness
- Matches glTF 2.0 specification

### 4. Padding Artifacts at UV Seams

**Problem:** Black or colored lines appear at UV seams.

**Solution:** Set padding algorithm to **"infinite"** in export settings:
```python
"paddingAlgorithm": "infinite"
```

### 5. Oversized Textures for Web

**Problem:** 4K textures cause long load times and memory issues on web.

**Solution:**
- Default to 1024×1024 for web
- Use 2048×2048 only for hero assets viewed close-up
- Implement LOD system with multiple resolution sets

### 6. Missing AO Map in Engine

**Problem:** AO map exported but not visible in engine.

**Solution:**
- Three.js: Requires second UV channel (`geometry.attributes.uv2`)
- Babylon.js: Set `material.useAmbientOcclusionFromMetallicTextureRed = true`
- Alternative: Bake AO into baseColor in Substance

## Resources

See bundled resources for complete workflows:

- **references/python_api_reference.md** - Complete Substance Painter Python API
- **references/export_presets.md** - Built-in and custom export preset catalog
- **references/pbr_channel_guide.md** - Deep dive into PBR texture channels
- **scripts/batch_export.py** - Batch export all texture sets
- **scripts/web_optimizer.py** - Post-process textures for web (resize, compress)
- **scripts/generate_export_preset.py** - Create custom export preset JSON
- **assets/export_templates/** - Pre-configured export presets for Three.js, Babylon.js, Unity

## Related Skills

- **blender-web-pipeline** - Complete 3D model → texture → web pipeline
- **threejs-webgl** - Loading and using PBR textures in Three.js
- **react-three-fiber** - R3F material workflows with Substance textures
- **babylonjs-engine** - Babylon.js PBR material system integration
