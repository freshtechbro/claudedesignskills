---
name: motion-framer
description: Modern animation library for React and JavaScript. Create smooth, production-ready animations with motion components, variants, gestures (hover/tap/drag), layout animations, AnimatePresence exit animations, spring physics, and scroll-based effects. Use when building interactive UI components, micro-interactions, page transitions, or complex animation sequences.
---

# Motion & Framer Motion

## Overview

Motion (formerly Framer Motion) is a production-ready animation library for React and JavaScript that enables declarative, performant animations with minimal code. It provides `motion` components that wrap HTML elements with animation superpowers, supports gesture recognition (hover, tap, drag, focus), and includes advanced features like layout animations, exit animations, and spring physics.

**When to use this skill:**
- Building interactive UI components (buttons, cards, menus)
- Creating micro-interactions and hover effects
- Implementing page transitions and route animations
- Adding scroll-based animations and parallax effects
- Animating layout changes (resizing, reordering, shared element transitions)
- Drag-and-drop interfaces
- Complex animation sequences and state-based animations
- Replacing CSS transitions with more powerful, controllable animations

**Technology:**
- **Motion** (v11+) - The modern, smaller library from Framer Motion creators
- **Framer Motion** - The full-featured predecessor (still widely used)
- React 18+ compatible, also supports Vue
- Supports TypeScript
- Works with Next.js, Vite, Remix, and all modern React frameworks

## Core Concepts

### 1. Motion Components

Convert any HTML/SVG element into an animatable component by prefixing with `motion.`:

```jsx
import { motion } from "framer-motion"

// Regular HTML becomes motion component
<motion.div />
<motion.button />
<motion.svg />
<motion.path />
```

Every motion component accepts animation props like `animate`, `initial`, `transition`, and gesture props like `whileHover`, `whileTap`, etc.

### 2. Animate Prop

The `animate` prop defines the target animation state. When values change, Motion automatically animates to them:

```jsx
// Simple animation - x position changes
<motion.div animate={{ x: 100 }} />

// Multiple properties
<motion.div animate={{ x: 100, opacity: 1, scale: 1.2 }} />

// Animates when state changes
const [isOpen, setIsOpen] = useState(false)
<motion.div animate={{ width: isOpen ? 300 : 100 }} />
```

### 3. Initial State

Set the initial state before animation using the `initial` prop:

```jsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  animate={{ opacity: 1, y: 0 }}
/>
```

Set `initial={false}` to disable initial animations on mount.

### 4. Transitions

Control how animations move between states using the `transition` prop:

```jsx
// Duration-based
<motion.div
  animate={{ x: 100 }}
  transition={{ duration: 0.5, ease: "easeInOut" }}
/>

// Spring physics
<motion.div
  animate={{ scale: 1.2 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
/>

// Different transitions for different properties
<motion.div
  animate={{ x: 100, opacity: 1 }}
  transition={{
    x: { type: "spring", stiffness: 300 },
    opacity: { duration: 0.2 }
  }}
/>
```

**Transition types:**
- `"tween"` (default) - Duration-based with easing
- `"spring"` - Physics-based spring animation
- `"inertia"` - Decelerating animation (used in drag)

### 5. Variants

Organize animation states using named variants for cleaner code and propagation to children:

```jsx
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, scale: 0.9 }
}

<motion.div
  variants={variants}
  initial="hidden"
  animate="visible"
  exit="exit"
/>
```

**Variant propagation** - Children automatically inherit parent variant states:

```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1  // Stagger child animations
    }
  }
}

const itemVariants = {
  hidden: { x: -20, opacity: 0 },
  visible: { x: 0, opacity: 1 }
}

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  <motion.li variants={itemVariants} />
  <motion.li variants={itemVariants} />
  <motion.li variants={itemVariants} />
</motion.ul>
```

## Common Patterns

### 1. Hover Animations

Animate on hover using `whileHover` prop:

```jsx
// Simple hover effect
<motion.button
  whileHover={{ scale: 1.1 }}
  transition={{ duration: 0.2 }}
>
  Hover me
</motion.button>

// Multiple properties
<motion.div
  whileHover={{
    scale: 1.05,
    backgroundColor: "#f0f0f0",
    boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.2)"
  }}
>
  Hover card
</motion.div>

// With custom transition
<motion.button
  whileHover={{
    scale: 1.2,
    transition: { duration: 0.1 }  // Transition for gesture start
  }}
  transition={{ duration: 0.5 }}  // Transition for gesture end
>
  Button
</motion.button>
```

**Hover with nested elements:**

```jsx
<motion.div whileHover="hover" variants={cardVariants}>
  <motion.h3 variants={titleVariants}>Title</motion.h3>
  <motion.img variants={imageVariants} />
</motion.div>
```

### 2. Tap/Press Animations

Animate on tap/press using `whileTap` prop:

```jsx
// Scale down on tap
<motion.button
  whileTap={{ scale: 0.9 }}
>
  Click me
</motion.button>

// Combined hover + tap
<motion.button
  whileHover={{ scale: 1.1 }}
  whileTap={{ scale: 0.95, rotate: 3 }}
>
  Interactive button
</motion.button>

// With variants
const buttonVariants = {
  rest: { scale: 1 },
  hover: { scale: 1.1 },
  pressed: { scale: 0.95 }
}

<motion.button
  variants={buttonVariants}
  initial="rest"
  whileHover="hover"
  whileTap="pressed"
>
  Button
</motion.button>
```

### 3. Drag Interactions

Make elements draggable with the `drag` prop:

```jsx
// Basic dragging (both axes)
<motion.div drag />

// Constrain to axis
<motion.div drag="x" />  // Only horizontal
<motion.div drag="y" />  // Only vertical

// Drag constraints
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
/>

// Drag with parent constraints
<motion.div ref={constraintsRef}>
  <motion.div drag dragConstraints={constraintsRef} />
</motion.div>

// Visual feedback while dragging
<motion.div
  drag
  whileDrag={{
    scale: 1.1,
    boxShadow: "0px 10px 20px rgba(0,0,0,0.2)",
    cursor: "grabbing"
  }}
  dragElastic={0.1}  // Elasticity when dragging outside constraints
  dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
/>
```

**Drag events:**

```jsx
<motion.div
  drag
  onDragStart={(event, info) => console.log(info.point)}
  onDrag={(event, info) => console.log(info.offset)}
  onDragEnd={(event, info) => console.log(info.velocity)}
/>
```

### 4. Exit Animations (AnimatePresence)

Animate components when they're removed from the DOM using `AnimatePresence`:

```jsx
import { AnimatePresence } from "framer-motion"

// Basic exit animation
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

**Key requirements:**
- Component must be direct child of `<AnimatePresence>`
- Must have a unique `key` prop
- Use `exit` prop to define exit animation

**List items with exit animations:**

```jsx
<AnimatePresence>
  {items.map(item => (
    <motion.li
      key={item.id}
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 50 }}
      layout  // Smooth layout shifts
    >
      {item.name}
    </motion.li>
  ))}
</AnimatePresence>
```

**Staggered exit animations:**

```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      when: "beforeChildren",
      staggerChildren: 0.1
    }
  },
  exit: {
    opacity: 0,
    transition: {
      when: "afterChildren",
      staggerChildren: 0.05,
      staggerDirection: -1  // Reverse order
    }
  }
}

<AnimatePresence>
  {show && (
    <motion.div variants={containerVariants} initial="hidden" animate="visible" exit="exit">
      <motion.div variants={itemVariants} />
      <motion.div variants={itemVariants} />
      <motion.div variants={itemVariants} />
    </motion.div>
  )}
</AnimatePresence>
```

### 5. Layout Animations

Automatically animate layout changes (position, size) with the `layout` prop:

```jsx
// Animate all layout changes
<motion.div layout />

// Animate only position changes
<motion.div layout="position" />

// Animate only size changes
<motion.div layout="size" />
```

**Grid layout animation:**

```jsx
const [columns, setColumns] = useState(3)

