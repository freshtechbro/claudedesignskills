# GSAP & ScrollTrigger Common Patterns

A collection of copy-paste ready patterns for common web animation scenarios.

---

## Table of Contents

1. [Scroll-Triggered Animations](#scroll-triggered-animations)
2. [Pinning Patterns](#pinning-patterns)
3. [Horizontal Scrolling](#horizontal-scrolling)
4. [Parallax Effects](#parallax-effects)
5. [Stagger Animations](#stagger-animations)
6. [Timeline Sequences](#timeline-sequences)
7. [Text Animations](#text-animations)
8. [Image Reveals](#image-reveals)
9. [Navigation & UI](#navigation--ui)
10. [Page Transitions](#page-transitions)
11. [Scroll Progress Indicators](#scroll-progress-indicators)
12. [Image Sequences](#image-sequences)
13. [Responsive Patterns](#responsive-patterns)
14. [Integration Patterns](#integration-patterns)

---

## Scroll-Triggered Animations

### 1.1 Basic Fade In on Scroll

```javascript
// Fade in element when it enters viewport
gsap.from(".fade-in", {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: ".fade-in",
    start: "top 80%", // When top of element hits 80% of viewport
    toggleActions: "play none none none" // Play once
  }
});
```

### 1.2 Fade In with Scrub (Scroll-Controlled)

```javascript
// Animation synced to scroll position
gsap.from(".fade-in-scrub", {
  opacity: 0,
  y: 100,
  scrollTrigger: {
    trigger: ".fade-in-scrub",
    start: "top bottom",
    end: "top center",
    scrub: true // Smooth scrubbing (boolean or number for lag)
  }
});
```

### 1.3 Batch Fade In Multiple Elements

```javascript
// Efficiently animate many elements
ScrollTrigger.batch(".batch-item", {
  onEnter: batch => gsap.from(batch, {
    opacity: 0,
    y: 60,
    stagger: 0.15,
    duration: 0.8,
    ease: "power2.out"
  }),
  start: "top 90%",
  once: true // Only trigger once
});
```

### 1.4 Fade In from Different Directions

```javascript
// Left
gsap.from(".from-left", {
  x: -100,
  opacity: 0,
  scrollTrigger: {
    trigger: ".from-left",
    start: "top 80%",
    toggleActions: "play none none reverse"
  }
});

// Right
gsap.from(".from-right", {
  x: 100,
  opacity: 0,
  scrollTrigger: { trigger: ".from-right", start: "top 80%" }
});

// Scale up
gsap.from(".scale-in", {
  scale: 0.8,
  opacity: 0,
  scrollTrigger: { trigger: ".scale-in", start: "top 80%" }
});
```

### 1.5 Toggle Classes on Scroll

```javascript
// Add/remove CSS class based on scroll position
ScrollTrigger.create({
  trigger: ".section",
  start: "top center",
  end: "bottom center",
  toggleClass: { targets: ".section", className: "active" },
  // Or specific onEnter/onLeave actions
  onEnter: () => document.querySelector(".section").classList.add("active"),
  onLeave: () => document.querySelector(".section").classList.remove("active")
});
```

---

## Pinning Patterns

### 2.1 Basic Pin (Fixed Position While Scrolling)

```javascript
// Pin element while scrolling past it
ScrollTrigger.create({
  trigger: ".pin-section",
  start: "top top",
  end: "+=500", // Pin for 500px of scrolling
  pin: true,
  markers: true // Debug markers (remove in production)
});
```

### 2.2 Pin with Content Animation

```javascript
// Pin section and animate content inside
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".pin-animation",
    start: "top top",
    end: "+=1000",
    pin: true,
    scrub: 1
  }
});

tl.from(".content h1", { opacity: 0, y: 100 })
  .from(".content p", { opacity: 0, y: 50 }, "-=0.5")
  .to(".content img", { scale: 1.2, rotation: 5 });
```

### 2.3 Pin Until Another Element

```javascript
// Pin until bottom of another section
ScrollTrigger.create({
  trigger: ".hero",
  endTrigger: ".next-section", // Different end trigger
  start: "top top",
  end: "top bottom", // When top of next-section hits viewport bottom
  pin: true,
  pinSpacing: false // Don't add extra space
});
```

### 2.4 Multiple Pinned Sections (Stacked Cards)

```javascript
// Each section pins, then next one takes over
gsap.utils.toArray(".panel").forEach((panel, i) => {
  ScrollTrigger.create({
    trigger: panel,
    start: "top top",
    pin: true,
    pinSpacing: false
  });
});
```

### 2.5 Pin with Snap Points

```javascript
// Snap to specific positions while pinned
gsap.timeline({
  scrollTrigger: {
    trigger: ".snap-section",
    start: "top top",
    end: "+=2000",
    pin: true,
    scrub: 1,
    snap: {
      snapTo: [0, 0.33, 0.66, 1], // Snap to 0%, 33%, 66%, 100%
      duration: { min: 0.2, max: 0.5 },
      ease: "power1.inOut"
    }
  }
});
```

---

## Horizontal Scrolling

### 3.1 Basic Horizontal Scroll

```javascript
// Scroll horizontally when scrolling vertically
gsap.to(".horizontal-section", {
  x: () => -(document.querySelector(".horizontal-section").scrollWidth - window.innerWidth),
  ease: "none",
  scrollTrigger: {
    trigger: ".horizontal-wrapper",
    start: "top top",
    end: () => "+=" + document.querySelector(".horizontal-section").scrollWidth,
    scrub: 1,
    pin: true,
    anticipatePin: 1
  }
});
```

### 3.2 Horizontal Scroll with Multiple Sections

```javascript
// Scroll through multiple panels
const sections = gsap.utils.toArray(".panel");
const scrollTween = gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".container").offsetWidth
  }
});

// Animate each panel individually
sections.forEach((section, i) => {
  gsap.from(section.querySelector(".content"), {
    opacity: 0,
    scale: 0.8,
    scrollTrigger: {
      trigger: section,
      containerAnimation: scrollTween, // Link to horizontal scroll
      start: "left center",
      end: "right center",
      scrub: true
    }
  });
});
```

### 3.3 Horizontal Scroll with Snap

```javascript
gsap.to(".slides", {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".slider-container",
    pin: true,
    scrub: 1,
    snap: 1 / (sections.length - 1), // Snap to each section
    end: () => "+=" + document.querySelector(".slides").offsetWidth
  }
});
```

---

## Parallax Effects

### 4.1 Simple Parallax (Different Speeds)

```javascript
// Background moves slower than foreground
gsap.to(".bg", {
  y: 200,
  ease: "none",
  scrollTrigger: {
    trigger: ".parallax-section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});

// Foreground moves faster
gsap.to(".fg", {
  y: -100,
  ease: "none",
  scrollTrigger: {
    trigger: ".parallax-section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

### 4.2 Multi-Layer Parallax

```javascript
// Multiple layers with different speeds
gsap.utils.toArray(".parallax-layer").forEach(layer => {
  const depth = layer.dataset.depth; // data-depth="0.2" in HTML
  const movement = -(layer.offsetHeight * depth);

  gsap.to(layer, {
    y: movement,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-container",
      start: "top bottom",
      end: "bottom top",
      scrub: true
    }
  });
});
```

### 4.3 Parallax Hero Section

```javascript
// Hero image zooms out while scrolling
gsap.to(".hero-image", {
  scale: 1.5,
  y: 300,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "bottom top",
    scrub: true
  }
});

// Hero text fades out
gsap.to(".hero-text", {
  opacity: 0,
  y: 100,
  ease: "none",
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "center top",
    scrub: true
  }
});
```

---

## Stagger Animations

### 5.1 Basic Stagger

```javascript
// Stagger animation across multiple elements
gsap.from(".card", {
  opacity: 0,
  y: 50,
  duration: 0.8,
  stagger: 0.2, // 0.2s delay between each
  scrollTrigger: {
    trigger: ".card-container",
    start: "top 80%"
  }
});
```

### 5.2 Stagger from Center

```javascript
// Animate from center outward
gsap.from(".item", {
  scale: 0,
  opacity: 0,
  duration: 0.6,
  stagger: {
    each: 0.1,
    from: "center", // "start", "center", "end", "edges", "random"
    ease: "power2.out"
  },
  scrollTrigger: { trigger: ".grid", start: "top 80%" }
});
```

### 5.3 Grid Stagger

```javascript
// Stagger in a grid pattern
gsap.from(".grid-item", {
  opacity: 0,
  scale: 0.5,
  duration: 0.6,
  stagger: {
    grid: "auto", // Or [rows, columns] like [3, 4]
    from: "center",
    amount: 1.5 // Total time for all staggers
  },
  scrollTrigger: { trigger: ".grid", start: "top 80%" }
});
```

### 5.4 Text Stagger (Words/Characters)

```javascript
// Split text into words
const text = new SplitText(".title", { type: "words" });

gsap.from(text.words, {
  opacity: 0,
  y: 50,
  rotationX: -90,
  stagger: 0.05,
  scrollTrigger: { trigger: ".title", start: "top 80%" }
});

// Split text into characters
const chars = new SplitText(".subtitle", { type: "chars" });

gsap.from(chars.chars, {
  opacity: 0,
  scale: 0,
  stagger: 0.02,
  ease: "back.out(1.7)",
  scrollTrigger: { trigger: ".subtitle", start: "top 80%" }
});
```

---

## Timeline Sequences

### 6.1 Basic Timeline Sequence

```javascript
// Chained animations
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".sequence-section",
    start: "top 80%"
  }
});

tl.from(".heading", { opacity: 0, y: -50, duration: 0.6 })
  .from(".subheading", { opacity: 0, y: -30, duration: 0.5 }, "-=0.3") // Overlap by 0.3s
  .from(".button", { scale: 0, duration: 0.4, ease: "back.out(1.7)" });
```

### 6.2 Timeline with Labels

```javascript
// Use labels for complex timing
const tl = gsap.timeline({
  scrollTrigger: { trigger: ".story", start: "top center" }
});

tl.addLabel("start")
  .from(".hero", { opacity: 0, scale: 0.5 }, "start")
  .from(".text", { opacity: 0, x: -100 }, "start+=0.3")
  .addLabel("reveal")
  .from(".image", { opacity: 0, scale: 1.2 }, "reveal")
  .from(".caption", { opacity: 0 }, "reveal+=0.5");
```

### 6.3 Scrubbed Timeline

```javascript
// Timeline controlled by scroll
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".animation-section",
    start: "top top",
    end: "+=1500",
    scrub: 1,
    pin: true
  }
});

tl.to(".box1", { x: 500, rotation: 360 })
  .to(".box2", { y: 300, scale: 2 }, "-=0.5")
  .to(".box3", { opacity: 0, duration: 0.3 });
```

---

## Text Animations

### 7.1 Text Reveal (Line by Line)

```javascript
// Using SplitText (Club GreenSock plugin)
const split = new SplitText(".text-reveal", { type: "lines" });

gsap.from(split.lines, {
  opacity: 0,
  y: 20,
  stagger: 0.1,
  duration: 0.6,
  scrollTrigger: { trigger: ".text-reveal", start: "top 80%" }
});
```

### 7.2 Scrambled Text Effect

```javascript
// Using ScrambleText (Club GreenSock plugin)
gsap.to(".scramble", {
  duration: 2,
  scrambleText: {
    text: "REVEALED TEXT",
    chars: "lowerCase",
    speed: 0.3
  },
  scrollTrigger: { trigger: ".scramble", start: "top 80%" }
});
```

### 7.3 Typewriter Effect

```javascript
// Simple typewriter using text content
const text = "This text appears letter by letter.";
const element = document.querySelector(".typewriter");

gsap.to(element, {
  duration: text.length * 0.05,
  text: { value: text },
  ease: "none",
  scrollTrigger: { trigger: element, start: "top 80%" }
});
```

### 7.4 Text Highlight on Scroll

```javascript
// Highlight text as you scroll through it
gsap.to(".highlight", {
  backgroundSize: "100% 100%",
  ease: "none",
  scrollTrigger: {
    trigger: ".highlight",
    start: "top 80%",
    end: "top 20%",
    scrub: true
  }
});

// CSS required:
// .highlight {
//   background: linear-gradient(to right, yellow 0%, yellow 100%);
//   background-size: 0% 100%;
//   background-repeat: no-repeat;
// }
```

---

## Image Reveals

### 8.1 Image Curtain Reveal

```html
<!-- HTML Structure -->
<div class="img-curtain">
  <div class="curtain"></div>
  <img src="image.jpg" alt="">
</div>
```

```javascript
// Curtain slides to reveal image
gsap.to(".curtain", {
  xPercent: 100,
  duration: 1,
  ease: "power2.inOut",
  scrollTrigger: {
    trigger: ".img-curtain",
    start: "top 80%"
  }
});
```

```css
/* CSS */
.img-curtain {
  position: relative;
  overflow: hidden;
}
.curtain {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
  z-index: 1;
}
```

### 8.2 Image Scale Reveal

```javascript
// Image scales up and reveals from clip-path
gsap.from(".img-scale", {
  scale: 1.3,
  clipPath: "inset(100% 0% 0% 0%)",
  duration: 1.5,
  ease: "power2.out",
  scrollTrigger: {
    trigger: ".img-scale",
    start: "top 80%"
  }
});
```

### 8.3 Image Parallax Zoom

```javascript
// Image zooms while container scrolls
gsap.to(".img-zoom img", {
  scale: 1.2,
  ease: "none",
  scrollTrigger: {
    trigger: ".img-zoom",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});
```

---

## Navigation & UI

### 9.1 Sticky Header with Hide/Show

```javascript
// Hide on scroll down, show on scroll up
let lastScroll = 0;

ScrollTrigger.create({
  start: 100,
  end: 99999,
  onUpdate: (self) => {
    const currentScroll = self.scroll();

    if (currentScroll > lastScroll && currentScroll > 100) {
      // Scrolling down
      gsap.to(".header", { y: -100, duration: 0.3, ease: "power2.out" });
    } else {
      // Scrolling up
      gsap.to(".header", { y: 0, duration: 0.3, ease: "power2.out" });
    }

    lastScroll = currentScroll;
  }
});
```

### 9.2 Active Nav Item Based on Section

```javascript
// Highlight nav item when section is in view
const sections = gsap.utils.toArray("section");

sections.forEach((section, i) => {
  ScrollTrigger.create({
    trigger: section,
    start: "top center",
    end: "bottom center",
    onEnter: () => setActiveNav(i),
    onEnterBack: () => setActiveNav(i)
  });
});

function setActiveNav(index) {
  document.querySelectorAll(".nav-item").forEach((item, i) => {
    item.classList.toggle("active", i === index);
  });
}
```

### 9.3 Smooth Scroll to Anchor

```javascript
// Click anchor link to smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));

    gsap.to(window, {
      duration: 1,
      scrollTo: { y: target, offsetY: 100 }, // 100px offset for header
      ease: "power2.inOut"
    });
  });
});
```

### 9.4 Drawer/Sidebar Animation

```javascript
// Open drawer
function openDrawer() {
  gsap.to(".drawer", {
    x: 0,
    duration: 0.4,
    ease: "power2.out"
  });

  gsap.to(".overlay", {
    opacity: 1,
    duration: 0.3,
    pointerEvents: "all"
  });
}

// Close drawer
function closeDrawer() {
  gsap.to(".drawer", {
    x: "100%", // Or -100% for left drawer
    duration: 0.4,
    ease: "power2.in"
  });

  gsap.to(".overlay", {
    opacity: 0,
    duration: 0.3,
    pointerEvents: "none"
  });
}
```

---

## Page Transitions

### 10.1 Basic Page Transition (Overlay)

```javascript
// On link click
function pageTransition(url) {
  const tl = gsap.timeline({
    onComplete: () => window.location.href = url
  });

  tl.to(".transition-overlay", {
    yPercent: 0,
    duration: 0.5,
    ease: "power2.inOut"
  })
  .to(".transition-overlay", {
    yPercent: -100,
    duration: 0.5,
    ease: "power2.inOut"
  }, "+=0.1");
}

// Attach to links
document.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    pageTransition(link.href);
  });
});
```

### 10.2 Fade Page Transition

```javascript
// Fade out current page, load new page
function fadeTransition(url) {
  gsap.to(".page-container", {
    opacity: 0,
    duration: 0.5,
    onComplete: () => {
      window.location.href = url;
    }
  });
}

