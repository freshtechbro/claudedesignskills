---
name: blender-web-pipeline
description: Blender to web export workflows for 3D models and animations. Use this skill when exporting Blender models to glTF for web, optimizing 3D assets for Three.js or Babylon.js, batch processing models with Python scripts, automating Blender workflows, or creating web-ready 3D pipelines. Triggers on tasks involving Blender glTF export, bpy scripting, 3D asset optimization, model compression, texture baking, or Blender automation. Exports models for threejs-webgl, react-three-fiber, and babylonjs-engine skills.
---

# Blender Web Pipeline

## Overview

Blender Web Pipeline skill provides workflows for exporting 3D models and animations from Blender to web-optimized formats (primarily glTF 2.0). It covers Python scripting for batch processing, optimization techniques for web performance, and integration with web 3D libraries like Three.js and Babylon.js.

**When to use this skill:**
- Exporting Blender models for web applications
- Batch processing multiple 3D assets
- Optimizing file sizes for web delivery
- Automating repetitive Blender tasks
- Creating production pipelines for 3D web content
- Converting legacy formats to glTF

**Key capabilities:**
- glTF 2.0 export with optimization
- Python (bpy) automation scripts
- Texture baking and compression
- LOD (Level of Detail) generation
- Batch processing workflows
- Material and lighting optimization for web

## Core Concepts

### glTF 2.0 Format

**Why glTF for Web:**
- Industry-standard 3D format for web
- Efficient binary encoding (.glb)
- PBR materials support
- Animation and skinning
- Extensible with custom data
- Wide library support (Three.js, Babylon.js, etc.)

**glTF vs GLB:**
```
.gltf = JSON + external .bin + external textures
.glb  = Single binary file (recommended for web)
```

### Blender Python API (bpy)

**Access Blender data and operations via Python:**

```python
import bpy

# Access scene data
scene = bpy.context.scene
objects = bpy.data.objects

# Modify objects
obj = bpy.data.objects['Cube']
obj.location = (0, 0, 1)
obj.scale = (2, 2, 2)

# Export glTF
bpy.ops.export_scene.gltf(
    filepath='/path/to/model.glb',
    export_format='GLB'
)
```

### Web Optimization Goals

**Target Metrics:**
- File size: <5 MB per model (ideal <1 MB)
- Polygon count: <50k triangles for real-time
- Texture resolution: 2048x2048 max (1024x1024 preferred)
- Draw calls: Minimize via texture atlases
- Load time: <2 seconds on average connection

## Common Patterns

### 1. Basic glTF Export (Manual)

```python
# Blender Python Console or script

import bpy

# Select objects to export (optional - exports all if none selected)
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['MyModel'].select_set(True)

# Export as GLB
bpy.ops.export_scene.gltf(
    filepath='/path/to/output.glb',
    export_format='GLB',                # Binary format
    use_selection=True,                 # Export selected only
    export_apply=True,                  # Apply modifiers
    export_texcoords=True,              # UV coordinates
    export_normals=True,                # Normals
    export_materials='EXPORT',          # Export materials
    export_colors=True,                 # Vertex colors
    export_cameras=False,               # Skip cameras
    export_lights=False,                # Skip lights
    export_animations=True,             # Include animations
    export_draco_mesh_compression_enable=True,  # Compress geometry
    export_draco_mesh_compression_level=6,      # 0-10 (6 recommended)
    export_draco_position_quantization=14,      # 8-14 bits
    export_draco_normal_quantization=10,        # 8-10 bits
    export_draco_texcoord_quantization=12       # 8-12 bits
)
```

### 2. Python Script for Batch Export

```python
#!/usr/bin/env blender --background --python
"""
Batch export all .blend files in a directory to glTF
Usage: blender --background --python batch_export.py -- /path/to/blend/files
"""

import bpy
import os
import sys

# Get command line arguments after --
argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []

input_dir = argv[0] if argv else "/path/to/models"
output_dir = argv[1] if len(argv) > 1 else input_dir + "_gltf"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Find all .blend files
blend_files = [f for f in os.listdir(input_dir) if f.endswith('.blend')]

print(f"Found {len(blend_files)} .blend files")

for blend_file in blend_files:
    input_path = os.path.join(input_dir, blend_file)
    output_name = blend_file.replace('.blend', '.glb')
    output_path = os.path.join(output_dir, output_name)

    print(f"Processing: {blend_file}")

    # Open blend file
    bpy.ops.wm.open_mainfile(filepath=input_path)

    # Export as GLB with optimizations
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_apply=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6
    )

    print(f"  Exported: {output_name}")

print("Batch export complete!")
```

**Run batch script:**

```bash
blender --background --python batch_export.py -- /models/source /models/output
```

### 3. Optimize Model for Web (Decimation)