<motion.div className="grid">
  {items.map(item => (
    <motion.div
      key={item.id}
      layout
      transition={{ layout: { duration: 0.3, ease: "easeInOut" } }}
    />
  ))}
</motion.div>
```

**Shared layout animations (layoutId):**

Connect two different elements for smooth transitions using `layoutId`:

```jsx
// Tab indicator example
<nav>
  {tabs.map(tab => (
    <button key={tab.id} onClick={() => setActive(tab.id)}>
      {tab.label}
      {activeTab === tab.id && (
        <motion.div
          layoutId="underline"
          style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 2 }}
        />
      )}
    </button>
  ))}
</nav>

// Modal opening from thumbnail
<motion.img
  src={thumbnail}
  layoutId="product-image"
  onClick={() => setExpanded(true)}
/>

<AnimatePresence>
  {expanded && (
    <motion.div layoutId="product-image">
      <img src={fullsize} />
    </motion.div>
  )}
</AnimatePresence>
```

### 6. Scroll-Based Animations

Animate elements when they enter the viewport using `whileInView`:

```jsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.8 }}  // once: trigger once, amount: 80% visible
  transition={{ duration: 0.5 }}
>
  Animates when scrolled into view
</motion.div>
```

**Viewport options:**
- `once: true` - Animation triggers only once
- `amount: 0.5` - Percentage of element visible (0-1) or "some" | "all"
- `margin: "-100px"` - Offset viewport boundaries

**Staggered scroll animations:**

```jsx
<motion.ul
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true, amount: 0.3 }}
  variants={{
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    },
    hidden: { opacity: 0 }
  }}
>
  <motion.li variants={itemVariants} />
  <motion.li variants={itemVariants} />
  <motion.li variants={itemVariants} />
</motion.ul>
```

### 7. Spring Animations

Use spring physics for natural, bouncy animations:

```jsx
// Basic spring
<motion.div
  animate={{ scale: 1.2 }}
  transition={{ type: "spring" }}
/>

// Customize spring physics
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: "spring",
    stiffness: 300,  // Higher = faster, snappier (default: 100)
    damping: 20,     // Higher = less bouncy (default: 10)
    mass: 1,         // Higher = more inertia (default: 1)
  }}
/>

// Visual duration (easier spring control)
<motion.div
  animate={{ rotate: 90 }}
  transition={{
    type: "spring",
    visualDuration: 0.5,  // Perceived duration
    bounce: 0.25          // Bounciness (0-1, default: 0.25)
  }}
/>
```

**Spring presets:**
- **Gentle**: `stiffness: 100, damping: 20`
- **Wobbly**: `stiffness: 200, damping: 10`
- **Stiff**: `stiffness: 400, damping: 30`
- **Slow**: `stiffness: 50, damping: 20`

## Gesture Recognition

Motion provides declarative gesture handlers:

### Gesture Props

```jsx
<motion.div
  whileHover={{ scale: 1.1 }}        // Pointer hovers over element
  whileTap={{ scale: 0.9 }}          // Primary pointer presses element
  whileFocus={{ outline: "2px" }}    // Element gains focus
  whileDrag={{ scale: 1.1 }}         // Element is being dragged
  whileInView={{ opacity: 1 }}       // Element is in viewport
/>
```

### Gesture Events

```jsx
<motion.div
  onHoverStart={(event, info) => {}}
  onHoverEnd={(event, info) => {}}
  onTap={(event, info) => {}}
  onTapStart={(event, info) => {}}
  onTapCancel={(event, info) => {}}
  onDragStart={(event, info) => {}}
  onDrag={(event, info) => {}}
  onDragEnd={(event, info) => {}}
  onViewportEnter={(entry) => {}}
  onViewportLeave={(entry) => {}}
/>
```

**Event info objects contain:**
- `point: { x, y }` - Page coordinates
- `offset: { x, y }` - Offset from drag start
- `velocity: { x, y }` - Drag velocity

## Hooks

### useAnimate

Manually control animations with the `useAnimate` hook:

```jsx
import { useAnimate } from "framer-motion"

