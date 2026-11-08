# GSAP Easing Functions - Visual Guide

## What Are Easings?

Easings control the **rate of change** during an animation, making motion feel more natural and expressive. They define the acceleration curve between the start and end of an animation.

- **Linear**: Constant speed (robotic, unnatural)
- **Ease In**: Starts slow, ends fast (acceleration)
- **Ease Out**: Starts fast, ends slow (deceleration) - **Most common**
- **Ease InOut**: Starts slow, speeds up, ends slow (smooth both ends)

## Why Easings Matter

```javascript
// Without proper easing - feels robotic
gsap.to(".box", { x: 500, duration: 1, ease: "none" });

// With easing - feels natural
gsap.to(".box", { x: 500, duration: 1, ease: "power2.out" });
```

**The 80/20 Rule**: Most UI animations use `power2.out`, `power3.out`, or `back.out`.

---

## Easing Families

### 1. Power Easings (Most Common)

Power easings use polynomial curves. Higher numbers = more aggressive curves.

#### power1 (Quad)
```
Curve Shape:
  in:    ╱─────  Gentle acceleration
  out:   ─────╲  Gentle deceleration
  inOut: ╱───╲  Gentle both ends
```

**Use Cases**:
- Subtle UI transitions
- Small movements (tooltips, dropdowns)
- Background animations that shouldn't grab attention

**Example**:
```javascript
// Tooltip fade in
gsap.from(".tooltip", {
  opacity: 0,
  y: -10,
  duration: 0.3,
  ease: "power1.out"
});
```

---

#### power2 (Cubic) ⭐ MOST POPULAR
```
Curve Shape:
  in:    ╱╱────  Moderate acceleration
  out:   ────╲╲  Moderate deceleration
  inOut: ╱──╲  Moderate both ends
```

**Use Cases**:
- **Default choice for most UI animations**
- Button clicks, modal animations
- Element entrances/exits
- Smooth scrolling

**Example**:
```javascript
// Modal slide in
gsap.from(".modal", {
  y: 50,
  opacity: 0,
  duration: 0.5,
  ease: "power2.out" // ⭐ Most common choice
});
```

---

#### power3 (Quart)
```
Curve Shape:
  in:    ╱╱╱───  Strong acceleration
  out:   ───╲╲╲  Strong deceleration
  inOut: ╱─╲  Strong both ends
```

**Use Cases**:
- Hero animations
- Page transitions
- Large movements across screen
- Attention-grabbing effects

**Example**:
```javascript
// Hero section reveal
gsap.from(".hero", {
  scale: 0.8,
  opacity: 0,
  duration: 1,
  ease: "power3.out"
});
```

---

#### power4 (Quint)
```
Curve Shape:
  in:    ╱╱╱╱──  Very strong acceleration
  out:   ──╲╲╲╲  Very strong deceleration
  inOut: ╱╲  Very strong both ends
```

**Use Cases**:
- Dramatic reveals
- Full-screen transitions
- Heavy objects (metaphorically)
- When you want maximum impact

**Example**:
```javascript
// Full-screen overlay
gsap.to(".overlay", {
  scale: 1,
  opacity: 1,
  duration: 0.8,
  ease: "power4.out"
});
```

---

### 2. Back Easings (Overshoot)

Back easings **overshoot** the target, then settle back. Creates anticipation and playfulness.

```
Curve Shape:
  in:    ╲╱────  Backs up, then accelerates
  out:   ────╱╲  Overshoots, then settles
  inOut: ╲╱─╱╲  Both ends overshoot
```

**Parameters**: `back.out(1.7)` - Higher number = more overshoot (default: 1.7)

**Use Cases**:
- Playful UI elements
- Buttons with personality
- Attention-grabbing reveals
- Fun micro-interactions

**Example**:
```javascript
// Button with bounce
gsap.from(".button", {
  scale: 0,
  duration: 0.5,
  ease: "back.out(1.7)" // Classic overshoot
});

// Extreme overshoot for fun effect
gsap.from(".badge", {
  scale: 0,
  rotation: -180,
  duration: 0.8,
  ease: "back.out(3)" // More dramatic
});
```

**Pro Tip**: Use `back.out(1.2)` for subtle overshoot, `back.out(2.5)` for exaggerated effect.

---

### 3. Elastic Easings (Spring/Rubber Band)

Elastic easings create a **spring/bounce** effect, oscillating around the target.

```
Curve Shape:
  in:    ╲╱╲╱──  Oscillates, then accelerates
  out:   ──╱╲╱╲  Overshoots multiple times, then settles
  inOut: ╲╱╲╱╲  Both ends oscillate
```