```python
import bpy

def optimize_mesh(obj, target_ratio=0.5):
    """Reduce polygon count using decimation modifier."""

    if obj.type != 'MESH':
        return

    # Add Decimate modifier
    decimate = obj.modifiers.new(name='Decimate', type='DECIMATE')
    decimate.ratio = target_ratio  # 0.5 = 50% of original polygons
    decimate.use_collapse_triangulate = True

    # Apply modifier
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier='Decimate')

    print(f"Optimized {obj.name}: {len(obj.data.polygons)} polygons")

# Optimize all selected meshes
for obj in bpy.context.selected_objects:
    optimize_mesh(obj, target_ratio=0.3)
```

### 4. Texture Baking for Web

```python
import bpy

def bake_textures(obj, resolution=1024):
    """Bake all materials to single texture."""

    # Setup bake settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.bake_type = 'COMBINED'

    # Create bake image
    bake_image = bpy.data.images.new(
        name=f"{obj.name}_bake",
        width=resolution,
        height=resolution
    )

    # Create bake material
    mat = bpy.data.materials.new(name=f"{obj.name}_baked")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Add Image Texture node
    tex_node = nodes.new(type='ShaderNodeTexImage')
    tex_node.image = bake_image
    tex_node.select = True
    nodes.active = tex_node

    # Assign material
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    # Select object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Bake
    bpy.ops.object.bake(type='COMBINED')

    # Save baked texture
    bake_image.filepath_raw = f"/tmp/{obj.name}_bake.png"
    bake_image.file_format = 'PNG'
    bake_image.save()

    print(f"Baked {obj.name} to {bake_image.filepath_raw}")

# Bake selected objects
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        bake_textures(obj, resolution=2048)
```

### 5. Generate LOD (Level of Detail)

```python
import bpy

def generate_lods(obj, lod_levels=[0.75, 0.5, 0.25]):
    """Generate LOD copies with decreasing polygon counts."""

    lod_objects = []

    for i, ratio in enumerate(lod_levels):
        # Duplicate object
        lod_obj = obj.copy()
        lod_obj.data = obj.data.copy()
        lod_obj.name = f"{obj.name}_LOD{i}"

        # Link to scene
        bpy.context.collection.objects.link(lod_obj)

        # Add Decimate modifier
        decimate = lod_obj.modifiers.new(name='Decimate', type='DECIMATE')
        decimate.ratio = ratio

        # Apply modifier
        bpy.context.view_layer.objects.active = lod_obj
        bpy.ops.object.modifier_apply(modifier='Decimate')

        lod_objects.append(lod_obj)

        print(f"Created {lod_obj.name}: {len(lod_obj.data.polygons)} polygons")

    return lod_objects

# Generate LODs for selected object
if bpy.context.active_object:
    generate_lods(bpy.context.active_object)
```

### 6. Export with Texture Compression

```python
import bpy
import os

def export_optimized_gltf(filepath, texture_max_size=1024):
    """Export glTF with downscaled textures."""

    # Downscale all textures
    for img in bpy.data.images:
        if img.size[0] > texture_max_size or img.size[1] > texture_max_size:
            img.scale(texture_max_size, texture_max_size)
            print(f"Downscaled {img.name} to {texture_max_size}x{texture_max_size}")

    # Export with Draco compression
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        export_apply=True,
        export_image_format='JPEG',  # JPEG for smaller size (or PNG for quality)
        export_jpeg_quality=85,       # 0-100
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=8,  # Max compression
        export_draco_position_quantization=12,
        export_draco_normal_quantization=8,
        export_draco_texcoord_quantization=10
    )

# Export optimized
export_optimized_gltf('/path/to/optimized.glb', texture_max_size=512)
```

### 7. Command-Line Automation

```bash
#!/bin/bash
# Batch export Blender files to glTF without opening GUI

SCRIPT_DIR="$(dirname "$0")"

# Export all .blend files in current directory
for blend_file in *.blend; do
    echo "Exporting $blend_file..."

    blender --background "$blend_file" --python - <<EOF
import bpy
import os

# Get output filename
filename = os.path.splitext(bpy.data.filepath)[0]
output = filename + '.glb'

# Export
bpy.ops.export_scene.gltf(
    filepath=output,
    export_format='GLB',
    export_apply=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6
)

print(f'Exported to {output}')
EOF

done

echo "All files exported!"
```

## Integration Patterns

### With Three.js

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const loader = new GLTFLoader();

// Setup Draco decoder for compressed models
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');
loader.setDRACOLoader(dracoLoader);

// Load Blender export
loader.load('/models/exported.glb', (gltf) => {
  scene.add(gltf.scene);

  // Play animations
  if (gltf.animations.length > 0) {
    const mixer = new THREE.AnimationMixer(gltf.scene);
    const action = mixer.clipAction(gltf.animations[0]);
    action.play();
  }
});
```

### With React Three Fiber

```jsx
import { useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/models/exported.glb');
  return <primitive object={scene} />;
}

// Preload for better performance
useGLTF.preload('/models/exported.glb');
```

### With Babylon.js

```javascript
import * as BABYLON from '@babylonjs/core';
import '@babylonjs/loaders/glTF';

