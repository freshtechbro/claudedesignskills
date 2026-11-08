#!/usr/bin/env python3
"""
Spring Physics Calculator

Calculate optimal spring physics parameters for desired animation feel.

Usage:
    ./physics_calculator.py                          # Interactive mode
    ./physics_calculator.py --feel bouncy            # Calculate preset
    ./physics_calculator.py --tension 200 --friction 20  # Custom params
    ./physics_calculator.py --critical-damping --tension 170  # Calculate critical

Physics Concepts:
    - Mass: Weight/inertia of animated object
    - Tension: Spring strength (higher = faster)
    - Friction: Opposing force (higher = less bounce)
    - Critical Damping: No overshoot, fastest settle time
"""

import sys
import argparse
import math
from textwrap import dedent


# Preset configurations
PRESETS = {
    'default': {'mass': 1, 'tension': 170, 'friction': 26},
    'gentle': {'mass': 1, 'tension': 120, 'friction': 14},
    'wobbly': {'mass': 1, 'tension': 180, 'friction': 12},
    'stiff': {'mass': 1, 'tension': 210, 'friction': 20},
    'slow': {'mass': 1, 'tension': 280, 'friction': 60},
    'molasses': {'mass': 1, 'tension': 280, 'friction': 120},
    'snappy': {'mass': 0.8, 'tension': 300, 'friction': 20},
    'bouncy': {'mass': 1, 'tension': 180, 'friction': 12},
    'smooth': {'mass': 1, 'tension': 120, 'friction': 14},
    'heavy': {'mass': 5, 'tension': 170, 'friction': 26}
}


def calculate_damping_ratio(mass, tension, friction):
    """Calculate damping ratio (ζ) from spring parameters."""
    critical_friction = 2 * math.sqrt(tension * mass)
    damping_ratio = friction / critical_friction
    return damping_ratio


def calculate_critical_friction(mass, tension):
    """Calculate critical damping friction."""
    return 2 * math.sqrt(tension * mass)


def classify_damping(damping_ratio):
    """Classify damping behavior."""
    if damping_ratio < 1:
        return "Under-damped (oscillates/bounces)"
    elif damping_ratio == 1:
        return "Critically damped (no overshoot, fastest)"
    else:
        return "Over-damped (slow, no overshoot)"


def estimate_settle_time(mass, tension, friction):
    """Estimate approximate settle time in milliseconds."""
    damping_ratio = calculate_damping_ratio(mass, tension, friction)
    natural_frequency = math.sqrt(tension / mass)

    if damping_ratio >= 1:
        # Over-damped or critically damped
        settle_time = 4 / (damping_ratio * natural_frequency)
    else:
        # Under-damped
        damped_frequency = natural_frequency * math.sqrt(1 - damping_ratio**2)
        settle_time = 4 / (damping_ratio * natural_frequency)

    return settle_time * 1000  # Convert to ms


def display_config(config, name=None):
    """Display spring configuration with analysis."""
    mass = config['mass']
    tension = config['tension']
    friction = config['friction']

    damping_ratio = calculate_damping_ratio(mass, tension, friction)
    critical_friction = calculate_critical_friction(mass, tension)
    classification = classify_damping(damping_ratio)
    settle_time = estimate_settle_time(mass, tension, friction)

    if name:
        print(f"\n{'=' * 60}")
        print(f"Spring Configuration: {name}")
        print(f"{'=' * 60}")
    else:
        print(f"\n{'=' * 60}")
        print(f"Spring Configuration Analysis")
        print(f"{'=' * 60}")

    print(f"\nParameters:")
    print(f"  mass:     {mass}")
    print(f"  tension:  {tension}")
    print(f"  friction: {friction}")

    print(f"\nPhysics Analysis:")
    print(f"  Damping ratio (ζ):      {damping_ratio:.3f}")
    print(f"  Critical friction:      {critical_friction:.2f}")
    print(f"  Classification:         {classification}")
    print(f"  Est. settle time:       ~{settle_time:.0f}ms")

    print(f"\nReact Spring Code:")
    print(f"  config: {{ mass: {mass}, tension: {tension}, friction: {friction} }}")

    if abs(damping_ratio - 1.0) < 0.05:
        print(f"\n💡 Near critically damped - very efficient!")
    elif damping_ratio < 0.5:
        print(f"\n💡 Very bouncy - expect multiple oscillations")
    elif damping_ratio > 1.5:
        print(f"\n💡 Heavily damped - may feel sluggish")


