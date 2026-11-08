# Spring Physics Deep Dive

Understanding and tuning spring animations for natural, physically accurate motion.

## Table of Contents

- [Physics Fundamentals](#physics-fundamentals)
- [Spring Parameters](#spring-parameters)
- [Tuning Guide](#tuning-guide)
- [Common Configurations](#common-configurations)
- [Velocity and Momentum](#velocity-and-momentum)
- [Advanced Techniques](#advanced-techniques)

---

## Physics Fundamentals

### What is a Spring Animation?

Unlike duration-based animations (e.g., "move from A to B in 300ms"), spring animations simulate physical motion based on forces:

**Hooke's Law:**
```
F = -k * x

Where:
F = Force applied by spring
k = Spring constant (stiffness)
x = Displacement from rest position
```

**Damping Force:**
```
F_damping = -c * v

Where:
c = Damping coefficient (friction)
v = Velocity
```

**Result:** Natural, bouncy motion that **automatically calculates duration** based on physics.

---

## Spring Parameters

### Mass

**What it does:** Determines object's weight/inertia.

**Effect:**
- **Higher mass** (e.g., 5): Heavier, slower to accelerate/decelerate
- **Lower mass** (e.g., 0.5): Lighter, more responsive

**When to increase:**
- Large UI elements (modals, panels)
- Dramatic, weighty animations
- Slow, deliberate movements

**When to decrease:**
- Small UI elements (tooltips, badges)
- Quick, snappy interactions
- Lightweight, responsive feel

**Example:**
```jsx
// Heavy modal
{ mass: 5, tension: 170, friction: 26 }

// Lightweight tooltip
{ mass: 0.5, tension: 170, friction: 26 }
```

---

### Tension (Stiffness)

**What it does:** Spring's resistance to stretching (spring strength).

**Effect:**
- **Higher tension** (e.g., 300): Faster, stiffer spring
- **Lower tension** (e.g., 100): Slower, softer spring

**When to increase:**
- Quick, responsive interactions
- Snappy button feedback
- Alert animations

**When to decrease:**
- Gentle, smooth transitions
- Organic, flowing motion
- Relaxed page transitions

**Example:**
```jsx
// Snappy button press
{ tension: 300, friction: 20 }

// Gentle fade-in
{ tension: 120, friction: 14 }
```

---

### Friction (Damping)

**What it does:** Opposing force that slows motion.

**Effect:**
- **Higher friction** (e.g., 40): Less overshoot, faster settling
- **Lower friction** (e.g**, 10): More bounce, oscillation

**When to increase:**
- Minimal overshoot desired
- Professional, controlled feel
- Quick settle time

**When to decrease:**
- Playful, bouncy animations
- Noticeable spring effect
- Dramatic overshoot

**Example:**
```jsx
// Minimal bounce (controlled)
{ tension: 170, friction: 40 }

// Bouncy, playful
{ tension: 180, friction: 12 }
```

---

## Tuning Guide

### Step-by-Step Tuning Process

**1. Start with a preset:**
```jsx
import { config } from '@react-spring/web'

// Try these first:
config.default  // Balanced
config.gentle   // Smooth, slow
config.wobbly   // Bouncy
config.stiff    // Fast, minimal bounce
```

**2. Adjust tension for speed:**
```jsx
// Too slow? Increase tension
{ tension: 250, friction: 26 }

// Too fast? Decrease tension
{ tension: 120, friction: 26 }
```

**3. Adjust friction for bounce:**
```jsx
// Too bouncy? Increase friction
{ tension: 170, friction: 35 }

// Not bouncy enough? Decrease friction
{ tension: 170, friction: 15 }
```

**4. Adjust mass for weight:**
```jsx
// Feels too light? Increase mass
{ mass: 3, tension: 170, friction: 26 }

// Too heavy/sluggish? Decrease mass
{ mass: 0.7, tension: 170, friction: 26 }
```

---

### Visual Tuning Tool

React Spring provides an interactive tuning tool:

```jsx
import { useSpring, animated } from '@react-spring/web'
import { useControls } from 'leva'

function Tuner() {
  const config = useControls({
    mass: { value: 1, min: 0.1, max: 10 },
    tension: { value: 170, min: 1, max: 500 },
    friction: { value: 26, min: 1, max: 100 }
  })

  const springs = useSpring({
    from: { x: 0 },
    to: { x: 100 },
    config
  })

  return <animated.div style={springs} />
}
```

Install leva: `npm install leva`

---

## Common Configurations

### By Use Case

**Button Interactions (Quick, Responsive):**
```jsx
{ mass: 1, tension: 300, friction: 20 }
// Fast response, minimal bounce
```

**Modal Animations (Dramatic, Smooth):**
```jsx
{ mass: 2, tension: 150, friction: 30 }
// Weighty, controlled entrance
```

**Page Transitions (Smooth, Professional):**
```jsx
{ mass: 1, tension: 120, friction: 14 }
// Gentle, flowing motion
```

**Notifications/Toasts (Bouncy, Attention-Grabbing):**
```jsx
{ mass: 1, tension: 180, friction: 12 }
// Noticeable bounce, playful
```

**Drag-and-Drop (Natural Physics):**
```jsx
{ mass: 1, tension: 200, friction: 25 }
// Balanced, realistic feel
```

**Loading Indicators (Continuous, Smooth):**
```jsx
{ mass: 1, tension: 100, friction: 30 }
// Slow, controlled oscillation
```

---

### By Animation Feel

**Snappy:**
```jsx
{ mass: 0.8, tension: 300, friction: 20 }
```

**Bouncy:**
```jsx
{ mass: 1, tension: 180, friction: 12 }
```

**Smooth/Gentle:**
```jsx
{ mass: 1, tension: 120, friction: 14 }
```

**Stiff/Controlled:**
```jsx
{ mass: 1, tension: 210, friction: 20 }
```

**Slow/Lazy:**
```jsx
{ mass: 1, tension: 280, friction: 60 }
```

**Heavy/Dramatic:**
```jsx
{ mass: 5, tension: 170, friction: 26 }
```

---

## Velocity and Momentum

### Initial Velocity

Set starting velocity for momentum-based animations:

```jsx
const [springs, api] = useSpring(() => ({
  x: 0,
  config: { tension: 200, friction: 20 }
}), [])

api.start({
  x: 100,
  velocity: 500 // px/second
})
```

### Preserving Velocity (Interruptions)

Maintain momentum when interrupting an animation:

```jsx
const handleInterrupt = () => {
  api.start({
    x: newTarget,
    velocity: springs.x.getVelocity(), // Current velocity
    config: { tension: 300, friction: 25 }
  })
}
```

**Why this matters:**
- Natural feel when user changes direction mid-animation
- Smooth transitions between gesture states
- Realistic physics simulation

---

### Calculating Velocity from Gestures

```jsx
import { useDrag } from '@use-gesture/react'
import { useSpring, animated } from '@react-spring/web'

function DraggableElement() {
  const [{ x }, api] = useSpring(() => ({ x: 0 }))

  const bind = useDrag(({ down, movement: [mx], velocity: [vx] }) => {
    api.start({
      x: down ? mx : 0,
      velocity: vx * 1000, // Convert to px/second
      immediate: down,
      config: { tension: 200, friction: 30 }
    })
  })

  return <animated.div {...bind()} style={{ x }} />
}
```

---

## Advanced Techniques

### Conditional Spring Config

Different physics for different properties:

```jsx
const springs = useSpring({
  x: 100,
  scale: 1.5,
  opacity: 1,
  config: {
    x: { tension: 300, friction: 20 },      // Fast horizontal
    scale: { mass: 4, friction: 10 },       // Heavy scaling
    opacity: { tension: 120, friction: 14 }  // Gentle fade
  }
})
```

### Config as Function

Dynamic configuration based on property:

```jsx
const springs = useSpring({
  x: 100,
  y: 200,
  scale: 1.5,
  config: (key) => {
    if (key === 'scale') {
      return { mass: 4, friction: 10 }
    }
    if (key === 'x') {
      return { tension: 300, friction: 20 }
    }
    return config.default
  }
})
```

### Spring with Clamp

Prevent overshoot entirely:

```jsx
const springs = useSpring({
  x: 100,
  config: {
    tension: 300,
    friction: 20,
    clamp: true // No overshoot
  }
})
```

---

### Duration Override

Force a specific duration (not physically accurate):

```jsx
const springs = useSpring({
  x: 100,
  config: {
    duration: 500,  // Override physics
    easing: t => t  // Linear easing
  }
})
```

**Note:** When using `duration`, the animation is no longer physics-based. It becomes a traditional tween.

---

### Precision Tuning

Control when animation "completes":

```jsx
const springs = useSpring({
  x: 100,
  config: {
    tension: 170,
    friction: 26,
    precision: 0.01 // Stop when within 0.01 of target (default: 0.0001)
  }
})
```

**Higher precision (0.1):**
- Fewer updates
- Earlier completion
- Better performance
- Slight imprecision

**Lower precision (0.0001):**
- More updates
- Exact final value
- Slower performance
- Pixel-perfect

---

## Troubleshooting

### Animation Too Fast

**Solutions:**
1. Decrease `tension` (e.g., 170 → 120)
2. Increase `mass` (e.g., 1 → 2)
3. Increase `friction` (e.g., 26 → 40)

### Animation Too Slow

**Solutions:**
1. Increase `tension` (e.g., 170 → 250)
2. Decrease `mass` (e.g., 1 → 0.7)
3. Decrease `friction` (e.g., 26 → 15)

### Too Much Bounce/Overshoot

**Solutions:**
1. Increase `friction` (e.g., 26 → 40)
2. Enable `clamp: true`
3. Use `config.stiff` preset

### Not Enough Bounce

**Solutions:**
1. Decrease `friction` (e.g., 26 → 12)
2. Use `config.wobbly` preset
3. Increase `tension` slightly (e.g., 170 → 180)

### Animation Never Completes

**Solutions:**
1. Increase `precision` (e.g., 0.0001 → 0.01)
2. Check for conflicting animations
3. Ensure `restSpeed` is not set too low

---

## Mathematical Relationships

### Critical Damping

The point where spring returns to rest without oscillating:

```
c_critical = 2 * sqrt(k * m)

Where:
c = friction
k = tension
m = mass
```

**Damping Ratio:**
```
ζ = c / (2 * sqrt(k * m))

ζ > 1: Over-damped (no overshoot, slow)
ζ = 1: Critically damped (no overshoot, fast)
ζ < 1: Under-damped (overshoot, oscillation)
```

**Example:**
```jsx
// Calculate critically damped friction
const mass = 1
const tension = 170
const criticalFriction = 2 * Math.sqrt(tension * mass)
// criticalFriction ≈ 26 (default React Spring config!)

// Under-damped (bouncy)
{ mass: 1, tension: 170, friction: 12 } // ζ ≈ 0.46

// Critically damped
{ mass: 1, tension: 170, friction: 26 } // ζ = 1

// Over-damped (slow)
{ mass: 1, tension: 170, friction: 40 } // ζ ≈ 1.53
```

---

## Comparison: Duration vs Physics

### Duration-Based (Traditional)

```jsx
// CSS transition
transition: all 300ms ease-in-out;

// React Spring duration override
{ duration: 300, easing: easeInOut }
```

**Pros:**
- Predictable timing
- Easier to sync with other events
- Consistent across devices

**Cons:**
- Feels artificial when interrupted
- Loses momentum on direction change
- Not physically accurate

---

### Physics-Based (Spring)

```jsx
{ mass: 1, tension: 170, friction: 26 }
```

**Pros:**
- Natural, organic feel
- Interruptible without jarring
- Preserves momentum
- Realistic physics

**Cons:**
- Variable duration (depends on distance, velocity)
- Harder to sync precisely
- Requires tuning for desired feel

---

## Best Practices

1. **Start with presets** - Use `config.default`, `config.gentle`, etc.
2. **Tune visually** - Use Leva or similar tool to adjust in real-time
3. **Preserve velocity** - Use `getVelocity()` for interruptions
4. **Set appropriate precision** - Higher for better performance
5. **Test on target devices** - Physics may feel different on slow devices
6. **Use duration sparingly** - Only when exact timing is critical
7. **Document custom configs** - Add comments explaining physics choices
8. **Consistency matters** - Use similar configs for similar interactions

---

## Resources

- [Spring Physics Calculator](https://react-spring.dev/examples/springs) - Interactive tuning
- [Leva](https://github.com/pmndrs/leva) - Real-time config editor
- [Hooke's Law](https://en.wikipedia.org/wiki/Hooke%27s_law) - Physics fundamentals
- [Damped Harmonic Oscillator](https://en.wikipedia.org/wiki/Harmonic_oscillator#Damped_harmonic_oscillator) - Spring theory