**Parameters**: `elastic.out(amplitude, period)`
- **amplitude**: Strength of oscillation (default: 1)
- **period**: Frequency of oscillation (default: 0.3)

**Use Cases**:
- Cartoonish effects
- Game UI elements
- Fun landing pages
- Notification badges
- **Use sparingly** - can feel gimmicky

**Example**:
```javascript
// Notification badge
gsap.from(".badge", {
  scale: 0,
  duration: 1,
  ease: "elastic.out(1, 0.3)"
});

// Stronger spring effect
gsap.from(".icon", {
  y: -50,
  duration: 1.5,
  ease: "elastic.out(1.5, 0.4)" // More bounce
});
```

**Warning**: Elastic can feel unprofessional if overused. Best for gaming/playful interfaces.

---

### 4. Bounce Easings

Bounce easings simulate a **bouncing ball** landing.

```
Curve Shape:
  in:    ╲╱╲╱╲──  Bounces, then accelerates
  out:   ──╲╱╲╱╲  Lands with decreasing bounces
  inOut: ╲╱─╱╲  Both ends bounce
```

**Use Cases**:
- Elements "dropping" into place
- Playful UI (games, children's apps)
- Landing animations
- Fun effects (use sparingly)

**Example**:
```javascript
// Element drops in
gsap.from(".card", {
  y: -200,
  duration: 1,
  ease: "bounce.out"
});

// Multiple cards with stagger
gsap.from(".card", {
  y: -100,
  opacity: 0,
  duration: 1,
  ease: "bounce.out",
  stagger: 0.1
});
```

**Pro Tip**: Combine with `power2.in` for objects falling before bouncing.

---

### 5. Circ Easings (Circular)

Circular easings use a quarter-circle curve. Creates **sharp acceleration/deceleration**.

```
Curve Shape:
  in:    ╱╱────  Sharp acceleration (quarter circle)
  out:   ────╲╲  Sharp deceleration
  inOut: ╱──╲  Sharp both ends
```

**Use Cases**:
- Fast, snappy movements
- Material Design-style animations
- Quick transitions
- When you want instant impact

**Example**:
```javascript
// Quick slide-in drawer
gsap.to(".drawer", {
  x: 0,
  duration: 0.3,
  ease: "circ.out"
});
```

---

### 6. Expo Easings (Exponential)

Exponential easings create **very dramatic** acceleration/deceleration curves.

```
Curve Shape:
  in:    ╱╱╱───  Extremely slow start, then explodes
  out:   ───╲╲╲  Extremely fast start, then crawls
  inOut: ╱─╲  Extreme both ends
```

**Use Cases**:
- Dramatic reveals
- Cinematic effects
- Zoom-in/zoom-out animations
- When you want **maximum drama**

**Example**:
```javascript
// Dramatic zoom in
gsap.from(".hero-image", {
  scale: 5,
  opacity: 0,
  duration: 1.5,
  ease: "expo.out"
});

// Intense page transition
gsap.to(".page", {
  x: -window.innerWidth,
  duration: 1,
  ease: "expo.inOut"
});
```

---

### 7. Sine Easings

Sine easings are **extremely gentle**, using a sine wave curve.

```
Curve Shape:
  in:    ╱─────  Very gentle acceleration
  out:   ─────╲  Very gentle deceleration
  inOut: ╱───╲  Very gentle both ends
```

**Use Cases**:
- Subtle, barely-noticeable animations
- Background movements
- Ambient effects
- Parallax scrolling
- When animation should be **invisible**

**Example**:
```javascript
// Gentle parallax
gsap.to(".bg", {
  y: 100,
  ease: "sine.out",
  scrollTrigger: {
    scrub: true
  }
});

// Subtle float animation
gsap.to(".cloud", {
  y: "+=20",
  duration: 3,
  ease: "sine.inOut",
  yoyo: true,
  repeat: -1
});
```

---

### 8. None (Linear)

No easing at all - constant speed throughout.

```
Curve Shape: ──────  Perfectly straight line
```

**Use Cases**:
- **ScrollTrigger with scrub** (let user control speed)
- Loading bars (constant progress)
- Background loops
- Mechanical movements
- **Rarely used for regular animations**

**Example**:
```javascript
// Horizontal scroll (user controls speed)
gsap.to(".panels", {
  xPercent: -100,
  ease: "none", // User controls via scroll
  scrollTrigger: {
    scrub: true
  }
});

// Loading bar
gsap.to(".progress", {
  width: "100%",
  duration: 5,
  ease: "none"
});
```

---

## Quick Decision Tree

### 1. What's the purpose?

**Subtle UI transition** → `power1.out` or `power2.out`

**Standard animation** → `power2.out` ⭐ (default choice)

**Hero/dramatic effect** → `power3.out` or `power4.out`

**Playful/fun** → `back.out(1.7)` or `elastic.out()`

**Game/cartoon** → `bounce.out` or `elastic.out()`

**Scroll-driven** → `none` (with scrub)

**Background/ambient** → `sine.inOut`

---

### 2. How noticeable should it be?

```
Subtle          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━→ Dramatic
sine.out    power1.out    power2.out    power3.out    expo.out
                              ⭐ Start here

Gentle          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━→ Playful
circ.out    back.out(1.2)    back.out(1.7)    elastic.out()
```

---

## Common Patterns by Use Case

### UI Animations (80% of use cases)
```javascript
// Standard choice
ease: "power2.out"

// Slightly more dramatic
ease: "power3.out"

// Playful
ease: "back.out(1.7)"
```

### Scroll Animations
```javascript
// Let user control speed
ease: "none",
scrollTrigger: { scrub: true }

// Smooth snap scrolling
ease: "power2.inOut",
scrollTrigger: { snap: 1 }
```

### Micro-interactions
```javascript
// Button hover
ease: "power1.out", duration: 0.2

// Toggle switch
ease: "back.out(2)", duration: 0.4

// Ripple effect
ease: "power2.out", duration: 0.6
```

### Page Transitions
```javascript
// Standard page transition
ease: "power3.inOut", duration: 0.8

// Dramatic reveal
ease: "expo.out", duration: 1.2
```

### Loading States
```javascript
// Loading spinner
ease: "none", repeat: -1

// Progress bar
ease: "power2.out", duration: 2
```

---

## Easing Combinations

### Sequential Easings (Timeline)
```javascript
const tl = gsap.timeline();

// Slide in fast, settle slow
tl.to(".card", { y: 0, duration: 0.3, ease: "power3.in" })
  .to(".card", { scale: 1, duration: 0.4, ease: "back.out(2)" });
```

### Staggered with Different Easings
```javascript
gsap.from(".item", {
  opacity: 0,
  y: 50,
  duration: 0.6,
  ease: "power2.out",
  stagger: {
    each: 0.1,
    ease: "power1.inOut" // Easing for stagger timing itself
  }
});
```

### Physics-based Fallback
```javascript
// Light object (fast)
gsap.to(".feather", { y: 500, duration: 2, ease: "sine.in" });

// Heavy object (slow start)
gsap.to(".anvil", { y: 500, duration: 1.5, ease: "power4.in" });
```

---

## Custom Easings

### Custom Bezier Curve
```javascript
// Use CustomEase plugin (Club GreenSock)
gsap.registerPlugin(CustomEase);

CustomEase.create("customBounce", "0.5,0,0.75,1.5,1");

gsap.to(".box", {
  x: 500,
  duration: 1,
  ease: "customBounce"
});
```

### Steps (Stepped Animation)
```javascript
// Simulate frame-by-frame animation
gsap.to(".sprite", {
  x: 500,
  duration: 1,
  ease: "steps(12)" // 12 discrete steps
});
```

---

## Testing Easings

### Easing Visualizer (Inline Tool)

Save this as `easings.html` to test easings visually:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <style>
    body { font-family: system-ui; padding: 40px; background: #1a1a2e; color: white; }
    .box { width: 50px; height: 50px; background: #00ffcc; margin: 20px 0; border-radius: 8px; }
    button { padding: 10px 20px; margin: 5px; background: #00ffcc; border: none; border-radius: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>GSAP Easing Tester</h1>
  <div id="boxes"></div>
  <button onclick="testAll()">Test All Easings</button>

  <script>
    const easings = [
      "none",
      "power1.out", "power2.out", "power3.out", "power4.out",
      "back.out(1.7)", "elastic.out(1, 0.3)", "bounce.out",
      "circ.out", "expo.out", "sine.out"
    ];

    const container = document.getElementById('boxes');
    easings.forEach(ease => {
      const label = document.createElement('div');
      label.textContent = ease;
      label.style.marginTop = '20px';
      container.appendChild(label);

      const box = document.createElement('div');
      box.className = 'box';
      box.dataset.ease = ease;
      container.appendChild(box);
    });

    function testAll() {
      document.querySelectorAll('.box').forEach(box => {
        gsap.fromTo(box,
          { x: 0 },
          { x: 500, duration: 1.5, ease: box.dataset.ease }
        );
      });
    }
  </script>
</body>
</html>
```

**Online Tools**:
- [GreenSock Ease Visualizer](https://gsap.com/docs/v3/Eases)
- [Cubic Bezier Generator](https://cubic-bezier.com)

---

## Performance Notes

### Do Easings Affect Performance?

**No** - Easings are mathematical functions with negligible overhead. Choose based on aesthetics, not performance.

**Exception**: Custom bezier curves with many control points can be slightly slower (still negligible).

---

## Common Mistakes

### ❌ Using Linear for UI Animations
```javascript
// Feels robotic
gsap.to(".button", { scale: 1.1, duration: 0.3, ease: "none" });
```

✅ **Fix**: Use `power2.out`
```javascript
gsap.to(".button", { scale: 1.1, duration: 0.3, ease: "power2.out" });
```

---

### ❌ Over-using Elastic/Bounce
```javascript
// Every element bounces - feels gimmicky
gsap.from(".item", { scale: 0, ease: "elastic.out(2, 0.3)", stagger: 0.1 });
```

✅ **Fix**: Use sparingly for key elements
```javascript
// Only hero element has elastic
gsap.from(".hero", { scale: 0, ease: "elastic.out(1, 0.3)" });
gsap.from(".item", { scale: 0, ease: "back.out(1.7)", stagger: 0.1 });
```

---

### ❌ Wrong Direction (in vs out)
```javascript
// Element exits with ease.in (feels slow to start)
gsap.to(".modal", { opacity: 0, ease: "power2.in" });
```

✅ **Fix**: Use `out` for exits
```javascript
gsap.to(".modal", { opacity: 0, ease: "power2.out" });
```

**Rule**:
- **Entrances** → `ease.out` (fast start, slow end)
- **Exits** → `ease.out` (consistent)
- **Both** → `ease.inOut` (smooth both ends)

---

## Best Practices

### 1. Start with power2.out
It's the goldilocks easing - not too gentle, not too aggressive.

### 2. Match Easing to Content
- **Lightweight** (modals, tooltips) → `power1.out` or `power2.out`
- **Medium** (cards, sections) → `power2.out` or `power3.out`
- **Heavy** (full pages, heroes) → `power3.out` or `power4.out`

### 3. Be Consistent
Use the same easing family throughout your project for cohesion.

### 4. Test at Different Speeds
Easings behave differently at different durations:
```javascript
// Too short - easing barely noticeable
duration: 0.1, ease: "power3.out"

// Sweet spot
duration: 0.4, ease: "power3.out"

// Too long - feels sluggish
duration: 2, ease: "power3.out"
```

### 5. Consider Context
- **Professional/Corporate** → `power2.out`, `power3.out`
- **Playful/Fun** → `back.out`, `elastic.out`
- **Luxury/Premium** → `expo.out`, `power4.out`
- **Fast/Responsive** → `circ.out`, `power2.out`

---

## Cheat Sheet

| Use Case | Easing | Duration | Notes |
|----------|--------|----------|-------|
| Default UI | `power2.out` | 0.3-0.5s | Start here |
| Hero animation | `power3.out` | 0.8-1.2s | More impact |
| Button hover | `power1.out` | 0.2s | Quick & subtle |
| Modal open | `power2.out` | 0.4s | Smooth entrance |
| Tooltip | `power1.out` | 0.2s | Fast & light |
| Scroll scrub | `none` | N/A | User-controlled |
| Page transition | `power3.inOut` | 0.8s | Smooth both ends |
| Playful button | `back.out(1.7)` | 0.5s | Overshoot |
| Notification | `back.out(2)` | 0.6s | Attention-grabbing |
| Parallax | `sine.out` | N/A | Barely noticeable |
| Loading bar | `none` | Variable | Constant speed |
| Bounce-in | `bounce.out` | 1s | Use sparingly |

---

## Summary

**The 3 Easings You Need to Know**:

1. **power2.out** ⭐ - Your default choice (80% of animations)
2. **power3.out** - For dramatic effects
3. **back.out(1.7)** - For playful interactions

**Golden Rules**:
- When in doubt, use `power2.out`
- Entrances and exits both use `.out`
- ScrollTrigger with scrub uses `none`
- Be consistent across your project
- Test different durations to find the sweet spot

**Remember**: Good easing makes animations feel natural and purposeful. Bad easing makes them feel robotic or gimmicky.
