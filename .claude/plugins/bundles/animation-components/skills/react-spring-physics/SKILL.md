---
name: react-spring-physics
description: Physics-based animation library combining React Spring (spring dynamics, gesture integration, 60fps animations) and Popmotion (low-level composable animation utilities, reactive streams). Use when building fluid, natural-feeling UI animations, gesture-driven interfaces, physics simulations, or spring-loaded interactions. Triggers on tasks involving React Spring hooks, spring physics, inertia scrolling, physics-based motion, animation composition, or natural UI movements. Alternative physics approach to motion-framer for more physically accurate animations.
---

# React Spring Physics

Physics-based animation for React applications combining React Spring's declarative spring animations with Popmotion's low-level physics utilities.

## Overview

React Spring provides spring-physics animations that feel natural and interruptible. Unlike duration-based animations, springs calculate motion based on physical properties (mass, tension, friction), resulting in organic, realistic movement. Popmotion complements this with composable animation functions for keyframes, decay, and inertia.

**When to use this skill:**
- Natural, physics-based UI animations
- Gesture-driven interfaces (drag, swipe, scroll)
- Interruptible animations that respond to user input mid-motion
- Smooth transitions that maintain velocity across state changes
- Momentum scrolling and inertia effects

**Core libraries:**
- `@react-spring/web` - React hooks for spring animations
- `@react-spring/three` - Three.js integration
- `popmotion` - Low-level animation utilities (optional, for advanced use cases)

## Core Concepts

### Spring Physics

Springs animate values from current state to target state using physical simulation:

```jsx
import { useSpring, animated } from '@react-spring/web'

function SpringExample() {
  const springs = useSpring({
    from: { opacity: 0, y: -40 },
    to: { opacity: 1, y: 0 },
    config: {
      mass: 1,        // Weight of object
      tension: 170,   // Spring strength
      friction: 26    // Opposing force
    }
  })

  return <animated.div style={springs}>Hello</animated.div>
}
```

### useSpring Hook Patterns

Two initialization patterns for different use cases:

```jsx
// Object config (simpler, auto-updates on prop changes)
const springs = useSpring({
  from: { x: 0 },
  to: { x: 100 }
})

// Function config (more control, returns API for imperative updates)
const [springs, api] = useSpring(() => ({
  from: { x: 0 }
}), [])

// Trigger animation via API
const handleClick = () => {
  api.start({
    from: { x: 0 },
    to: { x: 100 }
  })
}
```

### Spring Configuration Presets

React Spring provides built-in config presets:

```jsx
import { config } from '@react-spring/web'

// Available presets
config.default  // { tension: 170, friction: 26 }
config.gentle   // { tension: 120, friction: 14 }
config.wobbly   // { tension: 180, friction: 12 }
config.stiff    // { tension: 210, friction: 20 }
config.slow     // { tension: 280, friction: 60 }
config.molasses // { tension: 280, friction: 120 }

// Usage
const springs = useSpring({
  from: { x: 0 },
  to: { x: 100 },
  config: config.wobbly
})
```

## Common Patterns

### 1. Click-Triggered Spring Animation

```jsx
import { useSpring, animated } from '@react-spring/web'

function ClickAnimated() {
  const [springs, api] = useSpring(() => ({
    from: { scale: 1 }
  }), [])

  const handleClick = () => {
    api.start({
      from: { scale: 1 },
      to: { scale: 1.2 },
      config: { tension: 300, friction: 10 }
    })
  }

  return (
    <animated.button
      onClick={handleClick}
      style={{
        transform: springs.scale.to(s => `scale(${s})`)
      }}
    >
      Click Me
    </animated.button>
  )
}
```

### 2. Multi-Element Trail Animation

```jsx
import { useTrail, animated } from '@react-spring/web'

function Trail({ items }) {
  const trails = useTrail(items.length, {
    from: { opacity: 0, x: -20 },
    to: { opacity: 1, x: 0 },
    config: config.gentle
  })

  return (
    <div>
      {trails.map((style, i) => (
        <animated.div key={i} style={style}>
          {items[i]}
        </animated.div>
      ))}
    </div>
  )
}
```

