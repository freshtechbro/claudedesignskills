#!/usr/bin/env python3
"""
Barba.js Transition Generator

Generates boilerplate code for Barba.js page transitions with GSAP animations.

Usage:
    ./transition_generator.py                          # Interactive mode
    ./transition_generator.py --type fade              # Generate fade transition
    ./transition_generator.py --type slide --sync      # Generate sync slide transition
    ./transition_generator.py --type custom --name my-transition

Transition Types:
    - fade: Simple fade in/out
    - crossfade: Simultaneous fade (sync mode)
    - slide: Horizontal slide
    - slide-vertical: Vertical slide
    - scale: Zoom with fade
    - stagger: Staggered element animation
    - curtain: Curtain overlay effect
    - custom: Empty template for custom transitions

Options:
    --type TYPE        Transition type (required in CLI mode)
    --name NAME        Custom transition name (default: based on type)
    --sync             Enable sync mode (leave and enter simultaneously)
    --duration SECS    Animation duration in seconds (default: 0.5)
    --ease EASE        GSAP easing (default: power2.inOut)
    --output FILE      Output file path (default: stdout)
"""

import sys
import argparse
from typing import Dict, Optional


TRANSITION_TEMPLATES = {
    'fade': {
        'name': 'fade',
        'sync': False,
        'code': '''{{
  name: '{name}',

  async leave({{ current }}) {{
    await gsap.to(current.container, {{
      opacity: 0,
      duration: {duration},
      ease: '{ease}'
    }});
  }},

  async enter({{ next }}) {{
    gsap.set(next.container, {{ opacity: 0 }});

    await gsap.to(next.container, {{
      opacity: 1,
      duration: {duration},
      ease: '{ease}'
    }});
  }}
}}'''
    },

    'crossfade': {
        'name': 'crossfade',
        'sync': True,
        'code': '''{{
  name: '{name}',
  sync: true,

  leave({{ current }}) {{
    return gsap.to(current.container, {{
      opacity: 0,
      duration: {duration},
      ease: '{ease}'
    }});
  }},

  enter({{ next }}) {{
    return gsap.from(next.container, {{
      opacity: 0,
      duration: {duration},
      ease: '{ease}'
    }});
  }}
}}'''
    },

    'slide': {
        'name': 'slide-horizontal',
        'sync': True,
        'code': '''{{
  name: '{name}',
  sync: true,

  leave({{ current }}) {{
    return gsap.to(current.container, {{
      x: '-100%',
      duration: {duration},
      ease: '{ease}'
    }});
  }},

  enter({{ next }}) {{
    gsap.set(next.container, {{ x: '100%' }});

    return gsap.to(next.container, {{
      x: '0%',
      duration: {duration},
      ease: '{ease}'
    }});
  }}
}}

/* CSS Required:
[data-barba="wrapper"] {{
  position: relative;
  overflow: hidden;
}}

[data-barba="container"] {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}}
*/'''
    },

    'slide-vertical': {
        'name': 'slide-vertical',
        'sync': True,
        'code': '''{{
  name: '{name}',
  sync: true,

  leave({{ current }}) {{
    return gsap.to(current.container, {{
      y: '-100%',
      duration: {duration},
      ease: '{ease}'
    }});
  }},

  enter({{ next }}) {{
    gsap.set(next.container, {{ y: '100%' }});

    return gsap.to(next.container, {{
      y: '0%',
      duration: {duration},
      ease: '{ease}'
    }});
  }}
}}

/* CSS Required:
[data-barba="wrapper"] {{
  position: relative;
  overflow: hidden;
}}

[data-barba="container"] {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}}
*/'''
    },

    'scale': {
        'name': 'scale-fade',
        'sync': False,
        'code': '''{{
  name: '{name}',

  async leave({{ current }}) {{
    await gsap.to(current.container, {{
      opacity: 0,
      scale: 0.95,
      duration: {duration},
      ease: 'power2.in'
    }});
  }},

  async enter({{ next }}) {{
    await gsap.fromTo(next.container,
      {{
        opacity: 0,
        scale: 1.05
      }},
      {{
        opacity: 1,
        scale: 1,
        duration: {duration},
        ease: 'power2.out'
      }}
    );
  }}
}}'''
    },

    'stagger': {
        'name': 'stagger',
        'sync': False,
        'code': '''{{
  name: '{name}',

  async leave({{ current }}) {{
    const tl = gsap.timeline();

    tl.to(current.container.querySelectorAll('.stagger-item'), {{
      y: -50,
      opacity: 0,
      duration: {duration},
      stagger: 0.05,
      ease: 'power2.in'
    }})
    .to(current.container, {{
      opacity: 0,
      duration: 0.3
    }}, '-=0.2');

    await tl.play();
  }},

  async enter({{ next }}) {{
    const tl = gsap.timeline();

    gsap.set(next.container.querySelectorAll('.stagger-item'), {{
      y: 50,
      opacity: 0
    }});

    tl.to(next.container.querySelectorAll('.stagger-item'), {{
      y: 0,
      opacity: 1,
      duration: {duration},
      stagger: 0.05,
      ease: 'power2.out'
    }});

    await tl.play();
  }}
}}

/* HTML Required: Add class="stagger-item" to elements you want to animate */'''
    },

    'curtain': {
        'name': 'curtain',
        'sync': False,
        'code': '''{{
  name: '{name}',

  async leave({{ current }}) {{
    const curtain = document.querySelector('.transition-curtain');

    await gsap.fromTo(curtain,
      {{ yPercent: -100 }},
      {{
        yPercent: 0,
        duration: {duration},
        ease: '{ease}'
      }}
    );
  }},

  async enter({{ next }}) {{
    const curtain = document.querySelector('.transition-curtain');

    await gsap.to(curtain, {{
      yPercent: 100,
      duration: {duration},
      ease: '{ease}'
    }});
  }}
}}

/* HTML Required:
<div class="transition-curtain"></div>
*/

/* CSS Required:
.transition-curtain {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 9999;
  pointer-events: none;
  transform: translateY(-100%);
}}
*/'''
    },

    'custom': {
        'name': 'custom-transition',
        'sync': False,
        'code': '''{{
  name: '{name}',

  async leave({{ current }}) {{
    // TODO: Add your leave animation here
    await gsap.to(current.container, {{
      opacity: 0,
      duration: {duration}
    }});
  }},

  async enter({{ next }}) {{
    // TODO: Add your enter animation here
    await gsap.from(next.container, {{
      opacity: 0,
      duration: {duration}
    }});
  }}
}}'''
    }
}


