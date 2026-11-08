# GSAP & ScrollTrigger API Quick Reference

## Core GSAP Methods

### gsap.to()
Animate FROM current state TO specified values.

```javascript
gsap.to(target, {
  x: 100,
  y: 50,
  rotation: 360,
  duration: 1,
  ease: "power2.inOut",
  onComplete: callback
});
```

### gsap.from()
Animate TO current state FROM specified values.

```javascript
gsap.from(target, {
  opacity: 0,
  y: -50,
  duration: 0.8,
  ease: "back.out"
});
```

### gsap.fromTo()
Define both starting and ending values.

```javascript
gsap.fromTo(target,
  { opacity: 0, scale: 0.5 }, // FROM
  { opacity: 1, scale: 1, duration: 1 } // TO
);
```

### gsap.set()
Immediately set properties (no animation).

```javascript
gsap.set(target, {
  x: 100,
  opacity: 0.5
});
```

## Timeline Methods

### Creating Timelines

```javascript
const tl = gsap.timeline({
  repeat: 2,
  repeatDelay: 1,
  yoyo: true,
  paused: false,
  onComplete: callback
});
```

### Adding Animations

```javascript
// Add to end of timeline
tl.to(".box", { x: 100 });

// Add at specific time
tl.to(".box", { y: 50 }, 2); // At 2 seconds

// Add relative to previous
tl.to(".box", { rotation: 360 }, "-=0.5"); // 0.5s before previous ends
tl.to(".box", { scale: 2 }, "+=1"); // 1s after previous ends

// Add at label
tl.addLabel("midpoint")
  .to(".box", { opacity: 0 }, "midpoint")
  .to(".circle", { x: 200 }, "midpoint+=0.5");
```

### Timeline Control

```javascript
tl.play();
tl.pause();
tl.resume();
tl.reverse();
tl.restart();
tl.seek(2); // Go to 2 seconds
tl.progress(0.5); // Go to 50% through timeline
tl.timeScale(2); // 2x speed
tl.kill(); // Destroy timeline
```

## Common Tween Properties

### Animation Control

```javascript
{
  duration: 1, // seconds
  delay: 0.5, // seconds before start
  repeat: 2, // times to repeat (-1 = infinite)
  repeatDelay: 1, // seconds between repeats
  yoyo: true, // alternate direction on repeat
  ease: "power2.inOut", // easing function
  paused: true, // start paused
  immediateRender: false, // don't render immediately
  overwrite: "auto" // handle conflicting tweens
}
```

### Callbacks

```javascript
{
  onStart: () => console.log("Started"),
  onUpdate: () => console.log("Updating"),
  onComplete: () => console.log("Complete"),
  onRepeat: () => console.log("Repeating"),
  onReverseComplete: () => console.log("Reversed"),
  callbackScope: this // scope for all callbacks
}
```

## Easing Functions

### Power Easings (Most Common)

```javascript
ease: "none" // Linear
ease: "power1.in"
ease: "power1.out"
ease: "power1.inOut"
ease: "power2.in"
ease: "power2.out"
ease: "power2.inOut"
ease: "power3.in"
ease: "power3.out"
ease: "power3.inOut"
ease: "power4.in"
ease: "power4.out"
ease: "power4.inOut"
```

### Special Easings

```javascript
ease: "back.in(1.7)" // Overshoot, parameter controls amount
ease: "back.out(1.7)"
ease: "back.inOut(1.7)"

ease: "elastic.in(1, 0.3)" // Elastic bounce
ease: "elastic.out(1, 0.3)"
ease: "elastic.inOut(1, 0.3)"

ease: "bounce.in"
ease: "bounce.out"
ease: "bounce.inOut"

ease: "circ.in" // Circular
ease: "circ.out"
ease: "circ.inOut"

ease: "expo.in" // Exponential
ease: "expo.out"
ease: "expo.inOut"

ease: "sine.in" // Sinusoidal
ease: "sine.out"
ease: "sine.inOut"
```

## Stagger Configuration

### Simple Stagger

```javascript
stagger: 0.1 // 0.1s between each element
```

### Advanced Stagger

```javascript
stagger: {
  each: 0.1, // time between each
  from: "center", // "start", "center", "end", "edges", "random", or index number
  grid: "auto", // [rows, columns] for grid layouts
  ease: "power2.inOut", // easing applied to stagger timing
  repeat: 2, // repeat the stagger pattern
  yoyo: true, // alternate direction
  axis: "y" // "x" or "y" for grid stagger direction
}
```

## ScrollTrigger Properties

### Core Properties

