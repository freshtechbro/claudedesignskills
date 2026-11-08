#!/usr/bin/env python3
"""
Locomotive Scroll Configuration Generator

Generates Locomotive Scroll configuration code with customizable options.

Usage:
    ./generate_config.py                    # Interactive mode
    ./generate_config.py --smooth           # Quick smooth scroll setup
    ./generate_config.py --horizontal       # Horizontal scroll setup
    ./generate_config.py --preset performance  # Use performance preset
"""

import sys
import json

PRESETS = {
    "basic": {
        "name": "Basic Smooth Scroll",
        "options": {
            "smooth": True,
            "lerp": 0.1,
            "multiplier": 1,
        }
    },
    "smooth": {
        "name": "Premium Smooth Experience",
        "options": {
            "smooth": True,
            "lerp": 0.05,
            "multiplier": 1,
            "class": "is-inview",
            "offset": ["10%", 0],
            "getSpeed": True,
            "getDirection": True,
        }
    },
    "performance": {
        "name": "Performance Optimized",
        "options": {
            "smooth": True,
            "lerp": 0.1,
            "multiplier": 1,
            "smartphone": {
                "smooth": False,
                "breakpoint": 768
            },
            "tablet": {
                "smooth": True,
                "breakpoint": 1024
            }
        }
    },
    "horizontal": {
        "name": "Horizontal Scroll",
        "options": {
            "smooth": True,
            "direction": "horizontal",
            "lerp": 0.1,
            "multiplier": 1,
        }
    },
    "parallax": {
        "name": "Parallax & Detection",
        "options": {
            "smooth": True,
            "lerp": 0.08,
            "class": "is-inview",
            "offset": ["10%", 0],
            "repeat": False,
        }
    }
}


def print_header():
    print("=" * 60)
    print("Locomotive Scroll Configuration Generator")
    print("=" * 60)
    print()


def print_presets():
    print("Available Presets:")
    print()
    for i, (key, preset) in enumerate(PRESETS.items(), 1):
        print(f"  {i}. {preset['name']} ({key})")
    print()


def get_user_choice(prompt, options, default=None):
    """Get validated user input"""
    while True:
        if default:
            choice = input(f"{prompt} (default: {default}): ").strip() or default
        else:
            choice = input(f"{prompt}: ").strip()

        if choice in options:
            return choice
        print(f"Invalid choice. Please choose from: {', '.join(options)}")


def get_bool_input(prompt, default=True):
    """Get boolean input from user"""
    default_str = "Y/n" if default else "y/N"
    while True:
        choice = input(f"{prompt} ({default_str}): ").strip().lower() or ("y" if default else "n")
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        print("Please enter 'y' or 'n'")


def get_number_input(prompt, default, min_val=None, max_val=None):
    """Get numeric input with validation"""
    while True:
        value = input(f"{prompt} (default: {default}): ").strip() or str(default)
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and num > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return num
        except ValueError:
            print("Please enter a valid number")


def interactive_config():
    """Interactive configuration builder"""
    print_header()
    print("Let's build your Locomotive Scroll configuration!\n")

    # Ask if user wants a preset
    use_preset = get_bool_input("Start with a preset?", default=True)

    if use_preset:
        print_presets()
        preset_choice = get_user_choice(
            "Choose preset",
            list(PRESETS.keys()),
            default="basic"
        )
        config = PRESETS[preset_choice]["options"].copy()
        print(f"\n✅ Starting with '{PRESETS[preset_choice]['name']}' preset\n")
    else:
        config = {}

    # Core options
    print("Core Options:")
    print("-" * 40)

    if "smooth" not in config:
        config["smooth"] = get_bool_input("Enable smooth scrolling?", default=True)

    if config.get("smooth"):
        if "lerp" not in config:
            config["lerp"] = get_number_input(
                "Lerp value (smoothness, lower = smoother)",
                default=0.1,
                min_val=0.01,
                max_val=1.0
            )

    if "direction" not in config:
        direction = get_user_choice(
            "Scroll direction",
            ["vertical", "horizontal"],
            default="vertical"
        )
        if direction != "vertical":
            config["direction"] = direction

    if "multiplier" not in config:
        config["multiplier"] = get_number_input(
            "Speed multiplier",
            default=1,
            min_val=0.1,
            max_val=5.0
        )

    # Advanced options
    print("\nAdvanced Options:")
    print("-" * 40)

    if get_bool_input("Configure viewport detection?", default=False):
        config["class"] = input("In-view class name (default: is-inview): ").strip() or "is-inview"
        config["repeat"] = get_bool_input("Repeat in-view detection?", default=False)

        if get_bool_input("Set global offset?", default=False):
            bottom = input("Bottom offset (default: 0): ").strip() or "0"
            top = input("Top offset (default: 0): ").strip() or "0"
            config["offset"] = [bottom, top]

    if get_bool_input("Enable scroll tracking (speed/direction)?", default=False):
        config["getSpeed"] = True
        config["getDirection"] = True

    # Mobile options
    print("\nMobile/Tablet Options:")
    print("-" * 40)

    if get_bool_input("Configure mobile settings?", default=True):
        # Smartphone
        config["smartphone"] = {
            "smooth": get_bool_input("Enable smooth scroll on smartphones?", default=False),
            "breakpoint": int(get_number_input("Smartphone breakpoint", default=768, min_val=320))
        }

        # Tablet
        config["tablet"] = {
            "smooth": get_bool_input("Enable smooth scroll on tablets?", default=True),
            "breakpoint": int(get_number_input("Tablet breakpoint", default=1024, min_val=768))
        }

    return config


