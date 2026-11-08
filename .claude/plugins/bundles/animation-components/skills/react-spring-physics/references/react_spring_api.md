# React Spring API Reference

Complete API documentation for React Spring hooks, components, and utilities.

## Table of Contents

- [Core Hooks](#core-hooks)
  - [useSpring](#usespring)
  - [useSprings](#usesprings)
  - [useTrail](#usetrail)
  - [useTransition](#usetransition)
  - [useSpringValue](#usespringvalue)
- [Utility Hooks](#utility-hooks)
  - [useScroll](#usescroll)
  - [useInView](#useinview)
  - [useSpringRef](#usespringref)
  - [useIsomorphicLayoutEffect](#useisomorphiclayouteffect)
- [Components](#components)
  - [animated](#animated)
- [Configuration](#configuration)
  - [Config Presets](#config-presets)
  - [Config Properties](#config-properties)
- [API Methods](#api-methods)
  - [SpringRef API](#springref-api)
  - [SpringValue Methods](#springvalue-methods)
- [Events](#events)
- [Globals](#globals)

---

## Core Hooks

### useSpring

Create a single spring animation.

**TypeScript Signature (Object Config):**
```typescript
function useSpring(config: SpringConfig): SpringValues
```

**TypeScript Signature (Function Config):**
```typescript
function useSpring(
  configFn: () => SpringConfig,
  deps?: any[]
): [SpringValues, SpringRef]
```

**Parameters:**
- `config` or `configFn` - Animation configuration
- `deps` - Dependency array for re-evaluation (function config only)

**Returns:**
- Object config: `SpringValues` for rendering
- Function config: `[SpringValues, SpringRef]` tuple

**Example (Object Config):**
```jsx
const springs = useSpring({
  from: { opacity: 0 },
  to: { opacity: 1 },
  config: { tension: 170, friction: 26 }
})
```

**Example (Function Config):**
```jsx
const [springs, api] = useSpring(() => ({
  from: { opacity: 0 },
  config: { tension: 170, friction: 26 }
}), [])

// Trigger animation imperatively
api.start({ to: { opacity: 1 } })
```

---

### useSprings

Create multiple spring animations with a unified API.

**TypeScript Signature (Object Config):**
```typescript
function useSprings(count: number, config: SpringConfig): SpringValues[]
```

**TypeScript Signature (Function Config):**
```typescript
function useSprings(
  count: number,
  configFn: (index: number) => SpringConfig,
  deps?: any[]
): [SpringValues[], SpringRef]
```

**Parameters:**
- `count` - Number of springs to create
- `config` or `configFn` - Configuration (function receives index)
- `deps` - Dependency array for re-evaluation

**Returns:**
- Object config: `SpringValues[]` array
- Function config: `[SpringValues[], SpringRef]` tuple

**Example:**
```jsx
const springs = useSprings(
  items.length,
  items.map((item, i) => ({
    from: { opacity: 0, x: -20 },
    to: { opacity: 1, x: 0 },
    delay: i * 100
  }))
)
```

---

### useTrail

Create a trailing animation where each spring follows the previous.

**TypeScript Signature (Object Config):**
```typescript
function useTrail(count: number, config: SpringConfig): SpringValues[]
```

**TypeScript Signature (Function Config):**
```typescript
function useTrail(
  count: number,
  configFn: () => SpringConfig,
  deps?: any[]
): [SpringValues[], SpringRef]
```

**Example:**
```jsx
const trails = useTrail(5, {
  from: { opacity: 0, x: -20 },
  to: { opacity: 1, x: 0 },
  config: config.gentle
})
```

---

### useTransition

Animate a dataset with enter/leave transitions.

**TypeScript Signature (Object Config):**
```typescript
function useTransition<Item>(
  data: Item[],
  config: TransitionConfig<Item>
): TransitionFn
```

**TypeScript Signature (Function Config):**
```typescript
function useTransition<Item>(
  data: Item[],
  configFn: () => TransitionConfig<Item>,
  deps?: any[]
): [TransitionFn, SpringRef]
```

**TransitionConfig Properties:**
- `from` - Initial styles for entering items
- `enter` - Target styles for entered items
- `leave` - Exit styles for leaving items
- `update` - Styles for items that update (optional)
- `keys` - Function or key to identify items

**Example:**
```jsx
const transitions = useTransition(items, {
  from: { opacity: 0, height: 0 },
  enter: { opacity: 1, height: 80 },
  leave: { opacity: 0, height: 0 },
  keys: item => item.id
})

return transitions((style, item) => (
  <animated.div style={style}>{item.text}</animated.div>
))
```

---

### useSpringValue

Create a single animated value.

**TypeScript Signature:**
```typescript
function useSpringValue<T>(
  initial: T,
  config?: SpringConfig
): SpringValue<T>
```

**Example:**
```jsx
const opacity = useSpringValue(0, {
  config: { mass: 2, friction: 5, tension: 80 }
})

// Update value
opacity.start(1)
```

---

## Utility Hooks

### useScroll

Track scroll position with spring physics.

**TypeScript Signature:**
```typescript
function useScroll(config?: ScrollConfig): {
  scrollX: SpringValue<number>
  scrollY: SpringValue<number>
  scrollXProgress: SpringValue<number>
  scrollYProgress: SpringValue<number>
}
```

**ScrollConfig Properties:**
- `container` - Scroll container ref (default: window)
- `config` - Spring configuration

**Example:**
```jsx
const { scrollYProgress } = useScroll()

return (
  <animated.div style={{ opacity: scrollYProgress }}>
    Fades in as you scroll
  </animated.div>
)
```

---

### useInView

Trigger animation when element enters viewport.

**TypeScript Signature:**
```typescript
function useInView<T extends HTMLElement>(
  configFn: () => SpringConfig,
  options?: IntersectionObserverInit
): [RefCallback<T>, SpringValues]
```

**Options (IntersectionObserverInit):**
- `root` - Viewport element (default: browser viewport)
- `rootMargin` - Margin around root (e.g., '-40% 0%')
- `threshold` - Visibility threshold (0-1)

**Example:**
```jsx
const [ref, springs] = useInView(
  () => ({
    from: { opacity: 0, y: 100 },
    to: { opacity: 1, y: 0 }
  }),
  { rootMargin: '-20% 0%' }
)

return <animated.div ref={ref} style={springs}>Content</animated.div>
```

---

### useSpringRef

Create a ref for controlling springs imperatively.

**TypeScript Signature:**
```typescript
function useSpringRef(): SpringRef
```

**Example:**
```jsx
const api = useSpringRef()

const springs = useSpring({
  ref: api,
  from: { opacity: 0 },
  to: { opacity: 1 }
})

// Control via ref
api.start({ opacity: 0.5 })
```

---

### useIsomorphicLayoutEffect

Cross-platform useLayoutEffect (server-safe).

**TypeScript Signature:**
```typescript
function useIsomorphicLayoutEffect(
  effect: EffectCallback,
  deps?: DependencyList
): void
```

**Usage:**
Use like `useLayoutEffect` but works on server-side rendering.

---

## Components

### animated

Higher-Order Component to make elements animatable.

**Built-in Animated Components:**
```jsx
import { animated } from '@react-spring/web'

animated.div
animated.span
animated.p
animated.svg
animated.path
animated.g
// ... all HTML elements
```

**Custom Component Animation:**
```jsx
import { animated } from '@react-spring/web'
import { CustomComponent } from './CustomComponent'

const AnimatedCustom = animated(CustomComponent)

// Component must forward style prop to native element
function CustomComponent({ style, ...props }) {
  return <div style={style} {...props} />
}
```

**Three.js Integration:**
```jsx
import { animated } from '@react-spring/three'
import { MeshDistortMaterial } from '@react-three/drei'

const AnimatedMaterial = animated(MeshDistortMaterial)
```

---

## Configuration

### Config Presets

Pre-defined spring configurations for common animation feels.

```jsx
import { config } from '@react-spring/web'

config.default  // { tension: 170, friction: 26 }
config.gentle   // { tension: 120, friction: 14 }
config.wobbly   // { tension: 180, friction: 12 }
config.stiff    // { tension: 210, friction: 20 }
config.slow     // { tension: 280, friction: 60 }
config.molasses // { tension: 280, friction: 120 }
```

**Usage:**
```jsx
useSpring({
  from: { x: 0 },
  to: { x: 100 },
  config: config.wobbly
})
```

---

### Config Properties

Fine-tune spring physics manually.

**SpringConfig Interface:**
```typescript
interface SpringConfig {
  mass?: number          // Mass of object (default: 1)
  tension?: number       // Spring strength (default: 170)
  friction?: number      // Opposing force (default: 26)
  clamp?: boolean        // Prevent overshooting (default: false)
  precision?: number     // Stop threshold (default: 0.0001)
  velocity?: number      // Initial velocity (default: 0)
  duration?: number      // Override physics with fixed duration
  easing?: EasingFunction // Easing function (requires duration)
  bounce?: number        // Bounce factor 0-1 (alternative to tension/friction)
}
```

**Property-Specific Config:**
```jsx
useSpring({
  x: 100,
  y: 200,
  config: {
    x: { tension: 300, friction: 20 }, // Fast horizontal
    y: { tension: 100, friction: 30 }  // Slow vertical
  }
})
```

**Config as Function:**
```jsx
useSpring({
  x: 100,
  scale: 1.5,
  config: (key) => {
    if (key === 'scale') return { mass: 4, friction: 10 }
    return config.default
  }
})
```

---

## API Methods

### SpringRef API

Imperative control interface returned by function-config hooks.

**Methods:**

#### api.start(config)

Start or update animation.

```jsx
api.start({
  from: { x: 0 },
  to: { x: 100 },
  config: { tension: 200 },
  onRest: () => console.log('Done!')
})
```

#### api.pause()

Pause all animations.

```jsx
api.pause()
```

#### api.resume()

Resume paused animations.

```jsx
api.resume()
```

#### api.stop()

Stop all animations immediately.

```jsx
api.stop()
```

#### api.set(values)

Instantly set values without animating.

```jsx
api.set({ x: 100, opacity: 1 })
```

---

### SpringValue Methods

Methods available on individual SpringValue instances.

**get()** - Get current value:
```jsx
const currentX = springs.x.get()
```

**getVelocity()** - Get current velocity:
```jsx
const velocity = springs.x.getVelocity()
```

**to()** - Transform value:
```jsx
<animated.div
  style={{
    transform: springs.x.to(x => `translateX(${x}px)`)
  }}
/>
```

**start()** - Animate this value:
```jsx
springs.opacity.start(1)
```

---

## Events

Event callbacks for animation lifecycle.

**Event Properties:**
```typescript
interface AnimationProps {
  onStart?: (result: AnimationResult) => void
  onChange?: (result: AnimationResult) => void
  onRest?: (result: AnimationResult) => void
  onPause?: () => void
  onResume?: () => void
}
```

**Global Events:**
```jsx
useSpring({
  x: 100,
  onStart: () => console.log('Animation started'),
  onRest: () => console.log('Animation completed')
})
```

**Key-Specific Events:**
```jsx
useSpring({
  x: 100,
  y: 200,
  onStart: {
    x: () => console.log('x started'),
    y: () => console.log('y started')
  }
})
```

---

## Globals

Global configuration for all animations.

**Globals.assign(config):**

```jsx
import { Globals } from '@react-spring/web'

// Skip all animations (accessibility)
Globals.assign({ skipAnimation: true })

// Custom frame loop
Globals.assign({ frameLoop: 'always' }) // or 'demand'

// Custom performance now
Globals.assign({ now: () => performance.now() })
```

**Common Use Cases:**

```jsx
// Prefers reduced motion
useEffect(() => {
  const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
  Globals.assign({ skipAnimation: mediaQuery.matches })
}, [])

// Testing mode
if (process.env.NODE_ENV === 'test') {
  Globals.assign({ skipAnimation: true })
}
```

---

## Advanced Patterns

### Chaining Animations

```jsx
const springs = useSpring({
  from: { x: 0, background: '#ff6d6d' },
  to: [
    { x: 100, background: '#fff59a' },
    { x: 0, background: '#88DFAB' }
  ],
  loop: true
})
```

### Async to Function

```jsx
const springs = useSpring({
  from: { x: 0 },
  to: async (next) => {
    await next({ x: 100 })
    await next({ x: 50 })
    await next({ x: 0 })
  }
})
```

### Conditional Animation

```jsx
const [springs, api] = useSpring(() => ({
  x: 0
}), [])

useEffect(() => {
  if (condition) {
    api.start({ x: 100 })
  } else {
    api.start({ x: 0 })
  }
}, [condition])
```

### Interpolation

```jsx
<animated.div
  style={{
    transform: springs.x.to({
      range: [0, 0.5, 1],
      output: ['translateX(0px)', 'translateX(50px)', 'translateX(100px)']
    })
  }}
/>
```

---

## Performance Tips

1. **Use function config for imperative control** - Avoids recreation on render
2. **Set appropriate precision** - Higher values reduce updates
3. **Batch similar animations** - Use `useSprings` for multiple similar items
4. **Skip animations in tests** - Use `Globals.assign({ skipAnimation: true })`
5. **Avoid animating layout** - Prefer transforms and opacity
6. **Use `immediate` for instant changes** - `api.start({ x: 100, immediate: true })`

---

## TypeScript Support

React Spring is fully typed. Key interfaces:

```typescript
import type {
  SpringValue,
  SpringValues,
  SpringRef,
  SpringConfig,
  AnimationResult
} from '@react-spring/web'
```

**Typing Custom Animations:**
```typescript
interface MySpringValues {
  x: number
  opacity: number
  color: string
}

const springs = useSpring<MySpringValues>({
  from: { x: 0, opacity: 0, color: '#fff' },
  to: { x: 100, opacity: 1, color: '#000' }
})
```
