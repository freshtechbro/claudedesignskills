#!/usr/bin/env python3
"""
Anime.js Timeline Builder

Build complex Anime.js timeline sequences with interactive configuration.

Usage:
    ./timeline_builder.py                      # Interactive mode
    ./timeline_builder.py --preset hero        # Use preset configuration
    ./timeline_builder.py --preset modal       # Modal animation sequence

Timeline Presets:
    hero        - Hero section entrance animation
    modal       - Modal popup with content reveal
    cards       - Card stagger with button reveal
    loader      - Loading sequence with spinner
    page        - Page transition animation
    toast       - Notification toast animation
    menu        - Menu open/close animation
"""

import sys

TIMELINE_PRESETS = {
    'hero': {
        'name': 'Hero Section Animation',
        'description': 'Hero background, title, subtitle, and CTA reveal',
        'code': '''const heroTimeline = anime.timeline({
  easing: 'easeOutExpo'
})

heroTimeline
  .add({
    targets: '.hero-bg',
    scale: [1.2, 1],
    opacity: [0, 1],
    duration: 1200
  })
  .add({
    targets: '.hero-title',
    translateY: [100, 0],
    opacity: [0, 1],
    duration: 800
  }, '-=800')  // Overlap by 800ms
  .add({
    targets: '.hero-subtitle',
    translateY: [50, 0],
    opacity: [0, 1],
    duration: 600
  }, '-=400')
  .add({
    targets: '.hero-cta',
    scale: [0, 1],
    duration: 400
  }, '-=200')'''
    },

    'modal': {
        'name': 'Modal Popup Animation',
        'description': 'Modal entrance with header, body, and footer reveal',
        'code': '''const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
})

tl.add({
  targets: '.modal',
  scale: [0, 1],
  opacity: [0, 1]
})
.add({
  targets: '.modal-header',
  translateY: [-20, 0],
  opacity: [0, 1]
}, '-=500')
.add({
  targets: '.modal-body',
  translateY: [20, 0],
  opacity: [0, 1]
}, '-=400')
.add({
  targets: '.modal-footer',
  opacity: [0, 1]
}, '-=300')'''
    },

    'cards': {
        'name': 'Card Grid Animation',
        'description': 'Cards stagger in, then button appears',
        'code': '''const tl = anime.timeline()

tl.add({
  targets: '.card',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(100),
  duration: 600,
  easing: 'easeOutQuad'
})
.add({
  targets: '.button',
  scale: [0, 1],
  duration: 400,
  easing: 'easeOutBack'
}, '-=200')'''
    },

    'loader': {
        'name': 'Loading Sequence',
        'description': 'Loader background, text, spinner, then fade to content',
        'code': '''const tl = anime.timeline()

tl.add({
  targets: '.loader-bg',
  scaleY: [0, 1],
  duration: 400,
  easing: 'easeInOutQuad'
})
.add({
  targets: '.loader-text',
  opacity: [0, 1],
  translateY: [20, 0],
  duration: 600
}, '-=200')
.add({
  targets: '.loader-spinner',
  rotate: '1turn',
  duration: 800,
  loop: 3
}, '-=400')
.add({
  targets: '.loader',
  opacity: 0,
  duration: 400
}, '+=500')
.add({
  targets: '.content',
  translateY: [50, 0],
  opacity: [0, 1],
  duration: 600
})'''
    },

    'page': {
        'name': 'Page Transition',
        'description': 'Slide out old page, slide in new page',
        'code': '''function pageTransition(oldPage, newPage) {
  const tl = anime.timeline()

  tl.add({
    targets: oldPage,
    translateX: [0, -100],
    opacity: [1, 0],
    duration: 400,
    easing: 'easeInQuad'
  })
  .add({
    targets: newPage,
    translateX: [100, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutQuad'
  }, '-=200')  // Overlap by 200ms for smooth transition

  return tl
}'''
    },

    'toast': {
        'name': 'Toast Notification',
        'description': 'Toast slides in, stays, then fades out',
        'code': '''function showToast(toast) {
  const tl = anime.timeline()

  tl.add({
    targets: toast,
    translateX: [400, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutBack'
  })
  .add({
    targets: toast,
    opacity: [1, 0],
    duration: 300,
    easing: 'easeInQuad'
  }, '+=3000')  // Wait 3 seconds before fading out

  return tl
}'''
    },

    'menu': {
        'name': 'Menu Open Animation',
        'description': 'Menu slides in with staggered items',
        'code': '''const tl = anime.timeline({ autoplay: false })

tl.add({
  targets: '.menu-overlay',
  translateX: ['-100%', 0],
  duration: 400,
  easing: 'easeOutQuad'
})
.add({
  targets: '.menu-item',
  translateX: [-50, 0],
  opacity: [0, 1],
  delay: anime.stagger(80),
  duration: 500,
  easing: 'easeOutExpo'
}, '-=200')

// Play on button click
document.querySelector('.menu-button').addEventListener('click', () => {
  tl.play()
})'''
    }
}