### 3. List Transitions (Enter/Exit)

```jsx
import { useTransition, animated } from '@react-spring/web'

function List({ items }) {
  const transitions = useTransition(items, {
    from: { opacity: 0, height: 0 },
    enter: { opacity: 1, height: 80 },
    leave: { opacity: 0, height: 0 },
    config: config.stiff,
    keys: item => item.id
  })

  return transitions((style, item) => (
    <animated.div style={style}>
      {item.text}
    </animated.div>
  ))
}
```

### 4. Scroll-Based Spring Animation

```jsx
import { useScroll, animated } from '@react-spring/web'

function ScrollReveal() {
  const { scrollYProgress } = useScroll()

  return (
    <animated.div
      style={{
        opacity: scrollYProgress.to([0, 0.5], [0, 1]),
        scale: scrollYProgress.to([0, 0.5], [0.8, 1])
      }}
    >
      Scroll to reveal
    </animated.div>
  )
}
```

### 5. Viewport Intersection Animation

```jsx
import { useInView, animated } from '@react-spring/web'

function FadeInOnView() {
  const [ref, springs] = useInView(
    () => ({
      from: { opacity: 0, y: 100 },
      to: { opacity: 1, y: 0 }
    }),
    { rootMargin: '-40% 0%' }
  )

  return <animated.div ref={ref} style={springs}>Content</animated.div>
}
```

### 6. Chained Async Animations

```jsx
import { useSpring, animated } from '@react-spring/web'

function ChainedAnimation() {
  const springs = useSpring({
    from: { x: 0, background: '#ff6d6d' },
    to: [
      { x: 80, background: '#fff59a' },
      { x: 0, background: '#88DFAB' },
      { x: 80, background: '#569AFF' }
    ],
    config: { tension: 200, friction: 20 },
    loop: true
  })

  return <animated.div style={springs} />
}
```

### 7. Spring with Velocity Preservation

```jsx
import { useSpring, animated } from '@react-spring/web'

function VelocityPreservation() {
  const [springs, api] = useSpring(() => ({
    x: 0,
    config: { tension: 300, friction: 30 }
  }), [])

  const handleDragEnd = () => {
    api.start({
      x: 0,
      velocity: springs.x.getVelocity(), // Preserve momentum
      config: { tension: 200, friction: 20 }
    })
  }

  return <animated.div style={springs} onMouseUp={handleDragEnd} />
}
```

## Integration Patterns

### With React Three Fiber (3D)

```jsx
import { useSpring, animated } from '@react-spring/three'
import { Canvas } from '@react-three/fiber'

const AnimatedBox = animated(MeshDistortMaterial)

function ThreeScene() {
  const [clicked, setClicked] = useState(false)

  const springs = useSpring({
    scale: clicked ? 1.5 : 1,
    color: clicked ? '#569AFF' : '#ff6d6d',
    config: { tension: 200, friction: 20 }
  })

  return (
    <Canvas>
      <mesh onClick={() => setClicked(!clicked)} scale={springs.scale}>
        <sphereGeometry args={[1, 64, 32]} />
        <AnimatedBox color={springs.color} />
      </mesh>
    </Canvas>
  )
}
```

### With Popmotion (Low-Level Physics)

```jsx
import { spring, inertia } from 'popmotion'
import { useState } from 'react'

function PopmotionIntegration() {
  const [x, setX] = useState(0)

  const handleDragEnd = (velocity) => {
    inertia({
      from: x,
      velocity: velocity,
      power: 0.3,
      timeConstant: 400,
      modifyTarget: v => Math.round(v / 100) * 100 // Snap to grid
    }).start(setX)
  }

  return <div style={{ transform: `translateX(${x}px)` }} />
}
```

### With Forms and Validation

