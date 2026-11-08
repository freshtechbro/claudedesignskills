#!/usr/bin/env blender --background --python
"""
Batch Export Blender Files to glTF

Usage:
    blender --background --python batch_export.py -- /input/dir /output/dir
"""

import bpy
import os
import sys

argv = sys.argv[argv.index("--") + 1:] if "--" in sys.argv else []
input_dir = argv[0] if argv else "/models"
output_dir = argv[1] if len(argv) > 1 else input_dir + "_gltf"

os.makedirs(output_dir, exist_ok=True)

blend_files = [f for f in os.listdir(input_dir) if f.endswith('.blend')]

for blend_file in blend_files:
    input_path = os.path.join(input_dir, blend_file)
    output_path = os.path.join(output_dir, blend_file.replace('.blend', '.glb'))

    bpy.ops.wm.open_mainfile(filepath=input_path)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        export_apply=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6
    )
    print(f"Exported: {blend_file}")
