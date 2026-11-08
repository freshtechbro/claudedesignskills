#!/usr/bin/env python3
"""
Locomotive Scroll + GSAP ScrollTrigger Integration Helper

Generates integration code for Locomotive Scroll with GSAP ScrollTrigger.

Usage:
    ./integration_helper.py                           # Interactive mode
    ./integration_helper.py --pattern fade-in         # Generate specific pattern
    ./integration_helper.py --framework react         # Framework-specific code
"""

import sys

ANIMATION_PATTERNS = {
    "fade-in": {
        "name": "Fade In on Scroll",
        "description": "Elements fade in as they enter viewport",
        "code": """gsap.to('.fade-in', {
  scrollTrigger: {
    trigger: '.fade-in',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 50%',
    scrub: true
  },
  opacity: 1,
  y: 0,
  duration: 1
});""",
        "html": """<div class="fade-in" style="opacity: 0; transform: translateY(50px);">
  Fades in on scroll
</div>"""
    },
    "pin-section": {
        "name": "Pin Section",
        "description": "Pin section while scrolling",
        "code": """ScrollTrigger.create({
  trigger: '#pinned-section',
  scroller: '[data-scroll-container]',
  pin: true,
  start: 'top top',
  end: 'bottom bottom',
  pinSpacing: false
});""",
        "html": """<div data-scroll-section id="pinned-section">
  This section pins while you scroll
</div>"""
    },
    "timeline": {
        "name": "Scrubbed Timeline",
        "description": "Timeline scrubbed with scroll progress",
        "code": """const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '#animated-section',
    scroller: '[data-scroll-container]',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1,
    pin: true
  }
});

tl.from('.box-1', { x: -100, opacity: 0 })
  .from('.box-2', { x: 100, opacity: 0 })
  .from('.box-3', { y: 100, opacity: 0 })
  .to('.box-1', { rotation: 360, scale: 1.5 });""",
        "html": """<div data-scroll-section id="animated-section">
  <div class="box-1">Box 1</div>
  <div class="box-2">Box 2</div>
  <div class="box-3">Box 3</div>
</div>"""
    },
    "horizontal-scroll": {
        "name": "Horizontal Scroll",
        "description": "Horizontal scrolling panels",
        "code": """const sections = gsap.utils.toArray('.panel');

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '#horizontal-container',
    scroller: '[data-scroll-container]',
    pin: true,
    scrub: 1,
    end: () => `+=\${document.querySelector('#horizontal-container').offsetWidth}`
  }
});""",
        "html": """<div data-scroll-section id="horizontal-container" style="display: flex; width: 300vw;">
  <div class="panel" style="width: 100vw;">Panel 1</div>
  <div class="panel" style="width: 100vw;">Panel 2</div>
  <div class="panel" style="width: 100vw;">Panel 3</div>
</div>"""
    },
    "stagger": {
        "name": "Stagger Animation",
        "description": "Staggered element animations",
        "code": """gsap.from('.item', {
  scrollTrigger: {
    trigger: '.items-container',
    scroller: '[data-scroll-container]',
    start: 'top 80%',
    end: 'top 30%',
    scrub: 1
  },
  y: 100,
  opacity: 0,
  stagger: 0.2
});""",
        "html": """<div class="items-container" data-scroll-section>
  <div class="item">Item 1</div>
  <div class="item">Item 2</div>
  <div class="item">Item 3</div>
  <div class="item">Item 4</div>
</div>"""
    },
    "progress-based": {
        "name": "Progress-Based Animation",
        "description": "Sync with Locomotive Scroll progress",
        "code": """locoScroll.on('scroll', (args) => {
  if (args.currentElements['hero']) {
    const progress = args.currentElements['hero'].progress;

    gsap.to('#hero-image', {
      scale: 1 + progress * 0.5,
      rotation: progress * 360,
      duration: 0
    });
  }
});""",
        "html": """<div data-scroll data-scroll-id="hero">
  <img id="hero-image" src="hero.jpg" alt="Hero">
</div>"""
    }
}