function Component() {
  const [scope, animate] = useAnimate()

  useEffect(() => {
    // Animate multiple elements
    animate([
      [scope.current, { opacity: 1 }],
      ["li", { x: 0, opacity: 1 }, { delay: stagger(0.1) }],
      [".button", { scale: 1.2 }]
    ])
  }, [])

  return (
    <div ref={scope}>
      <ul>
        <li>Item 1</li>
        <li>Item 2</li>
      </ul>
      <button className="button">Click</button>
    </div>
  )
}
```

**Animation controls:**

```jsx
const controls = animate(element, { x: 100 })
controls.play()
controls.pause()
controls.stop()
controls.speed = 0.5
controls.time = 0  // Seek to start
```

### useSpring

Create spring-animated motion values:

```jsx
import { useSpring } from "framer-motion"

function Component() {
  const x = useSpring(0, { stiffness: 300, damping: 20 })

  return (
    <motion.div style={{ x }}>
      <button onClick={() => x.set(100)}>Move</button>
    </motion.div>
  )
}
```

### useInView

Detect when an element is in viewport:

```jsx
import { useInView } from "framer-motion"

function Component() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.5 })

  return (
    <div ref={ref}>
      {isInView ? "In view!" : "Not in view"}
    </div>
  )
}
```

## Integration Patterns

### With GSAP

Combine Motion for React state-based animations and GSAP for complex timelines:

```jsx
import { motion } from "framer-motion"
import gsap from "gsap"

function Component() {
  const boxRef = useRef()

  const handleClick = () => {
    // Use GSAP for complex timeline
    const tl = gsap.timeline()
    tl.to(boxRef.current, { rotation: 360, duration: 1 })
      .to(boxRef.current, { scale: 1.5, duration: 0.5 })
  }

  return (
    // Use Motion for hover/tap/layout animations
    <motion.div
      ref={boxRef}
      whileHover={{ scale: 1.1 }}
      onClick={handleClick}
    />
  )
}
```

### With React Three Fiber

Animate 3D objects using Motion values:

```jsx
import { motion } from "framer-motion"
import { useFrame } from "@react-three/fiber"

function Box() {
  const x = useMotionValue(0)

  useFrame(() => {
    // Sync Motion value with Three.js position
    meshRef.current.position.x = x.get()
  })

  return (
    <>
      <mesh ref={meshRef}>
        <boxGeometry />
        <meshStandardMaterial />
      </mesh>
      <motion.div
        style={{ x }}
        drag="x"
        dragConstraints={{ left: -5, right: 5 }}
      />
    </>
  )
}
```

### With Form Libraries

Animate form validation states:

```jsx
import { motion, AnimatePresence } from "framer-motion"

function FormField({ error }) {
  return (
    <div>
      <motion.input
        animate={{
          borderColor: error ? "#ff0000" : "#cccccc",
          x: error ? [0, -10, 10, -10, 10, 0] : 0  // Shake animation
        }}
        transition={{ duration: 0.4 }}
      />
      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            style={{ color: "#ff0000" }}
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  )
}
```

## Performance Optimization

### 1. Use Transform Properties

Transform properties (x, y, scale, rotate) are hardware-accelerated:

```jsx
// ✅ Good - Hardware accelerated
<motion.div animate={{ x: 100, scale: 1.2 }} />

// ❌ Avoid - Triggers layout/paint
<motion.div animate={{ left: 100, width: 200 }} />
```

### 2. Individual Transform Properties

Motion supports individual transform properties for cleaner code:

```jsx
// Individual properties (Motion feature)
<motion.div style={{ x: 100, rotate: 45, scale: 1.2 }} />

// Traditional (also supported)
<motion.div style={{ transform: "translateX(100px) rotate(45deg) scale(1.2)" }} />
```

### 3. Reduce Motion for Accessibility

Respect user preferences for reduced motion:

```jsx
import { useReducedMotion } from "framer-motion"

function Component() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ x: 100 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.5 }}
    />
  )
}
```

### 4. Layout Animations Performance

Layout animations can be expensive. Optimize with:

```jsx
// Specify what to animate
<motion.div layout="position" />  // Only position, not size

