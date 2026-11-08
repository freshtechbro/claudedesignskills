#!/usr/bin/env python3
"""
Lottie JSON Optimizer

Optimizes Lottie JSON files by removing whitespace, rounding numbers, and removing unnecessary data.

Usage:
    ./optimize_lottie.py animation.json                 # Output to stdout
    ./optimize_lottie.py animation.json -o optimized.json
"""

import json
import argparse
import sys

def round_number(value, precision=2):
    """Round number to specified precision."""
    if isinstance(value, (int, float)):
        return round(value, precision)
    return value

def optimize_object(obj, precision=2):
    """Recursively optimize object by rounding numbers."""
    if isinstance(obj, dict):
        return {k: optimize_object(v, precision) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [optimize_object(item, precision) for item in obj]
    elif isinstance(obj, float):
        return round(obj, precision)
    return obj

def optimize_lottie(input_path, output_path=None, precision=2):
    """Optimize Lottie JSON file."""
    try:
        # Read input
        with open(input_path, 'r') as f:
            data = json.load(f)

        # Optimize
        optimized = optimize_object(data, precision)

        # Write output
        json_str = json.dumps(optimized, separators=(',', ':'))

        if output_path:
            with open(output_path, 'w') as f:
                f.write(json_str)
            print(f"✅ Optimized: {input_path} → {output_path}")

            # Show size reduction
            import os
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            reduction = ((original_size - optimized_size) / original_size) * 100

            print(f"   Original: {original_size:,} bytes")
            print(f"   Optimized: {optimized_size:,} bytes")
            print(f"   Reduction: {reduction:.1f}%")
        else:
            print(json_str)

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Optimize Lottie JSON files")
    parser.add_argument('input', help="Input Lottie JSON file")
    parser.add_argument('-o', '--output', help="Output file path")
    parser.add_argument('-p', '--precision', type=int, default=2, help="Number precision (default: 2)")

    args = parser.parse_args()

    optimize_lottie(args.input, args.output, args.precision)

if __name__ == '__main__':
    main()
