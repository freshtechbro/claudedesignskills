---
name: gsap-scrolltrigger
description: Comprehensive skill for GSAP (GreenSock Animation Platform) and ScrollTrigger plugin. Use this skill when creating web animations, scroll-driven experiences, timelines, tweens, scroll-triggered animations, pinning, scrubbing, parallax effects, or animating DOM elements, SVG, Canvas, WebGL, or Three.js. Triggers on tasks involving GSAP, ScrollTrigger, smooth animations, scroll effects, or animation sequencing.
---

# GSAP & ScrollTrigger Development

## Core Concepts

### Tweens

```javascript
// Animate TO a state (from current)
gsap.to(".box", {
  x: 200,
  rotation: 360,
  duration: 1,
  ease: "power2.inOut"
});

// Animate FROM a state (to current)
gsap.from(".box", {
  opacity: 0,
  y: -50,
  duration: 0.8
});

// Animate FROM-TO (define both start and end)
gsap.fromTo(".box",
  { opacity: 0, scale: 0.5 }, // FROM
  { opacity: 1, scale: 1, duration: 1 } // TO
);
```

### Timelines

```javascript
const tl = gsap.timeline();

// Sequential by default
tl.to(".box1", { x: 100, duration: 1 })
  .to(".box2", { y: 100, duration: 1 })
  .to(".box3", { rotation: 360, duration: 1 });

// With labels for organization
tl.addLabel("start")
  .to(".hero", { opacity: 1, duration: 1 })
  .addLabel("reveal")
  .to(".content", { y: 0, duration: 0.8 }, "reveal") // Start at "reveal" label
  .to(".cta", { scale: 1, duration: 0.5 }, "reveal+=0.5"); // 0.5s after "reveal"
```

### Position Parameter (Timeline Timing)

Control when animations start within a timeline:

```javascript
const tl = gsap.timeline();

// Default: One after another
tl.to(".box1", { x: 100 })
  .to(".box2", { x: 100 }); // Starts after box1 finishes

// Start at the same time
tl.to(".box1", { x: 100 })
  .to(".box2", { y: 100 }, 0); // Starts at 0 seconds

// Relative positioning
tl.to(".box1", { x: 100, duration: 2 })
  .to(".box2", { y: 100 }, "-=1"); // Starts 1 second before box1 ends
  .to(".box3", { rotation: 360 }, "+=0.5"); // Starts 0.5s after box2 finishes

// At a specific time
tl.to(".box1", { x: 100 }, 2.5); // Starts at 2.5 seconds
```

## ScrollTrigger Fundamentals

### Basic Scroll Animation

```javascript
gsap.registerPlugin(ScrollTrigger);

gsap.to(".box", {
  x: 500,
  scrollTrigger: {
    trigger: ".box",
    start: "top center", // When top of trigger hits center of viewport
    end: "bottom center",
    markers: true, // Development only - shows start/end positions
    scrub: true, // Links animation to scrollbar
    toggleActions: "play none none reverse" // onEnter onLeave onEnterBack onLeaveBack
  }
});
```

> Start/end positions, scrub options, toggleActions reference → see `references/api_reference.md`

## Common Patterns

### 1. Fade In On Scroll

```javascript
gsap.from(".fade-in", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: ".fade-in",
    start: "top 80%",
    end: "top 50%",
    scrub: 1,
    once: true // Only animate once
  }
});
```

### 2. Pin Element While Scrolling

```javascript
ScrollTrigger.create({
  trigger: ".panel",
  start: "top top",
  end: "+=500", // Pin for 500px of scrolling
  pin: true,
  pinSpacing: true // Add spacing (default true)
});
```

### 3. Horizontal Scroll Section

```javascript
const sections = gsap.utils.toArray(".panel");

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".container").offsetWidth
  }
});
```

### 4. Parallax Effect

