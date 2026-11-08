#!/usr/bin/env python3
"""
Babylon.js Mesh Builder

Interactive tool for generating Babylon.js mesh creation code.
Supports all MeshBuilder shapes with full parameter customization.

Usage:
    python3 mesh_builder.py --shape sphere --name mySphere --output meshes.js
    python3 mesh_builder.py --shape box --params '{"size": 2}' --typescript
    python3 mesh_builder.py --interactive
"""

import argparse
import json
import sys
from pathlib import Path


MESH_SHAPES = {
    'box': {
        'description': 'Rectangular box',
        'params': {
            'size': {'type': 'number', 'default': 1, 'description': 'Overall size'},
            'width': {'type': 'number', 'description': 'Width (X axis)'},
            'height': {'type': 'number', 'description': 'Height (Y axis)'},
            'depth': {'type': 'number', 'description': 'Depth (Z axis)'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'sphere': {
        'description': 'Sphere/ellipsoid',
        'params': {
            'diameter': {'type': 'number', 'default': 1, 'description': 'Overall diameter'},
            'diameterX': {'type': 'number', 'description': 'X diameter'},
            'diameterY': {'type': 'number', 'description': 'Y diameter'},
            'diameterZ': {'type': 'number', 'description': 'Z diameter'},
            'segments': {'type': 'number', 'default': 32, 'description': 'Segments'},
            'arc': {'type': 'number', 'default': 1, 'description': 'Horizontal coverage (0-1)'},
            'slice': {'type': 'number', 'default': 1, 'description': 'Vertical coverage (0-1)'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'cylinder': {
        'description': 'Cylinder/cone',
        'params': {
            'height': {'type': 'number', 'default': 2, 'description': 'Height'},
            'diameter': {'type': 'number', 'default': 1, 'description': 'Overall diameter'},
            'diameterTop': {'type': 'number', 'description': 'Top diameter (for cone)'},
            'diameterBottom': {'type': 'number', 'description': 'Bottom diameter'},
            'tessellation': {'type': 'number', 'default': 24, 'description': 'Radial segments'},
            'subdivisions': {'type': 'number', 'default': 1, 'description': 'Height subdivisions'},
            'arc': {'type': 'number', 'default': 1, 'description': 'Arc coverage (0-1)'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'plane': {
        'description': 'Flat plane',
        'params': {
            'size': {'type': 'number', 'default': 1, 'description': 'Overall size'},
            'width': {'type': 'number', 'description': 'Width'},
            'height': {'type': 'number', 'description': 'Height'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'ground': {
        'description': 'Ground plane',
        'params': {
            'width': {'type': 'number', 'default': 1, 'description': 'Width'},
            'height': {'type': 'number', 'default': 1, 'description': 'Height (depth)'},
            'subdivisions': {'type': 'number', 'default': 1, 'description': 'Subdivisions'},
            'subdivisionsX': {'type': 'number', 'description': 'X subdivisions'},
            'subdivisionsY': {'type': 'number', 'description': 'Y subdivisions'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'torus': {
        'description': 'Torus (donut)',
        'params': {
            'diameter': {'type': 'number', 'default': 1, 'description': 'Overall diameter'},
            'thickness': {'type': 'number', 'default': 0.5, 'description': 'Tube thickness'},
            'tessellation': {'type': 'number', 'default': 16, 'description': 'Radial segments'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'torus-knot': {
        'description': 'Torus knot',
        'params': {
            'radius': {'type': 'number', 'default': 2, 'description': 'Overall radius'},
            'tube': {'type': 'number', 'default': 0.5, 'description': 'Tube radius'},
            'radialSegments': {'type': 'number', 'default': 32, 'description': 'Radial segments'},
            'tubularSegments': {'type': 'number', 'default': 32, 'description': 'Tube segments'},
            'p': {'type': 'number', 'default': 2, 'description': 'P parameter'},
            'q': {'type': 'number', 'default': 3, 'description': 'Q parameter'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'capsule': {
        'description': 'Capsule (cylinder with rounded ends)',
        'params': {
            'radius': {'type': 'number', 'default': 0.5, 'description': 'Radius'},
            'height': {'type': 'number', 'default': 2, 'description': 'Height'},
            'radiusTop': {'type': 'number', 'description': 'Top radius'},
            'radiusBottom': {'type': 'number', 'description': 'Bottom radius'},
            'tessellation': {'type': 'number', 'default': 16, 'description': 'Segments'},
            'subdivisions': {'type': 'number', 'default': 1, 'description': 'Height subdivisions'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'lines': {
        'description': 'Line segments',
        'params': {
            'points': {'type': 'vector3[]', 'description': 'Array of Vector3 points'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'ribbon': {
        'description': 'Ribbon from path array',
        'params': {
            'pathArray': {'type': 'vector3[][]', 'description': '2D array of Vector3 paths'},
            'closeArray': {'type': 'boolean', 'default': False, 'description': 'Close the ribbon'},
            'closePath': {'type': 'boolean', 'default': False, 'description': 'Close each path'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'tube': {
        'description': 'Tube along path',
        'params': {
            'path': {'type': 'vector3[]', 'description': 'Path curve'},
            'radius': {'type': 'number', 'default': 1, 'description': 'Tube radius'},
            'tessellation': {'type': 'number', 'default': 64, 'description': 'Radial segments'},
            'cap': {'type': 'number', 'default': 0, 'description': 'Cap mode (0-3)'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'polyhedron': {
        'description': 'Regular polyhedron',
        'params': {
            'type': {'type': 'number', 'default': 0, 'description': 'Type (0-19)'},
            'size': {'type': 'number', 'default': 1, 'description': 'Size'},
            'sizeX': {'type': 'number', 'description': 'X size'},
            'sizeY': {'type': 'number', 'description': 'Y size'},
            'sizeZ': {'type': 'number', 'description': 'Z size'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    },
    'icosphere': {
        'description': 'Geodesic sphere',
        'params': {
            'radius': {'type': 'number', 'default': 1, 'description': 'Radius'},
            'radiusX': {'type': 'number', 'description': 'X radius'},
            'radiusY': {'type': 'number', 'description': 'Y radius'},
            'radiusZ': {'type': 'number', 'description': 'Z radius'},
            'subdivisions': {'type': 'number', 'default': 4, 'description': 'Subdivisions'},
            'flat': {'type': 'boolean', 'default': True, 'description': 'Flat shading'},
            'updatable': {'type': 'boolean', 'default': False}
        }
    }
}

MATERIAL_PRESETS = {
    'standard': {
        'description': 'Basic Standard Material',
        'code': """const material = new StandardMaterial('{name}Material', scene);
material.diffuseColor = new Color3(1, 0, 0);
material.specularColor = new Color3(0.5, 0.5, 0.5);
material.specularPower = 32;
{mesh}.material = material;"""
    },
    'pbr': {
        'description': 'PBR Material',
        'code': """const material = new PBRMaterial('{name}Material', scene);
material.metallic = 1.0;
material.roughness = 0.3;
material.baseColor = new Color3(0.9, 0.9, 0.9);
{mesh}.material = material;"""
    },
    'textured': {
        'description': 'Textured Standard Material',
        'code': """const material = new StandardMaterial('{name}Material', scene);
material.diffuseTexture = new Texture('path/to/texture.jpg', scene);
{mesh}.material = material;"""
    }
}


def generate_mesh_code(shape, name, params, use_typescript, material_preset=None):
    """Generate mesh creation code."""
    # Convert shape name
    shape_func = ''.join(word.capitalize() for word in shape.split('-'))

    # Build parameters
    param_strs = []
    for key, value in params.items():
        if isinstance(value, bool):
            param_strs.append(f'{key}: {str(value).lower()}')
        elif isinstance(value, (int, float)):
            param_strs.append(f'{key}: {value}')
        elif isinstance(value, str):
            param_strs.append(f'{key}: {value}')  # Assume already formatted

    params_str = ', '.join(param_strs) if param_strs else ''

    # Generate code
    code = f"const {name} = Create{shape_func}('{name}', {{ {params_str} }}, scene);"

    # Add material if specified
    if material_preset and material_preset in MATERIAL_PRESETS:
        material_code = MATERIAL_PRESETS[material_preset]['code'].format(
            name=name,
            mesh=name
        )
        code = f"{code}\n\n{material_code}"

    return code


def generate_imports(shapes, use_typescript, include_materials):
    """Generate imports for mesh builders."""
    ext = '' if use_typescript else '.js'
    imports = set()

    # Shape imports
    for shape in shapes:
        shape_func = ''.join(word.capitalize() for word in shape.split('-'))
        builder_name = shape.split('-')[0] + 'Builder'  # e.g., boxBuilder, sphereBuilder

        if shape in ['lines', 'ribbon', 'tube']:
            imports.add(f"import {{ Create{shape_func} }} from '@babylonjs/core/Meshes/Builders/{shape}Builder{ext}';")
        else:
            imports.add(f"import {{ Create{shape_func} }} from '@babylonjs/core/Meshes/Builders/{builder_name}{ext}';")

    # Material imports
    if include_materials:
        imports.add(f"import {{ StandardMaterial }} from '@babylonjs/core/Materials/standardMaterial{ext}';")
        imports.add(f"import {{ PBRMaterial }} from '@babylonjs/core/Materials/PBR/pbrMaterial{ext}';")
        imports.add(f"import {{ Texture }} from '@babylonjs/core/Materials/Textures/texture{ext}';")
        imports.add(f"import {{ Color3 }} from '@babylonjs/core/Maths/math.color{ext}';")

    return '\n'.join(sorted(imports))


def interactive_mode():
    """Interactive CLI for mesh building."""
    print("\n🎨 Babylon.js Mesh Builder - Interactive Mode\n")

    meshes = []

    while True:
        # Shape selection
        print("\nSelect mesh shape:")
        shapes_list = list(MESH_SHAPES.keys())
        for i, shape in enumerate(shapes_list, 1):
            desc = MESH_SHAPES[shape]['description']
            print(f"  {i:2d}. {shape:15s} - {desc}")

        shape_choice = input("\nEnter number (or 'done' to finish): ").strip()

        if shape_choice.lower() == 'done':
            break

        shape = shapes_list[int(shape_choice) - 1]

        # Mesh name
        default_name = f"{shape.replace('-', '')}1"
        name = input(f"\nMesh name (default: {default_name}): ").strip() or default_name

        # Parameters
        print(f"\nConfigure {shape} parameters (press Enter for defaults):")
        params = {}
        for param_name, param_info in MESH_SHAPES[shape]['params'].items():
            if param_info['type'] in ['vector3[]', 'vector3[][]']:
                # Skip complex types in interactive mode
                continue

            prompt = f"  {param_name}"
            if 'default' in param_info:
                prompt += f" (default: {param_info['default']})"
            if 'description' in param_info:
                prompt += f" - {param_info['description']}"
            prompt += ": "

            value = input(prompt).strip()

            if value:
                if param_info['type'] == 'boolean':
                    params[param_name] = value.lower() in ['true', 'yes', 'y', '1']
                elif param_info['type'] == 'number':
                    params[param_name] = float(value) if '.' in value else int(value)
                else:
                    params[param_name] = value

        # Material
        print("\nAdd material?")
        print("  1. None")
        print("  2. Standard Material")
        print("  3. PBR Material")
        print("  4. Textured Material")

        material_choice = input("\nEnter number (default: 1): ").strip() or "1"
        material_preset = None
        if material_choice == '2':
            material_preset = 'standard'
        elif material_choice == '3':
            material_preset = 'pbr'
        elif material_choice == '4':
            material_preset = 'textured'

        meshes.append({
            'shape': shape,
            'name': name,
            'params': params,
            'material': material_preset
        })

        print(f"\n✅ Added {name}")

    if not meshes:
        print("\n❌ No meshes created")
        return

    # Generate code
    use_typescript = input("\nGenerate TypeScript? (y/N): ").strip().lower() == 'y'

    ext = 'ts' if use_typescript else 'js'
    output_file = input(f"\nOutput file (default: meshes.{ext}): ").strip() or f"meshes.{ext}"

    # Build code
    shapes = list(set(m['shape'] for m in meshes))
    has_materials = any(m['material'] for m in meshes)

    imports = generate_imports(shapes, use_typescript, has_materials)

    mesh_codes = []
    for mesh in meshes:
        code = generate_mesh_code(
            mesh['shape'],
            mesh['name'],
            mesh['params'],
            use_typescript,
            mesh['material']
        )
        mesh_codes.append(code)

    final_code = f"""// Generated by Babylon.js Mesh Builder
{imports}

export function createMeshes(scene{': Scene' if use_typescript else ''}) {{
  {chr(10).join('  ' + line for mc in mesh_codes for line in mc.split(chr(10)))}
}}
"""

    Path(output_file).write_text(final_code)
    print(f"\n✅ Generated: {output_file}")
    print(f"📝 Created {len(meshes)} mesh(es)")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Babylon.js mesh creation code',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--shape',
        choices=list(MESH_SHAPES.keys()),
        help='Mesh shape'
    )

    parser.add_argument(
        '--name',
        default='mesh1',
        help='Mesh name (default: mesh1)'
    )

    parser.add_argument(
        '--params',
        type=json.loads,
        default={},
        help='Mesh parameters as JSON'
    )

    parser.add_argument(
        '--material',
        choices=list(MATERIAL_PRESETS.keys()),
        help='Material preset'
    )

    parser.add_argument(
        '--typescript',
        action='store_true',
        help='Generate TypeScript'
    )

    parser.add_argument(
        '--output',
        help='Output file'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode'
    )

    parser.add_argument(
        '--list-shapes',
        action='store_true',
        help='List available shapes'
    )

    args = parser.parse_args()

    # List shapes
    if args.list_shapes:
        print("\nAvailable mesh shapes:\n")
        for shape, info in MESH_SHAPES.items():
            print(f"  {shape}:")
            print(f"    {info['description']}")
            print(f"    Parameters:")
            for param, details in info['params'].items():
                default = f" (default: {details['default']})" if 'default' in details else ""
                desc = details.get('description', '')
                print(f"      - {param}: {details['type']}{default} - {desc}")
            print()
        return

    # Interactive mode
    if args.interactive or not args.shape:
        interactive_mode()
        return

    # Generate from args
    ext = 'ts' if args.typescript else 'js'
    output_file = args.output or f"mesh_{args.name}.{ext}"

    shapes = [args.shape]
    has_materials = args.material is not None

    imports = generate_imports(shapes, args.typescript, has_materials)
    mesh_code = generate_mesh_code(
        args.shape,
        args.name,
        args.params,
        args.typescript,
        args.material
    )

    final_code = f"""// Generated by Babylon.js Mesh Builder
{imports}

export function createMesh(scene{': Scene' if args.typescript else ''}) {{
  {chr(10).join('  ' + line for line in mesh_code.split(chr(10)))}
}}
"""

    Path(output_file).write_text(final_code)
    print(f"✅ Generated: {output_file}")


if __name__ == '__main__':
    main()
