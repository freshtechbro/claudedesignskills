# AOS Animation Catalog

Complete catalog of all 50+ built-in animations available in AOS (Animate On Scroll).

## Table of Contents

- [Fade Animations](#fade-animations)
- [Slide Animations](#slide-animations)
- [Zoom Animations](#zoom-animations)
- [Flip Animations](#flip-animations)
- [Animation Combinations](#animation-combinations)
- [Custom Animations](#custom-animations)

## Fade Animations

Fade animations gradually change opacity. These are the simplest and most performant animations.

### Basic Fade

#### `fade-in`

Simple fade in from transparent to opaque.

```html
<div data-aos="fade-in">Fades in</div>
```

**Use cases**: Simple reveals, subtle content appearance

### Directional Fades

#### `fade-up`

Fades in while moving upward from below.

```html
<div data-aos="fade-up">Fades up from bottom</div>
```

**Use cases**: Content blocks, cards, text sections, CTA buttons

#### `fade-down`

Fades in while moving downward from above.

```html
<div data-aos="fade-down">Fades down from top</div>
```

**Use cases**: Headers, hero titles, navigation menus

#### `fade-left`

Fades in while moving left (coming from the right).

```html
<div data-aos="fade-left">Fades left from right</div>
```

**Use cases**: Text blocks, images on right side of layout

#### `fade-right`

Fades in while moving right (coming from the left).

```html
<div data-aos="fade-right">Fades right from left</div>
```

**Use cases**: Text blocks, images on left side of layout

### Diagonal Fades

#### `fade-up-right`

Fades in while moving diagonally up and to the right.

```html
<div data-aos="fade-up-right">Fades up-right diagonally</div>
```

**Use cases**: Grid items, cards in top-left position

#### `fade-up-left`

Fades in while moving diagonally up and to the left.

```html
<div data-aos="fade-up-left">Fades up-left diagonally</div>
```

**Use cases**: Grid items, cards in top-right position

#### `fade-down-right`

Fades in while moving diagonally down and to the right.

```html
<div data-aos="fade-down-right">Fades down-right diagonally</div>
```

**Use cases**: Grid items, cards in bottom-left position

#### `fade-down-left`

Fades in while moving diagonally down and to the left.

```html
<div data-aos="fade-down-left">Fades down-left diagonally</div>
```

**Use cases**: Grid items, cards in bottom-right position

## Slide Animations

Slide animations move elements without changing opacity. More dramatic than fades.

### `slide-up`

Slides up from below (no fade).

```html
<div data-aos="slide-up">Slides up</div>
```

**Use cases**: Modal overlays, bottom sheets, notifications

### `slide-down`

Slides down from above (no fade).

```html
<div data-aos="slide-down">Slides down</div>
```

**Use cases**: Dropdown menus, alerts, top banners

### `slide-left`

Slides left from the right (no fade).

```html
<div data-aos="slide-left">Slides left</div>
```

**Use cases**: Side panels, drawer menus, image carousels

### `slide-right`

Slides right from the left (no fade).

```html
<div data-aos="slide-right">Slides right</div>
```

**Use cases**: Side panels, drawer menus, timeline items

## Zoom Animations

Zoom animations scale elements from small to normal size (or vice versa).

### Basic Zoom

#### `zoom-in`

Zooms in from smaller to normal size, centered.

```html
<div data-aos="zoom-in">Zooms in</div>
```

**Use cases**: Featured images, product photos, logos, icons

#### `zoom-out`

Zooms out from larger to normal size, centered.

```html
<div data-aos="zoom-out">Zooms out</div>
```

**Use cases**: Background images, hero sections, splash screens

### Directional Zoom In

#### `zoom-in-up`

Zooms in while moving upward.

```html
<div data-aos="zoom-in-up">Zooms in from bottom</div>
```

**Use cases**: Gallery images, product cards, testimonials

#### `zoom-in-down`

Zooms in while moving downward.

```html
<div data-aos="zoom-in-down">Zooms in from top</div>
```

**Use cases**: Headers, hero content, call-to-action sections

#### `zoom-in-left`

Zooms in while moving left (from right).

```html
<div data-aos="zoom-in-left">Zooms in from right</div>
```

**Use cases**: Content blocks, feature highlights (right side)

#### `zoom-in-right`

Zooms in while moving right (from left).

```html
<div data-aos="zoom-in-right">Zooms in from left</div>
```

**Use cases**: Content blocks, feature highlights (left side)

### Directional Zoom Out

#### `zoom-out-up`

Zooms out while moving upward.

```html
<div data-aos="zoom-out-up">Zooms out moving up</div>
```

**Use cases**: Attention-grabbing elements, special announcements

#### `zoom-out-down`

Zooms out while moving downward.

```html
<div data-aos="zoom-out-down">Zooms out moving down</div>
```

**Use cases**: Hero overlays, introductory content

#### `zoom-out-left`

Zooms out while moving left.

```html
<div data-aos="zoom-out-left">Zooms out moving left</div>
```

**Use cases**: Dynamic content transitions

#### `zoom-out-right`

Zooms out while moving right.

```html
<div data-aos="zoom-out-right">Zooms out moving right</div>
```

**Use cases**: Dynamic content transitions

## Flip Animations

Flip animations create 3D rotation effects. These are more complex and should be used sparingly.

### `flip-up`

Flips up (rotates around X-axis).

```html
<div data-aos="flip-up">Flips up</div>
```

**Use cases**: Cards, product reveals, special features

**Note**: More CPU-intensive than other animations

### `flip-down`

Flips down (rotates around X-axis).

```html
<div data-aos="flip-down">Flips down</div>
```

**Use cases**: Cards, dropdown reveals

**Note**: More CPU-intensive than other animations

### `flip-left`

Flips left (rotates around Y-axis).

```html
<div data-aos="flip-left">Flips left</div>
```

**Use cases**: Card flips, panel transitions

**Note**: More CPU-intensive than other animations

### `flip-right`

Flips right (rotates around Y-axis).

```html
<div data-aos="flip-right">Flips right</div>
```

**Use cases**: Card flips, panel transitions

**Note**: More CPU-intensive than other animations

## Animation Combinations

### Staggered Animations

Create sequential reveals by using delays:

```html
<div class="feature-grid">
  <div data-aos="fade-up" data-aos-delay="0">Item 1</div>
  <div data-aos="fade-up" data-aos-delay="100">Item 2</div>
  <div data-aos="fade-up" data-aos-delay="200">Item 3</div>
  <div data-aos="fade-up" data-aos-delay="300">Item 4</div>
</div>
```

**Recommended delay increment**: 50-150ms between items

### Mixed Animations

Combine different animation types for visual interest:

```html
<!-- Hero section -->
<h1 data-aos="fade-down">Heading</h1>
<p data-aos="fade-up" data-aos-delay="200">Subtext</p>
<button data-aos="zoom-in" data-aos-delay="400">CTA</button>
```

### Alternating Patterns

Create rhythm with alternating directions:

```html
<div class="content-section">
  <div class="item" data-aos="fade-right">From left</div>
  <div class="item" data-aos="fade-left">From right</div>
  <div class="item" data-aos="fade-right">From left</div>
  <div class="item" data-aos="fade-left">From right</div>
</div>
```

## Custom Animations

Create custom animations using CSS:

### Example: Custom Bounce

```css
/* Define animation */
@keyframes custom-bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-30px);
  }
  60% {
    transform: translateY(-15px);
  }
}

/* Apply to AOS element */
[data-aos="custom-bounce"] {
  opacity: 0;
  transform: translateY(100px);
  transition-property: transform, opacity;
}

[data-aos="custom-bounce"].aos-animate {
  opacity: 1;
  transform: translateY(0);
  animation: custom-bounce 1s ease-out;
}
```

```html
<div data-aos="custom-bounce">Bounces in!</div>
```

### Example: Custom Rotate

```css
[data-aos="rotate-in"] {
  opacity: 0;
  transform: rotate(-180deg) scale(0.5);
  transition-property: transform, opacity;
}

[data-aos="rotate-in"].aos-animate {
  opacity: 1;
  transform: rotate(0) scale(1);
}
```

```html
<div data-aos="rotate-in" data-aos-duration="1000">Rotates in!</div>
```

### Example: Custom Slide Bounce

```css
[data-aos="slide-bounce"] {
  opacity: 0;
  transform: translateX(-100px);
  transition-property: transform, opacity;
}

[data-aos="slide-bounce"].aos-animate {
  opacity: 1;
  transform: translateX(0);
  animation: bounce-effect 0.6s;
}

@keyframes bounce-effect {
  0% { transform: translateX(-100px); }
  60% { transform: translateX(10px); }
  80% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}
```

```html
<div data-aos="slide-bounce">Slides with bounce!</div>
```

## Animation Performance Guide

### Performance Ranking (Best to Worst)

1. **Fade** animations (opacity only)
   - Best performance, GPU-accelerated
   - Use for most content

2. **Slide** and **Zoom** animations (transform only)
   - Good performance, GPU-accelerated
   - Use for featured content

3. **Flip** animations (3D transforms)
   - Lower performance, more CPU-intensive
   - Use sparingly for special elements

### Optimization Tips

#### 1. Prefer Simpler Animations

```html
<!-- Better performance -->
<div data-aos="fade-up">Content</div>

<!-- Lower performance -->
<div data-aos="flip-left">Content</div>
```

#### 2. Limit Animation Count

```html
<!-- Good: Selective animation -->
<div class="grid">
  <div data-aos="fade-up">Animated</div>
  <div>Static</div>
  <div>Static</div>
  <div data-aos="fade-up">Animated</div>
</div>

<!-- Avoid: Everything animated -->
<div class="grid">
  <div data-aos="fade-up">Item 1</div>
  <div data-aos="fade-up">Item 2</div>
  <div data-aos="fade-up">Item 3</div>
  <!-- ...50 more animated items -->
</div>
```

#### 3. Use Shorter Durations

```html
<!-- Fast, smooth -->
<div data-aos="fade-up" data-aos-duration="400">Content</div>

<!-- Potentially janky on slower devices -->
<div data-aos="flip-left" data-aos-duration="1500">Content</div>
```

#### 4. Disable on Mobile (Optional)

```javascript
AOS.init({
  disable: 'mobile' // or window.innerWidth < 768
});
```

## Animation Selection Guide

### By Content Type

| Content Type | Recommended Animation | Alternative |
|--------------|----------------------|-------------|
| Hero Heading | `fade-down` | `zoom-in-down` |
| Hero Subtext | `fade-up` | `slide-up` |
| CTA Button | `zoom-in` | `fade-up` |
| Feature Cards | `fade-up` (staggered) | `zoom-in-up` |
| Image Gallery | `zoom-in-up` | `fade-in` |
| Testimonials | `zoom-in` | `fade-in` |
| Statistics | `zoom-in` | `fade-up` |
| Timeline Items | `slide-right` / `slide-left` | `fade-right` / `fade-left` |
| Modal Overlay | `zoom-in` | `fade-in` |
| Notifications | `slide-down` | `fade-down` |
| Product Cards | `zoom-in-up` | `fade-up` |
| Text Blocks | `fade-right` / `fade-left` | `slide-right` / `slide-left` |
| Icons | `zoom-in` | `fade-in` |
| Navigation | `fade-down` | `slide-down` |

### By User Experience Goal

| Goal | Animation | Example |
|------|-----------|---------|
| **Subtle** | `fade-in`, `fade-up` | About text, descriptions |
| **Attention-grabbing** | `zoom-in`, `zoom-out` | CTA buttons, special offers |
| **Directional flow** | `slide-*`, `fade-*` with direction | Reading flow, timelines |
| **Playful** | `flip-*`, diagonal fades | Portfolio items, creative sections |
| **Professional** | `fade-up`, `fade-in` | Corporate sites, documentation |

## Quick Reference

### Fade Animations (9)
- `fade-in`
- `fade-up`, `fade-down`, `fade-left`, `fade-right`
- `fade-up-right`, `fade-up-left`, `fade-down-right`, `fade-down-left`

### Slide Animations (4)
- `slide-up`, `slide-down`, `slide-left`, `slide-right`

### Zoom Animations (11)
- `zoom-in`, `zoom-out`
- `zoom-in-up`, `zoom-in-down`, `zoom-in-left`, `zoom-in-right`
- `zoom-out-up`, `zoom-out-down`, `zoom-out-left`, `zoom-out-right`

### Flip Animations (4)
- `flip-up`, `flip-down`, `flip-left`, `flip-right`

**Total**: 28 built-in animations

## Best Practices

1. **Consistency**: Stick to 2-3 animation types per page
2. **Hierarchy**: Use more dramatic animations (zoom, flip) for important content
3. **Direction**: Match animation direction to layout flow
4. **Timing**: Use delays to create sequences (100-200ms between items)
5. **Performance**: Prefer fade/slide over flip animations
6. **Mobile**: Consider disabling or simplifying animations on mobile
7. **Accessibility**: Respect `prefers-reduced-motion` user preference

```javascript
// Respect reduced motion preference
AOS.init({
  disable: function() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
});
```
