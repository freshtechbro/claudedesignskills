#!/usr/bin/env python3
"""
GSAP Animation Code Generator

Generates boilerplate GSAP animation code for common patterns.
Supports various animation types, ScrollTrigger configurations, and export formats.

Usage:
    python3 generate_animation.py --type fade-in --trigger ".box" --output code.js
    python3 generate_animation.py --type horizontal-scroll --sections 5 --output code.js
    python3 generate_animation.py --type timeline --steps "fade,slide,scale" --output code.js
"""

import argparse
import sys
from pathlib import Path

# Animation Templates
TEMPLATES = {
    "fade-in": '''// Fade in animation
gsap.from("{trigger}", {{
  opacity: 0,
  y: {distance},
  duration: {duration},
  ease: "{ease}",
  scrollTrigger: {{
    trigger: "{trigger}",
    start: "{start}",
    end: "{end}",
    toggleActions: "{toggle_actions}"{scrub}{markers}
  }}
}});''',

    "fade-in-scrub": '''// Fade in with scroll scrubbing
gsap.from("{trigger}", {{
  opacity: 0,
  y: {distance},
  scrollTrigger: {{
    trigger: "{trigger}",
    start: "{start}",
    end: "{end}",
    scrub: {scrub_value}{markers}
  }}
}});''',

    "pin-section": '''// Pin section while scrolling
ScrollTrigger.create({{
  trigger: "{trigger}",
  start: "{start}",
  end: "{end}",
  pin: true,
  pinSpacing: {pin_spacing},
  anticipatePin: 1{markers}
}});''',

    "pin-with-animation": '''// Pin with content animation
const tl = gsap.timeline({{
  scrollTrigger: {{
    trigger: "{trigger}",
    start: "{start}",
    end: "{end}",
    pin: true,
    scrub: {scrub_value}{markers}
  }}
}});

tl.from("{trigger} .content", {{ opacity: 0, y: 100 }})
  .from("{trigger} .subtitle", {{ opacity: 0, y: 50 }}, "-=0.5")
  .to("{trigger} .image", {{ scale: 1.2, rotation: 5 }});''',

    "horizontal-scroll": '''// Horizontal scroll
const sections = gsap.utils.toArray("{trigger}");
gsap.to(sections, {{
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {{
    trigger: "{container}",
    pin: true,
    scrub: 1,
    snap: {snap},
    end: () => "+=" + document.querySelector("{container}").offsetWidth{markers}
  }}
}});''',

    "parallax": '''// Parallax effect
gsap.to("{trigger}", {{
  y: {distance},
  ease: "none",
  scrollTrigger: {{
    trigger: "{container}",
    start: "top bottom",
    end: "bottom top",
    scrub: true{markers}
  }}
}});''',

    "stagger": '''// Stagger animation
gsap.from("{trigger}", {{
  opacity: 0,
  y: {distance},
  duration: {duration},
  ease: "{ease}",
  stagger: {{
    each: {stagger_delay},
    from: "{stagger_from}"{stagger_grid}
  }},
  scrollTrigger: {{
    trigger: "{container}",
    start: "{start}"{markers}
  }}
}});''',

    "timeline": '''// Timeline sequence
const tl = gsap.timeline({{
  scrollTrigger: {{
    trigger: "{trigger}",
    start: "{start}"{markers}
  }}
}});

{timeline_steps}''',

    "batch": '''// Batch animation
ScrollTrigger.batch("{trigger}", {{
  onEnter: batch => gsap.from(batch, {{
    opacity: 0,
    y: {distance},
    stagger: {stagger_delay},
    duration: {duration},
    ease: "{ease}"
  }}),
  start: "{start}",
  once: {once}{markers}
}});''',

    "toggle-class": '''// Toggle class on scroll
ScrollTrigger.create({{
  trigger: "{trigger}",
  start: "{start}",
  end: "{end}",
  toggleClass: {{ targets: "{trigger}", className: "{class_name}" }}{markers}
}});''',

    "image-sequence": '''// Canvas image sequence
const canvas = document.querySelector("{canvas}");
const context = canvas.getContext("2d");

const frameCount = {frame_count};
const images = [];
const imageSeq = {{ frame: 0 }};

// Preload images
for (let i = 0; i < frameCount; i++) {{
  const img = new Image();
  img.src = `{image_path}/frame_${{String(i).padStart(4, '0')}}.jpg`;
  images.push(img);
}}

function render() {{
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(images[imageSeq.frame], 0, 0);
}}

gsap.to(imageSeq, {{
  frame: frameCount - 1,
  snap: "frame",
  ease: "none",
  scrollTrigger: {{
    trigger: "{trigger}",
    start: "top top",
    end: "+=3000",
    pin: true,
    scrub: 0.5,
    onUpdate: render{markers}
  }}
}});

images[0].onload = render;''',

    "smooth-scroll-to": '''// Smooth scroll to element
document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
  anchor.addEventListener("click", function(e) {{
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));

    gsap.to(window, {{
      duration: {duration},
      scrollTo: {{ y: target, offsetY: {offset} }},
      ease: "{ease}"
    }});
  }});
}});''',

    "progress-bar": '''// Progress bar
gsap.to("{trigger}", {{
  scaleX: 1,
  ease: "none",
  scrollTrigger: {{
    start: "top top",
    end: "bottom bottom",
    scrub: 0.3{markers}
  }}
}});

// CSS required:
// {trigger} {{ transform-origin: left; }}''',
}

