# Anime.js Timeline Guide

Complete guide to creating complex animation sequences with Anime.js timelines.

## Overview

Timelines allow you to chain multiple animations with precise control over timing and sequencing. They provide a declarative way to choreograph complex multi-step animations.

## Creating a Timeline

### Basic Timeline

```javascript
const timeline = anime.timeline()
```

### Timeline with Default Parameters

```javascript
const timeline = anime.timeline({
  duration: 1000,      // Default duration for all animations
  easing: 'easeOutExpo', // Default easing
  loop: false,         // Loop entire timeline
  direction: 'normal',  // 'normal', 'reverse', 'alternate'
  autoplay: true       // Auto-start
})
```

---

## Adding Animations

### .add() Method

```javascript
timeline.add({
  targets: '.element',
  translateX: 250,
  duration: 800
})
```

### Chaining Animations

```javascript
timeline
  .add({
    targets: '.box1',
    translateX: 250
  })
  .add({
    targets: '.box2',
    translateX: 250
  })
  .add({
    targets: '.box3',
    translateX: 250
  })
```

---

## Timeline Offsets

Control when each animation starts relative to the previous one.

### Absolute Time

```javascript
timeline.add({
  targets: '.element',
  translateX: 250
}, 1000) // Start at 1000ms from timeline start
```

### Relative to Previous (+=)

```javascript
timeline
  .add({
    targets: '.box1',
    translateX: 250,
    duration: 1000
  })
  .add({
    targets: '.box2',
    translateX: 250
  }, '+=500') // Start 500ms AFTER box1 completes
```

### Overlap with Previous (-=)

```javascript
timeline
  .add({
    targets: '.box1',
    translateX: 250,
    duration: 1000
  })
  .add({
    targets: '.box2',
    translateX: 250
  }, '-=500') // Start 500ms BEFORE box1 completes (overlap)
```

---

## Common Patterns

### 1. Sequential Animations

Each animation starts after the previous completes:

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.title',
  translateY: [-50, 0],
  opacity: [0, 1]
})
.add({
  targets: '.subtitle',
  translateY: [-30, 0],
  opacity: [0, 1]
})
.add({
  targets: '.button',
  scale: [0, 1]
})
```

### 2. Overlapping Animations

Create smooth transitions between animations:

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.section1',
  opacity: [1, 0],
  duration: 600
})
.add({
  targets: '.section2',
  opacity: [0, 1],
  duration: 600
}, '-=300') // Overlap by 300ms for crossfade
```

### 3. Staggered Timeline

Combine timeline with stagger:

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.card',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(100)
})
.add({
  targets: '.button',
  scale: [0, 1]
}, '-=200')
```

### 4. Multi-Stage Animation

Complex multi-step sequence:

```javascript
const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
})

tl.add({
  targets: '.modal',
  scale: [0, 1],
  opacity: [0, 1]
})
.add({
  targets: '.modal-header',
  translateY: [-20, 0],
  opacity: [0, 1]
}, '-=500')
.add({
  targets: '.modal-body',
  translateY: [20, 0],
  opacity: [0, 1]
}, '-=400')
.add({
  targets: '.modal-footer',
  opacity: [0, 1]
}, '-=300')
```

### 5. Looping Timeline

```javascript
const tl = anime.timeline({
  loop: true,
  direction: 'alternate'
})

tl.add({
  targets: '.ball',
  translateY: -200,
  duration: 1000
})
.add({
  targets: '.ball',
  translateX: 200,
  duration: 1000
})
```

### 6. Loading Sequence

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.loader-bg',
  scaleY: [0, 1],
  duration: 400,
  easing: 'easeInOutQuad'
})
.add({
  targets: '.loader-text',
  opacity: [0, 1],
  translateY: [20, 0],
  duration: 600
}, '-=200')
.add({
  targets: '.loader-spinner',
  rotate: '1turn',
  duration: 800,
  loop: 3
}, '-=400')
.add({
  targets: '.loader',
  opacity: 0,
  duration: 400
}, '+=500')
.add({
  targets: '.content',
  translateY: [50, 0],
  opacity: [0, 1],
  duration: 600
})
```

### 7. Page Transition

```javascript
function pageTransition(oldPage, newPage) {
  const tl = anime.timeline()

  tl.add({
    targets: oldPage,
    translateX: [0, -100],
    opacity: [1, 0],
    duration: 400,
    easing: 'easeInQuad'
  })
  .add({
    targets: newPage,
    translateX: [100, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutQuad'
  }, '-=200')

  return tl
}
```

---

## Timeline Controls

### Playback Methods

```javascript
const tl = anime.timeline({ autoplay: false })

tl.play()       // Play from current position
tl.pause()      // Pause
tl.restart()    // Restart from beginning
tl.reverse()    // Reverse direction
tl.seek(2000)   // Seek to 2000ms
```

### Properties

```javascript
tl.duration      // Total duration
tl.currentTime   // Current time
tl.progress      // Progress (0-100)
tl.reversed      // Is reversed?
tl.paused        // Is paused?
tl.began         // Has begun?
tl.finished      // Is finished?
```

---

## Advanced Techniques

### Labels

Mark specific points in the timeline:

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.intro',
  opacity: [0, 1]
})
.add({}, '+=500') // Add label "intro-done" at this point
.add({
  targets: '.content',
  translateY: [50, 0],
  opacity: [0, 1]
})

// Seek to label
tl.seek('intro-done')
```

### Nested Timelines

```javascript
function createIntroTimeline() {
  const tl = anime.timeline({ autoplay: false })
  tl.add({
    targets: '.logo',
    scale: [0, 1]
  })
  .add({
    targets: '.tagline',
    opacity: [0, 1]
  })
  return tl
}

