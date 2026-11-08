#!/usr/bin/env python3
"""
Substance 3D Painter Export Preset Generator

Interactive tool for creating custom export preset JSON configurations.

Usage:
    # Interactive mode
    ./generate_export_preset.py

    # Quick presets
    ./generate_export_preset.py --preset gltf
    ./generate_export_preset.py --preset threejs
    ./generate_export_preset.py --preset orm

    # Output to file
    ./generate_export_preset.py --preset gltf --output my_preset.json

Presets:
    - gltf: glTF 2.0 standard (MetallicRoughness)
    - threejs: Three.js optimized (separate channels)
    - babylonjs: Babylon.js PBR format
    - orm: Occlusion-Roughness-Metallic packed
    - mobile: Mobile-optimized (512px, JPEG color)

Requirements:
    - Python 3.6+
    - Standard library only
"""

import json
import sys
import argparse


# Preset templates
PRESETS = {
    'gltf': {
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
                        "sizeLog2": 10
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
    },

    'threejs': {
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
                    "parameters": {"fileFormat": "jpeg", "bitDepth": "8", "sizeLog2": 10}
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
    },

    'babylonjs': {
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
    },

    'orm': {
        "exportPresets": [{
            "name": "Web_ORM",
            "maps": [
                {
                    "fileName": "$textureSet_baseColor",
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
                    "fileName": "$textureSet_ORM",
                    "channels": [
                        {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "ambientOcclusion"},
                        {"destChannel": "G", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "roughness"},
                        {"destChannel": "B", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "metallic"}
                    ],
                    "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 10}
                }
            ]
        }]
    },

    'mobile': {
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
                    "parameters": {"fileFormat": "jpeg", "bitDepth": "8", "sizeLog2": 9}
                },
                {
                    "fileName": "$textureSet_normal",
                    "channels": [
                        {"destChannel": "R", "srcChannel": "R", "srcMapType": "documentMap", "srcMapName": "normal"},
                        {"destChannel": "G", "srcChannel": "G", "srcMapType": "documentMap", "srcMapName": "normal"}
                    ],
                    "parameters": {"fileFormat": "png", "bitDepth": "8", "sizeLog2": 9}
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
}


def print_preset_info(preset_name):
    """Print information about a preset."""
    descriptions = {
        'gltf': "glTF 2.0 standard format with MetallicRoughness packing (OpenGL normals)",
        'threejs': "Three.js optimized with separate channels and JPEG color",
        'babylonjs': "Babylon.js PBR format with MetallicRoughness packing",
        'orm': "Occlusion-Roughness-Metallic packed format (most efficient)",
        'mobile': "Mobile-optimized with 512px resolution and aggressive compression"
    }

    if preset_name in descriptions:
        print(f"\n{preset_name.upper()} Preset:")
        print(f"  {descriptions[preset_name]}")


def generate_preset_json(preset_name):
    """Generate preset JSON configuration."""
    if preset_name not in PRESETS:
        print(f"ERROR: Unknown preset '{preset_name}'")
        print(f"Available presets: {', '.join(PRESETS.keys())}")
        return None

    return PRESETS[preset_name]


def print_usage_example(preset_name, output_file=None):
    """Print usage example for the generated preset."""
    print("\n" + "=" * 60)
    print("USAGE EXAMPLE (Python)")
    print("=" * 60)

    if output_file:
        print(f"""
import json
import substance_painter.export

# Load custom preset
with open('{output_file}', 'r') as f:
    custom_preset = json.load(f)

config = {{
    "exportPath": "C:/export",
    "exportPresets": custom_preset["exportPresets"],
    "exportList": [{{"rootPath": "MyAsset", "exportPreset": "{PRESETS[preset_name]['exportPresets'][0]['name']}"}}],
    "exportParameters": [{{
        "parameters": {{"paddingAlgorithm": "infinite"}}
    }}]
}}

result = substance_painter.export.export_project_textures(config)
""")
    else:
        print(f"""
import substance_painter.export

preset = {json.dumps(PRESETS[preset_name], indent=2)}

config = {{
    "exportPath": "C:/export",
    "exportPresets": preset["exportPresets"],
    "exportList": [{{"rootPath": "MyAsset", "exportPreset": "{PRESETS[preset_name]['exportPresets'][0]['name']}"}}]
}}

result = substance_painter.export.export_project_textures(config)
""")


def interactive_mode():
    """Interactive preset builder."""
    print("=" * 60)
    print("Substance 3D Painter - Export Preset Generator")
    print("=" * 60)

    print("\nAvailable presets:\n")

    for i, (name, _) in enumerate(PRESETS.items(), 1):
        print(f"{i}. {name}")
        print_preset_info(name)

    print()

    while True:
        try:
            choice = input("Select preset (1-5) or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                sys.exit(0)

            preset_index = int(choice) - 1
            preset_names = list(PRESETS.keys())

            if 0 <= preset_index < len(preset_names):
                preset_name = preset_names[preset_index]
                break
            else:
                print("Invalid selection. Try again.")

        except ValueError:
            print("Invalid input. Enter a number 1-5.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)

    # Generate preset
    preset_json = generate_preset_json(preset_name)

    print("\n" + "=" * 60)
    print(f"Generated {preset_name.upper()} Preset")
    print("=" * 60)
    print(json.dumps(preset_json, indent=2))

    # Ask to save
    save = input("\nSave to file? (y/n): ").strip().lower()

    if save == 'y':
        filename = input("Enter filename (default: export_preset.json): ").strip()
        if not filename:
            filename = "export_preset.json"

        if not filename.endswith('.json'):
            filename += '.json'

        with open(filename, 'w') as f:
            json.dump(preset_json, f, indent=2)

        print(f"\n✓ Preset saved to: {filename}")
        print_usage_example(preset_name, filename)
    else:
        print_usage_example(preset_name)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate custom Substance 3D Painter export presets"
    )

    parser.add_argument(
        '--preset',
        choices=list(PRESETS.keys()),
        help="Preset type (gltf, threejs, babylonjs, orm, mobile)"
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help="Output JSON file path"
    )

    args = parser.parse_args()

    # Interactive mode if no preset specified
    if args.preset is None:
        interactive_mode()
        return

    # Generate preset
    preset_json = generate_preset_json(args.preset)

    if preset_json is None:
        sys.exit(1)

    # Output to file or stdout
    if args.output_file:
        with open(args.output_file, 'w') as f:
            json.dump(preset_json, f, indent=2)

        print(f"✓ {args.preset.upper()} preset saved to: {args.output_file}")
        print_usage_example(args.preset, args.output_file)
    else:
        print(json.dumps(preset_json, indent=2))
        print_usage_example(args.preset)


if __name__ == "__main__":
    main()
