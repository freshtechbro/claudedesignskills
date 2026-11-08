#!/usr/bin/env python3
"""
Generate LOD (Level of Detail) Copies

Usage:
    blender --background model.blend --python generate_lods.py
"""

import bpy

def generate_lods(obj, levels=[0.75, 0.5, 0.25]):
    """Create LOD copies with decreasing detail."""
    for i, ratio in enumerate(levels):
        lod_obj = obj.copy()
        lod_obj.data = obj.data.copy()
        lod_obj.name = f"{obj.name}_LOD{i}"

        bpy.context.collection.objects.link(lod_obj)

        decimate = lod_obj.modifiers.new(name='Decimate', type='DECIMATE')
        decimate.ratio = ratio

        bpy.context.view_layer.objects.active = lod_obj
        bpy.ops.object.modifier_apply(modifier='Decimate')

        print(f"Created {lod_obj.name}: {len(lod_obj.data.polygons)} polygons")

# Generate LODs for all meshes
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        generate_lods(obj)

print("LOD generation complete")