```jsx
import { useSpring, animated } from '@react-spring/web'

function ValidatedInput() {
  const [error, setError] = useState(false)

  const shakeAnimation = useSpring({
    x: error ? [0, -10, 10, -10, 10, 0] : 0,
    config: { tension: 300, friction: 10 },
    onRest: () => setError(false)
  })

  return <animated.input style={shakeAnimation} />
}
```

## Performance Optimization

### On-Demand Rendering

```jsx
// Only re-render when animation is active
const [springs, api] = useSpring(() => ({
  from: { x: 0 },
  config: { precision: 0.01 } // Higher value = less updates
}), [])
```

### Batch Multiple Springs

```jsx
// Use useSprings for multiple similar animations
const springs = useSprings(
  items.length,
  items.map(item => ({
    from: { opacity: 0 },
    to: { opacity: 1 }
  }))
)
```

### Skip Animation (Testing/Accessibility)

```jsx
import { Globals } from '@react-spring/web'

// Skip all animations (prefers-reduced-motion)
useEffect(() => {
  Globals.assign({ skipAnimation: true })
  return () => Globals.assign({ skipAnimation: false })
}, [])
```

## Common Pitfalls

### 1. Forgetting Dependencies Array

```jsx
// ❌ Wrong: No dependencies, creates new spring every render
const springs = useSpring(() => ({ x: 0 }))

// ✅ Correct: Empty array prevents recreation
const [springs, api] = useSpring(() => ({ x: 0 }), [])
```

### 2. Mutating Spring Values

```jsx
// ❌ Wrong: Direct mutation
springs.x.set(100)

// ✅ Correct: Use API to animate
api.start({ x: 100 })
```

### 3. Ignoring Config Precision

```jsx
// ❌ Default precision too fine (0.0001), causing unnecessary renders
const springs = useSpring({ x: 0 })

// ✅ Set appropriate precision for your use case
const springs = useSpring({
  x: 0,
  config: { precision: 0.01 } // Stop updating when within 0.01 of target
})
```

### 4. Not Handling Velocity

```jsx
// ❌ Abrupt stop when interrupting animation
api.start({ x: 0 })

// ✅ Preserve momentum
api.start({
  x: 0,
  velocity: springs.x.getVelocity()
})
```

### 5. Mixing Config Patterns

```jsx
// ❌ Wrong: Using both object and function config
const springs = useSpring({
  from: { x: 0 }
})
api.start({ x: 100 }) // api is undefined

// ✅ Correct: Use function config for imperative control
const [springs, api] = useSpring(() => ({
  from: { x: 0 }
}), [])
```

### 6. Animating Non-Numerical Values

```jsx
// ❌ Wrong: Spring can't interpolate complex strings directly
const springs = useSpring({ transform: 'translateX(100px) rotate(45deg)' })

// ✅ Correct: Animate individual values
const springs = useSpring({ x: 100, rotation: 45 })
// Then combine: transform: `translateX(${x}px) rotate(${rotation}deg)`
```

## Resources

### Scripts
- `spring_generator.py` - Generate React Spring boilerplate code
- `physics_calculator.py` - Calculate optimal spring physics parameters

### References
- `react_spring_api.md` - Complete React Spring hooks and API reference
- `popmotion_api.md` - Popmotion functions and reactive streams
- `physics_guide.md` - Spring physics deep dive with tuning guide

### Assets
- `starter_spring/` - React + Vite template with React Spring examples
- `examples/` - Real-world patterns (gestures, scroll, 3D integration)

## Related Skills

- **motion-framer** - Alternative declarative animation approach with variants
- **gsap-scrolltrigger** - Timeline-based animations for complex sequences
- **react-three-fiber** - 3D scene management (use @react-spring/three for animations)
- **animated-component-libraries** - Pre-built animated components using Motion

**Physics vs Timeline**: Use React Spring for natural, physics-based motion that responds to user input. Use GSAP for precise, timeline-based choreography and complex multi-step sequences.
