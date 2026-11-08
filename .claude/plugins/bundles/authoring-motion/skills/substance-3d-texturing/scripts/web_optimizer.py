#!/usr/bin/env python3
"""
Web Texture Optimizer

Post-processes exported textures from Substance 3D Painter for optimal web delivery.
Performs resizing, format conversion, and reports file size savings.

Features:
- Resize textures to target resolution
- Convert baseColor to JPEG (lossy compression)
- Keep data maps as PNG (lossless)
- Generate multiple LOD levels
- Report file size savings

Usage:
    ./web_optimizer.py <input_directory> [options]

    ./web_optimizer.py C:/exports/MyAsset --resolution 1024
    ./web_optimizer.py C:/exports/MyAsset --lod 3
    ./web_optimizer.py C:/exports/MyAsset --jpeg-quality 80

Requirements:
    - Python 3.6+
    - Pillow library (optional, for image processing)
      Install: pip install Pillow
    - If Pillow not available, provides instructions for manual optimization

Note:
    This script uses only standard library when Pillow is not installed.
    With Pillow, it can perform automatic image processing.
"""

import os
import sys
import argparse
from pathlib import Path


def check_pillow():
    """Check if Pillow is installed."""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False


def get_file_size_mb(file_path):
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)


def resize_texture(input_path, output_path, target_size, quality=85):
    """
    Resize texture and optionally convert format.

    Args:
        input_path (str): Input image path
        output_path (str): Output image path
        target_size (int): Target resolution (width = height)
        quality (int): JPEG quality (1-100)

    Returns:
        bool: Success
    """
    try:
        from PIL import Image

        img = Image.open(input_path)

        # Resize with high-quality resampling
        resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)

        # Save with appropriate settings
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            resized.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif output_path.lower().endswith('.png'):
            resized.save(output_path, 'PNG', optimize=True)
        else:
            resized.save(output_path)

        return True

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def analyze_directory(input_dir):
    """
    Analyze texture directory and categorize files.

    Args:
        input_dir (str): Input directory path

    Returns:
        dict: Categorized texture files
    """
    textures = {
        'baseColor': [],
        'normal': [],
        'metallicRoughness': [],
        'emissive': [],
        'other': []
    }

    for file_path in Path(input_dir).glob('*.png'):
        file_name = file_path.name.lower()

        if 'basecolor' in file_name or '_color' in file_name or '_diffuse' in file_name:
            textures['baseColor'].append(file_path)
        elif 'normal' in file_name:
            textures['normal'].append(file_path)
        elif 'metallic' in file_name or 'roughness' in file_name:
            textures['metallicRoughness'].append(file_path)
        elif 'emissive' in file_name:
            textures['emissive'].append(file_path)
        else:
            textures['other'].append(file_path)

    # Also check for existing JPEGs
    for file_path in Path(input_dir).glob('*.jpg'):
        textures['baseColor'].append(file_path)

    return textures


def optimize_directory(input_dir, output_dir, target_resolution=1024, jpeg_quality=80):
    """
    Optimize all textures in a directory.

    Args:
        input_dir (str): Input directory
        output_dir (str): Output directory
        target_resolution (int): Target texture size
        jpeg_quality (int): JPEG quality (1-100)

    Returns:
        dict: Optimization statistics
    """
    if not check_pillow():
        print("ERROR: Pillow library not installed.")
        print("Install with: pip install Pillow")
        print("\nAlternatively, use manual optimization tools:")
        print("  - ImageMagick: convert input.png -resize 1024x1024 output.png")
        print("  - pngquant: pngquant --quality 80-100 input.png")
        print("  - TinyPNG: https://tinypng.com/")
        return None

    from PIL import Image

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Analyze input directory
    textures = analyze_directory(input_dir)

    stats = {
        'files_processed': 0,
        'original_size_mb': 0,
        'optimized_size_mb': 0
    }

    print(f"\nOptimizing textures to {target_resolution}×{target_resolution}...")
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}\n")

    # Process baseColor textures (convert to JPEG)
    for file_path in textures['baseColor']:
        original_size = get_file_size_mb(file_path)
        stats['original_size_mb'] += original_size

        output_name = file_path.stem + '.jpg'
        output_path = os.path.join(output_dir, output_name)

        print(f"Processing {file_path.name} → {output_name} (JPEG {jpeg_quality}%)")

        if resize_texture(str(file_path), output_path, target_resolution, jpeg_quality):
            optimized_size = get_file_size_mb(output_path)
            stats['optimized_size_mb'] += optimized_size
            stats['files_processed'] += 1

            savings = ((original_size - optimized_size) / original_size) * 100
            print(f"  {original_size:.2f} MB → {optimized_size:.2f} MB (-{savings:.1f}%)\n")

    # Process data maps (keep as PNG)
    for category in ['normal', 'metallicRoughness', 'emissive', 'other']:
        for file_path in textures[category]:
            original_size = get_file_size_mb(file_path)
            stats['original_size_mb'] += original_size

            output_name = file_path.name
            output_path = os.path.join(output_dir, output_name)

            print(f"Processing {file_path.name} (PNG)")

            if resize_texture(str(file_path), output_path, target_resolution):
                optimized_size = get_file_size_mb(output_path)
                stats['optimized_size_mb'] += optimized_size
                stats['files_processed'] += 1

                savings = ((original_size - optimized_size) / original_size) * 100
                print(f"  {original_size:.2f} MB → {optimized_size:.2f} MB (-{savings:.1f}%)\n")

    return stats