def interactive_mode():
    """Run calculator in interactive mode."""
    print("Spring Physics Calculator")
    print("=" * 60)
    print("\nChoose an option:")
    print("  1. Use preset configuration")
    print("  2. Enter custom parameters")
    print("  3. Calculate critical damping")
    print("\nChoice (1-3): ", end='')

    try:
        choice = input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nCancelled.")
        return

    if choice == '1':
        # Preset mode
        print("\nAvailable presets:\n")
        for i, (name, config) in enumerate(PRESETS.items(), 1):
            print(f"  {i:2}. {name:12} - mass: {config['mass']}, tension: {config['tension']}, friction: {config['friction']}")

        print(f"\nSelect preset (1-{len(PRESETS)}): ", end='')
        try:
            preset_choice = int(input().strip()) - 1
            preset_name = list(PRESETS.keys())[preset_choice]
            config = PRESETS[preset_name]
            display_config(config, preset_name)
        except (ValueError, IndexError, KeyboardInterrupt, EOFError):
            print("\nInvalid selection.")
            return

    elif choice == '2':
        # Custom parameters
        try:
            print("\nEnter parameters:")
            mass = float(input("  mass (default 1): ") or 1)
            tension = float(input("  tension (default 170): ") or 170)
            friction = float(input("  friction (default 26): ") or 26)

            config = {'mass': mass, 'tension': tension, 'friction': friction}
            display_config(config)
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nInvalid input.")
            return

    elif choice == '3':
        # Critical damping calculator
        try:
            print("\nCalculate critical damping:")
            mass = float(input("  mass (default 1): ") or 1)
            tension = float(input("  tension (default 170): ") or 170)

            critical_friction = calculate_critical_friction(mass, tension)
            config = {'mass': mass, 'tension': tension, 'friction': critical_friction}

            print(f"\n✅ Critical friction: {critical_friction:.2f}")
            display_config(config, "Critically Damped")
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nInvalid input.")
            return
    else:
        print("\nInvalid choice.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Calculate spring physics parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent('''
        Examples:
          ./physics_calculator.py                      # Interactive mode
          ./physics_calculator.py --feel bouncy        # Use preset
          ./physics_calculator.py --mass 2 --tension 200 --friction 30
          ./physics_calculator.py --critical --tension 170 --mass 1
          ./physics_calculator.py --list               # List presets
        ''')
    )

    parser.add_argument(
        '--feel',
        choices=list(PRESETS.keys()),
        help='Use preset configuration'
    )

    parser.add_argument(
        '--mass', '-m',
        type=float,
        default=1,
        help='Object mass (default: 1)'
    )

    parser.add_argument(
        '--tension', '-t',
        type=float,
        default=170,
        help='Spring tension/stiffness (default: 170)'
    )

    parser.add_argument(
        '--friction', '-f',
        type=float,
        help='Spring friction/damping'
    )

    parser.add_argument(
        '--critical', '-c',
        action='store_true',
        help='Calculate critical damping friction'
    )

    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all preset configurations'
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable preset configurations:\n")
        for name, config in PRESETS.items():
            damping_ratio = calculate_damping_ratio(config['mass'], config['tension'], config['friction'])
            print(f"  {name:12} - mass: {config['mass']:3}, tension: {config['tension']:3}, friction: {config['friction']:3}  (ζ={damping_ratio:.2f})")
        return 0

    if args.feel:
        config = PRESETS[args.feel]
        display_config(config, args.feel)
        return 0

    if args.critical:
        critical_friction = calculate_critical_friction(args.mass, args.tension)
        config = {'mass': args.mass, 'tension': args.tension, 'friction': critical_friction}
        display_config(config, "Critically Damped")
        return 0

    if args.friction is not None:
        config = {'mass': args.mass, 'tension': args.tension, 'friction': args.friction}
        display_config(config)
        return 0

    # No arguments - interactive mode
    interactive_mode()
    return 0


if __name__ == '__main__':
    sys.exit(main())