def print_header():
    print("=" * 70)
    print("Locomotive Scroll + GSAP ScrollTrigger Integration Helper")
    print("=" * 70)
    print()


def print_patterns():
    print("Available Animation Patterns:")
    print()
    for i, (key, pattern) in enumerate(ANIMATION_PATTERNS.items(), 1):
        print(f"  {i}. {pattern['name']} ({key})")
        print(f"     {pattern['description']}")
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


def generate_base_integration():
    """Generate base Locomotive + GSAP integration code"""
    return """// Locomotive Scroll + GSAP ScrollTrigger Integration
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Initialize Locomotive Scroll
const locoScroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  smartphone: {
    smooth: true
  },
  tablet: {
    smooth: true
  }
});

// Sync Locomotive Scroll with ScrollTrigger
locoScroll.on('scroll', ScrollTrigger.update);

// Tell ScrollTrigger to use Locomotive Scroll's scroller
ScrollTrigger.scrollerProxy('[data-scroll-container]', {
  scrollTop(value) {
    return arguments.length
      ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
      : locoScroll.scroll.instance.scroll.y;
  },
  getBoundingClientRect() {
    return {
      top: 0,
      left: 0,
      width: window.innerWidth,
      height: window.innerHeight
    };
  },
  pinType: document.querySelector('[data-scroll-container]').style.transform
    ? 'transform'
    : 'fixed'
});

// Update ScrollTrigger when Locomotive Scroll updates
ScrollTrigger.addEventListener('refresh', () => locoScroll.update());

// Refresh both after DOM loads
ScrollTrigger.refresh();
"""


def generate_react_integration():
    """Generate React-specific integration"""
    return """import { useEffect, useRef } from 'react';
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

function App() {
  const scrollRef = useRef(null);
  const locoScrollRef = useRef(null);

  useEffect(() => {
    const locoScroll = new LocomotiveScroll({
      el: scrollRef.current,
      smooth: true,
      smartphone: { smooth: true },
      tablet: { smooth: true }
    });

    locoScrollRef.current = locoScroll;

    locoScroll.on('scroll', ScrollTrigger.update);

    ScrollTrigger.scrollerProxy(scrollRef.current, {
      scrollTop(value) {
        return arguments.length
          ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
          : locoScroll.scroll.instance.scroll.y;
      },
      getBoundingClientRect() {
        return {
          top: 0,
          left: 0,
          width: window.innerWidth,
          height: window.innerHeight
        };
      },
      pinType: scrollRef.current.style.transform ? 'transform' : 'fixed'
    });

    ScrollTrigger.addEventListener('refresh', () => locoScroll.update());
    ScrollTrigger.refresh();

    // Cleanup
    return () => {
      locoScroll.destroy();
      ScrollTrigger.getAll().forEach(st => st.kill());
    };
  }, []);

  // Add your animations in separate useEffect
  useEffect(() => {
    // Animation code here
  }, []);

  return (
    <div data-scroll-container ref={scrollRef}>
      <div data-scroll-section>
        {/* Your content */}
      </div>
    </div>
  );
}

export default App;
"""


def generate_vue_integration():
    """Generate Vue-specific integration"""
    return """<template>
  <div data-scroll-container ref="scrollContainer">
    <div data-scroll-section>
      <!-- Your content -->
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import LocomotiveScroll from 'locomotive-scroll';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default {
  setup() {
    const scrollContainer = ref(null);
    let locoScroll = null;

    onMounted(() => {
      locoScroll = new LocomotiveScroll({
        el: scrollContainer.value,
        smooth: true
      });

      locoScroll.on('scroll', ScrollTrigger.update);

      ScrollTrigger.scrollerProxy(scrollContainer.value, {
        scrollTop(value) {
          return arguments.length
            ? locoScroll.scrollTo(value, {duration: 0, disableLerp: true})
            : locoScroll.scroll.instance.scroll.y;
        },
        getBoundingClientRect() {
          return {
            top: 0,
            left: 0,
            width: window.innerWidth,
            height: window.innerHeight
          };
        },
        pinType: scrollContainer.value.style.transform ? 'transform' : 'fixed'
      });

      ScrollTrigger.addEventListener('refresh', () => locoScroll.update());
      ScrollTrigger.refresh();
    });

    onUnmounted(() => {
      if (locoScroll) locoScroll.destroy();
      ScrollTrigger.getAll().forEach(st => st.kill());
    });

    return { scrollContainer };
  }
};
</script>
"""