// On page load, fade in
window.addEventListener("load", () => {
  gsap.from(".page-container", {
    opacity: 0,
    duration: 0.5
  });
});
```

---

## Scroll Progress Indicators

### 11.1 Horizontal Progress Bar

```javascript
// Progress bar at top of page
gsap.to(".progress-bar", {
  scaleX: 1,
  ease: "none",
  scrollTrigger: {
    start: "top top",
    end: "bottom bottom",
    scrub: 0.3
  }
});

// CSS: .progress-bar { transform-origin: left; }
```

### 11.2 Circular Progress Indicator

```javascript
// Circular progress (SVG circle)
const circle = document.querySelector(".progress-circle");
const length = circle.getTotalLength();

// Set up circle
gsap.set(circle, {
  strokeDasharray: length,
  strokeDashoffset: length
});

// Animate on scroll
gsap.to(circle, {
  strokeDashoffset: 0,
  ease: "none",
  scrollTrigger: {
    start: "top top",
    end: "bottom bottom",
    scrub: 0.3
  }
});
```

### 11.3 Section Progress (Multi-step)

```javascript
// Update progress indicator through sections
const sections = gsap.utils.toArray(".step");
const progressDots = gsap.utils.toArray(".progress-dot");

sections.forEach((section, i) => {
  ScrollTrigger.create({
    trigger: section,
    start: "top center",
    end: "bottom center",
    onEnter: () => activateDot(i),
    onEnterBack: () => activateDot(i)
  });
});

