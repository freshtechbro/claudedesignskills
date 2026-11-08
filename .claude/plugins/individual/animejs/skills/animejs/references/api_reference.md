# Anime.js API Reference

Complete API documentation for Anime.js v3+.

## Table of Contents

- [anime() Function](#anime-function)
- [Targets](#targets)
- [Properties](#properties)
- [Property Parameters](#property-parameters)
- [Animation Parameters](#animation-parameters)
- [Timeline](#timeline)
- [Stagger](#stagger)
- [Easing Functions](#easing-functions)
- [Helpers](#helpers)
- [Callbacks](#callbacks)

---

## anime() Function

Main function to create animations.

```javascript
anime(options)
```

**Returns:** Animation instance with playback controls.

---

## Targets

Specify what to animate.

**CSS Selector:**
```javascript
targets: '.element'
targets: '#myId'
targets: 'div.className'
```

**DOM Element/NodeList:**
```javascript
targets: document.querySelector('.element')
targets: document.querySelectorAll('.elements')
```

**JavaScript Object:**
```javascript
const obj = { prop: 0 }
anime({ targets: obj, prop: 100 })
```

**Array:**
```javascript
targets: [el1, el2, el3]
targets: [obj1, obj2]
```

---

## Properties

### CSS Properties

**Transform (individual):**
```javascript
translateX: 250         // pixels
translateY: '10em'     // units
translateZ: '50vh'
rotate: '1turn'        // turns, deg, rad
rotateX, rotateY, rotateZ
scale: 2
scaleX, scaleY, scaleZ
skew: '10deg'
skewX, skewY
perspective: 1000
```

**Other CSS:**
```javascript
opacity: 0.5
backgroundColor: '#FFF'  // colors
borderRadius: '50%'
width: '100px'
left: '50%'
// Any valid CSS property (camelCase)
```

### SVG Attributes

```javascript
d: 'M10 80 Q 77.5 10, 145 80'  // Path morphing
points: '64 68 8 400 ...'       // Polygon points
strokeDashoffset: 100
fill: '#FF0000'
r: 50                           // Circle radius
cx, cy                          // Circle center
// Any SVG attribute
```

### DOM Attributes

```javascript
value: 100              // Input value
volume: 0.5            // Audio/video
textContent: 'Hello'   // Text content
innerHTML: '<div></div>'
// Any DOM attribute
```

### JavaScript Object Properties

```javascript
const obj = { x: 0, y: 0 }
anime({
  targets: obj,
  x: 100,
  y: 200
})
```

---

## Property Parameters

Define how each property animates.

### Value Formats

**Single Value:**
```javascript
translateX: 250  // Animate from current to 250
```

**From-To Array:**
```javascript
translateX: [0, 250]  // Explicit from/to
opacity: [0, 1]
```

**Function-Based:**
```javascript
translateX: (el, i) => 50 + (i * 50)  // Different per element
delay: (el, i, total) => i * 100
```

**Keyframes:**
```javascript
translateX: [
  { value: 100, duration: 500 },
  { value: 200, duration: 500 },
  { value: 0, duration: 500 }
]
```

### Units

```javascript
'250px'      // Pixels
'10em'       // Ems
'50%'        // Percentage
'100vh'      // Viewport
'1turn'      // Turns
'45deg'      // Degrees
'1.5rad'     // Radians
```

### Relative Values

```javascript
translateX: '+=250'   // Add 250 to current
translateX: '-=100'   // Subtract 100
translateX: '*=2'     // Multiply by 2
```

### Colors

```javascript
'#FF0000'               // Hex
'rgb(255, 0, 0)'       // RGB
'rgba(255, 0, 0, 0.5)' // RGBA
'hsl(0, 100%, 50%)'    // HSL
```

---

## Animation Parameters

Global animation settings.

```javascript
anime({
  targets: '.element',
  translateX: 250,

  // Timing
  duration: 1000,              // Milliseconds
  delay: 500,                  // Start delay
  endDelay: 200,               // End delay

  // Easing
  easing: 'easeInOutQuad',     // Built-in easing

  // Playback
  direction: 'normal',         // 'normal', 'reverse', 'alternate'
  loop: 3,                     // Number or true for infinite
  autoplay: true,              // Auto-start

  // Advanced
  round: 1,                    // Round values to 1 decimal
  specific Property Parameters
  specificProperty: {
    value: 100,
    duration: 2000,
    delay: 500,
    easing: 'linear'
  }
})
```

---

## Timeline

Chain multiple animations with precise control.

### Create Timeline

```javascript
const tl = anime.timeline({
  duration: 1000,
  easing: 'easeOutExpo',
  loop: true
})
```

### Add Animations

```javascript
tl.add({
  targets: '.el1',
  translateX: 250
})
.add({
  targets: '.el2',
  translateX: 250
}, '-=500')  // Offset
```

### Timeline Parameters

All animation parameters plus:

```javascript
anime.timeline({
  duration: 1000,        // Default duration
  delay: 500,            // Default delay
  easing: 'linear',      // Default easing
  direction: 'normal',
  loop: false,
  autoplay: true
})
```

### Offset

Control when animations start:

```javascript
'+=500'   // Start 500ms after previous ends
'-=500'   // Start 500ms before previous ends
500       // Start at absolute time 500ms
```

### Timeline Methods

```javascript
tl.play()
tl.pause()
tl.restart()
tl.reverse()
tl.seek(1000)          // Seek to 1000ms
tl.add(animation)      // Add animation
```

---

## Stagger

Distribute delays across multiple elements.

### Basic Stagger

```javascript
delay: anime.stagger(100)  // Increment by 100ms
```

### Stagger Options

```javascript
delay: anime.stagger(100, {
  start: 500,              // Start delay
  from: 'center',          // 'first', 'last', 'center', index, [x, y]
  direction: 'normal',     // 'normal', 'reverse'
  easing: 'easeOutQuad',   // Easing for delay
  grid: [10, 10],          // Grid dimensions
  axis: 'x'                // 'x', 'y', null
})
```

### Stagger Values

```javascript
// Stagger delays
delay: anime.stagger(100)

// Stagger values
translateX: anime.stagger([0, 100, 200, 300])

// Stagger ranges
scale: anime.stagger([1, 2], { from: 'center' })
```

### Grid Stagger

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

---

## Easing Functions

### Built-in Easings

**Linear:**
```javascript
'linear'
```

**Ease In/Out:**
```javascript
'easeInQuad', 'easeOutQuad', 'easeInOutQuad'
'easeInCubic', 'easeOutCubic', 'easeInOutCubic'
'easeInQuart', 'easeOutQuart', 'easeInOutQuart'
'easeInQuint', 'easeOutQuint', 'easeInOutQuint'
'easeInSine', 'easeOutSine', 'easeInOutSine'
'easeInExpo', 'easeOutExpo', 'easeInOutExpo'
'easeInCirc', 'easeOutCirc', 'easeInOutCirc'
'easeInBack', 'easeOutBack', 'easeInOutBack'
'easeInElastic', 'easeOutElastic', 'easeInOutElastic'
'easeInBounce', 'easeOutBounce', 'easeInOutBounce'
```

### Custom Easings

**Cubic Bezier:**
```javascript
easing: 'cubicBezier(.5, .05, .1, .3)'
```

**Spring Physics:**
```javascript
easing: 'spring(1, 80, 10, 0)'
// mass, stiffness, damping, velocity
```

**Steps:**
```javascript
easing: 'steps(5)'  // 5 steps
```

**Linear Keyframes:**
```javascript
easing: 'linear(0, 0.5, 1)'
```

---

## Helpers

### anime.setDashoffset(el)

Calculate strokeDashoffset for line drawing:

```javascript
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0]
})
```

### anime.path(path)

Get coordinates and angle from SVG path:

```javascript
const path = anime.path('#motion-path')

anime({
  targets: '.element',
  translateX: path('x'),
  translateY: path('y'),
  rotate: path('angle')
})
```

### anime.random(min, max)

Generate random value:

```javascript
translateX: () => anime.random(0, 100)
```

### anime.get(targets, prop)

Get current value:

```javascript
const currentX = anime.get('.element', 'translateX')
```

### anime.set(targets, prop)

Set value without animating:

```javascript
anime.set('.element', { translateX: 100, opacity: 0.5 })
```

---

## Callbacks

### Animation Callbacks

```javascript
anime({
  targets: '.element',
  translateX: 250,

  begin: (anim) => {
    console.log('Animation begins')
  },

  update: (anim) => {
    console.log('Animation updates', anim.progress)
  },

  complete: (anim) => {
    console.log('Animation completes')
  },

  loopBegin: (anim) => {
    console.log('Loop begins')
  },

  loopComplete: (anim) => {
    console.log('Loop completes')
  },

  changeBegin: (anim) => {
    console.log('Direction changes')
  },

  changeComplete: (anim) => {
    console.log('Direction change completes')
  }
})
```

### Callback Parameters

**anim Object:**
```javascript
anim.progress      // Animation progress (0-100)
anim.currentTime   // Current time (ms)
anim.duration      // Total duration (ms)
anim.remaining     // Remaining loops
anim.reversed      // Direction reversed?
anim.paused        // Animation paused?
anim.began         // Animation began?
anim.finished      // Animation finished?
```

---

## Animation Instance

### Properties

```javascript
const animation = anime({ ... })

animation.progress      // 0-100
animation.currentTime   // Milliseconds
animation.duration      // Milliseconds
animation.remaining     // Remaining loops
animation.reversed      // Boolean
animation.paused        // Boolean
animation.began         // Boolean
animation.finished      // Boolean
animation.animatables   // Array of targets
animation.animations    // Array of property animations
```

### Methods

```javascript
animation.play()
animation.pause()
animation.restart()
animation.reverse()
animation.seek(time)       // Seek to time (ms or %)
animation.tick(time)       // Manual tick
```

---

## Examples

### Basic Animation

```javascript
anime({
  targets: '.box',
  translateX: 250,
  rotate: '1turn',
  duration: 800,
  easing: 'easeInOutQuad'
})
```

### From-To Animation

```javascript
anime({
  targets: '.element',
  translateX: [0, 250],
  opacity: [0, 1],
  duration: 1000
})
```

### Keyframe Animation

```javascript
anime({
  targets: '.element',
  keyframes: [
    { translateX: 100 },
    { translateY: 100 },
    { translateX: 0 },
    { translateY: 0 }
  ],
  duration: 4000,
  loop: true
})
```

### Timeline Animation

```javascript
const tl = anime.timeline()

tl.add({
  targets: '.box1',
  translateX: 250
})
.add({
  targets: '.box2',
  translateX: 250
}, '-=500')
```

### Stagger Animation

```javascript
anime({
  targets: '.stagger-item',
  translateY: [-50, 0],
  opacity: [0, 1],
  delay: anime.stagger(100, { from: 'center' })
})
```

### SVG Path Animation

```javascript
anime({
  targets: '#morphing-path',
  d: 'M10 80 Q 77.5 150, 145 80',
  duration: 2000,
  easing: 'easeInOutQuad'
})
```

### JavaScript Object Animation

```javascript
const obj = { count: 0 }

anime({
  targets: obj,
  count: 100,
  round: 1,
  update: () => {
    document.querySelector('.counter').textContent = obj.count
  }
})
```
