# Barba.js + GSAP Integration Guide

Complete guide to using GSAP (Green Sock Animation Platform) with Barba.js for smooth, performant page transitions.

## Table of Contents

- [Why GSAP + Barba](#why-gsap--barba)
- [Setup](#setup)
- [Basic Integration Patterns](#basic-integration-patterns)
- [Timeline-Based Transitions](#timeline-based-transitions)
- [Advanced Patterns](#advanced-patterns)
- [Performance Tips](#performance-tips)
- [Common Issues](#common-issues)

---

## Why GSAP + Barba

**Barba.js** handles navigation and lifecycle management.
**GSAP** handles the actual animations.

This combination provides:
- **Performance**: GSAP uses GPU acceleration and optimized rendering
- **Control**: Precise timing with timelines, stagger, and easing
- **Simplicity**: GSAP returns promises that Barba can await
- **Power**: Complex sequences, morphing, and advanced effects

---

## Setup

### Installation

```bash
# Install both libraries
npm install --save-dev @barba/core gsap

# Optional: GSAP plugins
npm install --save-dev gsap/ScrollTrigger
```

### Basic Import

```javascript
import barba from '@barba/core';
import gsap from 'gsap';

// Optional GSAP plugins
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```

---

## Basic Integration Patterns

### Pattern 1: Simple Fade

```javascript
barba.init({
  transitions: [{
    name: 'fade',

    async leave({ current }) {
      await gsap.to(current.container, {
        opacity: 0,
        duration: 0.5,
        ease: 'power2.inOut'
      });
    },

    async enter({ next }) {
      // Set initial state
      gsap.set(next.container, { opacity: 0 });

      // Animate in
      await gsap.to(next.container, {
        opacity: 1,
        duration: 0.5,
        ease: 'power2.inOut'
      });
    }
  }]
});
```

**Key Points**:
- GSAP's `to()` returns a promise
- Use `await` to make Barba wait for animation completion
- `gsap.set()` sets initial state without animation

### Pattern 2: Slide Transitions

```javascript
{
  name: 'slide',
  sync: true, // Play leave and enter simultaneously

  leave({ current }) {
    return gsap.to(current.container, {
      x: '-100%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  },

  enter({ next }) {
    // Start off-screen
    gsap.set(next.container, { x: '100%' });

    // Slide in
    return gsap.to(next.container, {
      x: '0%',
      duration: 0.7,
      ease: 'power3.inOut'
    });
  }
}
```

**Key Points**:
- `sync: true` enables crossfade/overlap effect
- Use `return` instead of `await` (same result)
- GPU-accelerated properties (`x`, `y`, `opacity`, `scale`)

### Pattern 3: Scale and Fade

```javascript
{
  name: 'scale-fade',

  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      scale: 0.95,
      duration: 0.5,
      ease: 'power2.in'
    });
  },

  async enter({ next }) {
    await gsap.fromTo(next.container,
      // From
      {
        opacity: 0,
        scale: 1.05
      },
      // To
      {
        opacity: 1,
        scale: 1,
        duration: 0.5,
        ease: 'power2.out'
      }
    );
  }
}
```

**Key Points**:
- `fromTo()` sets initial state and animates to final state
- Different easings for enter/exit (asymmetric feel)

---

## Timeline-Based Transitions

GSAP Timelines provide precise control over complex sequences.

### Basic Timeline

```javascript
{
  name: 'timeline-fade',

  async leave({ current }) {
    const tl = gsap.timeline();

    tl.to(current.container.querySelector('h1'), {
      y: -50,
      opacity: 0,
      duration: 0.3
    })
    .to(current.container.querySelector('.content'), {
      y: -30,
      opacity: 0,
      duration: 0.3
    }, '-=0.2') // Overlap by 0.2s
    .to(current.container, {
      opacity: 0,
      duration: 0.2
    });

    await tl.play();
  },

  async enter({ next }) {
    const tl = gsap.timeline();

    // Set initial states
    gsap.set(next.container, { opacity: 1 });
    gsap.set(next.container.querySelector('h1'), { y: 50, opacity: 0 });
    gsap.set(next.container.querySelector('.content'), { y: 30, opacity: 0 });

    tl.to(next.container.querySelector('h1'), {
      y: 0,
      opacity: 1,
      duration: 0.5,
      ease: 'power3.out'
    })
    .to(next.container.querySelector('.content'), {
      y: 0,
      opacity: 1,
      duration: 0.5,
      ease: 'power3.out'
    }, '-=0.3');

    await tl.play();
  }
}
```

**Timeline Position Parameter**:
- `'-=0.2'` - Start 0.2s before previous animation ends (overlap)
- `'+=0.2'` - Start 0.2s after previous animation ends (delay)
- `'<'` - Start at beginning of previous animation
- `'>'` - Start at end of previous animation

### Staggered Elements

```javascript
{
  async leave({ current }) {
    const tl = gsap.timeline();

    tl.to(current.container.querySelectorAll('.item'), {
      y: -30,
      opacity: 0,
      duration: 0.4,
      stagger: 0.05, // 0.05s delay between each item
      ease: 'power2.in'
    })
    .to(current.container, {
      opacity: 0,
      duration: 0.3
    });

    await tl.play();
  },

  async enter({ next }) {
    const tl = gsap.timeline();

    gsap.set(next.container.querySelectorAll('.item'), { y: 30, opacity: 0 });

    tl.to(next.container.querySelectorAll('.item'), {
      y: 0,
      opacity: 1,
      duration: 0.5,
      stagger: 0.05,
      ease: 'power2.out'
    });

    await tl.play();
  }
}
```

**Stagger Options**:
```javascript
stagger: {
  amount: 0.5,      // Total duration for all staggers
  from: 'start',    // 'start', 'end', 'center', or index number
  grid: [5, 10],    // For grid layouts [rows, columns]
  axis: 'y',        // 'x', 'y', or null
  ease: 'power2.in' // Easing for stagger distribution
}
```

### Timeline with Labels

```javascript
{
  async leave({ current }) {
    const tl = gsap.timeline();

    // Add labels for reference
    tl.addLabel('start')
      .to(current.container.querySelector('.hero'), {
        scale: 0.9,
        opacity: 0,
        duration: 0.5
      })
      .addLabel('hero-done')
      .to(current.container.querySelector('.content'), {
        y: -50,
        opacity: 0,
        duration: 0.4
      }, 'hero-done-=0.2') // Start 0.2s before hero-done
      .addLabel('content-done')
      .to(current.container, {
        opacity: 0,
        duration: 0.2
      }, 'content-done');

    await tl.play();
  }
}
```

---

## Advanced Patterns

### Pattern 1: Conditional Animations

```javascript
{
  async leave({ current, next }) {
    const isProduct = current.namespace === 'product' && next.namespace === 'product';

    if (isProduct) {
      // Fast transition between products
      await gsap.to(current.container, {
        opacity: 0,
        scale: 0.95,
        duration: 0.3
      });
    } else {
      // Slower, more elaborate transition
      const tl = gsap.timeline();

      tl.to(current.container.querySelectorAll('.fade-item'), {
        y: -30,
        opacity: 0,
        duration: 0.4,
        stagger: 0.05
      })
      .to(current.container, {
        opacity: 0,
        duration: 0.3
      });

      await tl.play();
    }
  }
}
```

### Pattern 2: Direction-Based Transitions

```javascript
{
  async leave({ current }) {
    const direction = barba.history.direction;
    const isBack = direction === 'back';

    await gsap.to(current.container, {
      x: isBack ? '100%' : '-100%', // Slide right if going back
      duration: 0.6,
      ease: 'power2.inOut'
    });
  },

  async enter({ next }) {
    const direction = barba.history.direction;
    const isBack = direction === 'back';

    gsap.set(next.container, {
      x: isBack ? '-100%' : '100%' // Come from left if going back
    });

    await gsap.to(next.container, {
      x: '0%',
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}
```

### Pattern 3: Curtain Effect

```javascript
{
  async leave({ current }) {
    // Animate curtain down
    const curtain = document.querySelector('.transition-curtain');

    await gsap.fromTo(curtain,
      { yPercent: -100 },
      {
        yPercent: 0,
        duration: 0.6,
        ease: 'power2.inOut'
      }
    );
  },

  async enter({ next }) {
    // Animate curtain up
    const curtain = document.querySelector('.transition-curtain');

    await gsap.to(curtain, {
      yPercent: 100,
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}
```

**HTML for Curtain**:
```html
<div class="transition-curtain"></div>
```

**CSS for Curtain**:
```css
.transition-curtain {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
  z-index: 9999;
  pointer-events: none;
  transform: translateY(-100%);
}
```

### Pattern 4: Morphing Transitions

```javascript
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin';
gsap.registerPlugin(MorphSVGPlugin);

{
  async leave({ current }) {
    const shape = document.querySelector('.transition-shape path');

    await gsap.to(shape, {
      morphSVG: '.shape-expanded',
      duration: 0.8,
      ease: 'power2.inOut'
    });
  },

  async enter({ next }) {
    const shape = document.querySelector('.transition-shape path');

    await gsap.to(shape, {
      morphSVG: '.shape-collapsed',
      duration: 0.8,
      ease: 'power2.inOut'
    });
  }
}
```

### Pattern 5: Split Text Animations

```javascript
import { SplitText } from 'gsap/SplitText';
gsap.registerPlugin(SplitText);

{
  async enter({ next }) {
    const title = next.container.querySelector('h1');
    const split = new SplitText(title, { type: 'chars,words' });

    await gsap.from(split.chars, {
      opacity: 0,
      y: 50,
      rotationX: -90,
      stagger: 0.02,
      duration: 0.8,
      ease: 'back.out(1.7)'
    });

    // Clean up
    split.revert();
  }
}
```

### Pattern 6: Parallax Layers

```javascript
{
  sync: true,

  async leave({ current }) {
    const tl = gsap.timeline();

    tl.to(current.container.querySelector('.layer-1'), {
      y: -100,
      opacity: 0,
      duration: 0.8
    }, 0)
    .to(current.container.querySelector('.layer-2'), {
      y: -50,
      opacity: 0,
      duration: 0.8
    }, 0)
    .to(current.container.querySelector('.layer-3'), {
      y: -25,
      opacity: 0,
      duration: 0.8
    }, 0);

    await tl.play();
  },

  async enter({ next }) {
    const tl = gsap.timeline();

    gsap.set(next.container.querySelectorAll('[class^="layer-"]'), {
      opacity: 0
    });

    tl.from(next.container.querySelector('.layer-1'), {
      y: 100,
      opacity: 0,
      duration: 0.8
    }, 0)
    .from(next.container.querySelector('.layer-2'), {
      y: 50,
      opacity: 0,
      duration: 0.8
    }, 0)
    .from(next.container.querySelector('.layer-3'), {
      y: 25,
      opacity: 0,
      duration: 0.8
    }, 0);

    await tl.play();
  }
}
```

---

## Performance Tips

### 1. Use GPU-Accelerated Properties

```javascript
// ✅ Good - GPU accelerated
gsap.to(element, {
  x: 100,
  y: 50,
  opacity: 0.5,
  scale: 1.2,
  rotation: 45
});

// ❌ Avoid - causes reflow/repaint
gsap.to(element, {
  left: '100px',
  top: '50px',
  width: '200px',
  height: '300px'
});
```

### 2. Use will-change with Caution

```css
/* Add to elements that will animate */
[data-barba="container"] {
  will-change: transform, opacity;
}

/* Remove after transition */
```

```javascript
barba.hooks.after(() => {
  // Remove will-change after transition
  document.querySelectorAll('[data-barba="container"]').forEach(el => {
    el.style.willChange = 'auto';
  });
});
```

### 3. Kill Running Animations

```javascript
{
  beforeLeave({ current }) {
    // Kill any running animations on current page
    gsap.killTweensOf(current.container.querySelectorAll('*'));
  }
}
```

### 4. Batch DOM Queries

```javascript
// ❌ Slow - queries DOM multiple times
{
  async leave({ current }) {
    await gsap.to(current.container.querySelector('h1'), { opacity: 0 });
    await gsap.to(current.container.querySelector('.content'), { opacity: 0 });
    await gsap.to(current.container.querySelector('.footer'), { opacity: 0 });
  }
}

// ✅ Fast - queries DOM once
{
  async leave({ current }) {
    const h1 = current.container.querySelector('h1');
    const content = current.container.querySelector('.content');
    const footer = current.container.querySelector('.footer');

    const tl = gsap.timeline();

    tl.to(h1, { opacity: 0 })
      .to(content, { opacity: 0 }, '<')
      .to(footer, { opacity: 0 }, '<');

    await tl.play();
  }
}
```

### 5. Use force3D for Mobile

```javascript
gsap.to(element, {
  x: 100,
  force3D: true, // Force GPU acceleration
  duration: 0.5
});
```

---

## Common Issues

### Issue 1: Animation Doesn't Wait

**Problem**: Page transitions instantly without animation.

**Solution**: Always return promise or use `await`:

```javascript
// ❌ Wrong
leave({ current }) {
  gsap.to(current.container, { opacity: 0 });
}

// ✅ Correct
leave({ current }) {
  return gsap.to(current.container, { opacity: 0 });
}

// ✅ Also correct
async leave({ current }) {
  await gsap.to(current.container, { opacity: 0 });
}
```

### Issue 2: Flash of Content (FOUC)

**Problem**: New page visible before enter animation.

**Solution**: Set initial state in `beforeEnter` or CSS:

```javascript
beforeEnter({ next }) {
  gsap.set(next.container, { opacity: 0 });
}
```

Or in CSS:
```css
[data-barba="container"] {
  opacity: 0;
}
```

### Issue 3: Sync Mode Layout Shift

**Problem**: Containers stack during sync transitions.

**Solution**: Position absolutely during transition:

```css
[data-barba="wrapper"] {
  position: relative;
}

[data-barba="container"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
}
```

Or in JavaScript:
```javascript
{
  sync: true,
  beforeLeave({ current }) {
    gsap.set(current.container, {
      position: 'absolute',
      top: 0,
      width: '100%'
    });
  }
}
```

### Issue 4: ScrollTrigger Conflicts

**Problem**: ScrollTrigger instances persist after page change.

**Solution**: Kill ScrollTriggers in `beforeLeave`:

```javascript
import { ScrollTrigger } from 'gsap/ScrollTrigger';

barba.hooks.beforeLeave(() => {
  // Kill all ScrollTrigger instances
  ScrollTrigger.getAll().forEach(trigger => trigger.kill());
});

// Or use scoped instances
barba.init({
  views: [{
    namespace: 'home',
    afterEnter() {
      // Create ScrollTriggers
      this.scrollTriggers = [];

      this.scrollTriggers.push(
        ScrollTrigger.create({
          trigger: '.section',
          // ...
        })
      );
    },
    beforeLeave() {
      // Kill scoped ScrollTriggers
      this.scrollTriggers.forEach(trigger => trigger.kill());
    }
  }]
});
```

### Issue 5: Memory Leaks

**Problem**: Timelines/tweens accumulate.

**Solution**: Kill tweens before creating new ones:

```javascript
barba.hooks.beforeLeave(({ current }) => {
  // Kill all tweens on current page
  gsap.killTweensOf(current.container);
  gsap.killTweensOf(current.container.querySelectorAll('*'));
});
```

### Issue 6: Timeline Doesn't Await

**Problem**: Timeline starts but doesn't wait for completion.

**Solution**: Call `.play()` on timeline (it returns a promise):

```javascript
// ❌ Wrong
async leave({ current }) {
  const tl = gsap.timeline();
  tl.to(current.container, { opacity: 0 });
  // Timeline starts but function returns immediately
}

// ✅ Correct
async leave({ current }) {
  const tl = gsap.timeline();
  tl.to(current.container, { opacity: 0 });
  await tl.play(); // Wait for timeline to complete
}
```

---

## Easing Reference

Common GSAP easings for transitions:

```javascript
// Smooth and natural
ease: 'power2.inOut'

// Gentle acceleration
ease: 'power1.out'

// Strong deceleration
ease: 'power3.out'

// Bounce effect
ease: 'back.out(1.7)'

// Elastic effect
ease: 'elastic.out(1, 0.3)'

// Custom bezier
ease: 'cubic-bezier(0.4, 0, 0.2, 1)'
```

**Recommended for Barba transitions**:
- Leave: `'power2.in'` or `'power2.inOut'`
- Enter: `'power2.out'` or `'power3.out'`
