# Popmotion API Reference

Low-level animation library providing composable animation functions. Useful for advanced physics simulations and custom animation logic.

## Table of Contents

- [Core Animations](#core-animations)
  - [spring](#spring)
  - [inertia](#inertia)
  - [keyframes](#keyframes)
  - [decay](#decay)
  - [physics](#physics)
- [Animation Control](#animation-control)
- [Easing Functions](#easing-functions)
- [Utilities](#utilities)

---

## Core Animations

### spring

Physics-based spring animation.

**Signature:**
```typescript
spring(config: SpringConfig): Animation
```

**Config Properties:**
```typescript
interface SpringConfig {
  from?: number | object | array
  to?: number | object | array
  stiffness?: number    // Spring strength (default: 100)
  damping?: number      // Opposing force (default: 10)
  mass?: number         // Object mass (default: 1)
  velocity?: number     // Initial velocity (default: 0)
  restSpeed?: number    // Stop threshold (default: 0.001)
  restDelta?: number    // Position threshold (default: 0.01)
}
```

**Examples:**
```javascript
import { spring } from 'popmotion'

// Basic spring
spring({
  from: 0,
  to: 100,
  stiffness: 200,
  damping: 20
}).start(v => console.log(v))

// With velocity
spring({
  from: ballXY.get(),
  velocity: ballXY.getVelocity(),
  stiffness: 300,
  damping: 10
}).start(ballXY)

// Object values
spring({
  from: { x: 0, y: 0 },
  to: { x: 100, y: 200 },
  stiffness: { x: 200, y: 1000 },
  damping: { x: 10, y: 50 }
}).start(({ x, y }) => console.log(x, y))
```

**Value Types:**
- Numbers: `spring({ from: 0, to: 100 })`
- Units: `spring({ from: '0px', to: '100px' })`
- Colors: `spring({ from: '#fff', to: '#000' })`
- Objects: `spring({ from: { x: 0 }, to: { x: 100 } })`
- Arrays: `spring({ from: [0, 0], to: [100, 200] })`

---

### inertia

Momentum-based deceleration with spring-loaded boundaries.

**Signature:**
```typescript
inertia(config: InertiaConfig): Animation
```

**Config Properties:**
```typescript
interface InertiaConfig {
  from?: number
  velocity?: number       // Initial velocity (required)
  power?: number          // Deceleration strength (default: 0.8)
  timeConstant?: number   // Deceleration duration (default: 350)
  restDelta?: number      // Stop threshold (default: 0.5)
  min?: number            // Minimum boundary
  max?: number            // Maximum boundary
  bounceStiffness?: number // Boundary spring strength (default: 500)
  bounceDamping?: number  // Boundary spring damping (default: 10)
  modifyTarget?: (v: number) => number // Snap function
}
```

**Examples:**
```javascript
import { inertia } from 'popmotion'

// Basic momentum scroll
inertia({
  from: 50,
  velocity: 500
}).start(v => console.log(v))

// With boundaries
inertia({
  from: 50,
  velocity: 500,
  min: 0,
  max: 1000,
  bounceStiffness: 1000,
  bounceDamping: 300
}).start(v => console.log(v))

// Snap to grid
inertia({
  from: 50,
  velocity: 200,
  modifyTarget: v => Math.round(v / 100) * 100
}).start(v => console.log(v))
```

**Use Cases:**
- Momentum scrolling
- Swipe-to-dismiss
- Physics-based drag release
- Snap-to-grid animations

---

### keyframes

Animate through a sequence of values.

**Signature:**
```typescript
keyframes(config: KeyframesConfig): Animation
```

**Config Properties:**
```typescript
interface KeyframesConfig {
  values: any[]           // Keyframe values
  times?: number[]        // Progress points (0-1)
  duration?: number       // Total duration (default: 300)
  easings?: Easing[]      // Per-segment easings
}
```

**Examples:**
```javascript
import { keyframes, linear, easeInOut } from 'popmotion'

// Basic keyframes
keyframes({
  values: [0, 100, 200],
  duration: 1000
}).start(v => console.log(v))

// With times and easings
keyframes({
  values: [0, 100, 200],
  times: [0, 0.2, 1],
  duration: 1000,
  easings: [linear, easeInOut]
}).start(v => console.log(v))

// Color animation
keyframes({
  values: ['#fff', '#000', '#f00'],
  duration: 2000
}).start(color => console.log(color))
```

---

### decay

Exponential deceleration (no terminal velocity).

**Signature:**
```typescript
decay(config: DecayConfig): Animation
```

**Config Properties:**
```typescript
interface DecayConfig {
  from?: number
  velocity?: number     // Initial velocity (required)
  power?: number        // Deceleration strength (default: 0.8)
  timeConstant?: number // Controls decay rate (default: 350)
  restDelta?: number    // Stop threshold (default: 0.5)
  modifyTarget?: (v: number) => number
}
```

**Example:**
```javascript
import { decay } from 'popmotion'

decay({
  from: 0,
  velocity: 1000,
  power: 0.8,
  timeConstant: 400
}).start(v => console.log(v))
```

---

### physics

Integrated physics simulation (velocity, acceleration, friction, springs).

**Signature:**
```typescript
physics(config: PhysicsConfig): Animation
```

**Config Properties:**
```typescript
interface PhysicsConfig {
  from?: number
  velocity?: number         // Units per second (default: 0)
  acceleration?: number     // Increase velocity (default: 0)
  friction?: number         // 0-1 deceleration (default: 0)
  springStrength?: number   // Spring force (with `to`)
  to?: number               // Spring target (with `springStrength`)
  restSpeed?: number        // Stop threshold (default: 0.001)
}
```

**Examples:**
```javascript
import { physics } from 'popmotion'

// Accelerating object
physics({
  from: 0,
  velocity: 0,
  acceleration: 100
}).start(v => console.log(v))

// Friction-based deceleration
physics({
  from: 0,
  velocity: 1000,
  friction: 0.8
}).start(v => console.log(v))

// Spring simulation
physics({
  from: 0,
  velocity: 1000,
  friction: 0.8,
  to: 400,
  springStrength: 500
}).start(v => console.log(v))
```

**Playback Methods:**
```javascript
const animation = physics({ from: 0, velocity: 100 }).start(v => {})

animation.setVelocity(500)
animation.setAcceleration(200)
animation.setFriction(0.9)
animation.setSpringStrength(600)
animation.setSpringTarget(500)
animation.stop()
```

---

## Animation Control

All animations return playback controls via `.start()`.

**Basic Start:**
```javascript
animation.start(v => {
  // Update callback
})
```

**With Complete Callback:**
```javascript
animation.start({
  update: v => { /* on update */ },
  complete: () => { /* on complete */ }
})
```

**Common Methods:**
```javascript
const controls = animation.start(v => {})

controls.stop()  // Stop animation
```

**Chaining Methods:**
```javascript
// Filter values
spring({ from: 0, to: 100 })
  .filter(v => v > 50)
  .start(v => console.log(v)) // Only outputs values > 50

// Transform output
spring({ from: 0, to: 100 })
  .pipe(Math.round, v => v * 2)
  .start(v => console.log(v)) // Rounded and doubled

// Conditional completion
spring({ from: 0, to: 100 })
  .while(v => v < 75)
  .start(v => console.log(v)) // Stops when v >= 75
```

---

## Easing Functions

**Importing:**
```javascript
import {
  linear,
  easeIn, easeOut, easeInOut,
  circIn, circOut, circInOut,
  backIn, backOut, backInOut,
  anticipate,
  cubicBezier
} from 'popmotion'
```

**Built-in Easings:**
- `linear` - Constant speed
- `easeIn, easeOut, easeInOut` - Quadratic easing
- `circIn, circOut, circInOut` - Circular easing
- `backIn, backOut, backInOut` - Back easing (overshoot)
- `anticipate` - Pull back then overshoot

**Custom Cubic Bezier:**
```javascript
import { cubicBezier } from 'popmotion'

const customEase = cubicBezier(0.17, 0.67, 0.83, 0.67)
```

**Creating Custom Easings:**
```javascript
import {
  createExpoIn,
  createBackIn,
  createAnticipate,
  mirrorEasing,
  reverseEasing
} from 'popmotion'

// Exponential easing
const expoIn = createExpoIn(4)
const expoOut = mirrorEasing(expoIn)
const expoInOut = reverseEasing(expoIn)

// Back easing with custom overshoot
const backIn = createBackIn(4)

// Anticipate with custom power
const anticipate = createAnticipate(4)
```

**Usage with Keyframes:**
```javascript
import { keyframes, easeInOut } from 'popmotion'

keyframes({
  values: [0, 100],
  duration: 1000,
  easings: [easeInOut]
}).start(v => console.log(v))
```

---

## Utilities

### animate

High-level animation API (similar to GSAP/CSS animations).

```javascript
import { animate, spring, linear } from 'popmotion'

// Duration-based
animate({
  from: 0,
  to: 100,
  duration: 1000,
  ease: linear
}).start(v => console.log(v))

// Spring-based
animate({
  from: 0,
  to: 100,
  type: 'spring',
  stiffness: 1000,
  damping: 50
}).start(v => console.log(v))
```

### Multi-value Animations

**Objects:**
```javascript
spring({
  from: { x: 0, y: 0 },
  to: { x: 100, y: 200 }
}).start(({ x, y }) => {
  console.log(`x: ${x}, y: ${y}`)
})
```

**Arrays:**
```javascript
spring({
  from: [0, 0],
  to: [100, 200]
}).start(([x, y]) => {
  console.log(`x: ${x}, y: ${y}`)
})
```

**Complex Strings:**
```javascript
spring({
  from: '0px 0px 0px inset rgba(0, 0, 0, 0.2)',
  to: '3px 3px 10px inset rgba(0, 0, 0, 0.5)'
}).start(shadow => {
  element.style.boxShadow = shadow
})
```

---

## Integration with React Spring

Popmotion is typically used for advanced use cases where React Spring's declarative API isn't sufficient.

**Example: Custom Physics:**
```jsx
import { physics } from 'popmotion'
import { useState, useEffect } from 'react'

function CustomPhysics() {
  const [x, setX] = useState(0)

  const handleDragEnd = (velocity) => {
    physics({
      from: x,
      velocity: velocity,
      friction: 0.8,
      to: 0,
      springStrength: 500
    }).start(setX)
  }

  return <div style={{ transform: `translateX(${x}px)` }} />
}
```

**Example: Snap-to-Grid Inertia:**
```jsx
import { inertia } from 'popmotion'
import { useState } from 'react'

function SnapGrid() {
  const [x, setX] = useState(0)

  const handleDragEnd = (velocity) => {
    inertia({
      from: x,
      velocity: velocity,
      modifyTarget: v => Math.round(v / 100) * 100,
      bounceStiffness: 1000,
      bounceDamping: 300
    }).start(setX)
  }

  return <div style={{ transform: `translateX(${x}px)` }} />
}
```

---

## Performance Notes

1. **Composable** - Chain `.filter()`, `.pipe()`, `.while()` for custom behavior
2. **Low-level** - No React overhead, direct DOM manipulation
3. **Tree-shakeable** - Import only what you need
4. **Zero dependencies** - Tiny bundle size (~5KB)
5. **60fps** - Optimized for frame-based updates

---

## Common Patterns

### Drag with Inertia

```javascript
import { inertia } from 'popmotion'

let velocity = 0

// Track velocity during drag
const handleDrag = (dx, dt) => {
  velocity = dx / dt
}

// Apply inertia on release
const handleDragEnd = () => {
  inertia({
    from: currentX,
    velocity: velocity,
    power: 0.8,
    timeConstant: 400
  }).start(setX)
}
```

### Spring Taper (Follow Pointer)

```javascript
import { physics } from 'popmotion'

const springTo = physics({
  velocity: ballXY.getVelocity(),
  friction: 0.6,
  springStrength: 400,
  to: ballXY.get(),
  restSpeed: false
}).start(ballXY)

pointer(ballXY.get())
  .start(v => springTo.setSpringTarget(v))
```

### Boundary Constraints

```javascript
import { spring } from 'popmotion'

const handleRelease = () => {
  const x = handleX.get()

  if (x < 0 || x > 250) {
    spring({
      from: x,
      to: x < 0 ? 0 : 250,
      velocity: handleX.getVelocity(),
      stiffness: 900,
      damping: 30
    }).start(handleX)
  } else {
    handleX.stop()
  }
}
```
