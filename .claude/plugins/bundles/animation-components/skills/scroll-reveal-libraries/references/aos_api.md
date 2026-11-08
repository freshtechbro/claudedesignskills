# AOS API Reference

Complete reference for AOS (Animate On Scroll) configuration, methods, and data attributes.

## Table of Contents

- [Initialization](#initialization)
- [Global Configuration Options](#global-configuration-options)
- [Data Attributes](#data-attributes)
- [JavaScript Methods](#javascript-methods)
- [Events](#events)
- [Easing Functions](#easing-functions)
- [Anchor Placement Values](#anchor-placement-values)
- [Disable Options](#disable-options)

## Initialization

### Basic Initialization

```javascript
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init();
```

### With Configuration

```javascript
AOS.init({
  // Global settings
  duration: 800,
  easing: 'ease-in-out',
  once: true,
  offset: 120
});
```

## Global Configuration Options

All options can be set globally via `AOS.init()` or overridden per-element using data attributes.

### Animation Settings

#### `duration`

- **Type**: `number`
- **Default**: `400`
- **Range**: `0` - `3000`
- **Description**: Animation duration in milliseconds

```javascript
AOS.init({ duration: 800 });
```

```html
<div data-aos="fade-up" data-aos-duration="1000">Content</div>
```

#### `delay`

- **Type**: `number`
- **Default**: `0`
- **Range**: `0` - `3000`
- **Description**: Delay before animation starts (ms)

```javascript
AOS.init({ delay: 100 });
```

```html
<div data-aos="fade-up" data-aos-delay="200">Content</div>
```

#### `easing`

- **Type**: `string`
- **Default**: `"ease"`
- **Description**: CSS easing function for animations
- **See**: [Easing Functions](#easing-functions) for all available values

```javascript
AOS.init({ easing: 'ease-in-out' });
```

```html
<div data-aos="fade-up" data-aos-easing="ease-out-cubic">Content</div>
```

### Trigger Settings

#### `offset`

- **Type**: `number`
- **Default**: `120`
- **Description**: Offset (in pixels) from the original trigger point

```javascript
AOS.init({ offset: 200 });
```

```html
<div data-aos="fade-up" data-aos-offset="100">Content</div>
```

#### `anchorPlacement`

- **Type**: `string`
- **Default**: `"top-bottom"`
- **Description**: Defines which position of the element regarding the viewport should trigger the animation
- **See**: [Anchor Placement Values](#anchor-placement-values) for all options

```javascript
AOS.init({ anchorPlacement: 'center-center' });
```

```html
<div data-aos="fade-up" data-aos-anchor-placement="top-center">Content</div>
```

#### `anchor`

- **Type**: `string | null`
- **Default**: `null`
- **Description**: CSS selector of element whose scroll position will be used to trigger animation

```html
<div id="trigger-element">Scroll past this...</div>
<div data-aos="fade-up" data-aos-anchor="#trigger-element">Animates when trigger scrolls</div>
```

### Behavior Settings

#### `once`

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Whether animation should happen only once - while scrolling down

```javascript
AOS.init({ once: true });
```

```html
<div data-aos="fade-up" data-aos-once="true">Content</div>
```

#### `mirror`

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Whether elements should animate out while scrolling past them

```javascript
AOS.init({ mirror: true });
```

```html
<div data-aos="fade-up" data-aos-mirror="true">Content</div>
```

### Device Settings

#### `disable`

- **Type**: `boolean | string | function`
- **Default**: `false`
- **Description**: Condition when AOS should be disabled
- **See**: [Disable Options](#disable-options) for details

```javascript
// Disable on mobile
AOS.init({ disable: 'mobile' });

// Disable with function
AOS.init({
  disable: function() {
    return window.innerWidth < 768;
  }
});
```

### Performance Settings

#### `startEvent`

- **Type**: `string`
- **Default**: `"DOMContentLoaded"`
- **Values**: `"DOMContentLoaded"`, `"load"`
- **Description**: Name of the event dispatched on the document, that AOS should initialize on

```javascript
AOS.init({ startEvent: 'load' });
```

#### `throttleDelay`

- **Type**: `number`
- **Default**: `99`
- **Description**: The delay on throttle used while scrolling (in ms)

```javascript
AOS.init({ throttleDelay: 120 });
```

#### `debounceDelay`

- **Type**: `number`
- **Default**: `50`
- **Description**: The delay on debounce used while resizing window (in ms)

```javascript
AOS.init({ debounceDelay: 80 });
```

#### `disableMutationObserver`

- **Type**: `boolean`
- **Default**: `false`
- **Description**: Disables automatic mutations' detections (advanced)

```javascript
AOS.init({ disableMutationObserver: true });
```

## Data Attributes

All configuration options can be set per-element using data attributes:

### `data-aos`

**Required**. Specifies the animation type.

```html
<div data-aos="fade-up">Content</div>
```

See Animation Catalog for all available animations.

### `data-aos-duration`

Animation duration (overrides global `duration`)

```html
<div data-aos="fade-up" data-aos-duration="1000">Content</div>
```

### `data-aos-delay`

Animation delay (overrides global `delay`)

```html
<div data-aos="fade-up" data-aos-delay="500">Content</div>
```

### `data-aos-easing`

Animation easing (overrides global `easing`)

```html
<div data-aos="fade-up" data-aos-easing="ease-in-cubic">Content</div>
```

### `data-aos-offset`

Offset from trigger point (overrides global `offset`)

```html
<div data-aos="fade-up" data-aos-offset="200">Content</div>
```

### `data-aos-anchor`

Element whose offset will be used to trigger animation

```html
<div data-aos="fade-up" data-aos-anchor="#trigger">Content</div>
```

### `data-aos-anchor-placement`

Anchor placement (overrides global `anchorPlacement`)

```html
<div data-aos="fade-up" data-aos-anchor-placement="top-center">Content</div>
```

### `data-aos-once`

Whether to animate only once (overrides global `once`)

```html
<div data-aos="fade-up" data-aos-once="true">Content</div>
```

### `data-aos-mirror`

Whether to animate out (overrides global `mirror`)

```html
<div data-aos="fade-up" data-aos-mirror="true">Content</div>
```

### `data-aos-id`

Optional ID for specific element (used with anchors)

```html
<div data-aos="fade-up" data-aos-id="my-element">Content</div>
```

## JavaScript Methods

### `AOS.init(options)`

Initialize AOS with optional configuration.

```javascript
AOS.init({
  duration: 800,
  once: true
});
```

**Parameters:**
- `options` (Object): Configuration object

**Returns:** `void`

### `AOS.refresh()`

Recalculate all offsets and positions of elements. Should be called after dynamic content changes.

```javascript
// After adding new elements
const newElement = document.createElement('div');
newElement.setAttribute('data-aos', 'fade-in');
container.appendChild(newElement);

AOS.refresh(); // Recalculate positions
```

**Returns:** `void`

### `AOS.refreshHard()`

Reinitialize array with AOS elements and trigger refresh. More comprehensive than `refresh()`.

```javascript
// After major DOM changes
AOS.refreshHard();
```

**Returns:** `void`

## Events

AOS dispatches custom events on animated elements:

### `aos:in`

Fired when element enters the viewport and animation starts.

```javascript
document.addEventListener('aos:in', ({ detail }) => {
  console.log('Animated element:', detail);
});
```

### `aos:out`

Fired when element leaves the viewport (when `mirror: true`).

```javascript
document.addEventListener('aos:out', ({ detail }) => {
  console.log('Animation reversed:', detail);
});
```

### Event Details

Event detail object contains:
- Element reference
- Animation name
- Configuration

```javascript
document.addEventListener('aos:in', ({ detail }) => {
  console.log(detail); // HTMLElement with AOS attributes
});
```

## Easing Functions

Available easing values for `easing` option:

### Standard Easing

- `linear`
- `ease`
- `ease-in`
- `ease-out`
- `ease-in-out`

### Back Easing

- `ease-in-back`
- `ease-out-back`
- `ease-in-out-back`

### Sine Easing

- `ease-in-sine`
- `ease-out-sine`
- `ease-in-out-sine`

### Quad Easing

- `ease-in-quad`
- `ease-out-quad`
- `ease-in-out-quad`

### Cubic Easing

- `ease-in-cubic`
- `ease-out-cubic`
- `ease-in-out-cubic`

### Quart Easing

- `ease-in-quart`
- `ease-out-quart`
- `ease-in-out-quart`

### Usage Example

```javascript
AOS.init({ easing: 'ease-out-cubic' });
```

```html
<div data-aos="fade-up" data-aos-easing="ease-in-out-sine">Content</div>
```

## Anchor Placement Values

Defines which position of element and viewport triggers animation.

Format: `{element-position}-{viewport-position}`

### Element Positions

- `top` - Top edge of element
- `center` - Center of element
- `bottom` - Bottom edge of element

### Viewport Positions

- `top` - Top edge of viewport
- `center` - Center of viewport
- `bottom` - Bottom edge of viewport

### All Combinations

| Value | Description |
|-------|-------------|
| `top-bottom` | Element's top edge hits viewport's bottom edge |
| `top-center` | Element's top edge hits viewport's center |
| `top-top` | Element's top edge hits viewport's top edge |
| `center-bottom` | Element's center hits viewport's bottom edge |
| `center-center` | Element's center hits viewport's center |
| `center-top` | Element's center hits viewport's top edge |
| `bottom-bottom` | Element's bottom edge hits viewport's bottom edge |
| `bottom-center` | Element's bottom edge hits viewport's center |
| `bottom-top` | Element's bottom edge hits viewport's top edge |

### Visual Examples

```
top-bottom (default):
┌─────────────┐
│  Viewport   │
│             │
│             │
│          ┌──┼──┐  ← Element top hits viewport bottom
└──────────┼──┘  │
           │ El  │
           └─────┘

center-center:
┌─────────────┐
│  Viewport   │
│      ┌──────┼────┐  ← Element center hits viewport center
│      │ Elem │    │
│      └──────┼────┘
└─────────────┘

bottom-top:
           ┌─────┐
           │ El  │
┌──────────┼──┐  │  ← Element bottom hits viewport top
│          └──┼──┘
│  Viewport   │
│             │
└─────────────┘
```

### Usage

```html
<!-- Trigger early (when bottom of element reaches top of viewport) -->
<div data-aos="fade-up" data-aos-anchor-placement="bottom-top">
  Content
</div>

<!-- Trigger when centered -->
<div data-aos="fade-up" data-aos-anchor-placement="center-center">
  Content
</div>
```

## Disable Options

The `disable` option controls when AOS is disabled.

### Boolean

```javascript
AOS.init({ disable: false }); // Always enabled
AOS.init({ disable: true });  // Always disabled
```

### String Values

#### `"mobile"`

Disables on mobile devices (phones and tablets).

```javascript
AOS.init({ disable: 'mobile' });
```

Matches: `window.innerWidth < 768 || navigator.userAgent.match(/Mobile|Tablet/)`

#### `"phone"`

Disables only on phones.

```javascript
AOS.init({ disable: 'phone' });
```

Matches: `window.innerWidth < 480`

#### `"tablet"`

Disables only on tablets.

```javascript
AOS.init({ disable: 'tablet' });
```

Matches: `window.innerWidth < 1024 && window.innerWidth >= 768`

### Function

Custom function for fine-grained control.

```javascript
AOS.init({
  disable: function() {
    // Disable on small screens
    return window.innerWidth < 768;
  }
});
```

```javascript
AOS.init({
  disable: function() {
    // Disable in IE
    return /MSIE|Trident/.test(navigator.userAgent);
  }
});
```

```javascript
AOS.init({
  disable: function() {
    // Disable based on user preference
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
});
```

## Complete Example

```javascript
import AOS from 'aos';
import 'aos/dist/aos.css';

// Initialize with full configuration
AOS.init({
  // Animation settings
  duration: 800,
  delay: 0,
  easing: 'ease-out-cubic',

  // Trigger settings
  offset: 120,
  anchorPlacement: 'top-bottom',

  // Behavior
  once: true,
  mirror: false,

  // Device settings
  disable: 'mobile',

  // Performance
  startEvent: 'DOMContentLoaded',
  throttleDelay: 99,
  debounceDelay: 50,
  disableMutationObserver: false
});

// Listen to events
document.addEventListener('aos:in', ({ detail }) => {
  console.log('Element animated in:', detail);
});

// Refresh after dynamic changes
function addNewElement() {
  const el = document.createElement('div');
  el.setAttribute('data-aos', 'fade-up');
  el.textContent = 'New content';
  document.body.appendChild(el);

  // Refresh AOS to detect new element
  AOS.refresh();
}
```

## Browser Support

AOS works in all modern browsers:

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- iOS Safari (latest)
- Chrome for Android (latest)

**Note**: IE11 support requires polyfills for:
- `Array.prototype.forEach`
- `Element.prototype.classList`
- `Object.assign`

## Performance Considerations

### Best Practices

1. **Use `once: true` for better performance**
   ```javascript
   AOS.init({ once: true });
   ```

2. **Increase throttle/debounce delays on slower devices**
   ```javascript
   AOS.init({
     throttleDelay: 120,
     debounceDelay: 80
   });
   ```

3. **Disable on mobile if not needed**
   ```javascript
   AOS.init({ disable: 'mobile' });
   ```

4. **Use simpler animations**
   - Prefer `fade-*` over `flip-*`
   - Avoid excessive animation count

5. **Call `refresh()` sparingly**
   - Only after actual DOM changes
   - Debounce if calling frequently

### Accessibility

Respect user preferences for reduced motion:

```javascript
AOS.init({
  disable: function() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
});
```

## Troubleshooting

### Animations not triggering

1. Verify AOS is initialized: `AOS.init()`
2. Check CSS is imported: `import 'aos/dist/aos.css'`
3. Ensure `data-aos` attribute is set
4. Call `AOS.refresh()` after dynamic content

### Elements flash before animating

Add to global CSS:

```css
[data-aos] {
  pointer-events: none;
}

[data-aos].aos-animate {
  pointer-events: auto;
}
```

### Animations not working in React

Initialize in `useEffect`:

```jsx
useEffect(() => {
  AOS.init();
}, []);
```

Refresh on route changes:

```jsx
const location = useLocation();

useEffect(() => {
  AOS.refresh();
}, [location]);
```