```javascript
// Slower movement (background layer)
gsap.to(".bg", {
  y: 200,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});

// Faster movement (foreground layer)
gsap.to(".fg", {
  y: -100,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

### 5. Scroll-Triggered Timeline

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".container",
    start: "top top",
    end: "+=500",
    scrub: 1,
    pin: true,
    snap: {
      snapTo: "labels", // Snap to timeline labels
      duration: { min: 0.2, max: 3 },
      delay: 0.2,
      ease: "power1.inOut"
    }
  }
});

tl.addLabel("start")
  .from(".title", { scale: 0.3, rotation: 45, autoAlpha: 0 })
  .addLabel("color")
  .from(".box", { backgroundColor: "#28a92b" })
  .addLabel("spin")
  .to(".box", { rotation: 360 })
  .addLabel("end");
```

### 6. Batch Animations (Multiple Elements)

```javascript
// Loop through multiple elements
gsap.utils.toArray(".box").forEach((box, i) => {
  gsap.from(box, {
    y: 100,
    opacity: 0,
    scrollTrigger: {
      trigger: box,
      start: "top 80%",
      end: "top 50%",
      scrub: 1
    }
  });
});

// Or use ScrollTrigger.batch
ScrollTrigger.batch(".box", {
  onEnter: batch => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.15 }),
  onLeave: batch => gsap.set(batch, { opacity: 0 }),
  start: "top 80%",
  once: true
});
```

### 7. Staggered Animations

```javascript
gsap.from(".item", {
  y: 50,
  opacity: 0,
  duration: 0.8,
  stagger: 0.1, // 0.1s between each item
  scrollTrigger: {
    trigger: ".grid",
    start: "top 80%"
  }
});

// Advanced stagger
gsap.from(".item", {
  scale: 0,
  duration: 1,
  stagger: {
    each: 0.1,
    from: "center", // "start", "center", "end", "edges", or index number
    grid: "auto", // For grid layouts
    ease: "power2.inOut"
  }
});
```

## Integration Patterns

### With Three.js / WebGL

```javascript
import * as THREE from 'three';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// Animate camera
gsap.to(camera.position, {
  x: 5,
  y: 3,
  z: 10,
  scrollTrigger: {
    trigger: "#section2",
    start: "top top",
    end: "bottom top",
    scrub: 1,
    onUpdate: () => camera.lookAt(scene.position)
  }
});

// Animate mesh rotation
gsap.to(mesh.rotation, {
  y: Math.PI * 2,
  scrollTrigger: {
    trigger: "#section3",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});

// Animate material properties
gsap.to(material, {
  opacity: 0,
  scrollTrigger: {
    trigger: "#section4",
    start: "top center",
    end: "center center",
    scrub: 1
  }
});
```

### With React (useGSAP Hook)

```javascript
import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

function Component() {
  const container = useRef();
  const box = useRef();

  useGSAP(() => {
    gsap.to(box.current, {
      x: 200,
      scrollTrigger: {
        trigger: box.current,
        start: "top center",
        end: "bottom center",
        scrub: true,
        markers: true
      }
    });
  }, { scope: container }); // Scoping for cleanup

  return (
    <div ref={container}>
      <div ref={box} className="box">Animated Box</div>
    </div>
  );
}
```

> Shared React timelines, Locomotive Scroll, image sequence scrubbing → see `references/common_patterns.md`

### Conditional Animations (Media Queries)

```javascript
ScrollTrigger.matchMedia({
  // Desktop
  "(min-width: 800px)": function() {
    gsap.to(".box", {
      x: 500,
      scrollTrigger: {
        trigger: ".box",
        start: "top center",
        end: "bottom top",
        scrub: true
      }
    });
  },

  // Mobile
  "(max-width: 799px)": function() {
    gsap.to(".box", {
      y: 200,
      scrollTrigger: {
        trigger: ".box",
        start: "top 80%",
        scrub: 1
      }
    });
  }
});
```

## Performance Best Practices

### 1. Limit Repaints

```javascript
// Good: Animate transform/opacity (GPU accelerated)
gsap.to(".box", { x: 100, opacity: 0.5 });

// Avoid: Animating layout properties
// gsap.to(".box", { width: 500, height: 300 }); // Causes reflow
```

### 2. Dispose of ScrollTriggers

