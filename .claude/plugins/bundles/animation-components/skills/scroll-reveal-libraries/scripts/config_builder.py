#!/usr/bin/env python3
"""
AOS Config Builder

Generates AOS initialization configurations with customizable options.
Outputs JavaScript code for AOS.init() with selected settings.

Usage:
    ./config_builder.py                              # Interactive mode
    ./config_builder.py --preset marketing          # Use preset
    ./config_builder.py --duration 1000 --once true # Custom config
"""

import sys
import argparse
import json

# Configuration presets
PRESETS = {
    "marketing": {
        "name": "Marketing Page",
        "description": "Optimized for marketing/landing pages with once-only animations",
        "config": {
            "duration": 800,
            "delay": 0,
            "offset": 120,
            "easing": "ease-out",
            "once": True,
            "mirror": False,
            "anchorPlacement": "top-bottom",
            "disable": "mobile"
        }
    },
    "interactive": {
        "name": "Interactive Experience",
        "description": "Repeating animations for interactive scrolling experiences",
        "config": {
            "duration": 600,
            "delay": 0,
            "offset": 80,
            "easing": "ease-in-out",
            "once": False,
            "mirror": True,
            "anchorPlacement": "center-center",
            "disable": False
        }
    },
    "blog": {
        "name": "Blog/Content Site",
        "description": "Subtle animations for content-heavy sites",
        "config": {
            "duration": 500,
            "delay": 0,
            "offset": 100,
            "easing": "ease",
            "once": True,
            "mirror": False,
            "anchorPlacement": "top-bottom",
            "disable": False
        }
    },
    "performance": {
        "name": "Performance Optimized",
        "description": "Minimal animations for best performance",
        "config": {
            "duration": 400,
            "delay": 0,
            "offset": 50,
            "easing": "linear",
            "once": True,
            "mirror": False,
            "anchorPlacement": "top-bottom",
            "disable": "mobile",
            "disableMutationObserver": True,
            "throttleDelay": 120,
            "debounceDelay": 80
        }
    },
    "showcase": {
        "name": "Portfolio/Showcase",
        "description": "Dramatic animations for portfolios and showcases",
        "config": {
            "duration": 1200,
            "delay": 100,
            "offset": 150,
            "easing": "ease-out-cubic",
            "once": False,
            "mirror": True,
            "anchorPlacement": "center-center",
            "disable": False
        }
    }
}

# Available configuration options
CONFIG_OPTIONS = {
    "duration": {
        "type": "number",
        "default": 800,
        "range": [0, 3000],
        "description": "Animation duration in milliseconds"
    },
    "delay": {
        "type": "number",
        "default": 0,
        "range": [0, 3000],
        "description": "Delay before animation starts (ms)"
    },
    "offset": {
        "type": "number",
        "default": 120,
        "description": "Offset (in px) from original trigger point"
    },
    "easing": {
        "type": "enum",
        "default": "ease",
        "values": [
            "linear", "ease", "ease-in", "ease-out", "ease-in-out",
            "ease-in-back", "ease-out-back", "ease-in-out-back",
            "ease-in-sine", "ease-out-sine", "ease-in-out-sine",
            "ease-in-quad", "ease-out-quad", "ease-in-out-quad",
            "ease-in-cubic", "ease-out-cubic", "ease-in-out-cubic",
            "ease-in-quart", "ease-out-quart", "ease-in-out-quart"
        ],
        "description": "Easing function for animations"
    },
    "once": {
        "type": "boolean",
        "default": False,
        "description": "Whether animation should happen only once"
    },
    "mirror": {
        "type": "boolean",
        "default": False,
        "description": "Whether elements should animate out while scrolling past them"
    },
    "anchorPlacement": {
        "type": "enum",
        "default": "top-bottom",
        "values": [
            "top-bottom", "top-center", "top-top",
            "center-bottom", "center-center", "center-top",
            "bottom-bottom", "bottom-center", "bottom-top"
        ],
        "description": "Anchor placement - which position triggers animation"
    },
    "disable": {
        "type": "mixed",
        "default": False,
        "values": [False, "mobile", "phone", "tablet"],
        "description": "Disable AOS on specific devices"
    },
    "startEvent": {
        "type": "enum",
        "default": "DOMContentLoaded",
        "values": ["DOMContentLoaded", "load"],
        "description": "Event on which AOS should be initialized"
    },
    "disableMutationObserver": {
        "type": "boolean",
        "default": False,
        "description": "Disable mutation observer (for static content)"
    },
    "throttleDelay": {
        "type": "number",
        "default": 99,
        "description": "Delay on throttle used while scrolling (ms)"
    },
    "debounceDelay": {
        "type": "number",
        "default": 50,
        "description": "Delay on debounce used while resizing window (ms)"
    }
}


def format_value(key, value):
    """Format configuration value for JavaScript output."""
    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is False:
        return "false"
    else:
        return str(value)


def generate_js_config(config, format_type="modern"):
    """Generate JavaScript AOS initialization code."""
    lines = []

    if format_type == "modern":
        lines.append("import AOS from 'aos';")
        lines.append("import 'aos/dist/aos.css';")
        lines.append("")
    elif format_type == "cdn":
        lines.append("<!-- Add to <head> -->")
        lines.append('<link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />')
        lines.append("")
        lines.append("<!-- Add before </body> -->")
        lines.append('<script src="https://unpkg.com/aos@next/dist/aos.js"></script>')
        lines.append("<script>")

    lines.append("AOS.init({")

    # Sort config keys for consistent output
    sorted_config = sorted(config.items())

    for i, (key, value) in enumerate(sorted_config):
        comma = "," if i < len(sorted_config) - 1 else ""

        # Add comment for each option
        if key in CONFIG_OPTIONS:
            lines.append(f"  // {CONFIG_OPTIONS[key]['description']}")

        lines.append(f"  {key}: {format_value(key, value)}{comma}")

    lines.append("});")

    if format_type == "cdn":
        lines.append("</script>")

    return "\n".join(lines)