function activateDot(index) {
  progressDots.forEach((dot, i) => {
    if (i <= index) {
      dot.classList.add("active");
    } else {
      dot.classList.remove("active");
    }
  });
}
```

---

## Image Sequences

### 12.1 Canvas Image Sequence on Scroll

```javascript
// Scrub through image sequence
const canvas = document.querySelector("#canvas");
const context = canvas.getContext("2d");

const frameCount = 148;
const images = [];
const imageSeq = { frame: 0 };

// Preload images
for (let i = 0; i < frameCount; i++) {
  const img = new Image();
  img.src = `./frames/frame_${String(i).padStart(4, '0')}.jpg`;
  images.push(img);
}

// Render frame
function render() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(images[imageSeq.frame], 0, 0);
}

// Animate frame property on scroll
gsap.to(imageSeq, {
  frame: frameCount - 1,
  snap: "frame",
  ease: "none",
  scrollTrigger: {
    trigger: ".image-sequence",
    start: "top top",
    end: "+=3000",
    pin: true,
    scrub: 0.5,
    onUpdate: render
  }
});

// Initial render
images[0].onload = render;
```

---

## Responsive Patterns

### 13.1 Different Animations per Breakpoint

```javascript
// Use ScrollTrigger.matchMedia for responsive animations
ScrollTrigger.matchMedia({
  // Desktop
  "(min-width: 800px)": function() {
    gsap.to(".element", {
      x: 500,
      scrollTrigger: {
        trigger: ".element",
        start: "top 80%",
        scrub: true
      }
    });
  },

  // Mobile
  "(max-width: 799px)": function() {
    gsap.to(".element", {
      y: 200, // Different animation on mobile
      scrollTrigger: {
        trigger: ".element",
        start: "top 80%",
        scrub: true
      }
    });
  }
});
```

### 13.2 Kill Animations on Mobile

```javascript
// Disable ScrollTrigger animations on mobile
if (window.innerWidth > 768) {
  // Desktop-only animations
  gsap.from(".desktop-animation", {
    opacity: 0,
    y: 100,
    scrollTrigger: {
      trigger: ".desktop-animation",
      start: "top 80%"
    }
  });
} else {
  // Simple CSS fallback on mobile
  gsap.set(".desktop-animation", { opacity: 1, y: 0 });
}
```

---

## Integration Patterns

### 14.1 GSAP + React (useGSAP hook)

```javascript
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

