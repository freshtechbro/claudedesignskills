---
name: gsap-scrolltrigger
description: Comprehensive skill for GSAP (GreenSock Animation Platform) and ScrollTrigger plugin. Use this skill when creating web animations, scroll-driven experiences, timelines, tweens, scroll-triggered animations, pinning, scrubbing, parallax effects, or animating DOM elements, SVG, Canvas, WebGL, or Three.js. Triggers on tasks involving GSAP, ScrollTrigger, smooth animations, scroll effects, or animation sequencing.
---

# GSAP & ScrollTrigger Development

## Overview

GSAP (GreenSock Animation Platform) is the industry-leading JavaScript animation library for creating high-performance, production-quality animations. ScrollTrigger is GSAP's powerful plugin for scroll-driven animations. Together, they enable everything from simple UI transitions to complex scroll-based storytelling experiences.

## Core Concepts

### The Basics: Tweens

A **tween** is a single animation from point A to point B.

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

### Timelines: Sequencing Animations

**Timelines** orchestrate multiple tweens in sequence or overlap.

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

### Start & End Positions

Format: `"[trigger position] [viewport position]"`

```javascript
// Common patterns
start: "top top"      // Trigger top hits viewport top
start: "top center"   // Trigger top hits viewport center (default)
start: "top bottom"   // Trigger top hits viewport bottom
start: "center center" // Trigger center hits viewport center

// With offsets
start: "top top+=100"   // 100px below viewport top
start: "top 80%"        // 80% down the viewport
end: "+=500"            // 500px after start position
end: "bottom top"       // Trigger bottom hits viewport top
```

### Scrubbing (Scroll-Synced Animation)

```javascript
// Boolean: Direct link to scrollbar (immediate)
scrub: true

// Number: Smoothing delay in seconds
scrub: 1  // Takes 1 second to "catch up" to scrollbar
scrub: 0.5 // Faster, tighter feel
```

### Toggle Actions

Control animation at four scroll points:

```javascript
toggleActions: "play pause resume reset"
// onEnter | onLeave | onEnterBack | onLeaveBack

// Actions: play, pause, resume, restart, reset, complete, reverse, none
```

Common patterns:
```javascript
toggleActions: "play none none none"       // Play once on enter
toggleActions: "play none none reverse"    // Play forward, reverse back
toggleActions: "play complete reverse reset" // Full control
toggleActions: "restart pause resume pause"  // Restart on each enter
```

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

### Sharing Timeline in React

```javascript
function App() {
  const [tl, setTl] = useState();

  useGSAP(() => {
    const timeline = gsap.timeline();
    setTl(timeline);
  }, []);

  return (
    <div>
      <Box timeline={tl} index={0} />
      <Circle timeline={tl} index={1} />
    </div>
  );
}

function Box({ timeline, index }) {
  const ref = useRef();

  useGSAP(() => {
    timeline && timeline.to(ref.current, { x: 100 }, index * 0.1);
  }, [timeline, index]);

  return <div ref={ref} className="box" />;
}
```

### Locomotive Scroll Integration

```javascript
import LocomotiveScroll from 'locomotive-scroll';

const scroller = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true
});

ScrollTrigger.scrollerProxy("[data-scroll-container]", {
  scrollTop(value) {
    return arguments.length ? scroller.scrollTo(value, 0, 0) : scroller.scroll.instance.scroll.y;
  },
  getBoundingClientRect() {
    return {top: 0, left: 0, width: window.innerWidth, height: window.innerHeight};
  },
  pinType: document.querySelector("[data-scroll-container]").style.transform ? "transform" : "fixed"
});

ScrollTrigger.addEventListener("refresh", () => scroller.update());
ScrollTrigger.refresh();
```

## Advanced Techniques

### Image Sequence Scrubbing

```javascript
const canvas = document.querySelector("canvas");
const context = canvas.getContext("2d");

const images = [];
const imageCount = 147;
const currentFrame = { value: 0 };

for (let i = 0; i < imageCount; i++) {
  const img = new Image();
  img.src = `./frames/frame_${i.toString().padStart(4, '0')}.jpg`;
  images.push(img);
}

images[0].onload = () => {
  canvas.width = images[0].width;
  canvas.height = images[0].height;
  render();
};

function render() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(images[Math.floor(currentFrame.value)], 0, 0);
}

gsap.to(currentFrame, {
  value: imageCount - 1,
  snap: "value",
  ease: "none",
  scrollTrigger: {
    trigger: canvas,
    start: "top top",
    end: "+=500%",
    scrub: true,
    pin: true
  },
  onUpdate: render
});
```

### Smooth Scroll to Element

```javascript
gsap.registerPlugin(ScrollToPlugin);

// Scroll to element
gsap.to(window, {
  duration: 1,
  scrollTo: "#section2",
  ease: "power2.inOut"
});

// With offset
gsap.to(window, {
  duration: 1.5,
  scrollTo: { y: "#section2", offsetY: 50 },
  ease: "expo.inOut"
});

// Horizontal scroll
gsap.to(".container", {
  duration: 2,
  scrollTo: { x: 1000, autoKill: true }
});
```

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

### 1. Use `will-change` CSS

```css
.animated-element {
  will-change: transform, opacity;
}
```

### 2. Limit Repaints

```javascript
// Good: Animate transform/opacity (GPU accelerated)
gsap.to(".box", { x: 100, opacity: 0.5 });

// Avoid: Animating layout properties
// gsap.to(".box", { width: 500, height: 300 }); // Causes reflow
```

### 3. Dispose of ScrollTriggers

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

### 4. Debounce Resize

ScrollTrigger handles this automatically, but for custom resize logic:

```javascript
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    ScrollTrigger.refresh();
  }, 250);
});
```

### 5. Use `invalidateOnRefresh`

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

## Easing Reference

```javascript
// Power easings (most common)
ease: "power1.out"  // Subtle deceleration
ease: "power2.inOut" // Smooth acceleration/deceleration
ease: "power3.in"   // Strong acceleration
ease: "power4.out"  // Very strong deceleration

// Special easings
ease: "elastic.out"  // Bouncy overshoot
ease: "back.out"     // Slight overshoot
ease: "bounce.out"   // Bouncing effect
ease: "circ.inOut"   // Circular motion feel
ease: "expo.inOut"   // Exponential (dramatic)

// Linear (for scrubbed scroll animations)
ease: "none"
```

## ScrollTrigger Methods

```javascript
// Refresh all ScrollTriggers (after DOM changes)
ScrollTrigger.refresh();

// Get all ScrollTriggers
const triggers = ScrollTrigger.getAll();

// Get specific trigger by ID
const st = ScrollTrigger.getById("myTrigger");

// Kill trigger
st.kill();

// Update trigger
st.scroll(500); // Programmatically set scroll position
st.enable();
st.disable();

// Global ScrollTrigger config
ScrollTrigger.config({
  limitCallbacks: true, // Improve performance
  syncInterval: 15 // Throttle scroll checks (ms)
});

// Debug mode
ScrollTrigger.defaults({
  markers: true // Show markers on all triggers
});
```

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

## When to Use This Skill

Use this skill when:
- Creating smooth web animations
- Building scroll-driven experiences
- Implementing parallax effects
- Sequencing complex animations
- Animating DOM, SVG, Canvas, or WebGL
- Integrating animations with Three.js or React
- Building scrollytelling websites
- Creating interactive UI transitions

For Three.js-specific animations, also reference the **threejs-webgl** skill.
For React components with built-in animations, reference the **motion-framer** skill.