const mainTimeline = anime.timeline()
mainTimeline.add(createIntroTimeline())
```

### Timeline Callbacks

```javascript
const tl = anime.timeline({
  begin: () => console.log('Timeline begins'),
  update: (tl) => console.log('Progress:', tl.progress),
  complete: () => console.log('Timeline completes')
})
```

### Conditional Timeline

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.element1',
  translateX: 250
})

if (condition) {
  tl.add({
    targets: '.element2',
    opacity: [0, 1]
  })
}

tl.add({
  targets: '.element3',
  scale: [0, 1]
})
```

---

## Timeline vs Individual Animations

### Without Timeline (Hard to Manage)

```javascript
anime({
  targets: '.box1',
  translateX: 250,
  duration: 1000
})

setTimeout(() => {
  anime({
    targets: '.box2',
    translateX: 250,
    duration: 1000
  })
}, 1000)

setTimeout(() => {
  anime({
    targets: '.box3',
    translateX: 250,
    duration: 1000
  })
}, 2000)
```

### With Timeline (Clean & Maintainable)

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.box1',
  translateX: 250,
  duration: 1000
})
.add({
  targets: '.box2',
  translateX: 250,
  duration: 1000
})
.add({
  targets: '.box3',
  translateX: 250,
  duration: 1000
})
```

---

## Performance Optimization

### 1. Use Relative Offsets

```javascript
// ✅ Good: Flexible timing
.add({...}, '-=500')

// ❌ Avoid: Brittle absolute timing
.add({...}, 1500)
```

### 2. Batch Similar Animations

```javascript
// ✅ Good: Single animation
tl.add({
  targets: ['.el1', '.el2', '.el3'],
  translateX: 250
})

// ❌ Avoid: Multiple separate animations
tl.add({ targets: '.el1', translateX: 250 })
  .add({ targets: '.el2', translateX: 250 })
  .add({ targets: '.el3', translateX: 250 })
```

### 3. Set Default Parameters

```javascript
// ✅ Good: DRY
const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 800
})

// ❌ Avoid: Repetition
tl.add({ targets: '.el1', easing: 'easeOutExpo', duration: 800 })
  .add({ targets: '.el2', easing: 'easeOutExpo', duration: 800 })
```

---

## Common Mistakes

### ❌ Wrong: Missing Offset Operator

```javascript
tl.add({
  targets: '.box1',
  translateX: 250
})
.add({
  targets: '.box2',
  translateX: 250
}, '500') // Treated as absolute time!
```

### ✅ Correct: Use Relative Operator

```javascript
tl.add({
  targets: '.box1',
  translateX: 250
})
.add({
  targets: '.box2',
  translateX: 250
}, '+=500') // Relative to previous
```

### ❌ Wrong: Forgetting autoplay: false

```javascript
const tl = anime.timeline() // Starts immediately

// Later...
button.addEventListener('click', () => {
  tl.play() // Already playing!
})
```

### ✅ Correct: Disable autoplay

```javascript
const tl = anime.timeline({ autoplay: false })

button.addEventListener('click', () => {
  tl.play() // Now it works
})
```

---

## Real-World Examples

### Hero Section Animation

```javascript
const heroTimeline = anime.timeline({
  easing: 'easeOutExpo'
})

heroTimeline
  .add({
    targets: '.hero-bg',
    scale: [1.2, 1],
    opacity: [0, 1],
    duration: 1200
  })
  .add({
    targets: '.hero-title',
    translateY: [100, 0],
    opacity: [0, 1],
    duration: 800
  }, '-=800')
  .add({
    targets: '.hero-subtitle',
    translateY: [50, 0],
    opacity: [0, 1],
    duration: 600
  }, '-=400')
  .add({
    targets: '.hero-cta',
    scale: [0, 1],
    duration: 400
  }, '-=200')
```

### Card Flip Animation

```javascript
function flipCard(card) {
  const tl = anime.timeline({ autoplay: false })

  tl.add({
    targets: card.querySelector('.front'),
    rotateY: [0, 90],
    duration: 300,
    easing: 'easeInQuad'
  })
  .add({
    targets: card.querySelector('.back'),
    rotateY: [-90, 0],
    duration: 300,
    easing: 'easeOutQuad'
  }, '-=0')

  return tl
}
```

### Notification Toast

```javascript
function showToast(toast) {
  const tl = anime.timeline()

  tl.add({
    targets: toast,
    translateX: [400, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutBack'
  })
  .add({
    targets: toast,
    opacity: [1, 0],
    duration: 300,
    easing: 'easeInQuad'
  }, '+=3000')

  return tl
}
```

---

## Debugging Timelines

### Log Timeline Progress

```javascript
const tl = anime.timeline({
  update: (tl) => {
    console.log(`Progress: ${tl.progress.toFixed(2)}%`)
    console.log(`Current time: ${tl.currentTime}ms`)
  }
})
```

### Visualize Timeline

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.box1',
  translateX: 250,
  duration: 1000,
  begin: () => console.log('[0ms] Box1 begins'),
  complete: () => console.log('[1000ms] Box1 completes')
})
.add({
  targets: '.box2',
  translateX: 250,
  duration: 1000,
  begin: () => console.log('[1000ms] Box2 begins'),
  complete: () => console.log('[2000ms] Box2 completes')
}, '-=500')
```

---

## Resources

- Official Timeline Documentation: https://animejs.com/documentation/#timeline
- Timeline Examples: https://codepen.io/collection/DxpqGJ/
- Advanced Sequencing: https://animejs.com/documentation/#timelineBasics