def generate_js_code(config):
    """Generate JavaScript initialization code"""
    code = f"""// Locomotive Scroll Configuration
import LocomotiveScroll from 'locomotive-scroll';
import 'locomotive-scroll/dist/locomotive-scroll.css';

const scroll = new LocomotiveScroll({{
  el: document.querySelector('[data-scroll-container]'),
{format_config_object(config, indent=1)}
}});

// Update on window resize
let resizeTimer;
window.addEventListener('resize', () => {{
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => scroll.update(), 250);
}});

// Cleanup
window.addEventListener('beforeunload', () => scroll.destroy());

export default scroll;
"""
    return code


def format_config_object(config, indent=0):
    """Format configuration object for JavaScript"""
    lines = []
    indent_str = "  " * indent

    for key, value in config.items():
        if isinstance(value, bool):
            lines.append(f"{indent_str}{key}: {str(value).lower()},")
        elif isinstance(value, (int, float)):
            lines.append(f"{indent_str}{key}: {value},")
        elif isinstance(value, str):
            lines.append(f"{indent_str}{key}: '{value}',")
        elif isinstance(value, list):
            formatted_list = str(value).replace("'", '"')
            lines.append(f"{indent_str}{key}: {formatted_list},")
        elif isinstance(value, dict):
            lines.append(f"{indent_str}{key}: {{")
            lines.append(format_config_object(value, indent + 1))
            lines.append(f"{indent_str}}},")

    return "\n".join(lines)


def generate_html_template():
    """Generate HTML template"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Locomotive Scroll</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/locomotive-scroll/dist/locomotive-scroll.min.css">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    [data-scroll-container] {
      /* Container styles */
    }

    [data-scroll-section] {
      min-height: 100vh;
      padding: 4rem 2rem;
    }

    .is-inview {
      opacity: 1;
      transform: translateY(0);
      transition: opacity 0.6s, transform 0.6s;
    }

    [data-scroll] {
      opacity: 0;
      transform: translateY(50px);
    }
  </style>
</head>
<body>
  <div data-scroll-container>

    <div data-scroll-section>
      <h1 data-scroll data-scroll-speed="2">
        Locomotive Scroll
      </h1>
      <p data-scroll data-scroll-speed="1">
        Smooth scrolling experience
      </p>
    </div>

    <div data-scroll-section>
      <h2 data-scroll>Section 2</h2>
      <div data-scroll data-scroll-sticky>
        Sticky element
      </div>
    </div>

    <div data-scroll-section>
      <h2 data-scroll>Section 3</h2>
      <p data-scroll data-scroll-call="playVideo">
        Triggers callback
      </p>
    </div>

  </div>

  <script type="module" src="main.js"></script>
</body>
</html>
"""


def main():
    """Main function"""
    # Check for CLI arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lstrip('-')

        if arg in PRESETS:
            config = PRESETS[arg]["options"].copy()
            print(f"✅ Using '{PRESETS[arg]['name']}' preset")
        elif arg == "help":
            print(__doc__)
            return
        else:
            print(f"Unknown option: {arg}")
            print("Available presets:", ", ".join(PRESETS.keys()))
            return
    else:
        # Interactive mode
        config = interactive_config()

    # Generate code
    print("\n" + "=" * 60)
    print("Generated Configuration")
    print("=" * 60 + "\n")

    js_code = generate_js_code(config)
    print("JavaScript (main.js):")
    print("-" * 60)
    print(js_code)

    # Ask if user wants HTML template
    if get_bool_input("\nGenerate HTML template?", default=True):
        html = generate_html_template()
        print("\nHTML (index.html):")
        print("-" * 60)
        print(html)

    # Save to files?
    if get_bool_input("\nSave to files?", default=True):
        with open("locomotive-config.js", "w") as f:
            f.write(js_code)
        print("✅ Saved to locomotive-config.js")

        with open("locomotive-template.html", "w") as f:
            f.write(generate_html_template())
        print("✅ Saved to locomotive-template.html")

        # Save config as JSON
        with open("locomotive-config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✅ Saved to locomotive-config.json")

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
