#!/usr/bin/env python3
"""
Motion Variant Builder
======================

Interactive CLI tool to build Motion/Framer Motion variant configurations.

Usage:
    python3 variant_builder.py
    python3 variant_builder.py --preset fade --output variants.js
    python3 variant_builder.py --typescript

Presets:
    - fade: Fade in/out animation
    - slide: Slide animation (left, right, up, down)
    - scale: Scale animation
    - rotate: Rotation animation
    - stagger: Staggered children animation
    - modal: Modal enter/exit animation
    - page: Page transition animation
    - custom: Build from scratch

Features:
    - Interactive CLI for building variants
    - Multiple animation states
    - Transition configurations
    - Stagger settings for children
    - TypeScript support
    - Code generation
"""

import argparse
import sys
import json
from typing import Dict, List, Optional, Any


class VariantBuilder:
    """Build Motion variant configurations interactively."""

    PRESETS = {
        'fade': {
            'hidden': {
                'opacity': 0
            },
            'visible': {
                'opacity': 1,
                'transition': {'duration': 0.5}
            }
        },
        'slide': {
            'hidden': {
                'opacity': 0,
                'x': -100
            },
            'visible': {
                'opacity': 1,
                'x': 0,
                'transition': {'type': 'spring', 'stiffness': 300, 'damping': 30}
            }
        },
        'scale': {
            'hidden': {
                'opacity': 0,
                'scale': 0.8
            },
            'visible': {
                'opacity': 1,
                'scale': 1,
                'transition': {'duration': 0.3}
            }
        },
        'rotate': {
            'hidden': {
                'opacity': 0,
                'rotate': -180
            },
            'visible': {
                'opacity': 1,
                'rotate': 0,
                'transition': {'type': 'spring', 'stiffness': 200, 'damping': 20}
            }
        },
        'stagger': {
            'hidden': {
                'opacity': 0
            },
            'visible': {
                'opacity': 1,
                'transition': {
                    'staggerChildren': 0.1,
                    'delayChildren': 0.2
                }
            }
        },
        'modal': {
            'hidden': {
                'opacity': 0,
                'scale': 0.9,
                'y': 20
            },
            'visible': {
                'opacity': 1,
                'scale': 1,
                'y': 0,
                'transition': {
                    'type': 'spring',
                    'stiffness': 300,
                    'damping': 30
                }
            },
            'exit': {
                'opacity': 0,
                'scale': 0.9,
                'y': -20,
                'transition': {'duration': 0.2}
            }
        },
        'page': {
            'initial': {
                'opacity': 0,
                'x': 300
            },
            'in': {
                'opacity': 1,
                'x': 0,
                'transition': {'duration': 0.3}
            },
            'out': {
                'opacity': 0,
                'x': -300,
                'transition': {'duration': 0.3}
            }
        }
    }

    def __init__(self, preset: Optional[str] = None, typescript: bool = False):
        self.variants: Dict[str, Dict[str, Any]] = {}
        self.typescript = typescript

        if preset and preset in self.PRESETS:
            self.variants = self.PRESETS[preset].copy()

    def add_state(self, name: str, properties: Dict[str, Any]) -> None:
        """Add a variant state."""
        self.variants[name] = properties

    def generate_code(self) -> str:
        """Generate variant code."""
        if self.typescript:
            return self._generate_typescript()
        else:
            return self._generate_javascript()

    def _generate_javascript(self) -> str:
        """Generate JavaScript variant code."""
        code = "const variants = {\n"

        for state_name, properties in self.variants.items():
            code += f"  {state_name}: {{\n"
            code += self._format_properties(properties, indent=4)
            code += "  },\n"

        code += "}\n\nexport default variants"
        return code

    def _generate_typescript(self) -> str:
        """Generate TypeScript variant code."""
        code = "import type { Variants } from 'framer-motion'\n\n"
        code += "const variants: Variants = {\n"

        for state_name, properties in self.variants.items():
            code += f"  {state_name}: {{\n"
            code += self._format_properties(properties, indent=4)
            code += "  },\n"

        code += "}\n\nexport default variants"
        return code

    def _format_properties(self, properties: Dict[str, Any], indent: int = 0) -> str:
        """Format properties as JavaScript object."""
        lines = []
        indent_str = " " * indent

        for key, value in properties.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{key}: {{")
                lines.append(self._format_properties(value, indent + 2).rstrip())
                lines.append(f"{indent_str}}},")
            elif isinstance(value, str):
                lines.append(f"{indent_str}{key}: '{value}',")
            elif isinstance(value, bool):
                lines.append(f"{indent_str}{key}: {str(value).lower()},")
            else:
                lines.append(f"{indent_str}{key}: {value},")

        return "\n".join(lines) + "\n"

    def interactive_build(self) -> None:
        """Interactive CLI for building variants."""
        print("\n🎨 Motion Variant Builder - Interactive Mode\n")
        print("=" * 60)

        # Choose preset or custom
        print("\nChoose a starting point:")
        print("  1. fade        - Simple fade in/out")
        print("  2. slide       - Slide animation")
        print("  3. scale       - Scale animation")
        print("  4. rotate      - Rotation animation")
        print("  5. stagger     - Staggered children")
        print("  6. modal       - Modal enter/exit")
        print("  7. page        - Page transition")
        print("  8. custom      - Build from scratch")

        choice = input("\nSelect preset (1-8): ").strip()

        preset_map = {
            '1': 'fade',
            '2': 'slide',
            '3': 'scale',
            '4': 'rotate',
            '5': 'stagger',
            '6': 'modal',
            '7': 'page',
        }

        if choice in preset_map:
            preset = preset_map[choice]
            self.variants = self.PRESETS[preset].copy()
            print(f"\n✅ Loaded '{preset}' preset")
        else:
            print("\n📝 Building custom variants...")

        # Add/modify states
        while True:
            print("\n" + "=" * 60)
            print("Current variants:")
            for state_name in self.variants.keys():
                print(f"  - {state_name}")

            print("\nOptions:")
            print("  1. Add new state")
            print("  2. Modify existing state")
            print("  3. Remove state")
            print("  4. Preview code")
            print("  5. Done")

            option = input("\nChoose option (1-5): ").strip()

            if option == '1':
                self._add_state_interactive()
            elif option == '2':
                self._modify_state_interactive()
            elif option == '3':
                self._remove_state_interactive()
            elif option == '4':
                print("\n" + "=" * 60)
                print("Generated Code:")
                print("=" * 60)
                print(self.generate_code())
            elif option == '5':
                break

    def _add_state_interactive(self) -> None:
        """Add state interactively."""
        print("\n📝 Add New State")
        state_name = input("State name (e.g., 'hidden', 'visible', 'exit'): ").strip()

        if not state_name:
            print("❌ Invalid state name")
            return

        properties = self._build_properties_interactive()
        self.variants[state_name] = properties
        print(f"✅ Added state '{state_name}'")

    def _modify_state_interactive(self) -> None:
        """Modify state interactively."""
        if not self.variants:
            print("❌ No states to modify")
            return

        print("\n✏️  Modify State")
        print("Available states:")
        for i, name in enumerate(self.variants.keys(), 1):
            print(f"  {i}. {name}")

        choice = input("\nSelect state number: ").strip()
        try:
            state_name = list(self.variants.keys())[int(choice) - 1]
            print(f"\nModifying '{state_name}'...")
            properties = self._build_properties_interactive()
            self.variants[state_name] = properties
            print(f"✅ Modified state '{state_name}'")
        except (ValueError, IndexError):
            print("❌ Invalid selection")

    def _remove_state_interactive(self) -> None:
        """Remove state interactively."""
        if not self.variants:
            print("❌ No states to remove")
            return

        print("\n🗑️  Remove State")
        print("Available states:")
        for i, name in enumerate(self.variants.keys(), 1):
            print(f"  {i}. {name}")

        choice = input("\nSelect state number: ").strip()
        try:
            state_name = list(self.variants.keys())[int(choice) - 1]
            del self.variants[state_name]
            print(f"✅ Removed state '{state_name}'")
        except (ValueError, IndexError):
            print("❌ Invalid selection")

    def _build_properties_interactive(self) -> Dict[str, Any]:
        """Build properties interactively."""
        properties = {}

        print("\nAdd properties (leave empty to skip):")

        # Common animation properties
        opacity = input("  opacity (0-1): ").strip()
        if opacity:
            properties['opacity'] = float(opacity)

        x = input("  x position (px): ").strip()
        if x:
            properties['x'] = int(x)

        y = input("  y position (px): ").strip()
        if y:
            properties['y'] = int(y)

        scale = input("  scale (0-n): ").strip()
        if scale:
            properties['scale'] = float(scale)

        rotate = input("  rotate (degrees): ").strip()
        if rotate:
            properties['rotate'] = int(rotate)

        # Transition
        add_transition = input("\nAdd transition? (y/n): ").strip().lower()
        if add_transition == 'y':
            transition = self._build_transition_interactive()
            if transition:
                properties['transition'] = transition

        return properties

    def _build_transition_interactive(self) -> Dict[str, Any]:
        """Build transition interactively."""
        transition = {}

        print("\nTransition type:")
        print("  1. tween (duration-based)")
        print("  2. spring (physics-based)")
        print("  3. stagger (for children)")

        choice = input("Select type (1-3): ").strip()

        if choice == '1':
            duration = input("  duration (seconds): ").strip()
            if duration:
                transition['duration'] = float(duration)

            ease = input("  ease (linear/easeIn/easeOut/easeInOut): ").strip()
            if ease:
                transition['ease'] = ease

        elif choice == '2':
            transition['type'] = 'spring'

            stiffness = input("  stiffness (default 100): ").strip()
            if stiffness:
                transition['stiffness'] = int(stiffness)

            damping = input("  damping (default 10): ").strip()
            if damping:
                transition['damping'] = int(damping)

        elif choice == '3':
            stagger = input("  staggerChildren (seconds): ").strip()
            if stagger:
                transition['staggerChildren'] = float(stagger)

            delay = input("  delayChildren (seconds): ").strip()
            if delay:
                transition['delayChildren'] = float(delay)

        return transition


def main():
    parser = argparse.ArgumentParser(
        description='Build Motion variant configurations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--preset',
        choices=['fade', 'slide', 'scale', 'rotate', 'stagger', 'modal', 'page'],
        help='Use a preset variant configuration'
    )

    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    parser.add_argument(
        '--typescript',
        action='store_true',
        help='Generate TypeScript code'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    args = parser.parse_args()

    # Create builder
    builder = VariantBuilder(preset=args.preset, typescript=args.typescript)

    # Run interactive mode if requested or no preset given
    if args.interactive or (not args.preset and len(sys.argv) == 1):
        builder.interactive_build()

    # Generate code
    if builder.variants:
        code = builder.generate_code()

        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"\n✅ Variants generated → {args.output}")
        else:
            print("\n" + "=" * 60)
            print("Generated Code:")
            print("=" * 60)
            print(code)
    else:
        print("❌ No variants to generate")
        sys.exit(1)


if __name__ == '__main__':
    main()