def generate_lod_levels(input_dir, output_base_dir, levels=3):
    """
    Generate multiple LOD levels from input textures.

    Args:
        input_dir (str): Input directory with original textures
        output_base_dir (str): Base output directory
        levels (int): Number of LOD levels (1-4)

    Returns:
        bool: Success
    """
    if not check_pillow():
        print("ERROR: Pillow library required for LOD generation.")
        return False

    # LOD resolution mapping
    lod_resolutions = {
        0: 2048,  # LOD0 - highest detail
        1: 1024,  # LOD1 - medium detail
        2: 512,   # LOD2 - low detail
        3: 256    # LOD3 - very low detail
    }

    print(f"\nGenerating {levels} LOD level(s)...\n")

    for lod in range(levels):
        resolution = lod_resolutions[lod]
        output_dir = os.path.join(output_base_dir, f'LOD{lod}')

        print(f"LOD{lod}: {resolution}×{resolution}")
        print(f"Output: {output_dir}\n")

        stats = optimize_directory(input_dir, output_dir, resolution)

        if stats:
            print(f"LOD{lod} complete: {stats['files_processed']} files")
            print(f"Total size: {stats['optimized_size_mb']:.2f} MB\n")
            print("-" * 60 + "\n")

    return True


def print_manual_instructions(input_dir):
    """Print manual optimization instructions when Pillow is not available."""
    print("\n" + "=" * 60)
    print("MANUAL OPTIMIZATION INSTRUCTIONS")
    print("=" * 60)
    print("\nSince Pillow is not installed, use these tools:\n")

    print("1. ImageMagick (batch processing):")
    print("   # Resize to 1024×1024")
    print(f"   for file in {input_dir}/*.png; do")
    print("     convert \"$file\" -resize 1024x1024 \"optimized_$(basename $file)\"")
    print("   done\n")

    print("2. pngquant (PNG compression):")
    print("   # Compress PNGs (lossy but smaller)")
    print(f"   pngquant --quality 80-100 {input_dir}/*.png\n")

    print("3. cwebp (WebP conversion - best for web):")
    print("   # Convert to WebP (90% smaller than PNG)")
    print(f"   for file in {input_dir}/*_baseColor.png; do")
    print("     cwebp -q 80 \"$file\" -o \"$(basename $file .png).webp\"")
    print("   done\n")

    print("4. Online tools:")
    print("   - TinyPNG: https://tinypng.com/")
    print("   - Squoosh: https://squoosh.app/")
    print("\n" + "=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Optimize Substance 3D Painter textures for web delivery"
    )

    parser.add_argument(
        'input_dir',
        help="Input directory containing exported textures"
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        help="Output directory (default: input_dir_optimized)"
    )

    parser.add_argument(
        '-r', '--resolution',
        type=int,
        default=1024,
        choices=[256, 512, 1024, 2048, 4096],
        help="Target resolution (default: 1024)"
    )

    parser.add_argument(
        '-q', '--jpeg-quality',
        type=int,
        default=80,
        choices=range(1, 101),
        metavar='1-100',
        help="JPEG quality for baseColor (default: 80)"
    )

    parser.add_argument(
        '--lod',
        type=int,
        choices=[1, 2, 3, 4],
        help="Generate LOD levels (1-4)"
    )

    args = parser.parse_args()

    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"ERROR: Input directory not found: {args.input_dir}")
        sys.exit(1)

    # Determine output directory
    if args.output_dir is None:
        args.output_dir = args.input_dir + '_optimized'

    print("=" * 60)
    print("Web Texture Optimizer")
    print("=" * 60)

    # Check if Pillow is available
    if not check_pillow():
        print("\nWARNING: Pillow library not installed.")
        print_manual_instructions(args.input_dir)
        sys.exit(1)

    # Generate LOD levels or single optimization
    if args.lod:
        success = generate_lod_levels(args.input_dir, args.output_dir, args.lod)
        if not success:
            sys.exit(1)
    else:
        stats = optimize_directory(
            args.input_dir,
            args.output_dir,
            args.resolution,
            args.jpeg_quality
        )

        if stats is None:
            sys.exit(1)

        # Print summary
        print("=" * 60)
        print("OPTIMIZATION SUMMARY")
        print("=" * 60)
        print(f"Files processed: {stats['files_processed']}")
        print(f"Original size: {stats['original_size_mb']:.2f} MB")
        print(f"Optimized size: {stats['optimized_size_mb']:.2f} MB")

        total_savings = stats['original_size_mb'] - stats['optimized_size_mb']
        savings_percent = (total_savings / stats['original_size_mb']) * 100

        print(f"Total savings: {total_savings:.2f} MB ({savings_percent:.1f}%)")
        print("=" * 60)

    print(f"\nOptimized textures saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
