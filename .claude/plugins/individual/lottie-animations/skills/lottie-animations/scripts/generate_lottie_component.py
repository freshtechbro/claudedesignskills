#!/usr/bin/env python3
"""
Lottie Component Generator

Generates React, Vue, or Svelte Lottie component boilerplate with common patterns.

Usage:
    ./generate_lottie_component.py                          # Interactive mode
    ./generate_lottie_component.py --framework react --type basic
    ./generate_lottie_component.py --framework vue --type interactive
"""

import argparse
import sys

TEMPLATES = {
    'react_basic': '''import React from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export const {ComponentName} = () => {
  return (
    <DotLottieReact
      src="{animationSrc}"
      loop
      autoplay
      style=\u007b\u007b height: {height}, width: {width} \u007d\u007d
    />
  );
};
''',
    'react_interactive': '''import React, \u007b useState \u007d from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

export const {ComponentName} = () => {
  const [dotLottie, setDotLottie] = useState(null);

  const handlePlay = () => dotLottie?.play();
  const handlePause = () => dotLottie?.pause();
  const handleStop = () => dotLottie?.stop();

  return (
    <div>
      <DotLottieReact
        src="{animationSrc}"
        loop
        autoplay=\u007bfalse\u007d
        dotLottieRefCallback=\u007bsetDotLottie\u007d
        style=\u007b\u007b height: {height}, width: {width} \u007d\u007d
      />
      <div style=\u007b\u007b marginTop: 16 \u007d\u007d>
        <button onClick=\u007bhandlePlay\u007d>Play</button>
        <button onClick=\u007bhandlePause\u007d>Pause</button>
        <button onClick=\u007bhandleStop\u007d>Stop</button>
      </div>
    </div>
  );
};
''',
    'vue_basic': '''<script setup>
import { DotLottieVue } from '@lottiefiles/dotlottie-vue';
</script>

<template>
  <DotLottieVue
    src="{animationSrc}"
    :autoplay="true"
    :loop="true"
    :style="{ height: '{height}px', width: '{width}px' }"
  />
</template>
''',
    'svelte_basic': '''<script lang="ts">
  import { DotLottieSvelte } from '@lottiefiles/dotlottie-svelte';
</script>

<DotLottieSvelte
  src="{animationSrc}"
  loop=\u007btrue\u007d
  autoplay=\u007btrue\u007d
  style="height: {height}px; width: {width}px;"
/>
'''
}

def generate_component(framework, component_type, component_name, animation_src, height, width):
    """Generate component code based on parameters."""
    key = f"{framework}_{component_type}"

    if key not in TEMPLATES:
        print(f"Error: Template '{key}' not found")
        sys.exit(1)

    template = TEMPLATES[key]

    code = template.format(
        ComponentName=component_name,
        animationSrc=animation_src,
        height=height,
        width=width
    )

    return code

def interactive_mode():
    """Run interactive mode to gather component parameters."""
    print("Lottie Component Generator")
    print("-" * 40)

    # Framework selection
    print("\nSelect framework:")
    print("1. React")
    print("2. Vue")
    print("3. Svelte")
    framework_choice = input("Enter choice (1-3): ").strip()

    framework_map = {'1': 'react', '2': 'vue', '3': 'svelte'}
    framework = framework_map.get(framework_choice, 'react')

    # Component type
    if framework == 'react':
        print("\nSelect component type:")
        print("1. Basic (just displays animation)")
        print("2. Interactive (with playback controls)")
        type_choice = input("Enter choice (1-2): ").strip()
        component_type = 'interactive' if type_choice == '2' else 'basic'
    else:
        component_type = 'basic'

    # Component details
    component_name = input("\nComponent name (e.g., HeroAnimation): ").strip() or "LottieAnimation"
    animation_src = input("Animation source URL or path: ").strip() or "/animations/animation.lottie"
    height = input("Height in pixels (default 400): ").strip() or "400"
    width = input("Width in pixels (default 400): ").strip() or "400"

    code = generate_component(framework, component_type, component_name, animation_src, height, width)

    # Output
    extensions = {'react': 'jsx', 'vue': 'vue', 'svelte': 'svelte'}
    filename = f"{component_name}.{extensions[framework]}"

    print(f"\nGenerated {filename}:")
    print("-" * 40)
    print(code)

    save = input("\nSave to file? (y/n): ").strip().lower()
    if save == 'y':
        with open(filename, 'w') as f:
            f.write(code)
        print(f"✅ Saved to {filename}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Lottie component boilerplate")
    parser.add_argument('--framework', choices=['react', 'vue', 'svelte'], help="Framework to use")
    parser.add_argument('--type', choices=['basic', 'interactive'], default='basic', help="Component type")
    parser.add_argument('--name', default='LottieAnimation', help="Component name")
    parser.add_argument('--src', default='/animations/animation.lottie', help="Animation source")
    parser.add_argument('--height', default='400', help="Height in pixels")
    parser.add_argument('--width', default='400', help="Width in pixels")
    parser.add_argument('--output', help="Output file path")

    args = parser.parse_args()

    # Interactive mode if no framework specified
    if not args.framework:
        interactive_mode()
        return

    code = generate_component(
        args.framework,
        args.type,
        args.name,
        args.src,
        args.height,
        args.width
    )

    if args.output:
        with open(args.output, 'w') as f:
            f.write(code)
        print(f"✅ Generated {args.output}")
    else:
        print(code)

if __name__ == '__main__':
    main()
