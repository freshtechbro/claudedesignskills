#!/usr/bin/env python3
"""
Component Importer

Assists with importing and customizing components from Magic UI and React Bits.
Generates installation commands and boilerplate code for selected components.

Usage:
    ./component_importer.py                      # Interactive mode
    ./component_importer.py --library magicui --component grid-pattern
    ./component_importer.py --library reactbits --component blur-text
"""

import sys
import argparse

# Magic UI components catalog
MAGIC_UI_COMPONENTS = {
    "grid-pattern": {
        "name": "Grid Pattern",
        "install": "npx shadcn@latest add https://magicui.design/r/grid-pattern",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": False
    },
    "animated-grid-pattern": {
        "name": "Animated Grid Pattern",
        "install": "npx shadcn@latest add https://magicui.design/r/animated-grid-pattern",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": True,
        "css_keyframes": ["grid-fade"]
    },
    "shimmer-button": {
        "name": "Shimmer Button",
        "install": "npx shadcn@latest add https://magicui.design/r/shimmer-button",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": True,
        "css_keyframes": ["shimmer-slide", "spin-around"]
    },
    "border-beam": {
        "name": "Border Beam",
        "install": "npx shadcn@latest add https://magicui.design/r/border-beam",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": True,
        "css_keyframes": ["beam"]
    },
    "marquee": {
        "name": "Marquee",
        "install": "npx shadcn@latest add https://magicui.design/r/marquee",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": True,
        "css_keyframes": ["marquee", "marquee-vertical"]
    },
    "spinning-text": {
        "name": "Spinning Text",
        "install": "npx shadcn@latest add https://magicui.design/r/spinning-text",
        "deps": ["motion", "clsx", "tailwind-merge"],
        "css_required": False
    },
    "bento-grid": {
        "name": "Bento Grid",
        "install": "Manual installation (copy from website)",
        "deps": ["@radix-ui/react-icons"],
        "css_required": False
    }
}

# React Bits components catalog
REACT_BITS_COMPONENTS = {
    "blur-text": {
        "name": "BlurText",
        "install": "Manual copy from reactbits.dev",
        "deps": ["framer-motion"],
        "path": "components/BlurText.jsx"
    },
    "count-up": {
        "name": "CountUp",
        "install": "Manual copy from reactbits.dev",
        "deps": ["framer-motion"],
        "path": "components/CountUp.jsx"
    },
    "magnet": {
        "name": "Magnet",
        "install": "Manual copy from reactbits.dev",
        "deps": ["framer-motion"],
        "path": "components/Magnet.jsx"
    },
    "dock": {
        "name": "Dock",
        "install": "Manual copy from reactbits.dev",
        "deps": ["framer-motion", "react-icons"],
        "path": "components/Dock.jsx"
    },
    "stepper": {
        "name": "Stepper",
        "install": "Manual copy from reactbits.dev",
        "deps": ["framer-motion"],
        "path": "components/Stepper.jsx"
    },
    "particles": {
        "name": "Particles (WebGL)",
        "install": "Manual copy from reactbits.dev",
        "deps": ["ogl"],
        "path": "components/Particles.jsx"
    },
    "plasma": {
        "name": "Plasma",
        "install": "Manual copy from reactbits.dev",
        "deps": ["ogl"],
        "path": "components/Plasma.jsx"
    },
    "aurora": {
        "name": "Aurora",
        "install": "Manual copy from reactbits.dev",
        "deps": [],
        "path": "components/Aurora.jsx"
    }
}