def generate_react_config(config):
    """Generate React AOS initialization code."""
    lines = [
        "import { useEffect } from 'react';",
        "import AOS from 'aos';",
        "import 'aos/dist/aos.css';",
        "",
        "function App() {",
        "  useEffect(() => {",
        "    AOS.init({"
    ]

    sorted_config = sorted(config.items())

    for i, (key, value) in enumerate(sorted_config):
        comma = "," if i < len(sorted_config) - 1 else ""
        lines.append(f"      {key}: {format_value(key, value)}{comma}")

    lines.extend([
        "    });",
        "  }, []);",
        "",
        "  return (",
        "    <div>",
        "      <h1 data-aos=\"fade-down\">Your Content</h1>",
        "    </div>",
        "  );",
        "}"
    ])

    return "\n".join(lines)


def list_presets():
    """List all available configuration presets."""
    print("\nAvailable Presets:")
    print("=" * 60)

    for preset_id, preset in PRESETS.items():
        print(f"\n{preset_id}")
        print(f"  Name: {preset['name']}")
        print(f"  Description: {preset['description']}")
        print(f"  Config: {json.dumps(preset['config'], indent=2)}")

    print()


def interactive_mode():
    """Run interactive configuration builder."""
    print("\nAOS Config Builder - Interactive Mode")
    print("=" * 60)

    # Ask if user wants to start from a preset
    print("\nWould you like to start from a preset? (y/n)")
    use_preset = input("> ").strip().lower()

    config = {}

    if use_preset == 'y':
        list_presets()
        print("Enter preset name (or press Enter for default):")
        preset_name = input("> ").strip().lower()

        if preset_name in PRESETS:
            config = PRESETS[preset_name]["config"].copy()
            print(f"\nStarting with '{PRESETS[preset_name]['name']}' preset")
        else:
            print("\nNo preset selected, building from scratch")

    print("\nConfigure AOS options (press Enter to use default/current):")
    print("=" * 60)

    for option_name, option_info in CONFIG_OPTIONS.items():
        current_value = config.get(option_name, option_info["default"])

        print(f"\n{option_name}")
        print(f"  Description: {option_info['description']}")
        print(f"  Type: {option_info['type']}")
        print(f"  Current: {current_value}")

        if option_info["type"] == "enum" or option_info["type"] == "mixed":
            print(f"  Options: {', '.join(str(v) for v in option_info['values'])}")
        elif "range" in option_info:
            print(f"  Range: {option_info['range'][0]} - {option_info['range'][1]}")

        value = input("  Value: ").strip()

        if value:
            # Convert value based on type
            if option_info["type"] == "number":
                try:
                    config[option_name] = float(value) if '.' in value else int(value)
                except ValueError:
                    print("  Invalid number, using current value")
                    config[option_name] = current_value
            elif option_info["type"] == "boolean":
                config[option_name] = value.lower() in ["true", "yes", "1"]
            elif option_info["type"] == "mixed":
                if value.lower() in ["false", "no", "0"]:
                    config[option_name] = False
                else:
                    config[option_name] = value
            else:
                config[option_name] = value
        else:
            config[option_name] = current_value

    # Select output format
    print("\n\nSelect output format:")
    print("  1. Modern ES6 (import)")
    print("  2. CDN (script tags)")
    print("  3. React")

    format_choice = input("\nFormat (1-3): ").strip()

    print("\n" + "=" * 60)
    print("Generated Configuration:")
    print("=" * 60 + "\n")

    if format_choice == "2":
        print(generate_js_config(config, "cdn"))
    elif format_choice == "3":
        print(generate_react_config(config))
    else:
        print(generate_js_config(config, "modern"))

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate AOS initialization configurations"
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        help="Use a configuration preset"
    )
    parser.add_argument(
        "--format",
        choices=["modern", "cdn", "react"],
        default="modern",
        help="Output format (default: modern)"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available presets"
    )

    # Individual config options
    for option_name, option_info in CONFIG_OPTIONS.items():
        arg_name = f"--{option_name.replace('_', '-')}"

        if option_info["type"] == "boolean":
            parser.add_argument(arg_name, type=lambda x: x.lower() == 'true')
        elif option_info["type"] == "number":
            parser.add_argument(arg_name, type=int)
        else:
            parser.add_argument(arg_name, type=str)

    args = parser.parse_args()

    if args.list_presets:
        list_presets()
    elif args.preset or any(getattr(args, opt.replace('-', '_'), None) is not None
                           for opt in CONFIG_OPTIONS.keys()):
        # CLI mode with preset or custom config
        if args.preset:
            config = PRESETS[args.preset]["config"].copy()
        else:
            config = {}

        # Override with CLI arguments
        for option_name in CONFIG_OPTIONS.keys():
            arg_value = getattr(args, option_name, None)
            if arg_value is not None:
                config[option_name] = arg_value

        if args.format == "react":
            print(generate_react_config(config))
        else:
            print(generate_js_config(config, args.format))
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