```javascript
// Kill individual trigger
const trigger = ScrollTrigger.create({ /* ... */ });
trigger.kill();

// Kill all triggers
ScrollTrigger.getAll().forEach(t => t.kill());

// In React with cleanup
useGSAP(() => {
  const tween = gsap.to(".box", { /* ... */ });

  return () => {
    tween.kill();
  };
}, []);
```

### 3. Use `invalidateOnRefresh`

For dynamic values that change on resize:

```javascript
gsap.to(".box", {
  x: () => window.innerWidth / 2, // Dynamic value
  scrollTrigger: {
    trigger: ".box",
    start: "top center",
    invalidateOnRefresh: true // Recalculate x on resize
  }
});
```

## Common Pitfalls

### 1. Multiple Tweens on Same Element

```javascript
// Problem: Second tween conflicts with first
gsap.to('h1', { x: 100, scrollTrigger: { /* ... */ } });
gsap.to('h1', { x: 200, scrollTrigger: { /* ... */ } }); // Jumps!

// Solution 1: Use fromTo
gsap.fromTo('h1', { x: 100 }, { x: 200, scrollTrigger: { /* ... */ } });

// Solution 2: Use immediateRender: false
gsap.to('h1', { x: 200, immediateRender: false, scrollTrigger: { /* ... */ } });

// Solution 3: Apply ScrollTrigger to timeline
const tl = gsap.timeline({ scrollTrigger: { /* ... */ } });
tl.to('h1', { x: 100 })
  .to('h1', { x: 200 });
```

### 2. Not Using Loops for Multiple Elements

```javascript
// Wrong: Animates all at once
gsap.to('.section', {
  y: -100,
  scrollTrigger: { trigger: '.section', scrub: true }
});

// Right: Loop for individual triggers
gsap.utils.toArray('.section').forEach(section => {
  gsap.to(section, {
    y: -100,
    scrollTrigger: { trigger: section, scrub: true }
  });
});
```

### 3. Forgetting to Register Plugins

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ScrollToPlugin } from 'gsap/ScrollToPlugin';

gsap.registerPlugin(ScrollTrigger, ScrollToPlugin); // Must register!
```

### 4. Nested ScrollTriggers in Timelines

```javascript
// Wrong: ScrollTriggers on individual tweens in timeline
const tl = gsap.timeline();
tl.to('.box1', { x: 100, scrollTrigger: { /* ... */ } }) // Don't do this!
  .to('.box2', { y: 100, scrollTrigger: { /* ... */ } });

// Right: ScrollTrigger on parent timeline
const tl = gsap.timeline({
  scrollTrigger: { /* ... */ }
});
tl.to('.box1', { x: 100 })
  .to('.box2', { y: 100 });
```

## Debugging Workflow

1. Enable `markers: true` on ScrollTrigger to visualize start/end positions
2. Check `start`/`end` values match expected scroll positions
3. Verify `gsap.registerPlugin(ScrollTrigger)` is called before any ScrollTrigger usage
4. Check for conflicting tweens on the same element (use `GSDevTools` or browser timeline)
5. Test with `scrub: false` to isolate scroll-linking issues from animation issues
6. Inspect cleanup — missing `.kill()` calls cause zombie triggers after route changes
7. Force `ScrollTrigger.refresh()` after dynamic DOM changes or async content loads

## Resources

This skill includes bundled resources:

### references/
- `api_reference.md`: Quick API reference (tween methods, timeline methods, ScrollTrigger properties)
- `easing_guide.md`: Visual easing reference with use cases
- `common_patterns.md`: Copy-paste patterns for common scenarios

### scripts/
- `generate_animation.py`: Generate boilerplate GSAP code
- `timeline_builder.py`: Interactive timeline sequence builder

### assets/
- `starter_scroll/`: Complete scroll-driven site template
- `easings/`: Easing visualization HTML tool
- `examples/`: Real-world ScrollTrigger examples

## Related Skills

- **threejs-webgl**: Three.js-specific animations and WebGL integration
- **motion-framer**: React component animations with Framer Motion