function Component() {
  const containerRef = useRef();

  useGSAP(() => {
    gsap.from(".box", {
      opacity: 0,
      y: 50,
      scrollTrigger: {
        trigger: ".box",
        start: "top 80%"
      }
    });
  }, { scope: containerRef }); // Scope to container

  return <div ref={containerRef}>...</div>;
}
```

### 14.2 GSAP + Three.js

```javascript
// Animate Three.js camera on scroll
gsap.to(camera.position, {
  z: 10,
  ease: "none",
  scrollTrigger: {
    trigger: ".threejs-section",
    start: "top top",
    end: "bottom top",
    scrub: true
  }
});

// Animate object rotation
gsap.to(mesh.rotation, {
  y: Math.PI * 2,
  ease: "none",
  scrollTrigger: {
    trigger: ".threejs-section",
    scrub: 1
  }
});
```

### 14.3 GSAP + Locomotive Scroll

```javascript
// Use Locomotive Scroll as the scroller
import LocomotiveScroll from 'locomotive-scroll';

const locoScroll = new LocomotiveScroll({
  el: document.querySelector(".smooth-scroll"),
  smooth: true
});

// Tell ScrollTrigger to use Locomotive Scroll
ScrollTrigger.scrollerProxy(".smooth-scroll", {
  scrollTop(value) {
    return arguments.length ? locoScroll.scrollTo(value, 0, 0) : locoScroll.scroll.instance.scroll.y;
  },
  getBoundingClientRect() {
    return { top: 0, left: 0, width: window.innerWidth, height: window.innerHeight };
  }
});

