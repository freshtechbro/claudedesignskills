# Substance 3D Texturing Assets

Pre-configured export preset templates for various web engines and platforms.

## Directory Structure

```
assets/
└── export_templates/
    ├── gltf_standard.json          # glTF 2.0 compliant preset
    ├── threejs_optimized.json      # Three.js with separate channels
    ├── babylonjs_pbr.json          # Babylon.js PBR format
    ├── web_orm_packed.json         # ORM channel packing
    └── mobile_webgl.json           # Mobile-optimized preset
```

## Usage

### Method 1: Copy Preset Configuration

Copy the JSON content from any template file and use directly in your Python script:

```python
import json
import substance_painter.export

# Load preset from file
with open('assets/export_templates/gltf_standard.json', 'r') as f:
    custom_preset = json.load(f)

config = {
    "exportPath": "C:/export",
    "exportPresets": custom_preset["exportPresets"],
    "exportList": [{"rootPath": "MyAsset", "exportPreset": "glTF_Standard"}],
    "exportParameters": [{
        "parameters": {"paddingAlgorithm": "infinite"}
    }]
}

result = substance_painter.export.export_project_textures(config)
```

### Method 2: Use Preset Generator Script

Generate presets programmatically:

```bash
# Generate glTF preset
.claude/skills/substance-3d-texturing/scripts/generate_export_preset.py --preset gltf --output my_preset.json

# Interactive mode
.claude/skills/substance-3d-texturing/scripts/generate_export_preset.py
```

## Preset Descriptions

### gltf_standard.json

**Format:** glTF 2.0 compliant
**Resolution:** 1024×1024
**Outputs:**
- `baseColor.png` - RGB base color (sRGB)
- `normal.png` - RGB normal map (OpenGL format)
- `metallicRoughness.png` - Packed: G=Roughness, B=Metallic

**Best for:**
- glTF/GLB export
- Generic WebGL applications
- Three.js, Babylon.js (standard workflow)

---

### threejs_optimized.json

**Format:** Three.js MeshStandardMaterial
**Resolution:** 1024×1024
**Outputs:**
- `color.jpg` - JPEG base color (smaller file size)
- `normal.png` - RGB normal map
- `ao.png` - Ambient occlusion
- `metalness.png` - Metallic channel
- `roughness.png` - Roughness channel

**Best for:**
- Three.js projects requiring separate channels
- Maximum flexibility (individual map control)
- When file size is less critical than editability

---

### babylonjs_pbr.json

**Format:** Babylon.js PBRMaterial
**Resolution:** 1024×1024
**Outputs:**
- `albedo.png` - Base color
- `normal.png` - Normal map
- `metallicRoughness.png` - Packed: G=Roughness, B=Metallic

**Best for:**
- Babylon.js PBR workflows
- Similar to glTF but with Babylon naming conventions

---

### web_orm_packed.json

**Format:** ORM (Occlusion-Roughness-Metallic) Packed
**Resolution:** 1024×1024
**Outputs:**
- `baseColor.png` - RGB base color
- `normal.png` - RGB normal map
- `ORM.png` - Packed: R=AO, G=Roughness, B=Metallic

**Best for:**
- Maximum efficiency (3 textures instead of 6)
- Production web applications
- When texture count matters more than editability

**Texture memory savings:** ~50% reduction

---

### mobile_webgl.json

**Format:** Mobile-optimized
**Resolution:** 512×512
**Outputs:**
- `color.jpg` - JPEG base color (aggressive compression)
- `normal.png` - RG normal map (reconstruct Z in shader)
- `packed.png` - R=AO, G=Roughness, B=Metallic

**Best for:**
- Mobile web applications
- Low-end devices
- When load time and memory are critical

**File size:** ~3MB total vs. ~16MB standard

## Customization

All presets can be customized by modifying the JSON files:

### Change Resolution

Modify the `sizeLog2` parameter:
- `9` = 512×512
- `10` = 1024×1024 (default)
- `11` = 2048×2048
- `12` = 4096×4096

```json
{
  "parameters": {
    "sizeLog2": 11  // Change to 2048×2048
  }
}
```

### Change File Format

Modify the `fileFormat` parameter:
- `"png"` - Lossless (recommended for data maps)
- `"jpeg"` - Lossy compression (good for baseColor)
- `"tga"` - Targa format
- `"exr"` - HDR format (32-bit)

```json
{
  "parameters": {
    "fileFormat": "jpeg"  // Change to JPEG
  }
}
```

### Add Custom Channels

Add new map entries to pack additional channels:

```json
{
  "fileName": "$textureSet_emissive",
  "channels": [
    {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "emissive"},
    {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "emissive"},
    {"destChannel": "B", "srcChannel": "B", "srcMapType": "documentMap", "srcMapName": "emissive"}
  ],
  "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
}
```

## Integration Examples

### Three.js with glTF Preset

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

loader.load('model.glb', (gltf) => {
  // Textures automatically loaded from glTF
  scene.add(gltf.scene);
});
```

### Three.js with Separate Textures

```javascript
import * as THREE from 'three';

const textureLoader = new THREE.TextureLoader();

const material = new THREE.MeshStandardMaterial({
  map: textureLoader.load('Asset_color.jpg'),
  normalMap: textureLoader.load('Asset_normal.png'),
  aoMap: textureLoader.load('Asset_ao.png'),
  metalnessMap: textureLoader.load('Asset_metalness.png'),
  roughnessMap: textureLoader.load('Asset_roughness.png'),
});

// Set color space for baseColor
material.map.colorSpace = THREE.SRGBColorSpace;
```

### Babylon.js with PBR Preset

```javascript
import { PBRMaterial, Texture } from '@babylonjs/core';

const pbr = new PBRMaterial("pbr", scene);
pbr.albedoTexture = new Texture("Asset_albedo.png", scene);
pbr.bumpTexture = new Texture("Asset_normal.png", scene);
pbr.metallicTexture = new Texture("Asset_metallicRoughness.png", scene);

// Configure channel reading
pbr.useRoughnessFromMetallicTextureGreen = true;
pbr.useMetallnessFromMetallicTextureBlue = true;
```

### ORM Packed Workflow

```javascript
// Three.js with ORM texture
const ormTexture = textureLoader.load('Asset_ORM.png');

material.aoMap = ormTexture;        // Reads from Red channel
material.roughnessMap = ormTexture; // Reads from Green channel
material.metalnessMap = ormTexture; // Reads from Blue channel
```

## Troubleshooting

**Preset not found in Substance:**
- Presets are for custom export via Python API only
- Not visible in Substance UI preset dropdown
- Use via Python scripts or plugins

**Wrong channel order:**
- Verify glTF spec: G=Roughness, B=Metallic
- Unreal uses different packing: R=AO, G=Roughness, B=Metallic
- Check engine documentation for channel expectations

**Textures too large:**
- Reduce `sizeLog2` (e.g., 10 → 9 for 512px)
- Use mobile preset for aggressive optimization
- Convert baseColor to JPEG post-export

**Normal map inverted:**
- Substance uses OpenGL format (Y+)
- If using DirectX engine, flip green channel
- Or use engine setting to flip normal Y

## Additional Resources

- **Substance Python API:** https://helpx.adobe.com/substance-3d-painter-python/api/
- **glTF 2.0 Spec:** https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
- **Three.js Materials:** https://threejs.org/docs/#api/en/materials/MeshStandardMaterial
- **Babylon.js PBR:** https://doc.babylonjs.com/features/featuresDeepDive/materials/using/introToPBR

## License

These preset templates are provided as examples and can be freely modified for your projects.