BABYLON.SceneLoader.ImportMesh(
  '',
  '/models/',
  'exported.glb',
  scene,
  (meshes) => {
    console.log('Loaded meshes:', meshes);
  }
);
```

## Optimization Techniques

### 1. Geometry Optimization

**Decimate Modifier:**
```python
# Reduce polygon count by 70%
obj.modifiers.new(name='Decimate', type='DECIMATE')
obj.modifiers['Decimate'].ratio = 0.3
```

**Merge by Distance:**
```python
# Remove duplicate vertices
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.object.mode_set(mode='OBJECT')
```

**Triangulate Faces:**
```python
# Ensure all faces are triangles (required for some engines)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris()
bpy.ops.object.mode_set(mode='OBJECT')
```

### 2. Texture Optimization

**Image Compression:**
```python
# Save textures as JPEG (lossy but smaller)
for img in bpy.data.images:
    img.file_format = 'JPEG'
    img.filepath_raw = f"/output/{img.name}.jpg"
    img.save()
```

**Texture Atlas:**
```python
# Combine multiple textures into one atlas
# Use Smart UV Project for automatic atlasing
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')
```

### 3. Material Simplification

**Convert to PBR:**
```python
# Ensure materials use Principled BSDF (glTF standard)
for mat in bpy.data.materials:
    if not mat.use_nodes:
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    principled = nodes.get('Principled BSDF')

    if not principled:
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.get('Material Output')
        mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
```

## Common Pitfalls

### 1. Large File Sizes

**Problem:** Exported .glb files are 20+ MB

**Solutions:**
- Enable Draco compression (60-90% reduction)
- Reduce texture resolution (2048 → 1024 or 512)
- Use JPEG instead of PNG for textures
- Decimate geometry (target <50k triangles)
- Remove unused materials/textures

### 2. Missing Textures in Export

**Problem:** Textures don't appear in web viewer

**Solutions:**
- Ensure all images are saved (not packed)
- Use relative paths for textures
- Export with "Export Images" enabled
- Check image format compatibility (PNG/JPEG)

### 3. Animations Not Playing

**Problem:** Animations don't export or play incorrectly

**Solutions:**
- Ensure animations are on timeline (not NLA strips)
- Export with "Export Animations" enabled
- Check animation actions are assigned to objects
- Use "Bake Actions" for complex rigs

### 4. Materials Look Different

**Problem:** Materials render differently in web vs Blender

**Solutions:**
- Use Principled BSDF (maps to glTF PBR)
- Avoid custom shader nodes (won't export)
- Use supported texture types (Base Color, Metallic, Roughness, Normal, Emission)
- Test in glTF viewer before deploying

### 5. Slow Export Times

**Problem:** Export takes 10+ minutes

**Solutions:**
- Apply modifiers before export (don't export non-destructively)
- Reduce geometry complexity
- Remove unused data (orphan cleanup)
- Use command-line export (faster than GUI)

### 6. Performance Issues in Browser

**Problem:** Model lags in browser

**Solutions:**
- Generate LODs (Level of Detail)
- Use instancing for repeated objects
- Limit draw calls (merge objects, texture atlases)
- Reduce polygon count (<50k triangles)
- Optimize shaders (avoid transparency/refraction)

## Best Practices

### Pre-Export Checklist

```
☐ Apply all modifiers
☐ Merge vertices (remove doubles)
☐ Triangulate faces (if required)
☐ Optimize polygon count (<50k triangles)
☐ UV unwrap all meshes
☐ Bake materials (if complex)
☐ Resize textures (max 2048x2048)
☐ Use Principled BSDF materials
☐ Remove unused data (orphan cleanup)
☐ Name objects descriptively
☐ Set origin points correctly
☐ Apply transformations (Ctrl+A)
```

### Export Settings

```python
# Recommended glTF export settings
bpy.ops.export_scene.gltf(
    filepath='/output.glb',
    export_format='GLB',                # Binary format
    export_apply=True,                  # Apply modifiers
    export_image_format='JPEG',         # Smaller file size
    export_jpeg_quality=85,             # Quality vs size
    export_draco_mesh_compression_enable=True,  # Enable compression
    export_draco_mesh_compression_level=6,      # Balance speed/size
    export_animations=True,             # Include animations
    export_lights=False,                # Skip lights (recreate in code)
    export_cameras=False                # Skip cameras
)
```

## Resources

This skill includes:

### scripts/
- `batch_export.py` - Batch export .blend files to glTF
- `optimize_model.py` - Optimize geometry and textures for web
- `generate_lods.py` - Generate LOD copies automatically

### references/
- `gltf_export_guide.md` - Complete glTF export reference
- `bpy_api_reference.md` - Blender Python API quick reference
- `optimization_strategies.md` - Detailed optimization techniques

### assets/
- `export_template.blend` - Pre-configured export template
- `shader_library/` - Web-optimized PBR shaders

## Related Skills

- **threejs-webgl** - Load and render exported glTF models in Three.js
- **react-three-fiber** - Use glTF models in React applications
- **babylonjs-engine** - Alternative 3D engine for web
- **playcanvas-engine** - Game engine that supports glTF import