// Update ScrollTrigger when Locomotive Scroll updates
locoScroll.on("scroll", ScrollTrigger.update);
ScrollTrigger.addEventListener("refresh", () => locoScroll.update());
```

---

## Best Practices

### Performance Optimization

```javascript
// 1. Use will-change CSS for animated elements
gsap.set(".animated", { willChange: "transform, opacity" });

// 2. Kill animations when not needed
const st = ScrollTrigger.create({ /* ... */ });
st.kill(); // Clean up

// 3. Batch similar animations
ScrollTrigger.batch(".item", { /* ... */ });

// 4. Use scrub for smooth scroll-driven animations
scrub: 1 // 1 second lag for smoothness

// 5. Limit markers in production
markers: process.env.NODE_ENV === "development"
```

### Refresh After DOM Changes

```javascript
// After images load, layout shifts, etc.
window.addEventListener("load", () => {
  ScrollTrigger.refresh();
});

// Or after specific events
imagesLoaded(".gallery", () => {
  ScrollTrigger.refresh();
});
```

### Clean Up on Unmount (React/Vue)

```javascript
// React useEffect cleanup
useEffect(() => {
  const st = ScrollTrigger.create({ /* ... */ });

  return () => {
    st.kill(); // Clean up on unmount
  };
}, []);
```

---

## Common Gotchas

### ❌ Forgetting to Register Plugins

```javascript
// WRONG - ScrollTrigger won't work
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.to(".box", { scrollTrigger: { /* ... */ } }); // Error!

