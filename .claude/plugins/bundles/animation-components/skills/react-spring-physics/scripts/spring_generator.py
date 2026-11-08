#!/usr/bin/env python3
"""
React Spring Animation Generator

Generates React Spring boilerplate code for common animation patterns.

Usage:
    ./spring_generator.py                    # Interactive mode
    ./spring_generator.py --type click       # Generate click animation
    ./spring_generator.py --type scroll      # Generate scroll animation
    ./spring_generator.py --help             # Show help

Animation Types:
    click       - Click-triggered spring animation
    scroll      - Scroll-based spring animation
    trail       - Multi-element trail animation
    transition  - List enter/exit transitions
    inview      - Viewport intersection animation
    chain       - Chained async animations
    gesture     - Gesture-driven animation (drag)
"""

import sys
import argparse
from textwrap import dedent


ANIMATION_TYPES = {
    'click': {
        'name': 'Click-Triggered Spring',
        'code': '''import { useSpring, animated } from '@react-spring/web'

function ClickAnimation() {
  const [springs, api] = useSpring(() => ({
    from: { scale: 1 }
  }), [])

  const handleClick = () => {
    api.start({
      from: { scale: 1 },
      to: { scale: 1.2 },
      config: { tension: 300, friction: 10 }
    })
  }

  return (
    <animated.button
      onClick={handleClick}
      style={{
        transform: springs.scale.to(s => `scale($${s})`)
      }}
    >
      Click Me
    </animated.button>
  )
}

export default ClickAnimation'''
    },
    'scroll': {
        'name': 'Scroll-Based Spring',
        'code': '''import { useScroll, animated } from '@react-spring/web'

function ScrollAnimation() {
  const { scrollYProgress } = useScroll()

  return (
    <animated.div
      style={{
        opacity: scrollYProgress.to([0, 0.5], [0, 1]),
        scale: scrollYProgress.to([0, 0.5], [0.8, 1])
      }}
    >
      Scroll to reveal
    </animated.div>
  )
}

export default ScrollAnimation'''
    },
    'trail': {
        'name': 'Multi-Element Trail',
        'code': '''import { useTrail, animated, config } from '@react-spring/web'

function TrailAnimation({ items }) {
  const trails = useTrail(items.length, {
    from: { opacity: 0, x: -20 },
    to: { opacity: 1, x: 0 },
    config: config.gentle
  })

  return (
    <div>
      {trails.map((style, i) => (
        <animated.div key={i} style={style}>
          {items[i]}
        </animated.div>
      ))}
    </div>
  )
}

export default TrailAnimation'''
    },
    'transition': {
        'name': 'List Enter/Exit Transitions',
        'code': '''import { useTransition, animated, config } from '@react-spring/web'

function TransitionAnimation({ items }) {
  const transitions = useTransition(items, {
    from: { opacity: 0, height: 0 },
    enter: { opacity: 1, height: 80 },
    leave: { opacity: 0, height: 0 },
    config: config.stiff,
    keys: item => item.id
  })

  return (
    <div>
      {transitions((style, item) => (
        <animated.div style={style}>
          {item.text}
        </animated.div>
      ))}
    </div>
  )
}

export default TransitionAnimation'''
    },
    'inview': {
        'name': 'Viewport Intersection',
        'code': '''import { useInView, animated } from '@react-spring/web'

function InViewAnimation() {
  const [ref, springs] = useInView(
    () => ({
      from: { opacity: 0, y: 100 },
      to: { opacity: 1, y: 0 }
    }),
    { rootMargin: '-40% 0%' }
  )

  return (
    <animated.div ref={ref} style={springs}>
      Fades in when entering viewport
    </animated.div>
  )
}

export default InViewAnimation'''
    },
    'chain': {
        'name': 'Chained Async Animations',
        'code': '''import { useSpring, animated } from '@react-spring/web'

function ChainedAnimation() {
  const springs = useSpring({
    from: { x: 0, background: '#ff6d6d' },
    to: [
      { x: 80, background: '#fff59a' },
      { x: 0, background: '#88DFAB' },
      { x: 80, background: '#569AFF' }
    ],
    config: { tension: 200, friction: 20 },
    loop: true
  })

  return (
    <animated.div
      style={{
        width: 40,
        height: 40,
        borderRadius: 4,
        ...springs
      }}
    />
  )
}

export default ChainedAnimation'''
    },
    'gesture': {
        'name': 'Gesture-Driven Animation',
        'code': '''import { useSpring, animated } from '@react-spring/web'
import { useDrag } from '@use-gesture/react'

function GestureAnimation() {
  const [{ x, y }, api] = useSpring(() => ({ x: 0, y: 0 }))

  const bind = useDrag(({ down, movement: [mx, my], velocity: [vx, vy] }) => {
    api.start({
      x: down ? mx : 0,
      y: down ? my : 0,
      velocity: [vx * 1000, vy * 1000],
      immediate: down,
      config: { tension: 200, friction: 30 }
    })
  })

  return (
    <animated.div
      {...bind()}
      style={{
        x,
        y,
        width: 100,
        height: 100,
        background: '#569AFF',
        borderRadius: 8,
        touchAction: 'none'
      }}
    />
  )
}

export default GestureAnimation'''
    }
}