```javascript
ScrollTrigger.create({
  // Trigger & Viewport
  trigger: ".element", // Element or selector
  start: "top center", // "[trigger position] [viewport position]"
  end: "bottom top",
  endTrigger: ".other-element", // Different end trigger

  // Scrubbing
  scrub: true, // Boolean or number (smoothing seconds)
  pin: true, // Pin trigger element
  pinSpacing: true, // Add space for pinned element
  anticipatePin: 1, // Smooth pinning

  // Actions
  toggleActions: "play pause resume reset", // onEnter onLeave onEnterBack onLeaveBack
  toggleClass: "active", // CSS class to toggle

  // Animation
  animation: tween, // GSAP animation to control

  // Snapping
  snap: {
    snapTo: "labels", // "labels", 0.1, [0, 0.5, 1], or function
    duration: { min: 0.2, max: 3 },
    delay: 0.2,
    ease: "power1.inOut"
  },

  // Callbacks
  onEnter: callback,
  onLeave: callback,
  onEnterBack: callback,
  onLeaveBack: callback,
  onUpdate: (self) => {},
  onToggle: (self) => {},
  onRefresh: (self) => {},
  onScrubComplete: (self) => {},

  // Advanced
  markers: true, // Show visual markers (debug)
  id: "myTrigger", // Unique ID
  invalidateOnRefresh: false, // Recalculate values on refresh
  once: true, // Only trigger once
  horizontal: false, // Horizontal scrolling
  scroller: ".container", // Custom scroll container
  containerAnimation: timeline, // For horizontal scrolling sections
  fastScrollEnd: true // Better performance on fast scroll
});
```

### ScrollTrigger Start/End Values

```javascript
// Format: "[trigger position] [viewport position]"

start: "top top" // Trigger top hits viewport top
start: "top center" // Trigger top hits viewport center
start: "top bottom" // Trigger top hits viewport bottom
start: "center center" // Trigger center hits viewport center
start: "bottom top" // Trigger bottom hits viewport top

// With offsets
start: "top top+=100" // 100px below viewport top
start: "top 80%" // 80% down viewport
start: "top-=50 center" // 50px above trigger top

// Dynamic
start: () => "top " + (window.innerHeight * 0.8)
end: () => "+=" + element.offsetHeight
```

## ScrollTrigger Methods

### Static Methods

```javascript
// Refresh all ScrollTriggers (after DOM changes)
ScrollTrigger.refresh();

// Get all ScrollTriggers
const triggers = ScrollTrigger.getAll();

// Get by ID
const st = ScrollTrigger.getById("myTrigger");

// Kill all
ScrollTrigger.getAll().forEach(t => t.kill());

// Global configuration
ScrollTrigger.config({
  limitCallbacks: true, // Better performance
  syncInterval: 15, // Throttle scroll checks (ms)
  ignoreMobileResize: true // Don't refresh on mobile resize
});

// Defaults for all ScrollTriggers
ScrollTrigger.defaults({
  toggleActions: "play none none reverse",
  markers: false
});

// Batch animations
ScrollTrigger.batch(".element", {
  onEnter: batch => gsap.to(batch, { opacity: 1, stagger: 0.1 }),
  start: "top 80%"
});

// Match media queries
ScrollTrigger.matchMedia({
  "(min-width: 800px)": function() {
    // Desktop animations
  },
  "(max-width: 799px)": function() {
    // Mobile animations
  }
});
```

### Instance Methods

```javascript
const st = ScrollTrigger.create({ /* ... */ });

// Control
st.enable();
st.disable();
st.kill();
st.refresh();

// Query
st.isActive; // Boolean
st.progress; // 0-1
st.direction; // 1 (down) or -1 (up)
st.getVelocity(); // Scroll velocity

// Programmatic scroll
st.scroll(500); // Set scroll position

// Get animation
const tween = st.animation; // Associated animation
const scrubTween = st.getTween(); // Scrub tween
```

## Utility Methods

### gsap.utils

```javascript
// Array helpers
gsap.utils.toArray(".class"); // Convert to array
gsap.utils.shuffle(array); // Randomize array order

// Math helpers
gsap.utils.random(min, max); // Random number
gsap.utils.snap(5); // Snap to increment (returns function)
gsap.utils.clamp(min, max, value); // Clamp value
gsap.utils.interpolate(start, end, progress); // Linear interpolation
gsap.utils.wrap(min, max); // Wrap value (returns function)
gsap.utils.normalize(min, max, value); // Normalize to 0-1
gsap.utils.mapRange(inMin, inMax, outMin, outMax, value); // Map value

// Selector helpers
gsap.utils.selector(element); // Create scoped selector function

// Distribution helpers
gsap.utils.distribute({
  base: 0,
  amount: 100,
  from: "center",
  ease: "power2.out"
});
```

## Common Patterns

```javascript
// Fade in on scroll
gsap.from(".element", {
  opacity: 0,
  y: 50,
  scrollTrigger: {
    trigger: ".element",
    start: "top 80%",
    scrub: 1
  }
});

// Pin while scrolling
ScrollTrigger.create({
  trigger: ".panel",
  pin: true,
  start: "top top",
  end: "+=500"
});

// Horizontal scroll
gsap.to(".panels", {
  xPercent: -100,
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".panels").offsetWidth
  }
});

// Parallax
gsap.to(".bg", {
  y: 300,
  ease: "none",
  scrollTrigger: {
    trigger: ".section",
    start: "top bottom",
    end: "bottom top",
    scrub: true
  }
});

// Batch stagger
ScrollTrigger.batch(".box", {
  onEnter: batch => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.15 }),
  start: "top 80%"
});
```
