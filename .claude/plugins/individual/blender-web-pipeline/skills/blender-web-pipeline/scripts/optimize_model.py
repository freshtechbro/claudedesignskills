#!/usr/bin/env python3
"""
Optimize Blender Model for Web

Usage:
    blender --background model.blend --python optimize_model.py
"""

import bpy

def optimize_mesh(obj, ratio=0.5):
    """Reduce polygon count."""
    if obj.type != 'MESH':
        return

    decimate = obj.modifiers.new(name='Decimate', type='DECIMATE')
    decimate.ratio = ratio
    decimate.use_collapse_triangulate = True

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier='Decimate')

    print(f"Optimized {obj.name}: {len(obj.data.polygons)} polygons")

# Optimize all meshes
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        optimize_mesh(obj, ratio=0.3)

print("Optimization complete")
