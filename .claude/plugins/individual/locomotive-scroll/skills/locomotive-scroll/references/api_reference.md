# Locomotive Scroll API Reference

Complete API documentation for Locomotive Scroll.

## Table of Contents

- [Constructor Options](#constructor-options)
- [Data Attributes](#data-attributes)
- [Instance Methods](#instance-methods)
- [Events](#events)
- [Properties](#properties)

## Constructor Options

```javascript
new LocomotiveScroll(options)
```

### Global Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `el` | HTMLElement | `document` | Scroll container element |
| `name` | string | `'scroll'` | Data attribute prefix |
| `offset` | array | `[0, 0]` | Global offset `[bottom, top]` in px or % |
| `repeat` | boolean | `false` | Repeat in-view detection |
| `smooth` | boolean | `false` | Enable smooth scrolling |
| `initPosition` | object | `{x: 0, y: 0}` | Initial scroll position |
| `direction` | string | `'vertical'` | Scroll direction: `'vertical'` or `'horizontal'` |
| `gestureDirection` | string | `'vertical'` | Gesture direction: `'vertical'`, `'horizontal'`, or `'both'` |
| `reloadOnContextChange` | boolean | `false` | Reload on window resize |
| `lerp` | number | `0.1` | Linear interpolation amount (0-1, lower = smoother) |
| `class` | string | `'is-inview'` | Class applied to in-view elements |
| `scrollbarContainer` | HTMLElement/boolean | `false` | Custom scrollbar container or `false` to hide |
| `scrollbarClass` | string | `'c-scrollbar'` | Custom scrollbar class |
| `scrollingClass` | string | `'has-scroll-scrolling'` | Class added while scrolling |
| `draggingClass` | string | `'has-scroll-dragging'` | Class added while dragging scrollbar |
| `smoothClass` | string | `'has-scroll-smooth'` | Class added when smooth enabled |
| `initClass` | string | `'has-scroll-init'` | Class added on init |
| `getSpeed` | boolean | `false` | Add scroll speed to event |
| `getDirection` | boolean | `false` | Add scroll direction to event |
| `scrollFromAnywhere` | boolean | `false` | Trigger smooth scroll from anywhere |
| `multiplier` | number | `1` | Scroll speed multiplier |
| `firefoxMultiplier` | number | `50` | Firefox-specific multiplier |
| `touchMultiplier` | number | `2` | Touch scroll multiplier |
| `resetNativeScroll` | boolean | `true` | Reset scroll on refresh |

### Mobile/Tablet Options

```javascript
{
  tablet: {
    smooth: boolean,
    direction: string,
    gestureDirection: string,
    breakpoint: number  // Default: 1024
  },
  smartphone: {
    smooth: boolean,
    direction: string,
    gestureDirection: string,
    breakpoint: number  // Default: 767
  }
}
```

**Example**:
```javascript
new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  tablet: {
    smooth: true,
    breakpoint: 1024
  },
  smartphone: {
    smooth: false,
    breakpoint: 768
  }
});
```

## Data Attributes

### Container Attributes

| Attribute | Description |
|-----------|-------------|
| `data-scroll-container` | Main scroll container (required) |
| `data-scroll-section` | Section wrapper for performance optimization |

**Example**:
```html
<div data-scroll-container>
  <div data-scroll-section>
    <!-- Content -->
  </div>
</div>
```

### Element Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `data-scroll` | - | Mark element for detection |
| `data-scroll-id` | string | Unique identifier for element |
| `data-scroll-class` | string | Custom class when in view |
| `data-scroll-offset` | string | Element-specific offset (px or %) |
| `data-scroll-repeat` | boolean | Repeat in-view detection |
| `data-scroll-call` | string | Function to call when in view |
| `data-scroll-speed` | number | Parallax speed multiplier |
| `data-scroll-direction` | string | Parallax direction: `'vertical'` or `'horizontal'` |
| `data-scroll-delay` | number | Parallax delay (0-1) |
| `data-scroll-position` | string | When to start parallax: `'top'`, `'bottom'`, `'left'`, `'right'` |
| `data-scroll-target` | string | Target element selector for position reference |
| `data-scroll-sticky` | - | Enable sticky positioning |

### Detailed Attribute Explanations

#### `data-scroll-speed`

Controls parallax intensity:
- **Positive values**: Element moves faster than scroll
- **Negative values**: Element moves in opposite direction
- **0-1**: Element moves slower than scroll
- **> 1**: Element moves faster than scroll

```html
<!-- Background layer (slow) -->
<div data-scroll data-scroll-speed="0.5">Slow</div>

<!-- Normal speed -->
<div data-scroll data-scroll-speed="1">Normal</div>

<!-- Foreground layer (fast) -->
<div data-scroll data-scroll-speed="3">Fast</div>

<!-- Reverse -->
<div data-scroll data-scroll-speed="-2">Reverse</div>
```

#### `data-scroll-direction`

Axis for parallax effect:

```html
<!-- Vertical parallax (default) -->
<div data-scroll data-scroll-speed="2" data-scroll-direction="vertical">V</div>

<!-- Horizontal parallax -->
<div data-scroll data-scroll-speed="2" data-scroll-direction="horizontal">H</div>
```

#### `data-scroll-offset`

Custom trigger point:

```html
<!-- Trigger when element is 20% from bottom -->
<div data-scroll data-scroll-offset="20%">Offset %</div>

<!-- Trigger 100px from bottom -->
<div data-scroll data-scroll-offset="100">Offset px</div>

<!-- Different bottom/top offsets -->
<div data-scroll data-scroll-offset="10%,30%">Custom offsets</div>
```

#### `data-scroll-sticky`

Pin element within boundaries:

```html
<!-- Sticky within section -->
<div data-scroll-section>
  <div data-scroll data-scroll-sticky>
    Sticks within section
  </div>
</div>

<!-- Sticky with custom target -->
<div id="container">
  <div data-scroll data-scroll-sticky data-scroll-target="#container">
    Sticks within #container
  </div>
</div>
```

#### `data-scroll-call`

Trigger callback when in view:

```html
<div data-scroll data-scroll-call="myFunction">
  Triggers 'myFunction' when visible
</div>
```

```javascript
scroll.on('call', (func, way, obj) => {
  if (func === 'myFunction') {
    console.log('Element is', way); // 'enter' or 'exit'
  }
});
```

#### `data-scroll-repeat`

Re-trigger detection on each scroll:

```html
<!-- Fires once (default) -->
<div data-scroll>Fires once</div>

<!-- Fires every time -->
<div data-scroll data-scroll-repeat>Fires repeatedly</div>
```

## Instance Methods

### `init()`

Reinitialize scroll instance.

```javascript
scroll.init();
```

### `update()`

Recalculate element positions. Call after DOM changes.

```javascript
// After adding content
addContent();
scroll.update();
```

### `destroy()`

Remove event listeners and clean up. Essential for SPAs.

```javascript
scroll.destroy();
```

### `start()`

Resume scrolling after `stop()`.

```javascript
scroll.start();
```

### `stop()`

Pause scrolling (disable smooth scroll).

```javascript
scroll.stop();
```

### `scrollTo(target, options)`

Programmatically scroll to target.

**Parameters**:
- `target`: Can be:
  - `'top'` - Scroll to top
  - `'bottom'` - Scroll to bottom
  - `number` - Pixel value
  - `string` - CSS selector
  - `HTMLElement` - DOM element

- `options` (optional):
  ```javascript
  {
    offset: number,           // Offset in pixels (default: 0)
    callback: function,       // Callback after scroll
    duration: number,         // Duration in ms (default: 1000)
    easing: [n,n,n,n],       // Cubic bezier array (default: [0.25, 0.00, 0.35, 1.00])
    disableLerp: boolean,    // Disable smooth lerp (default: false)
    onComplete: function     // Same as callback
  }
  ```

**Examples**:
```javascript
// Scroll to top
scroll.scrollTo('top');

// Scroll to element
scroll.scrollTo('#section');

// Scroll to pixel value
scroll.scrollTo(500);

// Scroll with options
scroll.scrollTo('#section', {
  offset: -100,
  duration: 2000,
  easing: [0.25, 0.0, 0.35, 1.0],
  callback: () => console.log('Done!')
});

// Instant scroll (no smooth)
scroll.scrollTo('#section', {
  disableLerp: true
});
```

### `setScroll(x, y)`

Set scroll position instantly without animation.

```javascript
scroll.setScroll(0, 500); // x, y
```

### `on(event, callback)`

Add event listener.

```javascript
scroll.on('scroll', (args) => {
  console.log(args);
});
```

### `off(event, callback)`

Remove event listener.

```javascript
const handler = (args) => console.log(args);
scroll.on('scroll', handler);
scroll.off('scroll', handler);
```

## Events

### `scroll`

Fires on scroll. Receives object with:

```javascript
scroll.on('scroll', (args) => {
  // Scroll position
  console.log(args.scroll.x);     // Horizontal scroll
  console.log(args.scroll.y);     // Vertical scroll

  // Scroll limits
  console.log(args.limit.x);      // Max horizontal scroll
  console.log(args.limit.y);      // Max vertical scroll

  // Speed (if getSpeed: true)
  console.log(args.speed);

  // Direction (if getDirection: true)
  console.log(args.direction);    // 'up', 'down', 'left', 'right'

  // Current in-view elements
  console.log(args.currentElements);

  // Access specific element
  if (args.currentElements['hero']) {
    const el = args.currentElements['hero'];
    console.log(el.progress);  // 0 to 1
    console.log(el.el);        // DOM element
    console.log(el.id);        // data-scroll-id value
  }
});
```

**currentElements structure**:
```javascript
{
  'element-id': {
    el: HTMLElement,      // DOM element
    id: string,           // data-scroll-id
    class: string,        // data-scroll-class
    top: number,          // Distance from top
    middle: number,       // Distance from middle
    bottom: number,       // Distance from bottom
    offset: object,       // {top, bottom}
    progress: number,     // 0 to 1
    inView: boolean,      // Is in view
    call: string          // data-scroll-call value
  }
}
```

### `call`

Fires when element with `data-scroll-call` enters/exits viewport.

```javascript
scroll.on('call', (func, way, obj) => {
  console.log(func);  // data-scroll-call value
  console.log(way);   // 'enter' or 'exit'
  console.log(obj);   // {el, id}
});
```

**Example**:
```html
<div data-scroll data-scroll-call="playVideo">Video</div>
```

```javascript
scroll.on('call', (func, way) => {
  if (func === 'playVideo' && way === 'enter') {
    video.play();
  }
});
```

## Properties

### `scroll.scroll`

Current scroll state:

```javascript
console.log(scroll.scroll);
// {
//   x: 0,      // Horizontal position
//   y: 150     // Vertical position
// }
```

### `scroll.limit`

Max scroll values:

```javascript
console.log(scroll.limit);
// {
//   x: 0,      // Max horizontal
//   y: 2500    // Max vertical
// }
```

### `scroll.speed`

Current scroll speed (if `getSpeed: true`):

```javascript
console.log(scroll.speed); // Number
```

### `scroll.direction`

Current scroll direction (if `getDirection: true`):

```javascript
console.log(scroll.direction); // 'up' | 'down' | 'left' | 'right'
```

## Complete Usage Example

```javascript
import LocomotiveScroll from 'locomotive-scroll';

const scroll = new LocomotiveScroll({
  el: document.querySelector('[data-scroll-container]'),
  smooth: true,
  lerp: 0.05,
  multiplier: 1,
  class: 'is-inview',
  repeat: false,
  offset: ['10%', 0],
  getSpeed: true,
  getDirection: true,
  smartphone: {
    smooth: false,
    breakpoint: 768
  }
});

// Track scroll
scroll.on('scroll', (args) => {
  console.log(args.scroll.y);

  if (args.currentElements['hero']) {
    const progress = args.currentElements['hero'].progress;
    // Sync with animation
  }
});

// Handle call events
scroll.on('call', (func, way) => {
  if (func === 'lazyLoad' && way === 'enter') {
    loadImages();
  }
});

// Update on window resize
window.addEventListener('resize', () => scroll.update());

// Cleanup on unmount
window.addEventListener('beforeunload', () => scroll.destroy());
```