def generate_animation(anim_type, output_file=None):
    """Generate React Spring animation code."""
    if anim_type not in ANIMATION_TYPES:
        print(f"Error: Unknown animation type '{anim_type}'")
        print(f"Available types: {', '.join(ANIMATION_TYPES.keys())}")
        return False

    animation = ANIMATION_TYPES[anim_type]
    code = animation['code']

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(code)
            print(f"✅ Generated {animation['name']} → {output_file}")
            return True
        except IOError as e:
            print(f"❌ Error writing file: {e}")
            return False
    else:
        print(f"\n// {animation['name']}\n")
        print(code)
        return True


def interactive_mode():
    """Run generator in interactive mode."""
    print("React Spring Animation Generator")
    print("=" * 50)
    print("\nAvailable animation types:\n")

    for i, (key, value) in enumerate(ANIMATION_TYPES.items(), 1):
        print(f"  {i}. {value['name']} ({key})")

    print("\nSelect animation type (1-{}) or 'q' to quit: ".format(len(ANIMATION_TYPES)), end='')

    try:
        choice = input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nCancelled.")
        return

    if choice.lower() == 'q':
        return

    try:
        index = int(choice) - 1
        if 0 <= index < len(ANIMATION_TYPES):
            anim_type = list(ANIMATION_TYPES.keys())[index]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        # Maybe they typed the key name
        if choice in ANIMATION_TYPES:
            anim_type = choice
        else:
            print("Invalid selection.")
            return

    print("\nOutput to file? (leave empty for stdout): ", end='')
    try:
        output_file = input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nCancelled.")
        return

    output_file = output_file if output_file else None
    generate_animation(anim_type, output_file)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate React Spring animation boilerplate',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent('''
        Examples:
          ./spring_generator.py                    # Interactive mode
          ./spring_generator.py --type click       # Generate to stdout
          ./spring_generator.py --type scroll -o ScrollAnim.jsx
          ./spring_generator.py --list             # List all types
        ''')
    )

    parser.add_argument(
        '--type', '-t',
        choices=list(ANIMATION_TYPES.keys()),
        help='Animation type to generate'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available animation types'
    )

    args = parser.parse_args()

    if args.list:
        print("Available animation types:\n")
        for key, value in ANIMATION_TYPES.items():
            print(f"  {key:12} - {value['name']}")
        return 0

    if args.type:
        success = generate_animation(args.type, args.output)
        return 0 if success else 1
    else:
        # Interactive mode
        interactive_mode()
        return 0


if __name__ == '__main__':
    sys.exit(main())
