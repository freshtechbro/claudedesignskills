#!/usr/bin/env python3
"""
Props Generator

Generates component prop configurations for Magic UI and React Bits components.
Outputs TypeScript/JSX code with customizable prop values.

Usage:
    ./props_generator.py                                    # Interactive mode
    ./props_generator.py --component shimmer-button --format typescript
    ./props_generator.py --component blur-text --format jsx
"""

import sys
import argparse
import json

# Component prop templates
COMPONENT_PROPS = {
    "shimmer-button": {
        "library": "Magic UI",
        "props": {
            "shimmerColor": {"type": "string", "default": "#ffffff"},
            "shimmerSize": {"type": "string", "default": "0.05em"},
            "shimmerDuration": {"type": "string", "default": "3s"},
            "borderRadius": {"type": "string", "default": "100px"},
            "background": {"type": "string", "default": "rgba(0, 0, 0, 1)"},
            "className": {"type": "string", "default": "px-8 py-3"}
        }
    },
    "grid-pattern": {
        "library": "Magic UI",
        "props": {
            "width": {"type": "number", "default": 40},
            "height": {"type": "number", "default": 40},
            "x": {"type": "number", "default": -1},
            "y": {"type": "number", "default": -1},
            "squares": {"type": "array", "default": "[[4, 4], [8, 2]]"},
            "strokeDasharray": {"type": "string", "default": "0"},
            "className": {"type": "string", "default": ""}
        }
    },
    "animated-grid-pattern": {
        "library": "Magic UI",
        "props": {
            "numSquares": {"type": "number", "default": 50},
            "maxOpacity": {"type": "number", "default": 0.5},
            "duration": {"type": "number", "default": 4},
            "repeatDelay": {"type": "number", "default": 0.5},
            "className": {"type": "string", "default": ""}
        }
    },
    "blur-text": {
        "library": "React Bits",
        "props": {
            "text": {"type": "string", "default": "Your text here", "required": True},
            "delay": {"type": "number", "default": 100},
            "animateBy": {"type": "enum", "values": ["characters", "words"], "default": "words"},
            "direction": {"type": "enum", "values": ["top", "bottom", "left", "right"], "default": "top"},
            "threshold": {"type": "number", "default": 0.1},
            "className": {"type": "string", "default": ""}
        }
    },
    "count-up": {
        "library": "React Bits",
        "props": {
            "start": {"type": "number", "default": 0},
            "end": {"type": "number", "default": 100, "required": True},
            "duration": {"type": "number", "default": 2},
            "decimals": {"type": "number", "default": 0},
            "prefix": {"type": "string", "default": ""},
            "suffix": {"type": "string", "default": ""},
            "separator": {"type": "string", "default": ""},
            "className": {"type": "string", "default": ""}
        }
    },
    "particles": {
        "library": "React Bits",
        "props": {
            "particleCount": {"type": "number", "default": 200},
            "particleColors": {"type": "array", "default": "['#ffffff']"},
            "particleSpread": {"type": "number", "default": 10},
            "speed": {"type": "number", "default": 0.1},
            "moveParticlesOnHover": {"type": "boolean", "default": False},
            "particleBaseSize": {"type": "number", "default": 100},
            "className": {"type": "string", "default": ""}
        }
    },
    "magnet": {
        "library": "React Bits",
        "props": {
            "magnitude": {"type": "number", "default": 0.3},
            "maxDistance": {"type": "number", "default": 150},
            "damping": {"type": "number", "default": 25},
            "stiffness": {"type": "number", "default": 200},
            "className": {"type": "string", "default": ""}
        }
    },
    "marquee": {
        "library": "Magic UI",
        "props": {
            "reverse": {"type": "boolean", "default": False},
            "pauseOnHover": {"type": "boolean", "default": False},
            "vertical": {"type": "boolean", "default": False},
            "repeat": {"type": "number", "default": 4},
            "className": {"type": "string", "default": ""}
        }
    }
}


def format_prop_value(prop_type, value):
    """Format prop value based on type."""
    if prop_type == "string":
        return f'"{value}"'
    elif prop_type == "boolean":
        return "true" if value else "false"
    elif prop_type == "array":
        return value  # Already formatted
    elif prop_type == "enum":
        return f'"{value}"'
    else:  # number
        return str(value)