def main():
    """Main function"""
    # Check for CLI arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lstrip('-')

        if arg == "help":
            print(__doc__)
            return
        elif arg == "pattern":
            if len(sys.argv) > 2:
                pattern_key = sys.argv[2]
                if pattern_key in ANIMATION_PATTERNS:
                    pattern = ANIMATION_PATTERNS[pattern_key]
                    print(f"\n{pattern['name']}")
                    print("=" * 60)
                    print(f"{pattern['description']}\n")
                    print("JavaScript:")
                    print(pattern['code'])
                    print("\nHTML:")
                    print(pattern['html'])
                else:
                    print(f"Unknown pattern: {pattern_key}")
                    print("Available patterns:", ", ".join(ANIMATION_PATTERNS.keys()))
            else:
                print("Please specify a pattern")
            return
        elif arg == "framework":
            if len(sys.argv) > 2:
                framework = sys.argv[2].lower()
                if framework == "react":
                    print(generate_react_integration())
                elif framework == "vue":
                    print(generate_vue_integration())
                else:
                    print(f"Framework '{framework}' not supported. Available: react, vue")
            else:
                print("Please specify a framework (react or vue)")
            return

    # Interactive mode
    print_header()

    # Framework choice
    print("Choose your framework:")
    print("  1. Vanilla JavaScript")
    print("  2. React")
    print("  3. Vue")
    print()

    framework = get_user_choice("Framework", ["1", "2", "3"], default="1")

    print("\nGenerating base integration code...\n")
    print("=" * 70)

    if framework == "1":
        base_code = generate_base_integration()
        print(base_code)
    elif framework == "2":
        base_code = generate_react_integration()
        print(base_code)
    elif framework == "3":
        base_code = generate_vue_integration()
        print(base_code)

    # Add animation patterns
    if get_bool_input("\nAdd animation patterns?", default=True):
        print_patterns()

        patterns_to_add = []
        while True:
            pattern_key = get_user_choice(
                "Choose pattern (or 'done' to finish)",
                list(ANIMATION_PATTERNS.keys()) + ["done"],
                default="done"
            )

            if pattern_key == "done":
                break

            patterns_to_add.append(pattern_key)
            print(f"✅ Added {ANIMATION_PATTERNS[pattern_key]['name']}")

        if patterns_to_add:
            print("\n" + "=" * 70)
            print("Animation Patterns")
            print("=" * 70 + "\n")

            for pattern_key in patterns_to_add:
                pattern = ANIMATION_PATTERNS[pattern_key]
                print(f"// {pattern['name']}")
                print(f"// {pattern['description']}")
                print(pattern['code'])
                print()

            print("\n" + "=" * 70)
            print("Required HTML")
            print("=" * 70 + "\n")

            for pattern_key in patterns_to_add:
                pattern = ANIMATION_PATTERNS[pattern_key]
                print(f"<!-- {pattern['name']} -->")
                print(pattern['html'])
                print()

    # Save to file?
    if get_bool_input("\nSave to file?", default=True):
        filename = "locomotive-gsap-integration.js"

        with open(filename, "w") as f:
            f.write(base_code)

            if 'patterns_to_add' in locals() and patterns_to_add:
                f.write("\n// Animation Patterns\n")
                for pattern_key in patterns_to_add:
                    pattern = ANIMATION_PATTERNS[pattern_key]
                    f.write(f"\n// {pattern['name']}\n")
                    f.write(pattern['code'])
                    f.write("\n")

        print(f"✅ Saved to {filename}")

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