def generate_transition(
    transition_type: str,
    name: Optional[str] = None,
    sync: Optional[bool] = None,
    duration: float = 0.5,
    ease: str = 'power2.inOut'
) -> str:
    """Generate transition code based on type and options."""
    if transition_type not in TRANSITION_TEMPLATES:
        raise ValueError(f"Unknown transition type: {transition_type}. "
                        f"Available types: {', '.join(TRANSITION_TEMPLATES.keys())}")

    template = TRANSITION_TEMPLATES[transition_type]

    # Use custom name if provided, otherwise use template default
    transition_name = name if name else template['name']

    # Use custom sync if provided, otherwise use template default
    # (but only if the template supports it)
    use_sync = sync if sync is not None else template.get('sync', False)

    # Format the template
    code = template['code'].format(
        name=transition_name,
        duration=duration,
        ease=ease
    )

    # Override sync mode if explicitly requested
    if sync is not None and sync != template.get('sync', False):
        if sync:
            # Convert to sync mode
            code = code.replace('async leave', 'leave')
            code = code.replace('async enter', 'enter')
            code = code.replace('await gsap.to', 'return gsap.to')
            code = code.replace('await gsap.from', 'return gsap.from')
            if 'sync: true' not in code:
                code = code.replace("name: '" + transition_name + "',",
                                  "name: '" + transition_name + "',\n  sync: true,")
        else:
            # Convert to async mode
            code = code.replace('leave({', 'async leave({')
            code = code.replace('enter({', 'async enter({')
            code = code.replace('return gsap.to', 'await gsap.to')
            code = code.replace('return gsap.from', 'await gsap.from')
            code = code.replace('\n  sync: true,', '')

    return code


