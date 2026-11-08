# Anime.js Stagger Guide

Complete guide to Anime.js stagger utilities for creating sequential and coordinated animations.

## Overview

Stagger distributes animation delays across multiple elements, creating cascading or wave-like effects. Anime.js provides powerful stagger options including grid-based staggering, directional control, and custom easing.

## Basic Stagger

### Time-Based Stagger

```javascript
anime({
  targets: '.element',
  translateX: 250,
  delay: anime.stagger(100) // Increment delay by 100ms
})
```

**Result:** Each element animates 100ms after the previous one.

### Value-Based Stagger

```javascript
anime({
  targets: '.element',
  translateX: anime.stagger([0, 100, 200, 300])
})
```

**Result:** Each element animates to a different translateX value.

## Stagger Options

### Complete Syntax

```javascript
anime.stagger(value, {
  start: 0,              // Starting delay (ms)
  from: 'first',         // Starting point
  direction: 'normal',   // Direction of stagger
  easing: 'linear',      // Easing for stagger progression
  grid: [rows, cols],    // Grid dimensions
  axis: null             // Grid axis ('x', 'y', or null)
})
```

---

## Stagger From

Control where the stagger starts.

### from: 'first' (default)

Start from the first element:

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, { from: 'first' })
})
```

### from: 'last'

Start from the last element:

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, { from: 'last' })
})
```

### from: 'center'

Start from the center and expand outward:

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, { from: 'center' })
})
```

### from: index

Start from a specific index:

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, { from: 5 }) // Start from 6th element (0-indexed)
})
```

### from: [x, y]

Start from specific grid coordinates:

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [10, 10],
    from: [5, 5] // Start from center of grid
  })
})
```

---

## Grid Stagger

Stagger elements arranged in a grid pattern.

### Basic Grid

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [14, 5] // 14 columns, 5 rows
  })
})
```

### Grid with from: 'center'

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [14, 5],
    from: 'center'
  })
})
```

**Result:** Animates from center outward in all directions.

### Grid with Axis

Control which axis dominates the stagger:

```javascript
// Horizontal waves
anime({
  targets: '.grid-item',
  translateY: [-20, 0],
  delay: anime.stagger(30, {
    grid: [10, 10],
    from: 'center',
    axis: 'x' // Stagger primarily along x-axis
  })
})

// Vertical waves
anime({
  targets: '.grid-item',
  translateY: [-20, 0],
  delay: anime.stagger(30, {
    grid: [10, 10],
    from: 'center',
    axis: 'y' // Stagger primarily along y-axis
  })
})
```

---

## Stagger Direction

### direction: 'normal' (default)

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, { direction: 'normal' })
})
```

### direction: 'reverse'

Reverse the stagger order:

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, {
    from: 'first',
    direction: 'reverse' // Last to first
  })
})
```

---

## Stagger Easing

Apply easing to the stagger progression itself.

```javascript
anime({
  targets: '.element',
  translateY: [-50, 0],
  delay: anime.stagger(100, {
    easing: 'easeOutQuad' // Ease the delay distribution
  })
})
```

**Effect:** Early elements have shorter delays, later elements have longer delays (exponential distribution).

---

## Stagger Start

Add an initial delay before stagger begins.

```javascript
anime({
  targets: '.element',
  scale: [0, 1],
  delay: anime.stagger(100, {
    start: 500 // Wait 500ms before starting stagger
  })
})
```

**Result:**
- Element 1: 500ms delay
- Element 2: 600ms delay
- Element 3: 700ms delay

---

## Common Patterns

### 1. Sequential List Reveal

```javascript
anime({
  targets: '.list-item',
  translateY: [30, 0],
  opacity: [0, 1],
  delay: anime.stagger(80),
  easing: 'easeOutQuad'
})
```

### 2. Grid Expand from Center

```javascript
anime({
  targets: '.grid-square',
  scale: [0, 1],
  delay: anime.stagger(30, {
    grid: [10, 10],
    from: 'center'
  }),
  easing: 'easeOutElastic(1, .8)'
})
```

### 3. Wave Effect

```javascript
anime({
  targets: '.wave-element',
  translateY: [
    { value: -20, duration: 300 },
    { value: 0, duration: 300 }
  ],
  delay: anime.stagger(50),
  loop: true
})
```

### 4. Diagonal Wipe

```javascript
anime({
  targets: '.tile',
  opacity: [0, 1],
  translateX: [-50, 0],
  delay: anime.stagger(20, {
    grid: [10, 10],
    from: [0, 0], // Top-left corner
    axis: null // Both axes
  })
})
```

### 5. Text Character Reveal

```javascript
// Split text into characters first
const textWrapper = document.querySelector('.text')
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>")

