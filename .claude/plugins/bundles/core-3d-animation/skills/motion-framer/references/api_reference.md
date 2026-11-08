# Motion & Framer Motion - Complete API Reference

Comprehensive API documentation for Motion (v11+) and Framer Motion animation libraries.

## Table of Contents

1. [Motion Component Props](#motion-component-props)
2. [Animation Props](#animation-props)
3. [Gesture Props](#gesture-props)
4. [Layout Props](#layout-props)
5. [Transition Options](#transition-options)
6. [Variants](#variants)
7. [Hooks](#hooks)
8. [AnimatePresence](#animatepresence)
9. [Utilities](#utilities)

---

## Motion Component Props

All motion components (`motion.div`, `motion.button`, etc.) accept these props:

### Core Animation Props

```typescript
interface MotionProps {
  // Animation state
  animate?: AnimationControls | TargetAndTransition | VariantLabels
  initial?: boolean | Target | VariantLabels
  exit?: TargetAndTransition | VariantLabels

  // Transition
  transition?: Transition

  // Variants
  variants?: Variants

  // Style
  style?: MotionStyle

  // Layout
  layout?: boolean | "position" | "size"
  layoutId?: string
  layoutDependency?: any
  layoutScroll?: boolean

  // Gestures
  whileHover?: VariantLabels | TargetAndTransition
  whileTap?: VariantLabels | TargetAndTransition
  whileFocus?: VariantLabels | TargetAndTransition
  whileDrag?: VariantLabels | TargetAndTransition
  whileInView?: VariantLabels | TargetAndTransition

  // Drag
  drag?: boolean | "x" | "y"
  dragConstraints?: Constraints | RefObject<Element>
  dragElastic?: DragElastic
  dragMomentum?: boolean
  dragTransition?: InertiaOptions
  dragPropagation?: boolean
  dragSnapToOrigin?: boolean

  // Viewport
  viewport?: ViewportOptions

  // Events
  onUpdate?: (latest: Target) => void
  onAnimationStart?: (definition: AnimationDefinition) => void
  onAnimationComplete?: (definition: AnimationDefinition) => void

  // Hover events
  onHoverStart?: (event: MouseEvent, info: EventInfo) => void
  onHoverEnd?: (event: MouseEvent, info: EventInfo) => void

  // Tap events
  onTap?: (event: MouseEvent | TouchEvent | PointerEvent, info: TapInfo) => void
  onTapStart?: (event: MouseEvent | TouchEvent | PointerEvent, info: TapInfo) => void
  onTapCancel?: (event: MouseEvent | TouchEvent | PointerEvent, info: TapInfo) => void

  // Focus events
  onFocus?: (event: FocusEvent) => void
  onBlur?: (event: FocusEvent) => void

  // Drag events
  onDragStart?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void
  onDrag?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void
  onDragEnd?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void

  // Viewport events
  onViewportEnter?: (entry: IntersectionObserverEntry | null) => void
  onViewportLeave?: (entry: IntersectionObserverEntry | null) => void

  // Pan events
  onPan?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void
  onPanStart?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void
  onPanEnd?: (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => void
}
```

---

## Animation Props

### animate

Defines the target animation state. Accepts object, variant label, or animation controls.

```typescript
// As object
<motion.div animate={{ x: 100, opacity: 1 }} />

// As variant label
<motion.div animate="visible" />

// As array of variant labels (applied in order)
<motion.div animate={["visible", "active"]} />

// Dynamic based on state
<motion.div animate={isOpen ? "open" : "closed"} />
```

**Type:**
```typescript
animate?: AnimationControls | TargetAndTransition | VariantLabels
```

### initial

Sets the initial state before animation. Set to `false` to disable initial animation.

```typescript
// As object
<motion.div initial={{ opacity: 0, y: 50 }} />

// As variant label
<motion.div initial="hidden" />

// Disable initial animation
<motion.div initial={false} />
```

**Type:**
```typescript
initial?: boolean | Target | VariantLabels
```

### exit

Defines animation when component is removed from DOM. Requires `AnimatePresence`.

```typescript
<AnimatePresence>
  {show && (
    <motion.div
      exit={{ opacity: 0, scale: 0.9 }}
    />
  )}
</AnimatePresence>
```

**Type:**
```typescript
exit?: TargetAndTransition | VariantLabels
```

### style

Motion-specific style prop that supports individual transform properties.

```typescript
<motion.div
  style={{
    x: 100,           // translateX
    y: 50,            // translateY
    scale: 1.2,       // scale
    rotate: 45,       // rotate in degrees
    rotateX: 90,      // 3D rotation
    opacity: 0.5,
    backgroundColor: "#ff0000"
  }}
/>
```

**Transform properties:**
- `x`, `y`, `z` - Translation (px)
- `scale`, `scaleX`, `scaleY` - Scale (unitless)
- `rotate`, `rotateX`, `rotateY`, `rotateZ` - Rotation (deg)
- `skew`, `skewX`, `skewY` - Skew (deg)
- `originX`, `originY`, `originZ` - Transform origin (0-1 or px)
- `perspective` - 3D perspective (px)

---

## Gesture Props

### whileHover

Animation applied while element is hovered.

```typescript
<motion.button
  whileHover={{ scale: 1.1 }}
  // Or with custom transition
  whileHover={{
    scale: 1.2,
    transition: { duration: 0.1 }
  }}
/>
```

**Type:**
```typescript
whileHover?: VariantLabels | TargetAndTransition
```

### whileTap

Animation applied while element is pressed.

```typescript
<motion.button
  whileTap={{ scale: 0.9, rotate: 3 }}
/>
```

**Type:**
```typescript
whileTap?: VariantLabels | TargetAndTransition
```

### whileFocus

Animation applied while element has focus.

```typescript
<motion.input
  whileFocus={{ borderColor: "#0066ff", scale: 1.02 }}
/>
```

**Type:**
```typescript
whileFocus?: VariantLabels | TargetAndTransition
```

### whileDrag

Animation applied while element is being dragged.

```typescript
<motion.div
  drag
  whileDrag={{ scale: 1.1, cursor: "grabbing" }}
/>
```

**Type:**
```typescript
whileDrag?: VariantLabels | TargetAndTransition
```

### whileInView

Animation applied while element is in viewport.

```typescript
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
  viewport={{ once: true, amount: 0.5 }}
/>
```

**Type:**
```typescript
whileInView?: VariantLabels | TargetAndTransition
```

---

## Layout Props

### layout

Enables automatic layout animations for position/size changes.

```typescript
// Animate all layout changes
<motion.div layout />

// Animate only position
<motion.div layout="position" />

// Animate only size
<motion.div layout="size" />
```

**Type:**
```typescript
layout?: boolean | "position" | "size"
```

### layoutId

Creates shared layout animations between different components.

```typescript
// Animated tab indicator
{tabs.map(tab => (
  <div key={tab.id}>
    {tab.label}
    {activeTab === tab.id && (
      <motion.div layoutId="underline" />
    )}
  </div>
))}
```

**Type:**
```typescript
layoutId?: string
```

### layoutDependency

Forces layout animation when this value changes.

```typescript
<motion.div
  layout
  layoutDependency={sortOrder}
/>
```

**Type:**
```typescript
layoutDependency?: any
```

---

## Transition Options

### Transition Interface

```typescript
interface Transition {
  // Duration-based (tween)
  duration?: number
  ease?: Easing | Easing[]
  times?: number[]

  // Spring-based
  type?: "tween" | "spring" | "inertia"
  stiffness?: number
  damping?: number
  mass?: number
  velocity?: number
  restSpeed?: number
  restDelta?: number

  // Visual spring (easier configuration)
  visualDuration?: number
  bounce?: number

  // Timing
  delay?: number
  delayChildren?: number
  staggerChildren?: number
  staggerDirection?: 1 | -1

  // Orchestration
  when?: "beforeChildren" | "afterChildren" | false
  repeat?: number
  repeatType?: "loop" | "reverse" | "mirror"
  repeatDelay?: number

  // Per-property transitions
  [key: string]: any
}
```

### Tween Transitions (Duration-based)

```typescript
<motion.div
  animate={{ x: 100 }}
  transition={{
    duration: 0.5,
    ease: "easeInOut",
    times: [0, 0.5, 1],  // Keyframe times
    delay: 0.2
  }}
/>
```

**Easing options:**
- `"linear"`
- `"easeIn"`, `"easeOut"`, `"easeInOut"`
- `"circIn"`, `"circOut"`, `"circInOut"`
- `"backIn"`, `"backOut"`, `"backInOut"`
- `"anticipate"`
- Custom array: `[0.42, 0, 0.58, 1]` (cubic-bezier)

### Spring Transitions (Physics-based)

```typescript
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: "spring",
    stiffness: 300,   // Higher = faster (default: 100)
    damping: 20,      // Higher = less bouncy (default: 10)
    mass: 1,          // Higher = more inertia (default: 1)
    velocity: 50      // Initial velocity
  }}
/>
```

**Visual spring (simplified):**

```typescript
<motion.div
  animate={{ rotate: 90 }}
  transition={{
    type: "spring",
    visualDuration: 0.5,  // Perceived duration
    bounce: 0.25          // Bounciness (0-1)
  }}
/>
```

### Inertia Transitions (Decelerating)

Used automatically in drag. Can be customized:

```typescript
<motion.div
  drag
  dragTransition={{
    bounceStiffness: 600,
    bounceDamping: 20,
    power: 0.3,
    timeConstant: 200,
    min: 0,
    max: 100
  }}
/>
```

### Orchestration

**Staggering children:**

```typescript
const containerVariants = {
  visible: {
    transition: {
      staggerChildren: 0.1,        // Delay between each child
      delayChildren: 0.2,          // Delay before first child
      staggerDirection: 1,         // 1 = forward, -1 = reverse
      when: "beforeChildren"       // Animate parent before/after children
    }
  }
}
```

**Per-property transitions:**

```typescript
<motion.div
  animate={{ x: 100, opacity: 1 }}
  transition={{
    x: { type: "spring", stiffness: 300 },
    opacity: { duration: 0.2 },
    default: { ease: "linear" }
  }}
/>
```

**Repeating animations:**

```typescript
<motion.div
  animate={{ rotate: 360 }}
  transition={{
    repeat: Infinity,
    repeatType: "loop",     // "loop" | "reverse" | "mirror"
    repeatDelay: 1,
    duration: 2
  }}
/>
```

---

## Variants

Variants are predefined animation states that can be applied to components and their children.

### Variant Definition

```typescript
type Variants = {
  [key: string]: TargetAndTransition
}

// Example
const variants: Variants = {
  hidden: {
    opacity: 0,
    y: 20,
    transition: { duration: 0.3 }
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: 0.1 }
  }
}
```

### Variant Propagation

Children inherit parent variant labels automatically:

```typescript
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { x: -20, opacity: 0 },
  visible: { x: 0, opacity: 1 }
}

<motion.ul variants={container} initial="hidden" animate="visible">
  <motion.li variants={item} />
  <motion.li variants={item} />
  <motion.li variants={item} />
</motion.ul>
```

### Dynamic Variants

Variants can be functions that receive custom data:

```typescript
const variants = {
  visible: (i: number) => ({
    opacity: 1,
    transition: {
      delay: i * 0.1
    }
  })
}

{items.map((item, i) => (
  <motion.div
    key={item.id}
    custom={i}
    variants={variants}
    animate="visible"
  />
))}
```

---

## Hooks

### useAnimate

Manually control animations with imperative API.

```typescript
import { useAnimate, stagger } from "framer-motion"

function Component() {
  const [scope, animate] = useAnimate()

  // Animate single element
  animate(scope.current, { x: 100 })

  // Animate with selector
  animate("li", { opacity: 1 })

  // Sequence of animations
  animate([
    [scope.current, { opacity: 1 }],
    ["li", { x: 0 }, { delay: stagger(0.1) }],
    [".button", { scale: 1.2 }]
  ])

  return <div ref={scope}>...</div>
}
```

**Returns:** `[scope: RefObject, animate: AnimateFunction]`

**AnimationControls methods:**
```typescript
const controls = animate(element, { x: 100 })
controls.play()
controls.pause()
controls.stop()
controls.cancel()
controls.speed = 0.5
controls.time = 0
controls.then(() => console.log("Complete"))
```

### useMotionValue

Create a motion value that can be read, set, and animated.

```typescript
import { useMotionValue } from "framer-motion"

const x = useMotionValue(0)

// Get value
const currentX = x.get()

// Set value
x.set(100)

// Listen to changes
x.on("change", (latest) => console.log(latest))
x.on("animationStart", () => {})
x.on("animationComplete", () => {})

// Use in component
<motion.div style={{ x }} />
```

### useTransform

Transform one motion value into another.

```typescript
import { useMotionValue, useTransform } from "framer-motion"

const x = useMotionValue(0)

// Linear interpolation
const opacity = useTransform(x, [0, 100], [1, 0])

// Custom transform function
const backgroundColor = useTransform(
  x,
  [0, 100],
  ["#ff0000", "#0000ff"]
)

<motion.div style={{ x, opacity, backgroundColor }} />
```

### useSpring

Create spring-animated motion value.

```typescript
import { useSpring, useMotionValue } from "framer-motion"

const x = useMotionValue(0)
const springX = useSpring(x, { stiffness: 300, damping: 20 })

<motion.div style={{ x: springX }} />
```

**Options:**
```typescript
interface SpringOptions {
  stiffness?: number
  damping?: number
  mass?: number
  velocity?: number
  restSpeed?: number
  restDelta?: number
}
```

### useScroll

Track scroll position and velocity.

```typescript
import { useScroll } from "framer-motion"

const { scrollX, scrollY, scrollXProgress, scrollYProgress } = useScroll()

// With element ref
const ref = useRef(null)
const { scrollYProgress } = useScroll({
  target: ref,
  offset: ["start end", "end start"]
})

<motion.div style={{ scaleX: scrollYProgress }} />
```

**Options:**
```typescript
interface ScrollOptions {
  target?: RefObject<Element>
  offset?: ["start" | "end" | string, "start" | "end" | string]
  container?: RefObject<Element>
  layoutEffect?: boolean
}
```

### useInView

Detect when element is in viewport.

```typescript
import { useInView } from "framer-motion"

const ref = useRef(null)
const isInView = useInView(ref, {
  once: true,
  amount: 0.5,
  margin: "-100px"
})

<div ref={ref}>
  {isInView ? "Visible!" : "Not visible"}
</div>
```

**Options:**
```typescript
interface InViewOptions {
  once?: boolean
  amount?: "some" | "all" | number
  margin?: string
  root?: RefObject<Element>
}
```

### useReducedMotion

Detect user's motion preferences.

```typescript
import { useReducedMotion } from "framer-motion"

const shouldReduceMotion = useReducedMotion()

<motion.div
  animate={{ x: 100 }}
  transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.5 }}
/>
```

### useAnimationControls

Create animation controls for imperative animations.

```typescript
import { useAnimationControls } from "framer-motion"

const controls = useAnimationControls()

controls.start({ x: 100 })
controls.stop()
controls.set({ x: 0 })

<motion.div animate={controls} />
```

### usePresence

Detect if component is present (for custom exit animations).

```typescript
import { usePresence } from "framer-motion"

const [isPresent, safeToRemove] = usePresence()

useEffect(() => {
  if (!isPresent) {
    // Perform exit animation
    animate(ref.current, { opacity: 0 }).then(safeToRemove)
  }
}, [isPresent])
```

---

## AnimatePresence

Enables exit animations for removed components.

### Basic Usage

```typescript
import { AnimatePresence } from "framer-motion"

<AnimatePresence>
  {show && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

### Props

```typescript
interface AnimatePresenceProps {
  // Initial animation on first mount
  initial?: boolean

  // Custom data for exit animations
  custom?: any

  // Wait for all exiting animations to complete
  mode?: "wait" | "sync" | "popLayout"

  // Callback when all exit animations complete
  onExitComplete?: () => void

  // Propagate exit to nested AnimatePresence
  propagate?: boolean
}
```

### Mode Options

**"sync"** (default) - Exit and enter animations happen simultaneously:
```typescript
<AnimatePresence mode="sync">
  <Component key={page} />
</AnimatePresence>
```

**"wait"** - Wait for exit animation before starting enter animation:
```typescript
<AnimatePresence mode="wait">
  <Component key={page} />
</AnimatePresence>
```

**"popLayout"** - Exit components render in a separate layer:
```typescript
<AnimatePresence mode="popLayout">
  {items.map(item => (
    <motion.div key={item.id} layout />
  ))}
</AnimatePresence>
```

### Custom Data

Pass data to exiting components that can't receive new props:

```typescript
<AnimatePresence custom={direction}>
  <motion.div
    key={page}
    variants={variants}
    custom={direction}
    exit="exit"
  />
</AnimatePresence>

const variants = {
  exit: (direction) => ({
    x: direction > 0 ? 300 : -300
  })
}
```

---

## Utilities

### stagger

Create staggered delays for child animations.

```typescript
import { stagger } from "framer-motion"

animate("li", { opacity: 1 }, { delay: stagger(0.1) })

// With options
stagger(0.1, {
  startDelay: 0.2,
  from: "first" | "last" | "center" | number,
  ease: "easeInOut"
})
```

### animate (standalone)

Animate any element imperatively.

```typescript
import { animate } from "framer-motion"

// Single element
animate(element, { x: 100 }, { duration: 0.5 })

// Selector
animate(".box", { opacity: 1 })

// Returns controls
const controls = animate(element, { x: 100 })
controls.pause()
```

### transform

Transform values without motion values.

```typescript
import { transform } from "framer-motion"

const output = transform(input, [0, 100], [0, 1])
```

### mix

Mix two values.

```typescript
import { mix } from "framer-motion"

const output = mix(0, 100, 0.5) // 50
```

### clamp

Clamp value between min and max.

```typescript
import { clamp } from "framer-motion"

const output = clamp(0, 100, 150) // 100
```

---

## Event Info Types

### PanInfo (Drag events)

```typescript
interface PanInfo {
  point: Point         // Page coordinates
  delta: Point         // Change since last event
  offset: Point        // Offset from gesture start
  velocity: Point      // Current velocity
}
```

### TapInfo

```typescript
interface TapInfo {
  point: Point         // Page coordinates
}
```

### Point

```typescript
interface Point {
  x: number
  y: number
}
```

---

## TypeScript Support

### Import Types

```typescript
import type {
  TargetAndTransition,
  Transition,
  Variants,
  MotionProps,
  AnimationControls,
  PanInfo,
  TapInfo
} from "framer-motion"
```

### Custom Component with Motion

```typescript
import { motion, HTMLMotionProps } from "framer-motion"

interface Props extends HTMLMotionProps<"div"> {
  customProp: string
}

const CustomComponent = ({ customProp, ...props }: Props) => {
  return <motion.div {...props}>{customProp}</motion.div>
}
```

---

## Performance Tips

1. **Use transform properties** (x, y, scale, rotate) - hardware accelerated
2. **Avoid animating** width, height, top, left, margin, padding
3. **Use `layout` sparingly** - computationally expensive
4. **Use `will-change` CSS** for complex animations
5. **Use `layoutId` only when needed** - tracks elements globally
6. **Reduce motion values** - each creates subscription overhead
7. **Use `useReducedMotion`** - respect accessibility preferences

---

## Common Patterns Quick Reference

```typescript
// Hover effect
<motion.div whileHover={{ scale: 1.1 }} />

// Tap feedback
<motion.button whileTap={{ scale: 0.95 }} />

// Drag
<motion.div drag dragConstraints={{ left: 0, right: 300 }} />

// Fade in on mount
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} />

// Exit animation
<AnimatePresence>
  {show && <motion.div exit={{ opacity: 0 }} />}
</AnimatePresence>

// Layout animation
<motion.div layout />

// Shared layout animation
<motion.div layoutId="shared-element" />

// Scroll-triggered
<motion.div whileInView={{ opacity: 1 }} viewport={{ once: true }} />

// Stagger children
<motion.div variants={container}>
  <motion.div variants={item} />
  <motion.div variants={item} />
</motion.div>

// Spring animation
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 300 }}
/>
```

---

For more detailed examples and use cases, see the main SKILL.md and examples in the assets directory.
