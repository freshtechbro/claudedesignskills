#!/usr/bin/env python3
"""
Anime.js Animation Generator

Generates Anime.js animation boilerplate code for common animation patterns.

Usage:
    ./animation_generator.py                    # Interactive mode
    ./animation_generator.py --type stagger     # Generate stagger animation
    ./animation_generator.py --type timeline    # Generate timeline sequence

Animation Types:
    basic           - Simple translateX/Y, opacity animation
    stagger         - Sequential reveal with stagger
    grid-stagger    - Grid-based stagger animation
    svg-line        - SVG line drawing animation
    svg-morph       - SVG path morphing animation
    timeline        - Multi-step timeline sequence
    keyframe        - Keyframe animation with multiple steps
    scroll          - Scroll-triggered animation
"""

import sys

ANIMATION_TYPES = {
    'basic': {
        'name': 'Basic Animation',
        'description': 'Simple translateX/Y, opacity animation',
        'code': '''anime({
  targets: '.element',
  translateX: 250,
  rotate: '1turn',
  opacity: [0, 1],
  duration: 800,
  easing: 'easeInOutQuad'
})'''
    },

    'stagger': {
        'name': 'Stagger Animation',
        'description': 'Sequential reveal with stagger effect',
        'code': '''anime({
  targets: '.stagger-element',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(100), // Increment delay by 100ms
  easing: 'easeOutQuad',
  duration: 600
})'''
    },

    'grid-stagger': {
        'name': 'Grid Stagger Animation',
        'description': 'Grid-based stagger from center',
        'code': '''anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [14, 5],        // 14 columns, 5 rows
    from: 'center',       // Start from center
    axis: 'x'             // Primary axis
  }),
  easing: 'easeOutElastic(1, .8)',
  duration: 600
})'''
    },

    'svg-line': {
        'name': 'SVG Line Drawing',
        'description': 'SVG path line drawing animation',
        'code': '''anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutQuad',
  duration: 2000,
  delay: (el, i) => i * 250
})'''
    },

    'svg-morph': {
        'name': 'SVG Path Morphing',
        'description': 'Morph between SVG path shapes',
        'code': '''anime({
  targets: '#morphing-path',
  d: [
    { value: 'M10 80 Q 77.5 10, 145 80' },  // Start shape
    { value: 'M10 80 Q 77.5 150, 145 80' }  // End shape
  ],
  duration: 2000,
  easing: 'easeInOutQuad',
  loop: true,
  direction: 'alternate'
})'''
    },

    'timeline': {
        'name': 'Timeline Sequence',
        'description': 'Multi-step timeline with overlapping animations',
        'code': '''const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
})

tl.add({
  targets: '.title',
  translateY: [-50, 0],
  opacity: [0, 1]
})
.add({
  targets: '.subtitle',
  translateY: [-30, 0],
  opacity: [0, 1]
}, '-=500')  // Start 500ms before previous ends
.add({
  targets: '.button',
  scale: [0, 1],
  opacity: [0, 1]
}, '-=300')'''
    },

    'keyframe': {
        'name': 'Keyframe Animation',
        'description': 'Multiple keyframes for complex motion',
        'code': '''anime({
  targets: '.element',
  keyframes: [
    { translateX: 100 },
    { translateY: 100 },
    { translateX: 0 },
    { translateY: 0 }
  ],
  duration: 4000,
  easing: 'easeInOutQuad',
  loop: true
})'''
    },

    'scroll': {
        'name': 'Scroll-Triggered Animation',
        'description': 'Animation controlled by scroll position',
        'code': '''const animation = anime({
  targets: '.scroll-element',
  translateY: [100, 0],
  opacity: [0, 1],
  easing: 'easeOutQuad',
  autoplay: false
})

window.addEventListener('scroll', () => {
  const scrollPercent = window.scrollY / (document.body.scrollHeight - window.innerHeight)
  animation.seek(animation.duration * scrollPercent)
})'''
    }
}

def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print("Anime.js Animation Generator")
    print("="*60 + "\n")

def list_animation_types():
    """List all available animation types"""
    print("Available Animation Types:\n")
    for key, anim in ANIMATION_TYPES.items():
        print(f"  {key:15} - {anim['description']}")
    print()

def generate_animation(anim_type):
    """Generate animation code for given type"""
    if anim_type not in ANIMATION_TYPES:
        print(f"Error: Unknown animation type '{anim_type}'")
        print("Use --list to see available types")
        sys.exit(1)

    anim = ANIMATION_TYPES[anim_type]

    print(f"\n{anim['name']}")
    print("-" * 60)
    print(f"\n{anim['description']}\n")
    print("Generated Code:")
    print("-" * 60)
    print(anim['code'])
    print("\n" + "="*60 + "\n")

def interactive_mode():
    """Run in interactive mode"""
    print_header()
    list_animation_types()

    print("Enter animation type (or 'quit' to exit): ", end='')
    choice = input().strip().lower()

    if choice == 'quit':
        sys.exit(0)

    generate_animation(choice)

def main():
    """Main entry point"""
    args = sys.argv[1:]

    # No arguments - interactive mode
    if not args:
        interactive_mode()
        return

    # Parse arguments
    if '--list' in args:
        print_header()
        list_animation_types()
        return

    if '--type' in args:
        try:
            type_index = args.index('--type')
            anim_type = args[type_index + 1]
            print_header()
            generate_animation(anim_type)
        except IndexError:
            print("Error: --type requires an animation type")
            print("Usage: ./animation_generator.py --type <type>")
            sys.exit(1)
        return

    # Help or unknown arguments
    print(__doc__)

if __name__ == '__main__':
    main()