def generate_tsx_code(component_name, custom_props=None):
    """Generate TypeScript/JSX code for component."""
    if component_name not in COMPONENT_PROPS:
        return f"Error: Component '{component_name}' not found"

    comp = COMPONENT_PROPS[component_name]
    props = comp["props"].copy()

    # Apply custom props
    if custom_props:
        for key, value in custom_props.items():
            if key in props:
                props[key]["default"] = value

    # Generate import statement
    if comp["library"] == "Magic UI":
        component_pascal = ''.join(word.capitalize() for word in component_name.split('-'))
        import_stmt = f'import {{ {component_pascal} }} from "@/components/ui/{component_name}"'
    else:  # React Bits
        component_pascal = ''.join(word.capitalize() for word in component_name.split('-'))
        import_stmt = f'import {component_pascal} from "./components/{component_pascal}"'

    # Generate component code
    code_lines = [import_stmt, "", f"<{component_pascal}"]

    for prop_name, prop_info in props.items():
        value = format_prop_value(prop_info["type"], prop_info["default"])

        # Skip empty strings for className
        if prop_name == "className" and prop_info["default"] == "":
            continue

        code_lines.append(f"  {prop_name}={{{value}}}")

    code_lines.append(">")

    # Add children for certain components
    if component_name in ["shimmer-button", "magnet"]:
        code_lines.append("  {children}")
        code_lines.append(f"</{component_pascal}>")
    elif component_name == "marquee":
        code_lines.append("  {items.map((item) => (")
        code_lines.append("    <div key={item.id}>{item.content}</div>")
        code_lines.append("  ))}")
        code_lines.append(f"</{component_pascal}>")
    else:
        code_lines.append(f"/>")

    return "\n".join(code_lines)


def generate_jsx_code(component_name, custom_props=None):
    """Generate JSX code for component (similar to TSX but without type annotations)."""
    # For this simple generator, JSX is the same as TSX
    return generate_tsx_code(component_name, custom_props)


def list_available_components():
    """List all available components."""
    print("\nAvailable Components:")
    print("="*60)

    magic_ui = [k for k, v in COMPONENT_PROPS.items() if v["library"] == "Magic UI"]
    react_bits = [k for k, v in COMPONENT_PROPS.items() if v["library"] == "React Bits"]

    print("\nMagic UI:")
    for comp in magic_ui:
        print(f"  - {comp}")

    print("\nReact Bits:")
    for comp in react_bits:
        print(f"  - {comp}")

    print()


def interactive_mode():
    """Run interactive props generator."""
    print("\nProps Generator - Interactive Mode")
    print("="*60)

    list_available_components()

    component = input("Enter component name: ").strip().lower()

    if component not in COMPONENT_PROPS:
        print(f"Error: Component '{component}' not found")
        return

    comp_info = COMPONENT_PROPS[component]

    print(f"\n{comp_info['library']}: {component}")
    print("="*60)

    print("\nAvailable props (press Enter to use default):")

    custom_props = {}
    for prop_name, prop_info in comp_info["props"].items():
        required_marker = " (required)" if prop_info.get("required") else ""
        default_display = prop_info["default"]

        if prop_info["type"] == "enum":
            print(f"\n{prop_name}{required_marker} (options: {', '.join(prop_info['values'])})")
        else:
            print(f"\n{prop_name}{required_marker}")

        print(f"  Type: {prop_info['type']}")
        print(f"  Default: {default_display}")

        value = input(f"  Value: ").strip()

        if value:
            # Convert value based on type
            if prop_info["type"] == "number":
                try:
                    custom_props[prop_name] = float(value) if '.' in value else int(value)
                except ValueError:
                    print("  Invalid number, using default")
            elif prop_info["type"] == "boolean":
                custom_props[prop_name] = value.lower() in ["true", "yes", "1"]
            else:
                custom_props[prop_name] = value

    print("\nGenerated code:")
    print("="*60)
    print(generate_tsx_code(component, custom_props))
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate component prop configurations"
    )
    parser.add_argument(
        "--component",
        help="Component name (e.g., 'shimmer-button', 'blur-text')"
    )
    parser.add_argument(
        "--format",
        choices=["tsx", "jsx"],
        default="tsx",
        help="Output format (tsx or jsx)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available components"
    )
    parser.add_argument(
        "--props",
        help="Custom props as JSON string"
    )

    args = parser.parse_args()

    if args.list:
        list_available_components()
    elif args.component:
        custom_props = None
        if args.props:
            try:
                custom_props = json.loads(args.props)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in --props argument")
                return

        if args.format == "tsx":
            print(generate_tsx_code(args.component, custom_props))
        else:
            print(generate_jsx_code(args.component, custom_props))
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