// CORRECT
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
gsap.to(".box", { scrollTrigger: { /* ... */ } }); // Works!
```

### ❌ Animating Before DOM Ready

```javascript
// WRONG - Elements may not exist yet
gsap.from(".box", { opacity: 0 });

// CORRECT
window.addEventListener("load", () => {
  gsap.from(".box", { opacity: 0 });
});

// Or with DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  gsap.from(".box", { opacity: 0 });
});
```

### ❌ Not Refreshing After Layout Changes

```javascript
// WRONG - ScrollTrigger positions are stale
loadImages().then(() => {
  // Images loaded, layout shifted
  // ScrollTrigger positions are now wrong!
});

// CORRECT
loadImages().then(() => {
  ScrollTrigger.refresh(); // Recalculate positions
});
```

---

## Quick Copy-Paste Starter

```javascript
// Complete starter template
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Wait for DOM
document.addEventListener("DOMContentLoaded", () => {

  // Fade in on scroll
  gsap.utils.toArray(".fade-in").forEach(element => {
    gsap.from(element, {
      opacity: 0,
      y: 50,
      duration: 1,
      scrollTrigger: {
        trigger: element,
        start: "top 80%",
        toggleActions: "play none none reverse"
      }
    });
  });

  // Parallax
  gsap.to(".parallax", {
    y: 200,
    ease: "none",
    scrollTrigger: {
      trigger: ".parallax-section",
      start: "top bottom",
      end: "bottom top",
      scrub: true
    }
  });

  // Pin section
  ScrollTrigger.create({
    trigger: ".pin-section",
    start: "top top",
    end: "+=500",
    pin: true
  });

  // Refresh after images load
  window.addEventListener("load", () => {
    ScrollTrigger.refresh();
  });

});
```

---

## Resources

- [GSAP Documentation](https://gsap.com/docs/)
- [ScrollTrigger Demos](https://gsap.com/docs/v3/Plugins/ScrollTrigger)
- [GSAP Showcase](https://gsap.com/showcase/)
- [Codepen GSAP Examples](https://codepen.io/GreenSock/pens/popular)

---

**Remember**: Start simple, test often, and use `markers: true` during development to debug ScrollTrigger positions.