def print_header():
    """Print script header"""
    print("\n" + "="*60)
    print("Anime.js Timeline Builder")
    print("="*60 + "\n")

def list_presets():
    """List all available timeline presets"""
    print("Available Timeline Presets:\n")
    for key, preset in TIMELINE_PRESETS.items():
        print(f"  {key:12} - {preset['description']}")
    print()

def generate_timeline(preset_name):
    """Generate timeline code for given preset"""
    if preset_name not in TIMELINE_PRESETS:
        print(f"Error: Unknown preset '{preset_name}'")
        print("Use --list to see available presets")
        sys.exit(1)

    preset = TIMELINE_PRESETS[preset_name]

    print(f"\n{preset['name']}")
    print("-" * 60)
    print(f"\n{preset['description']}\n")
    print("Generated Timeline:")
    print("-" * 60)
    print(preset['code'])
    print("\n" + "="*60 + "\n")

def generate_custom_timeline():
    """Generate custom timeline with user input"""
    print("\nCustom Timeline Builder")
    print("-" * 60)
    print("\nEnter number of animation steps: ", end='')
    try:
        num_steps = int(input().strip())
    except ValueError:
        print("Error: Invalid number")
        sys.exit(1)

    if num_steps < 1 or num_steps > 10:
        print("Error: Number of steps must be between 1 and 10")
        sys.exit(1)

    print("\nGenerating timeline with", num_steps, "steps...\n")

    # Generate timeline code
    code = "const tl = anime.timeline({\n"
    code += "  duration: 750,\n"
    code += "  easing: 'easeOutExpo'\n"
    code += "})\n\n"

    for i in range(num_steps):
        code += f"tl.add({{\n"
        code += f"  targets: '.element-{i+1}',\n"
        code += f"  translateY: [50, 0],\n"
        code += f"  opacity: [0, 1]\n"
        if i > 0:
            code += f"}}, '-=300')  // Step {i+1}\n"
        else:
            code += f"}})  // Step {i+1}\n"

        if i < num_steps - 1:
            code += "\n"

    print("Generated Timeline:")
    print("-" * 60)
    print(code)
    print("\n" + "="*60 + "\n")

def interactive_mode():
    """Run in interactive mode"""
    print_header()
    list_presets()

    print("Enter preset name (or 'custom' for custom builder, 'quit' to exit): ", end='')
    choice = input().strip().lower()

    if choice == 'quit':
        sys.exit(0)
    elif choice == 'custom':
        generate_custom_timeline()
    else:
        generate_timeline(choice)

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
        list_presets()
        return

    if '--preset' in args:
        try:
            preset_index = args.index('--preset')
            preset_name = args[preset_index + 1]
            print_header()
            generate_timeline(preset_name)
        except IndexError:
            print("Error: --preset requires a preset name")
            print("Usage: ./timeline_builder.py --preset <name>")
            sys.exit(1)
        return

    # Help or unknown arguments
    print(__doc__)

if __name__ == '__main__':
    main()
