# Blender Python API Quick Reference

Essential bpy (Blender Python) API commands for automation.

## Accessing Data

```python
import bpy

# Scene and Objects
bpy.context.scene  # Active scene
bpy.data.objects  # All objects
bpy.data.objects['Name']  # Get object by name
bpy.context.selected_objects  # Selected objects
bpy.context.active_object  # Active object

# Collections
bpy.data.collections  # All collections
bpy.context.collection  # Active collection

# Materials and Textures
bpy.data.materials  # All materials
bpy.data.images  # All images/textures

# Meshes
bpy.data.meshes  # All mesh data
```

## Object Operations

```python
# Selection
bpy.ops.object.select_all(action='SELECT')  # Select all
bpy.ops.object.select_all(action='DESELECT')  # Deselect all
obj.select_set(True)  # Select specific object

# Transformation
obj.location = (x, y, z)
obj.rotation_euler = (rx, ry, rz)
obj.scale = (sx, sy, sz)

# Modifiers
modifier = obj.modifiers.new(name='Name', type='TYPE')
bpy.ops.object.modifier_apply(modifier='Name')

# Duplication
new_obj = obj.copy()
new_obj.data = obj.data.copy()
bpy.context.collection.objects.link(new_obj)
```

## Mesh Editing

```python
# Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

# Common Operations
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)  # Merge vertices
bpy.ops.mesh.quads_convert_to_tris()  # Triangulate
bpy.ops.uv.smart_project()  # UV unwrap

# Return to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')
```

## File Operations

```python
# Open File
bpy.ops.wm.open_mainfile(filepath='/path/to/file.blend')

# Save File
bpy.ops.wm.save_as_mainfile(filepath='/path/to/file.blend')

# Import/Export
bpy.ops.import_scene.obj(filepath='/path/to/model.obj')
bpy.ops.export_scene.gltf(filepath='/path/to/model.glb')
```