anime({
  targets: '.letter',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(30),
  easing: 'easeOutExpo'
})
```

### 6. Circular Stagger

```javascript
anime({
  targets: '.circle-item',
  scale: [0, 1],
  delay: anime.stagger(100, {
    from: 'center',
    easing: 'linear'
  }),
  rotate: anime.stagger([0, 360])
})
```

### 7. Alternating Direction

```javascript
anime({
  targets: '.row',
  translateX: (el, i) => i % 2 === 0 ? [-250, 0] : [250, 0],
  opacity: [0, 1],
  delay: anime.stagger(100)
})
```

---

## Stagger with Different Properties

### Stagger Delays, Same Values

```javascript
anime({
  targets: '.element',
  translateX: 250, // Same for all
  delay: anime.stagger(100) // Different delays
})
```

### Stagger Values, Same Timing

```javascript
anime({
  targets: '.element',
  translateX: anime.stagger([0, 50, 100, 150]), // Different values
  duration: 1000 // Same duration
})
```

### Stagger Both

```javascript
anime({
  targets: '.element',
  translateX: anime.stagger([0, 50, 100, 150]),
  delay: anime.stagger(100)
})
```

---

## Advanced Techniques

### Dynamic Grid Calculation

```javascript
function getGridSize() {
  const elements = document.querySelectorAll('.grid-item')
  const cols = Math.ceil(Math.sqrt(elements.length))
  const rows = Math.ceil(elements.length / cols)
  return [cols, rows]
}

anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: getGridSize(),
    from: 'center'
  })
})
```

### Stagger with Function Values

```javascript
anime({
  targets: '.element',
  translateX: anime.stagger((el, i, total) => {
    // Custom calculation
    return (i / total) * 100
  }),
  delay: anime.stagger(100)
})
```

### Multi-Property Stagger

```javascript
anime({
  targets: '.element',
  translateX: anime.stagger([0, 100]),
  translateY: anime.stagger([0, 50]),
  rotate: anime.stagger([0, 360]),
  delay: anime.stagger(100, { from: 'center' })
})
```

---

## Performance Tips

1. **Use transforms** - Stagger `translateX`, `translateY`, `scale`, `rotate` for GPU acceleration
2. **Limit element count** - Stagger works best with <100 elements
3. **Avoid layout properties** - Don't stagger `width`, `height`, `left`, `top`
4. **Use `will-change`** - Add `will-change: transform` for smoother animations
5. **Batch similar animations** - One stagger for multiple properties is more efficient than separate animations

---

## Common Mistakes

### ❌ Wrong: Stagger on Single Element

```javascript
anime({
  targets: '.single-element', // Only one element
  scale: [0, 1],
  delay: anime.stagger(100) // No effect
})
```

### ✅ Correct: Multiple Elements

```javascript
anime({
  targets: '.multiple-elements', // Multiple elements
  scale: [0, 1],
  delay: anime.stagger(100)
})
```

### ❌ Wrong: Grid Without Dimensions

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    from: 'center' // Missing grid dimensions!
  })
})
```

### ✅ Correct: Grid With Dimensions

```javascript
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, {
    grid: [10, 10],
    from: 'center'
  })
})
```

---

## Debugging Tips

**Log stagger values:**
```javascript
anime({
  targets: '.element',
  translateX: 250,
  delay: anime.stagger(100),
  begin: (anim) => {
    anim.animatables.forEach((animatable, i) => {
      console.log(`Element ${i}: delay ${animatable.delay}ms`)
    })
  }
})
```

**Visualize stagger:**
```javascript
// Add data-index to elements
document.querySelectorAll('.element').forEach((el, i) => {
  el.setAttribute('data-index', i)
})
```

---

## Resources

- Official Stagger Documentation: https://animejs.com/documentation/#stagger
- Grid Stagger Demo: https://codepen.io/juliangarnier/pen/JXaKpP
- Stagger Examples: https://animejs.com/documentation/#staggeringBasics