def interactive_mode():
    """Run generator in interactive mode with prompts."""
    print("🎬 Barba.js Transition Generator")
    print("=" * 50)
    print()

    # Choose transition type
    print("Available transition types:")
    for i, (key, value) in enumerate(TRANSITION_TEMPLATES.items(), 1):
        sync_indicator = " (sync)" if value.get('sync') else ""
        print(f"  {i}. {key}{sync_indicator}")

    print()
    choice = input("Select transition type (1-{}): ".format(len(TRANSITION_TEMPLATES)))

    try:
        choice_idx = int(choice) - 1
        transition_type = list(TRANSITION_TEMPLATES.keys())[choice_idx]
    except (ValueError, IndexError):
        print("❌ Invalid choice. Using 'fade' as default.")
        transition_type = 'fade'

    # Custom name
    default_name = TRANSITION_TEMPLATES[transition_type]['name']
    name = input(f"Transition name (default: {default_name}): ").strip()
    if not name:
        name = default_name

    # Sync mode
    sync_default = TRANSITION_TEMPLATES[transition_type].get('sync', False)
    sync_input = input(f"Sync mode? [y/N] (default: {'y' if sync_default else 'n'}): ").strip().lower()
    if sync_input in ['y', 'yes']:
        sync = True
    elif sync_input in ['n', 'no']:
        sync = False
    else:
        sync = sync_default

    # Duration
    duration_input = input("Animation duration in seconds (default: 0.5): ").strip()
    try:
        duration = float(duration_input) if duration_input else 0.5
    except ValueError:
        print("❌ Invalid duration. Using 0.5s as default.")
        duration = 0.5

    # Easing
    print()
    print("Common GSAP easings:")
    print("  - power2.inOut (smooth acceleration/deceleration)")
    print("  - power2.in (accelerate)")
    print("  - power2.out (decelerate)")
    print("  - power3.inOut (stronger curve)")
    print("  - back.out(1.7) (overshoot)")
    print("  - elastic.out(1, 0.3) (elastic bounce)")
    ease = input("Easing function (default: power2.inOut): ").strip()
    if not ease:
        ease = 'power2.inOut'

    print()
    print("=" * 50)
    print("Generating transition...")
    print()

    # Generate code
    code = generate_transition(transition_type, name, sync, duration, ease)

    # Output
    print(code)
    print()
    print("✅ Transition generated successfully!")
    print()
    print("To use this transition:")
    print("1. Import Barba.js and GSAP:")
    print("   import barba from '@barba/core';")
    print("   import gsap from 'gsap';")
    print()
    print("2. Add the transition to your Barba.init() call:")
    print("   barba.init({")
    print("     transitions: [")
    print("       // ... paste the generated code here")
    print("     ]")
    print("   });")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Barba.js transition boilerplate code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--type',
        choices=list(TRANSITION_TEMPLATES.keys()),
        help='Transition type'
    )

    parser.add_argument(
        '--name',
        help='Custom transition name'
    )

    parser.add_argument(
        '--sync',
        action='store_true',
        help='Enable sync mode (leave and enter simultaneously)'
    )

    parser.add_argument(
        '--duration',
        type=float,
        default=0.5,
        help='Animation duration in seconds (default: 0.5)'
    )

    parser.add_argument(
        '--ease',
        default='power2.inOut',
        help='GSAP easing function (default: power2.inOut)'
    )

    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Interactive mode if no type specified
    if not args.type:
        interactive_mode()
        return

    # CLI mode
    try:
        code = generate_transition(
            args.type,
            args.name,
            args.sync,
            args.duration,
            args.ease
        )

        if args.output:
            with open(args.output, 'w') as f:
                f.write(code)
            print(f"✅ Transition written to {args.output}")
        else:
            print(code)

    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
