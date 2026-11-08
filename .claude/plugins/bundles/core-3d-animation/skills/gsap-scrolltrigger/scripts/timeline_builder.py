#!/usr/bin/env python3
"""
GSAP Timeline Builder - Interactive

Interactive CLI tool to build complex GSAP timeline sequences step-by-step.
Helps visualize and generate timeline code with proper timing and positioning.

Usage:
    python3 timeline_builder.py
    python3 timeline_builder.py --output timeline.js
    python3 timeline_builder.py --load timeline.json --output code.js
"""

import argparse
import json
import sys
from pathlib import Path

class TimelineBuilder:
    """Interactive timeline builder."""

    def __init__(self):
        self.timeline_name = "tl"
        self.steps = []
        self.timeline_config = {
            "repeat": 0,
            "repeatDelay": 0,
            "yoyo": False,
            "paused": False,
            "scrollTrigger": None
        }
        self.labels = []

    def configure_timeline(self):
        """Configure timeline properties."""
        print("\n=== Timeline Configuration ===")

        name = input(f"Timeline variable name [{self.timeline_name}]: ").strip()
        if name:
            self.timeline_name = name

        repeat = input("Repeat count (0 = no repeat, -1 = infinite) [0]: ").strip()
        self.timeline_config["repeat"] = int(repeat) if repeat else 0

        if self.timeline_config["repeat"] != 0:
            repeat_delay = input("Repeat delay in seconds [0]: ").strip()
            self.timeline_config["repeatDelay"] = float(repeat_delay) if repeat_delay else 0

            yoyo = input("Yoyo (alternate direction)? (y/n) [n]: ").strip().lower()
            self.timeline_config["yoyo"] = yoyo == "y"

        paused = input("Start paused? (y/n) [n]: ").strip().lower()
        self.timeline_config["paused"] = paused == "y"

        scroll_trigger = input("Add ScrollTrigger? (y/n) [n]: ").strip().lower()
        if scroll_trigger == "y":
            self.configure_scroll_trigger()

    def configure_scroll_trigger(self):
        """Configure ScrollTrigger for timeline."""
        print("\n--- ScrollTrigger Configuration ---")

        trigger = input("Trigger element selector [.timeline-section]: ").strip()
        trigger = trigger or ".timeline-section"

        start = input("Start position [top 80%]: ").strip()
        start = start or "top 80%"

        end = input("End position (leave empty for auto): ").strip()

        scrub = input("Scrub? (y/n/number) [n]: ").strip().lower()
        if scrub == "y":
            scrub = True
        elif scrub == "n":
            scrub = None
        else:
            try:
                scrub = float(scrub)
            except:
                scrub = None

        pin = input("Pin element? (y/n) [n]: ").strip().lower()
        pin = pin == "y"

        markers = input("Show debug markers? (y/n) [n]: ").strip().lower()
        markers = markers == "y"

        self.timeline_config["scrollTrigger"] = {
            "trigger": trigger,
            "start": start,
            "end": end if end else None,
            "scrub": scrub,
            "pin": pin,
            "markers": markers
        }

    def add_step(self):
        """Add an animation step to the timeline."""
        print("\n=== Add Timeline Step ===")

        # Step type
        print("Animation type:")
        print("  1. to (animate TO values)")
        print("  2. from (animate FROM values)")
        print("  3. fromTo (define both start and end)")
        print("  4. set (instant, no animation)")
        print("  5. label (add timing label)")
        print("  6. call (callback function)")

        step_type = input("Choose type [1]: ").strip() or "1"

        if step_type == "5":
            return self.add_label()
        elif step_type == "6":
            return self.add_callback()

        # Target selector
        target = input("Target element selector (e.g., .box): ").strip()
        if not target:
            print("Error: Target is required")
            return

        # Properties
        print("\nAnimation properties (comma-separated):")
        print("  Examples: x, y, opacity, scale, rotation, backgroundColor")
        print("  Or type common presets: fade-in, slide-up, scale-up, rotate")

        props_input = input("Properties or preset: ").strip()
        props = self.parse_properties(props_input)

        # Duration
        duration = input("Duration in seconds [0.5]: ").strip()
        duration = float(duration) if duration else 0.5

        # Easing
        print("\nEasing (examples: power2.out, back.out(1.7), elastic.out)")
        ease = input("Easing [power2.out]: ").strip() or "power2.out"

        # Position parameter
        print("\nPosition in timeline:")
        print("  - Leave empty = append to end")
        print("  - Number (e.g., 2) = specific time")
        print("  - Relative (e.g., -=0.5) = 0.5s before previous ends")
        print("  - Relative (e.g., +=1) = 1s after previous ends")
        print("  - Label (e.g., midpoint) = at label position")

        position = input("Position: ").strip()

        step = {
            "type": self.get_method_name(step_type),
            "target": target,
            "properties": props,
            "duration": duration,
            "ease": ease,
            "position": position if position else None
        }

        # For fromTo, get initial values
        if step_type == "3":
            print("\nInitial values (FROM):")
            from_props = self.parse_properties(input("Properties: ").strip())
            step["from_properties"] = from_props

        self.steps.append(step)
        print(f"✅ Added: {step['type']}('{target}', ...)")

    def add_label(self):
        """Add a label to the timeline."""
        label_name = input("Label name: ").strip()
        if not label_name:
            print("Error: Label name is required")
            return

        position = input("Position (leave empty for current position): ").strip()

        self.labels.append({
            "name": label_name,
            "position": position if position else None
        })

        print(f"✅ Added label: '{label_name}'")

    def add_callback(self):
        """Add a callback to the timeline."""
        callback_name = input("Callback function name: ").strip()
        if not callback_name:
            print("Error: Callback name is required")
            return

        position = input("Position (leave empty for current position): ").strip()

        self.steps.append({
            "type": "call",
            "callback": callback_name,
            "position": position if position else None
        })

        print(f"✅ Added callback: {callback_name}()")

    def parse_properties(self, props_input):
        """Parse property input (preset or custom properties)."""
        presets = {
            "fade-in": {"opacity": 0},
            "fade-out": {"opacity": 0},
            "slide-up": {"y": 50, "opacity": 0},
            "slide-down": {"y": -50, "opacity": 0},
            "slide-left": {"x": 100, "opacity": 0},
            "slide-right": {"x": -100, "opacity": 0},
            "scale-up": {"scale": 0, "opacity": 0},
            "scale-down": {"scale": 1.5, "opacity": 0},
            "rotate": {"rotation": 360},
            "blur": {"filter": "blur(10px)"}
        }

        if props_input.lower() in presets:
            return presets[props_input.lower()]

        # Parse custom properties
        props = {}
        print("\nEnter property values (press Enter to skip):")

        prop_names = [p.strip() for p in props_input.split(",")]
        for prop_name in prop_names:
            value = input(f"  {prop_name}: ").strip()
            if value:
                # Try to convert to number
                try:
                    if "." in value:
                        props[prop_name] = float(value)
                    else:
                        props[prop_name] = int(value)
                except:
                    # Keep as string (for colors, etc.)
                    props[prop_name] = value

        return props

    def get_method_name(self, step_type):
        """Get GSAP method name from step type number."""
        methods = {
            "1": "to",
            "2": "from",
            "3": "fromTo",
            "4": "set"
        }
        return methods.get(step_type, "to")

    def visualize_timeline(self):
        """Visualize timeline structure."""
        if not self.steps:
            print("\n⚠️  Timeline is empty")
            return

        print("\n=== Timeline Visualization ===")
        print(f"Timeline: {self.timeline_name}")
        print(f"Steps: {len(self.steps)}")
        print(f"Labels: {len(self.labels)}")
        print()

        for i, step in enumerate(self.steps):
            if step["type"] == "call":
                position = step.get("position", "")
                print(f"  {i+1}. {step['type']}({step['callback']}){' at ' + position if position else ''}")
            else:
                target = step["target"]
                props = ", ".join(f"{k}={v}" for k, v in step["properties"].items())
                duration = step.get("duration", "")
                ease = step.get("ease", "")
                position = step.get("position", "")

                timing = f"{duration}s, {ease}" if duration and ease else ""
                pos_str = f" at {position}" if position else ""

                print(f"  {i+1}. {step['type']}('{target}', {{ {props} }}) [{timing}]{pos_str}")

        if self.labels:
            print("\nLabels:")
            for label in self.labels:
                pos = f" at {label['position']}" if label.get("position") else ""
                print(f"  - {label['name']}{pos}")

    def generate_code(self):
        """Generate GSAP timeline code."""
        lines = []

        # Imports
        lines.append('import gsap from "gsap";')

        if self.timeline_config.get("scrollTrigger"):
            lines.append('import { ScrollTrigger } from "gsap/ScrollTrigger";')
            lines.append('')
            lines.append('gsap.registerPlugin(ScrollTrigger);')

        lines.append('')

        # Timeline configuration
        config_parts = []

        if self.timeline_config["repeat"] != 0:
            config_parts.append(f'repeat: {self.timeline_config["repeat"]}')

            if self.timeline_config["repeatDelay"] > 0:
                config_parts.append(f'repeatDelay: {self.timeline_config["repeatDelay"]}')

            if self.timeline_config["yoyo"]:
                config_parts.append('yoyo: true')

        if self.timeline_config["paused"]:
            config_parts.append('paused: true')

        if self.timeline_config.get("scrollTrigger"):
            st = self.timeline_config["scrollTrigger"]
            st_parts = [f'trigger: "{st["trigger"]}"', f'start: "{st["start"]}"']

            if st.get("end"):
                st_parts.append(f'end: "{st["end"]}"')

            if st.get("scrub") is not None:
                if isinstance(st["scrub"], bool):
                    st_parts.append('scrub: true')
                else:
                    st_parts.append(f'scrub: {st["scrub"]}')

            if st.get("pin"):
                st_parts.append('pin: true')

            if st.get("markers"):
                st_parts.append('markers: true')

            st_config = ",\n    ".join(st_parts)
            config_parts.append(f'scrollTrigger: {{\n    {st_config}\n  }}')

        if config_parts:
            config_str = ",\n  ".join(config_parts)
            lines.append(f'const {self.timeline_name} = gsap.timeline({{')
            lines.append(f'  {config_str}')
            lines.append('});')
        else:
            lines.append(f'const {self.timeline_name} = gsap.timeline();')

        lines.append('')

        # Add steps
        for i, step in enumerate(self.steps):
            if step["type"] == "call":
                position = f', "{step["position"]}"' if step.get("position") else ""
                lines.append(f'{self.timeline_name}.call({step["callback"]}{position});')
                continue

            # Properties
            props_str = self.format_properties(step["properties"])

            # Build method call
            if step["type"] == "fromTo":
                from_props = self.format_properties(step["from_properties"])
                to_props = props_str.replace(f', duration: {step["duration"]}', "")
                to_props += f', duration: {step["duration"]}, ease: "{step["ease"]}"'

                position = f', "{step["position"]}"' if step.get("position") else ""
                lines.append(f'{self.timeline_name}.fromTo("{step["target"]}", {{ {from_props} }}, {{ {to_props} }}{position});')
            else:
                # Add duration and ease for animated methods
                if step["type"] != "set":
                    props_str += f', duration: {step["duration"]}, ease: "{step["ease"]}"'

                position = f', "{step["position"]}"' if step.get("position") else ""
                lines.append(f'{self.timeline_name}.{step["type"]}("{step["target"]}", {{ {props_str} }}{position});')

            # Add label if this step has one
            for label in self.labels:
                if label.get("after_step") == i:
                    lines.append(f'{self.timeline_name}.addLabel("{label["name"]}");')

        # Add labels at end
        for label in self.labels:
            if not label.get("after_step") and not label.get("position"):
                lines.append(f'{self.timeline_name}.addLabel("{label["name"]}");')

        return "\n".join(lines)

    def format_properties(self, props):
        """Format properties object for code generation."""
        parts = []
        for key, value in props.items():
            if isinstance(value, str):
                parts.append(f'{key}: "{value}"')
            else:
                parts.append(f'{key}: {value}')
        return ", ".join(parts)

    def save_timeline(self, filepath):
        """Save timeline configuration to JSON."""
        data = {
            "timeline_name": self.timeline_name,
            "config": self.timeline_config,
            "steps": self.steps,
            "labels": self.labels
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Timeline saved: {filepath}")

    def load_timeline(self, filepath):
        """Load timeline configuration from JSON."""
        with open(filepath, "r") as f:
            data = json.load(f)

        self.timeline_name = data.get("timeline_name", "tl")
        self.timeline_config = data.get("config", {})
        self.steps = data.get("steps", [])
        self.labels = data.get("labels", [])

        print(f"✅ Timeline loaded: {filepath}")

    def interactive_mode(self):
        """Run interactive timeline builder."""
        print("╔════════════════════════════════════════════════╗")
        print("║   GSAP Timeline Builder - Interactive Mode    ║")
        print("╚════════════════════════════════════════════════╝")

        self.configure_timeline()

        while True:
            print("\n" + "="*50)
            print("Options:")
            print("  1. Add animation step")
            print("  2. Add label")
            print("  3. Add callback")
            print("  4. Visualize timeline")
            print("  5. Generate code")
            print("  6. Save timeline (JSON)")
            print("  7. Configure timeline settings")
            print("  8. Exit")

            choice = input("\nChoose option: ").strip()

            if choice == "1":
                self.add_step()
            elif choice == "2":
                self.add_label()
            elif choice == "3":
                self.add_callback()
            elif choice == "4":
                self.visualize_timeline()
            elif choice == "5":
                code = self.generate_code()
                print("\n" + "="*50)
                print("Generated Code:")
                print("="*50)
                print(code)
                print("="*50)

                save = input("\nSave to file? (y/n): ").strip().lower()
                if save == "y":
                    filename = input("Filename [timeline.js]: ").strip() or "timeline.js"
                    Path(filename).write_text(code)
                    print(f"✅ Code saved: {filename}")
            elif choice == "6":
                filename = input("Filename [timeline.json]: ").strip() or "timeline.json"
                self.save_timeline(filename)
            elif choice == "7":
                self.configure_timeline()
            elif choice == "8":
                print("\n👋 Goodbye!")
                break
            else:
                print("⚠️  Invalid option")

def main():
    parser = argparse.ArgumentParser(
        description="Interactive GSAP Timeline Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python3 timeline_builder.py

  # Load existing timeline and generate code
  python3 timeline_builder.py --load timeline.json --output code.js

  # Save generated code to file
  python3 timeline_builder.py --output timeline.js

Workflow:
  1. Configure timeline (repeat, yoyo, ScrollTrigger)
  2. Add animation steps (to, from, fromTo, set)
  3. Add labels for complex timing
  4. Visualize timeline structure
  5. Generate and export code
        """
    )

    parser.add_argument("--load", "-l", help="Load timeline from JSON file")
    parser.add_argument("--output", "-o", help="Output file for generated code")

    args = parser.parse_args()

    builder = TimelineBuilder()

    # Load existing timeline if provided
    if args.load:
        try:
            builder.load_timeline(args.load)

            if args.output:
                # Generate and save code
                code = builder.generate_code()
                Path(args.output).write_text(code)
                print(f"✅ Generated code saved: {args.output}")
                return
        except FileNotFoundError:
            print(f"Error: File not found: {args.load}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON file: {args.load}")
            sys.exit(1)

    # Run interactive mode
    builder.interactive_mode()

    # Save code if output specified
    if args.output and builder.steps:
        code = builder.generate_code()
        Path(args.output).write_text(code)
        print(f"\n✅ Final code saved: {args.output}")

if __name__ == "__main__":
    main()
