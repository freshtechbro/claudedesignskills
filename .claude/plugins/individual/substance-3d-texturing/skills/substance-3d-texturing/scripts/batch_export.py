#!/usr/bin/env python3
"""
Substance 3D Painter Batch Export Script

Exports all texture sets from the currently open Substance Painter project
using the PBR Metallic Roughness preset optimized for web.

Usage:
    # Run from Substance Painter: File → Python → Execute Script
    # Or load as plugin

Requirements:
    - Substance 3D Painter must be running
    - A project must be open
    - substance_painter module (available in Substance environment)

Example:
    import batch_export
    batch_export.export_all_web()

    # Or customize export path
    batch_export.export_all_web(export_path="C:/MyExports")
"""

try:
    import substance_painter.export
    import substance_painter.resource
    import substance_painter.textureset
    import substance_painter.project
except ImportError:
    print("ERROR: This script must be run inside Substance 3D Painter")
    print("Go to: File → Python → Execute Script")
    exit(1)


def export_all_web(export_path=None, resolution=1024):
    """
    Export all texture sets with web-optimized settings.

    Args:
        export_path (str): Output directory. If None, exports next to .spp file.
        resolution (int): Texture size (512, 1024, 2048, 4096).

    Returns:
        bool: True if export succeeded, False otherwise.
    """
    # Verify project is open
    if not substance_painter.project.is_open():
        print("ERROR: No project is open. Open a project first.")
        return False

    # Determine export path
    if export_path is None:
        project_path = substance_painter.project.file_path()
        if not project_path:
            print("ERROR: Project has no file path (save the project first)")
            return False
        export_path = project_path.replace('.spp', '_textures')

    print(f"Export directory: {export_path}")

    # Map resolution to sizeLog2
    size_map = {
        512: 9,
        1024: 10,
        2048: 11,
        4096: 12
    }

    if resolution not in size_map:
        print(f"ERROR: Invalid resolution {resolution}. Use 512, 1024, 2048, or 4096.")
        return False

    size_log2 = size_map[resolution]

    # Define export preset
    try:
        export_preset = substance_painter.resource.ResourceID(
            context="starter_assets",
            name="PBR Metallic Roughness"
        )
    except Exception as e:
        print(f"ERROR: Could not load export preset: {e}")
        return False

    # Build export configuration
    config = {
        "exportShaderParams": False,
        "exportPath": export_path,
        "defaultExportPreset": export_preset.url(),
        "exportList": [],
        "exportParameters": [{
            "parameters": {
                "fileFormat": "png",
                "bitDepth": "8",
                "dithering": True,
                "paddingAlgorithm": "infinite",
                "sizeLog2": size_log2
            }
        }]
    }

    # Add all texture sets to export list
    texture_sets = substance_painter.textureset.all_texture_sets()

    if not texture_sets:
        print("WARNING: No texture sets found in project")
        return False

    for texture_set in texture_sets:
        config["exportList"].append({
            "rootPath": texture_set.name()
        })
        print(f"Added to export queue: {texture_set.name()}")

    print(f"\nExporting {len(texture_sets)} texture set(s) at {resolution}×{resolution}...")

    # Execute export
    try:
        result = substance_painter.export.export_project_textures(config)

        if result.status == substance_painter.export.ExportStatus.Success:
            print("\n✓ Export completed successfully!")
            print(f"\nExported textures:")

            total_files = 0
            for stack, files in result.textures.items():
                print(f"\n  {stack}:")
                for file_path in files:
                    print(f"    - {file_path}")
                    total_files += 1

            print(f"\nTotal files exported: {total_files}")
            return True
        else:
            print(f"\n✗ Export failed: {result.message}")
            return False

    except ValueError as e:
        print(f"\n✗ Export configuration error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error during export: {e}")
        return False


def export_mobile_optimized(export_path=None):
    """
    Export with aggressive mobile optimization.

    Features:
    - 512×512 resolution
    - JPEG for baseColor (smaller file size)
    - PNG for data maps (lossless required)

    Args:
        export_path (str): Output directory. If None, exports to project_mobile/.

    Returns:
        bool: True if export succeeded, False otherwise.
    """
    if not substance_painter.project.is_open():
        print("ERROR: No project is open.")
        return False

    # Determine export path
    if export_path is None:
        project_path = substance_painter.project.file_path()
        if not project_path:
            print("ERROR: Project has no file path (save the project first)")
            return False
        export_path = project_path.replace('.spp', '_mobile')

    print(f"Mobile export directory: {export_path}")

    # Define export preset
    export_preset = substance_painter.resource.ResourceID(
        context="starter_assets",
        name="PBR Metallic Roughness"
    )

    # Build export configuration with mobile optimizations
    config = {
        "exportShaderParams": False,
        "exportPath": export_path,
        "defaultExportPreset": export_preset.url(),
        "exportList": [],
        "exportParameters": [
            {
                # Default: JPEG for baseColor
                "filter": {"outputMaps": ["$textureSet_baseColor"]},
                "parameters": {
                    "fileFormat": "jpeg",
                    "bitDepth": "8",
                    "sizeLog2": 9,  # 512×512
                    "paddingAlgorithm": "infinite"
                }
            },
            {
                # PNG for normal and metallicRoughness (data maps need lossless)
                "filter": {"outputMaps": ["$textureSet_normal", "$textureSet_metallicRoughness"]},
                "parameters": {
                    "fileFormat": "png",
                    "bitDepth": "8",
                    "sizeLog2": 9,  # 512×512
                    "paddingAlgorithm": "infinite"
                }
            }
        ]
    }

    # Add all texture sets
    for texture_set in substance_painter.textureset.all_texture_sets():
        config["exportList"].append({"rootPath": texture_set.name()})

    print(f"Exporting {len(substance_painter.textureset.all_texture_sets())} texture set(s) for mobile...")

    # Execute export
    try:
        result = substance_painter.export.export_project_textures(config)

        if result.status == substance_painter.export.ExportStatus.Success:
            print("\n✓ Mobile export completed!")
            return True
        else:
            print(f"\n✗ Export failed: {result.message}")
            return False

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def print_texture_sets():
    """Print all texture sets in the current project."""
    if not substance_painter.project.is_open():
        print("No project is open.")
        return

    texture_sets = substance_painter.textureset.all_texture_sets()

    if not texture_sets:
        print("No texture sets found in project.")
        return

    print(f"\nFound {len(texture_sets)} texture set(s):\n")

    for i, ts in enumerate(texture_sets, 1):
        print(f"{i}. {ts.name()}")
        print(f"   Layered: {ts.is_layered_material()}")
        resolution = ts.get_resolution()
        print(f"   Resolution: {resolution.width}×{resolution.height}")
        print()


def main():
    """Main entry point when script is executed directly."""
    print("=" * 60)
    print("Substance 3D Painter - Batch Export Script")
    print("=" * 60)

    if not substance_painter.project.is_open():
        print("\nERROR: No project is open.")
        print("Please open a Substance Painter project first.")
        return

    # Show project info
    project_name = substance_painter.project.name()
    print(f"\nProject: {project_name}")

    # Show texture sets
    print_texture_sets()

    # Perform export
    print("Starting web export (1024×1024)...")
    success = export_all_web(resolution=1024)

    if success:
        print("\n" + "=" * 60)
        print("Export complete! Check the output directory.")
        print("=" * 60)
    else:
        print("\nExport failed. See errors above.")


if __name__ == "__main__":
    main()
