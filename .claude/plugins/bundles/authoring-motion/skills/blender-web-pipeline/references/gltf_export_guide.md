# Blender glTF Export Complete Guide

Reference guide for glTF 2.0 export settings and options in Blender.

## Export Format Options

```python
export_format='GLB'  # or 'GLTF_SEPARATE' or 'GLTF_EMBEDDED'
```

- **GLB**: Single binary file (recommended for web)
- **GLTF_SEPARATE**: JSON + separate .bin + separate textures
- **GLTF_EMBEDDED**: JSON with embedded Base64 data (large file)

## All Export Parameters

```python
bpy.ops.export_scene.gltf(
    # File Settings
    filepath='/path/to/output.glb',
    export_format='GLB',  # 'GLB', 'GLTF_SEPARATE', 'GLTF_EMBEDDED'

    # Include Settings
    use_selection=False,  # Export selected objects only
    use_visible=False,  # Export visible objects only
    use_renderable=False,  # Export renderable objects only
    use_active_collection=False,  # Export active collection only
    use_active_scene=False,  # Export active scene only

    # Transform Settings
    export_yup=True,  # Y-axis up (default for glTF)
    export_apply=False,  # Apply modifiers (True recommended)

    # Data Settings
    export_texcoords=True,  # UV coordinates
    export_normals=True,  # Normals
    export_draco_mesh_compression_enable=False,  # Enable Draco compression
    export_draco_mesh_compression_level=6,  # 0-10 (higher = smaller + slower)
    export_draco_position_quantization=14,  # 8-14 bits
    export_draco_normal_quantization=10,  # 8-10 bits
    export_draco_texcoord_quantization=12,  # 8-12 bits
    export_draco_color_quantization=10,  # 8-10 bits
    export_draco_generic_quantization=12,  # 8-12 bits
    export_tangents=False,  # Tangents (auto-computed by engines)
    export_materials='EXPORT',  # 'EXPORT', 'PLACEHOLDER', 'NONE'
    export_colors=True,  # Vertex colors
    export_attributes=True,  # Custom attributes
    export_cameras=False,  # Export cameras
    export_lights=False,  # Export lights

    # Animation Settings
    export_animations=True,  # Export animations
    export_frame_range=True,  # Use scene frame range
    export_frame_step=1,  # Frame step
    export_force_sampling=True,  # Force sampling (all frames)
    export_nla_strips=True,  # Export NLA strips
    export_nla_strips_merged_animation_name='Animation',  # Merged animation name
    export_def_bones=False,  # Export deformation bones only
    export_current_frame=False,  # Export current frame
    export_skins=True,  # Export skinning data
    export_all_influences=False,  # Export all bone influences
    export_morph=True,  # Export shape keys
    export_morph_normal=True,  # Export shape key normals
    export_morph_tangent=False,  # Export shape key tangents

    # Image Settings
    export_image_format='AUTO',  # 'AUTO', 'JPEG', 'PNG'
    export_jpeg_quality=75,  # 0-100
    export_keep_originals=False,  # Keep original images

    # Extras
    export_extras=False,  # Export custom properties
    export_copyright='',  # Copyright notice
    export_custom_props=False,  # Export custom properties
)
```

## Recommended Presets

### Minimal (Smallest File)
```python
export_format='GLB',
export_apply=True,
export_image_format='JPEG',
export_jpeg_quality=75,
export_draco_mesh_compression_enable=True,
export_draco_mesh_compression_level=10,  # Max compression
export_animations=False,
export_cameras=False,
export_lights=False
```

### Standard (Balanced)
```python
export_format='GLB',
export_apply=True,
export_image_format='JPEG',
export_jpeg_quality=85,
export_draco_mesh_compression_enable=True,
export_draco_mesh_compression_level=6,
export_animations=True
```

### High Quality (Larger Files)
```python
export_format='GLB',
export_apply=True,
export_image_format='PNG',
export_draco_mesh_compression_enable=False,
export_animations=True,
export_morph=True
```