// Optimize transition
<motion.div
  layout
  transition={{
    layout: { duration: 0.3, ease: "easeOut" }
  }}
/>
```

### 5. Use layoutId Sparingly

`layoutId` creates shared layout animations but tracks elements globally. Use only when needed.

## Common Pitfalls

### 1. Forgetting AnimatePresence for Exit Animations

**Problem:** Exit animations don't work

```jsx
// ❌ Wrong - No AnimatePresence
{show && <motion.div exit={{ opacity: 0 }} />}
```

```jsx
// ✅ Correct - Wrapped in AnimatePresence
<AnimatePresence>
  {show && <motion.div exit={{ opacity: 0 }} />}
</AnimatePresence>
```

### 2. Missing key Prop in Lists

**Problem:** AnimatePresence can't track elements

```jsx
// ❌ Wrong - No key
<AnimatePresence>
  {items.map(item => <motion.div exit={{ opacity: 0 }} />)}
</AnimatePresence>
```

```jsx
// ✅ Correct - Unique keys
<AnimatePresence>
  {items.map(item => (
    <motion.div key={item.id} exit={{ opacity: 0 }} />
  ))}
</AnimatePresence>
```

### 3. Animating Non-Transform Properties

**Problem:** Janky animations, poor performance

```jsx
// ❌ Avoid - Not hardware accelerated
<motion.div animate={{ top: 100, left: 50, width: 200 }} />
```

```jsx
// ✅ Better - Use transforms
<motion.div animate={{ x: 50, y: 100, scaleX: 2 }} />
```

### 4. Overusing Layout Animations

**Problem:** Performance issues with many layout-animated elements

```jsx
// ❌ Too many layout animations
{items.map(item => <motion.div layout>{item}</motion.div>)}
```

```jsx
// ✅ Use layout only where needed, optimize others
{items.map(item => (
  <motion.div
    key={item.id}
    animate={{ opacity: 1 }}  // Cheaper animation
    exit={{ opacity: 0 }}
  />
))}
```

### 5. Not Using Variants for Complex Animations

**Problem:** Duplicated animation code, no child orchestration

```jsx
// ❌ Repetitive
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />
```

```jsx
// ✅ Use variants
const variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

<motion.div variants={variants} initial="hidden" animate="visible" />
<motion.div variants={variants} initial="hidden" animate="visible" />
```

### 6. Incorrect Transition Timing

**Problem:** Transitions don't apply to specific gestures

```jsx
// ❌ Wrong - General transition won't apply to whileHover
<motion.div
  whileHover={{ scale: 1.2 }}
  transition={{ duration: 1 }}  // This applies to animate prop, not whileHover
/>
```

```jsx
// ✅ Correct - Transition in whileHover or separate gesture transition
<motion.div
  whileHover={{
    scale: 1.2,
    transition: { duration: 0.2 }  // Applies to hover start
  }}
  transition={{ duration: 0.5 }}  // Applies to hover end
/>
```

## Resources

### Official Documentation
- [Motion Docs](https://motion.dev/) - Official Motion documentation
- [Framer Motion Docs](https://www.framer.com/motion/) - Framer Motion (legacy)
- [Motion GitHub](https://github.com/framer/motion) - Source code & examples

### Bundled Resources

This skill includes:

**references/**
- `api_reference.md` - Complete Motion API reference
- `variants_patterns.md` - Variant patterns and orchestration
- `gesture_guide.md` - Comprehensive gesture handling guide

**scripts/**
- `animation_generator.py` - Generate Motion component boilerplate
- `variant_builder.py` - Interactive variant configuration tool

**assets/**
- `starter_motion/` - Complete Motion + Vite starter template
- `examples/` - Real-world Motion component patterns

### Community Resources
- [Motion Dev Discord](https://discord.gg/motion) - Official community
- [Framer Motion Examples](https://www.framer.com/motion/examples/) - Interactive examples
- [Motion Recipes](https://motion.dev/docs/recipes) - Common patterns
- [CodeSandbox Templates](https://codesandbox.io/s/framer-motion-examples) - Live demos