# Timeline step templates
TIMELINE_STEPS = {
    "fade": 'tl.from("{selector}", {{ opacity: 0, duration: 0.6 }})',
    "slide": 'tl.from("{selector}", {{ y: 50, duration: 0.5 }}, "-=0.3")',
    "scale": 'tl.from("{selector}", {{ scale: 0, duration: 0.4, ease: "back.out(1.7)" }})',
    "rotate": 'tl.to("{selector}", {{ rotation: 360, duration: 1 }})',
    "color": 'tl.to("{selector}", {{ backgroundColor: "#ff0000", duration: 0.5 }})',
}

# Preset configurations
PRESETS = {
    "subtle": {
        "duration": 0.6,
        "distance": 30,
        "ease": "power1.out"
    },
    "standard": {
        "duration": 0.8,
        "distance": 50,
        "ease": "power2.out"
    },
    "dramatic": {
        "duration": 1.2,
        "distance": 100,
        "ease": "power3.out"
    },
    "playful": {
        "duration": 0.8,
        "distance": 50,
        "ease": "back.out(1.7)"
    }
}

def generate_animation(args):
    """Generate GSAP animation code based on arguments."""

    template = TEMPLATES.get(args.type)
    if not template:
        print(f"Error: Unknown animation type '{args.type}'")
        print(f"Available types: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    # Get preset values
    preset = PRESETS.get(args.preset, PRESETS["standard"])

    # Prepare template variables
    variables = {
        "trigger": args.trigger,
        "container": args.container or args.trigger,
        "canvas": args.canvas or "#canvas",
        "start": args.start,
        "end": args.end,
        "duration": args.duration or preset["duration"],
        "distance": args.distance or preset["distance"],
        "ease": args.ease or preset["ease"],
        "toggle_actions": args.toggle_actions,
        "scrub": f",\n    scrub: {args.scrub}" if args.scrub and args.type != "fade-in" else "",
        "scrub_value": args.scrub if args.scrub else 1,
        "markers": f",\n    markers: {str(args.markers).lower()}" if args.markers else "",
        "pin_spacing": str(args.pin_spacing).lower(),
        "snap": f"1 / (sections.length - 1)" if args.snap else "false",
        "stagger_delay": args.stagger_delay,
        "stagger_from": args.stagger_from,
        "stagger_grid": f',\n    grid: "auto"' if args.stagger_grid else "",
        "once": str(args.once).lower(),
        "class_name": args.class_name or "active",
        "frame_count": args.frame_count or 100,
        "image_path": args.image_path or "./frames",
        "offset": args.offset or 100,
    }

    # Handle timeline steps
    if args.type == "timeline" and args.timeline_steps:
        steps = args.timeline_steps.split(",")
        timeline_code = []
        for i, step in enumerate(steps):
            step = step.strip()
            selector = f"{args.trigger} .step-{i+1}"
            if step in TIMELINE_STEPS:
                timeline_code.append(TIMELINE_STEPS[step].format(selector=selector))
        variables["timeline_steps"] = ";\n".join(timeline_code) + ";"

    # Generate code
    code = template.format(**variables)

    return code

def generate_imports(framework="vanilla"):
    """Generate import statements based on framework."""
    if framework == "vanilla":
        return '''import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

'''
    elif framework == "react":
        return '''import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function Component() {
  const containerRef = useRef();

  useGSAP(() => {
    // Animation code goes here
'''
    elif framework == "vue":
        return '''import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { onMounted } from "vue";

gsap.registerPlugin(ScrollTrigger);

export default {
  setup() {
    onMounted(() => {
      // Animation code goes here
'''
    return ""

def generate_wrapper(code, framework="vanilla"):
    """Wrap code with framework-specific setup."""
    imports = generate_imports(framework)

    if framework == "vanilla":
        return f'''{imports}
// Wait for DOM
document.addEventListener("DOMContentLoaded", () => {{

{code}

  // Refresh after images load
  window.addEventListener("load", () => {{
    ScrollTrigger.refresh();
  }});

}});
'''
    elif framework == "react":
        return f'''{imports}
{code}

  }}, {{ scope: containerRef }});

  return <div ref={{containerRef}}>...</div>;
}}
'''
    elif framework == "vue":
        return f'''{imports}
{code}

      // Refresh after mount
      ScrollTrigger.refresh();
    }});
  }}
}};
'''
    return code

def main():
    parser = argparse.ArgumentParser(
        description="Generate GSAP animation boilerplate code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic fade in
  python3 generate_animation.py --type fade-in --trigger ".box"

  # Fade in with scrubbing
  python3 generate_animation.py --type fade-in-scrub --trigger ".hero" --markers

  # Pin section
  python3 generate_animation.py --type pin-section --trigger ".panel"

  # Horizontal scroll
  python3 generate_animation.py --type horizontal-scroll --trigger ".panel" --container ".container" --snap

  # Parallax
  python3 generate_animation.py --type parallax --trigger ".bg" --distance 200

  # Stagger animation
  python3 generate_animation.py --type stagger --trigger ".card" --stagger-from center --stagger-grid

  # Timeline with steps
  python3 generate_animation.py --type timeline --trigger ".sequence" --timeline-steps "fade,slide,scale"

  # Batch animation
  python3 generate_animation.py --type batch --trigger ".item" --once

  # Image sequence
  python3 generate_animation.py --type image-sequence --trigger ".canvas-section" --frame-count 148

  # Progress bar
  python3 generate_animation.py --type progress-bar --trigger ".progress"

  # Generate React component
  python3 generate_animation.py --type fade-in --trigger ".box" --framework react --output Component.jsx

Animation Types:
  fade-in, fade-in-scrub, pin-section, pin-with-animation, horizontal-scroll,
  parallax, stagger, timeline, batch, toggle-class, image-sequence,
  smooth-scroll-to, progress-bar
        """
    )

    parser.add_argument("--type", required=True, help="Animation type")
    parser.add_argument("--trigger", default=".element", help="Trigger element selector")
    parser.add_argument("--container", help="Container element selector")
    parser.add_argument("--canvas", help="Canvas selector for image sequences")
    parser.add_argument("--start", default="top 80%", help="ScrollTrigger start position")
    parser.add_argument("--end", default="bottom 20%", help="ScrollTrigger end position")
    parser.add_argument("--duration", type=float, help="Animation duration in seconds")
    parser.add_argument("--distance", type=int, help="Movement distance in pixels")
    parser.add_argument("--ease", help="Easing function (e.g., power2.out)")
    parser.add_argument("--scrub", type=float, help="Scrub value (true = 1, or number for lag)")
    parser.add_argument("--markers", action="store_true", help="Show debug markers")
    parser.add_argument("--pin-spacing", type=bool, default=True, help="Pin spacing for pinned sections")
    parser.add_argument("--snap", action="store_true", help="Enable snap points")
    parser.add_argument("--stagger-delay", type=float, default=0.1, help="Stagger delay between elements")
    parser.add_argument("--stagger-from", default="start", help="Stagger from (start, center, end, edges, random)")
    parser.add_argument("--stagger-grid", action="store_true", help="Enable grid stagger")
    parser.add_argument("--toggle-actions", default="play none none reverse", help="ScrollTrigger toggle actions")
    parser.add_argument("--once", action="store_true", help="Trigger animation only once")
    parser.add_argument("--class-name", help="Class name to toggle")
    parser.add_argument("--frame-count", type=int, help="Number of frames for image sequence")
    parser.add_argument("--image-path", help="Path to image sequence frames")
    parser.add_argument("--offset", type=int, help="Scroll offset in pixels")
    parser.add_argument("--timeline-steps", help="Comma-separated timeline steps (fade,slide,scale,rotate,color)")
    parser.add_argument("--preset", default="standard", choices=["subtle", "standard", "dramatic", "playful"], help="Animation preset")
    parser.add_argument("--framework", default="vanilla", choices=["vanilla", "react", "vue"], help="Framework wrapper")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    # Generate animation code
    animation_code = generate_animation(args)

    # Wrap with framework setup
    full_code = generate_wrapper(animation_code, args.framework)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(full_code)
        print(f"✅ Generated animation code: {output_path}")
    else:
        print(full_code)

if __name__ == "__main__":
    main()