def print_magic_ui_instructions(component_key):
    """Print installation instructions for Magic UI component."""
    comp = MAGIC_UI_COMPONENTS.get(component_key)
    if not comp:
        print(f"Error: Component '{component_key}' not found in Magic UI catalog")
        return

    print(f"\n{'='*60}")
    print(f"Magic UI: {comp['name']}")
    print(f"{'='*60}\n")

    print("Step 1: Install component")
    print(f"  {comp['install']}\n")

    if comp['deps']:
        print("Step 2: Install dependencies")
        deps_cmd = "npm install " + " ".join(comp['deps'])
        print(f"  {deps_cmd}\n")

    if comp.get('css_required'):
        print("Step 3: Add CSS animations to globals.css")
        print("  See references/magic_ui_components.md for keyframes\n")

    print("Step 4: Ensure cn() utility exists")
    print("  lib/utils.ts should contain the cn() function\n")

    print("Usage example:")
    if component_key == "grid-pattern":
        print("""  import { GridPattern } from "@/components/ui/grid-pattern"

  <GridPattern
    squares={[[4, 4], [8, 2]]}
    className="[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]"
  />""")
    elif component_key == "shimmer-button":
        print("""  import { ShimmerButton } from "@/components/ui/shimmer-button"

  <ShimmerButton
    shimmerDuration="3s"
    className="px-8 py-3"
  >
    Click Me
  </ShimmerButton>""")
    elif component_key == "marquee":
        print("""  import { Marquee } from "@/components/ui/marquee"

  <Marquee pauseOnHover className="[--duration:40s]">
    {items.map((item) => <div key={item.id}>{item.content}</div>)}
  </Marquee>""")

    print()


def print_react_bits_instructions(component_key):
    """Print installation instructions for React Bits component."""
    comp = REACT_BITS_COMPONENTS.get(component_key)
    if not comp:
        print(f"Error: Component '{component_key}' not found in React Bits catalog")
        return

    print(f"\n{'='*60}")
    print(f"React Bits: {comp['name']}")
    print(f"{'='*60}\n")

    print("Step 1: Copy component code")
    print(f"  Visit https://reactbits.dev")
    print(f"  Find '{comp['name']}' component")
    print(f"  Copy code to: {comp['path']}\n")

    if comp['deps']:
        print("Step 2: Install dependencies")
        deps_cmd = "npm install " + " ".join(comp['deps'])
        print(f"  {deps_cmd}\n")

    print("Usage example:")
    if component_key == "blur-text":
        print("""  import BlurText from './components/BlurText'

  <BlurText
    text="Animated text reveal"
    delay={100}
    animateBy="words"
    className="text-5xl font-bold"
  />""")
    elif component_key == "count-up":
        print("""  import CountUp from './components/CountUp'

  <CountUp
    end={10000}
    duration={3}
    separator=","
    className="text-6xl font-bold"
  />""")
    elif component_key == "particles":
        print("""  import Particles from './components/Particles'

  <Particles
    particleCount={200}
    particleColors={['#FF6B6B', '#4ECDC4']}
    className="absolute inset-0"
  />""")

    print()


def interactive_mode():
    """Run interactive component selector."""
    print("\nComponent Importer - Interactive Mode")
    print("="*60)

    print("\nSelect library:")
    print("  1. Magic UI")
    print("  2. React Bits")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        print("\nMagic UI Components:")
        components = list(MAGIC_UI_COMPONENTS.keys())
        for idx, key in enumerate(components, 1):
            print(f"  {idx}. {MAGIC_UI_COMPONENTS[key]['name']}")

        comp_choice = input(f"\nSelect component (1-{len(components)}): ").strip()
        try:
            comp_idx = int(comp_choice) - 1
            if 0 <= comp_idx < len(components):
                print_magic_ui_instructions(components[comp_idx])
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")

    elif choice == "2":
        print("\nReact Bits Components:")
        components = list(REACT_BITS_COMPONENTS.keys())
        for idx, key in enumerate(components, 1):
            print(f"  {idx}. {REACT_BITS_COMPONENTS[key]['name']}")

        comp_choice = input(f"\nSelect component (1-{len(components)}): ").strip()
        try:
            comp_idx = int(comp_choice) - 1
            if 0 <= comp_idx < len(components):
                print_react_bits_instructions(components[comp_idx])
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    else:
        print("Invalid library choice")


def main():
    parser = argparse.ArgumentParser(
        description="Import and customize Magic UI or React Bits components"
    )
    parser.add_argument(
        "--library",
        choices=["magicui", "reactbits"],
        help="Component library (magicui or reactbits)"
    )
    parser.add_argument(
        "--component",
        help="Component name (e.g., 'grid-pattern', 'blur-text')"
    )

    args = parser.parse_args()

    if args.library and args.component:
        # CLI mode
        if args.library == "magicui":
            print_magic_ui_instructions(args.component)
        elif args.library == "reactbits":
            print_react_bits_instructions(args.component)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
