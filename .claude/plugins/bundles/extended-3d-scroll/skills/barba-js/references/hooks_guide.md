# Barba.js Hooks Guide

Comprehensive guide to all 11 Barba.js lifecycle hooks with execution order, use cases, and examples.

## Table of Contents

- [Hook Execution Order](#hook-execution-order)
- [Hook Types and Contexts](#hook-types-and-contexts)
- [Async Hook Patterns](#async-hook-patterns)
- [Individual Hooks](#individual-hooks)
- [Common Hook Patterns](#common-hook-patterns)
- [Best Practices](#best-practices)

---

## Hook Execution Order

### Initial Page Load

When the website first loads:

```
beforeOnce → once → afterOnce
```

**Timeline**:
1. `beforeOnce` - Setup before first render
2. `once` - Intro animation plays
3. `afterOnce` - Cleanup after first render

### Every Navigation

When navigating between pages:

```
before → beforeLeave → leave → afterLeave →
beforeEnter → enter → afterEnter → after
```

**Timeline**:
1. `before` - Transition starts
2. `beforeLeave` - Prepare to leave current page
3. `leave` - Animate current page out
4. `afterLeave` - Cleanup after leaving
5. **[Container swap happens here]**
6. `beforeEnter` - Prepare to enter new page
7. `enter` - Animate new page in
8. `afterEnter` - Initialize new page
9. `after` - Transition complete

### Sync Mode Execution Order

With `sync: true`, the order changes:

```
before → beforeLeave → beforeEnter →
(leave + enter simultaneously) →
afterLeave → afterEnter → after
```

**Key Difference**: `leave` and `enter` run at the same time (crossfade effect).

---

## Hook Types and Contexts

### 1. Global Hooks

Run on **every** transition, registered via `barba.hooks`:

```javascript
barba.hooks.before(() => {
  console.log('Every transition');
});

barba.hooks.afterEnter(({ next }) => {
  console.log('Entered:', next.namespace);
});
```

**Use for**:
- Universal behavior (analytics, scroll reset)
- Debug logging
- Loading indicators
- Third-party script re-initialization

### 2. Transition Hooks

Run when a **specific transition** matches:

```javascript
barba.init({
  transitions: [{
    name: 'fade',
    leave({ current }) {
      return gsap.to(current.container, { opacity: 0 });
    },
    enter({ next }) {
      return gsap.from(next.container, { opacity: 0 });
    }
  }]
});
```

**Use for**:
- Transition-specific animations
- Conditional behaviors based on navigation context

### 3. View Hooks

Run for **specific namespaces**:

```javascript
barba.init({
  views: [{
    namespace: 'home',
    afterEnter() {
      console.log('Home page entered');
      initHomeFeatures();
    },
    beforeLeave() {
      console.log('Leaving home page');
      cleanupHomeFeatures();
    }
  }]
});
```

**Use for**:
- Page-specific initialization
- Feature cleanup before leaving page

### Hook Availability Matrix

| Hook | Global | Transition | View |
|------|--------|------------|------|
| `beforeOnce` | ✅ | ✅ | ❌ |
| `once` | ✅ | ✅ | ❌ |
| `afterOnce` | ✅ | ✅ | ❌ |
| `before` | ✅ | ✅ | ❌ |
| `beforeLeave` | ✅ | ✅ | ✅ |
| `leave` | ✅ | ✅ | ❌ |
| `afterLeave` | ✅ | ✅ | ✅ |
| `beforeEnter` | ✅ | ✅ | ✅ |
| `enter` | ✅ | ✅ | ❌ |
| `afterEnter` | ✅ | ✅ | ✅ |
| `after` | ✅ | ✅ | ❌ |

---

## Async Hook Patterns

Hooks can be synchronous or asynchronous. Barba waits for async hooks to complete before continuing.

### Pattern 1: Returning Promises

```javascript
leave({ current }) {
  // Return the promise
  return gsap.to(current.container, {
    opacity: 0,
    duration: 0.5
  });
}
```

### Pattern 2: Async/Await

```javascript
async leave({ current }) {
  await gsap.to(current.container, {
    opacity: 0,
    duration: 0.5
  });

  // Can chain multiple awaits
  await someOtherAsyncOperation();
}
```

### Pattern 3: Manual async() Method

```javascript
leave({ current }) {
  const done = this.async();

  setTimeout(() => {
    gsap.to(current.container, { opacity: 0 });
    done(); // Signal completion
  }, 500);
}
```

### Pattern 4: Promise.all for Parallel Operations

```javascript
async leave({ current }) {
  // Run animations in parallel
  await Promise.all([
    gsap.to(current.container.querySelector('h1'), { opacity: 0 }),
    gsap.to(current.container.querySelector('.content'), { y: -50 }),
    fetch('/api/track-exit')
  ]);
}
```

---

## Individual Hooks

### beforeOnce

**Execution**: Before initial page load
**Available in**: Global, Transition
**Async**: Yes

**Purpose**: Setup before the first page renders.

**Common Use Cases**:
- Show loading screen
- Prepare intro animation
- Initial app setup

**Examples**:

```javascript
// Show loader
barba.hooks.beforeOnce(() => {
  document.querySelector('.loader').style.display = 'flex';
});

// In transition
{
  beforeOnce() {
    gsap.set('.intro-title', { opacity: 0, y: 50 });
  }
}
```

---

### once

**Execution**: During initial page load
**Available in**: Global, Transition
**Async**: Yes

**Purpose**: Animate the first page view (intro animation).

**Common Use Cases**:
- Intro animations
- Reveal content on first load
- Splash screen effects

**Examples**:

```javascript
// Simple fade in
{
  async once({ next }) {
    await gsap.from(next.container, {
      opacity: 0,
      duration: 1
    });
  }
}

// Complex intro sequence
{
  async once({ next }) {
    const tl = gsap.timeline();

    tl.to('.loader', { opacity: 0, duration: 0.5 })
      .set('.loader', { display: 'none' })
      .from('.intro-title', { opacity: 0, y: 50, duration: 0.8 })
      .from('.intro-subtitle', { opacity: 0, y: 30, duration: 0.6 }, '-=0.4')
      .from(next.container, { opacity: 0, duration: 0.5 });

    await tl.play();
  }
}
```

---

### afterOnce

**Execution**: After initial page load
**Available in**: Global, Transition
**Async**: Yes

**Purpose**: Cleanup or initialization after intro animation.

**Common Use Cases**:
- Hide loading screen
- Initialize page features
- Track page load

**Examples**:

```javascript
barba.hooks.afterOnce(() => {
  // Hide loader
  document.querySelector('.loader').style.display = 'none';

  // Track page load
  gtag('event', 'page_load', { page: window.location.pathname });
});
```

---

### before

**Execution**: Before every transition starts
**Available in**: Global, Transition
**Async**: Yes

**Purpose**: Setup before transition begins.

**Common Use Cases**:
- Show loading indicator
- Prepare global state
- Disable interactions during transition

**Examples**:

```javascript
// Global loading indicator
barba.hooks.before(() => {
  document.body.classList.add('is-transitioning');
  document.querySelector('.page-loader').classList.add('active');
});

// Disable scroll during transition
barba.hooks.before(() => {
  document.body.style.overflow = 'hidden';
});
```

---

### beforeLeave

**Execution**: Before leaving current page
**Available in**: Global, Transition, View
**Async**: Yes

**Purpose**: Prepare current page before leave animation.

**Common Use Cases**:
- Reset scroll position
- Prepare elements for leave animation
- Save page state

**Examples**:

```javascript
// Reset scroll (global)
barba.hooks.beforeLeave(() => {
  window.scrollTo(0, 0);
});

// Prepare animation elements
{
  beforeLeave({ current }) {
    // Reset any transforms that might interfere
    gsap.set(current.container.querySelectorAll('.animated'), {
      clearProps: 'all'
    });
  }
}

// View-specific cleanup
{
  views: [{
    namespace: 'gallery',
    beforeLeave() {
      // Save scroll position for this page
      sessionStorage.setItem('galleryScroll', window.scrollY);
    }
  }]
}
```

---

### leave

**Execution**: Current page exit animation
**Available in**: Global, Transition
**Async**: Yes (must return promise or use async/await)

**Purpose**: Animate current page out.

**Common Use Cases**:
- Fade out animation
- Slide out animation
- Complex exit sequences

**Examples**:

```javascript
// Simple fade out
{
  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      duration: 0.5
    });
  }
}

// Slide out left
{
  leave({ current }) {
    return gsap.to(current.container, {
      x: '-100%',
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}

// Complex staggered exit
{
  async leave({ current }) {
    const tl = gsap.timeline();

    tl.to(current.container.querySelector('h1'), {
      y: -50,
      opacity: 0,
      duration: 0.3
    })
    .to(current.container.querySelectorAll('.content > *'), {
      y: -30,
      opacity: 0,
      duration: 0.3,
      stagger: 0.05
    }, '-=0.2')
    .to(current.container, {
      opacity: 0,
      duration: 0.2
    });

    await tl.play();
  }
}
```

---

### afterLeave

**Execution**: After leaving current page
**Available in**: Global, Transition, View
**Async**: Yes

**Purpose**: Cleanup after current page has animated out.

**Common Use Cases**:
- Remove event listeners
- Clean up third-party widgets
- Debug logging

**Examples**:

```javascript
// Global cleanup
barba.hooks.afterLeave(({ current }) => {
  console.log('Left page:', current.namespace);
});

// View-specific cleanup
{
  views: [{
    namespace: 'video-gallery',
    afterLeave({ current }) {
      // Pause all videos
      current.container.querySelectorAll('video').forEach(video => {
        video.pause();
        video.currentTime = 0;
      });

      // Remove event listeners
      current.container.querySelectorAll('.video-play').forEach(btn => {
        btn.removeEventListener('click', handleVideoPlay);
      });
    }
  }]
}
```

---

### beforeEnter

**Execution**: Before entering new page
**Available in**: Global, Transition, View
**Async**: Yes

**Purpose**: Prepare new page before enter animation.

**Common Use Cases**:
- Set initial animation states
- Load images
- Prepare page-specific features

**Examples**:

```javascript
// Set initial state for animation
{
  beforeEnter({ next }) {
    gsap.set(next.container, { opacity: 0 });
  }
}

// Load images
barba.hooks.beforeEnter(({ next }) => {
  const images = next.container.querySelectorAll('img[data-src]');
  images.forEach(img => {
    img.src = img.dataset.src;
    img.removeAttribute('data-src');
  });
});

// Restore scroll position
{
  views: [{
    namespace: 'gallery',
    beforeEnter() {
      const savedScroll = sessionStorage.getItem('galleryScroll');
      if (savedScroll) {
        window.scrollTo(0, parseInt(savedScroll));
      }
    }
  }]
}
```

---

### enter

**Execution**: New page entrance animation
**Available in**: Global, Transition
**Async**: Yes (must return promise or use async/await)

**Purpose**: Animate new page in.

**Common Use Cases**:
- Fade in animation
- Slide in animation
- Complex entrance sequences

**Examples**:

```javascript
// Simple fade in
{
  async enter({ next }) {
    await gsap.from(next.container, {
      opacity: 0,
      duration: 0.5
    });
  }
}

// Slide in from right
{
  enter({ next }) {
    return gsap.from(next.container, {
      x: '100%',
      duration: 0.6,
      ease: 'power2.inOut'
    });
  }
}

// Complex staggered entrance
{
  async enter({ next }) {
    const tl = gsap.timeline();

    // Set initial states
    gsap.set(next.container, { opacity: 1 });
    gsap.set(next.container.querySelector('h1'), { y: 50, opacity: 0 });
    gsap.set(next.container.querySelectorAll('.content > *'), { y: 30, opacity: 0 });

    tl.to(next.container.querySelector('h1'), {
      y: 0,
      opacity: 1,
      duration: 0.5,
      ease: 'power3.out'
    })
    .to(next.container.querySelectorAll('.content > *'), {
      y: 0,
      opacity: 1,
      duration: 0.5,
      stagger: 0.05,
      ease: 'power2.out'
    }, '-=0.3');

    await tl.play();
  }
}
```

---

### afterEnter

**Execution**: After entering new page
**Available in**: Global, Transition, View
**Async**: Yes

**Purpose**: Initialize features after new page has animated in.

**Common Use Cases**:
- Initialize page features
- Track page views
- Start auto-playing content

**Examples**:

```javascript
// Global analytics tracking
barba.hooks.afterEnter(({ next }) => {
  gtag('config', 'GA_MEASUREMENT_ID', {
    page_path: next.url.path,
    page_title: document.title
  });
});

// Re-initialize third-party scripts
barba.hooks.afterEnter(() => {
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }

  if (typeof twttr !== 'undefined') {
    twttr.widgets.load();
  }
});

// View-specific initialization
{
  views: [
    {
      namespace: 'home',
      afterEnter() {
        initHomeSlider();
        initParallaxEffects();
      }
    },
    {
      namespace: 'product',
      afterEnter({ next }) {
        const productId = next.url.path.split('/').pop();
        loadProductData(productId);
      }
    },
    {
      namespace: 'video',
      afterEnter({ next }) {
        const video = next.container.querySelector('video');
        if (video) {
          video.play();
        }
      }
    }
  ]
}
```

---

### after

**Execution**: After every transition completes
**Available in**: Global, Transition
**Async**: Yes

**Purpose**: Final cleanup after transition.

**Common Use Cases**:
- Hide loading indicators
- Re-enable interactions
- Debug logging

**Examples**:

```javascript
// Global loading indicator
barba.hooks.after(() => {
  document.body.classList.remove('is-transitioning');
  document.querySelector('.page-loader').classList.remove('active');
});

// Re-enable scroll
barba.hooks.after(() => {
  document.body.style.overflow = '';
});

// Debug transition
barba.hooks.after(({ current, next }) => {
  console.log(`Transition complete: ${current.namespace} → ${next.namespace}`);
});
```

---

## Common Hook Patterns

### Pattern 1: Loading Indicator

```javascript
barba.hooks.before(() => {
  gsap.to('.loader', { opacity: 1, duration: 0.3 });
});

barba.hooks.after(() => {
  gsap.to('.loader', { opacity: 0, duration: 0.3 });
});
```

### Pattern 2: Scroll Management

```javascript
barba.hooks.beforeLeave(() => {
  // Save current scroll position
  sessionStorage.setItem('scrollPos', window.scrollY);
});

barba.hooks.beforeEnter(({ next }) => {
  // Reset to top for new pages
  window.scrollTo(0, 0);

  // Or restore scroll for same page
  // const savedScroll = sessionStorage.getItem('scrollPos');
  // if (savedScroll) window.scrollTo(0, parseInt(savedScroll));
});
```

### Pattern 3: Analytics Tracking

```javascript
barba.hooks.after(({ next }) => {
  // Google Analytics 4
  gtag('config', 'GA_MEASUREMENT_ID', {
    page_path: next.url.path,
    page_title: document.title
  });

  // Or GTM data layer
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'pageview',
    page: next.url.path
  });
});
```

### Pattern 4: Third-Party Script Re-Init

```javascript
barba.hooks.afterEnter(() => {
  // Syntax highlighting
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }

  // Social widgets
  if (typeof twttr !== 'undefined') {
    twttr.widgets.load();
  }

  if (typeof FB !== 'undefined') {
    FB.XFBML.parse();
  }

  // Custom form library
  if (typeof customForms !== 'undefined') {
    customForms.init();
  }
});
```

### Pattern 5: View-Specific Features

```javascript
barba.init({
  views: [
    {
      namespace: 'home',
      afterEnter() {
        initHomeSlider();
        initParallax();
      },
      beforeLeave() {
        destroyHomeSlider();
      }
    },
    {
      namespace: 'shop',
      afterEnter() {
        initProductFilters();
        initAddToCart();
      },
      beforeLeave() {
        // Cleanup
        document.querySelectorAll('.product-quick-view').forEach(el => {
          el.remove();
        });
      }
    }
  ]
});
```

### Pattern 6: Conditional Transitions

```javascript
barba.init({
  transitions: [
    // Slow fade for first visit
    {
      name: 'first-visit',
      once: async ({ next }) => {
        await gsap.from(next.container, {
          opacity: 0,
          duration: 1.5
        });
      }
    },
    // Fast fade for same namespace
    {
      name: 'same-page-type',
      custom: ({ current, next }) => current.namespace === next.namespace,
      leave: ({ current }) => {
        return gsap.to(current.container, { opacity: 0, duration: 0.2 });
      },
      enter: ({ next }) => {
        return gsap.from(next.container, { opacity: 0, duration: 0.2 });
      }
    },
    // Slower transition for different page types
    {
      name: 'different-page-type',
      leave: ({ current }) => {
        return gsap.to(current.container, { opacity: 0, duration: 0.5 });
      },
      enter: ({ next }) => {
        return gsap.from(next.container, { opacity: 0, duration: 0.5 });
      }
    }
  ]
});
```

---

## Best Practices

### 1. Always Return Promises or Use Async/Await

```javascript
// ❌ Wrong - animation won't wait
leave({ current }) {
  gsap.to(current.container, { opacity: 0 });
}

// ✅ Correct - returns promise
leave({ current }) {
  return gsap.to(current.container, { opacity: 0 });
}

// ✅ Also correct - async/await
async leave({ current }) {
  await gsap.to(current.container, { opacity: 0 });
}
```

### 2. Use Global Hooks for Universal Behavior

```javascript
// ✅ Good - analytics tracking applies everywhere
barba.hooks.after(({ next }) => {
  gtag('config', 'GA_ID', { page_path: next.url.path });
});

// ❌ Avoid - repeating in every transition
{
  transitions: [{
    after({ next }) {
      gtag('config', 'GA_ID', { page_path: next.url.path });
    }
  }]
}
```

### 3. Use View Hooks for Page-Specific Logic

```javascript
// ✅ Good - isolated to home page
{
  views: [{
    namespace: 'home',
    afterEnter() {
      initHomeSlider();
    }
  }]
}

// ❌ Avoid - checking namespace manually
barba.hooks.afterEnter(({ next }) => {
  if (next.namespace === 'home') {
    initHomeSlider();
  }
});
```

### 4. Clean Up in beforeLeave, Not afterLeave

```javascript
// ✅ Good - cleanup before leaving
{
  views: [{
    namespace: 'video',
    beforeLeave({ current }) {
      current.container.querySelectorAll('video').forEach(v => v.pause());
    }
  }]
}

// ❌ Risky - container might already be removed
{
  views: [{
    namespace: 'video',
    afterLeave({ current }) {
      // current.container might not be in DOM anymore
      current.container.querySelectorAll('video').forEach(v => v.pause());
    }
  }]
}
```

### 5. Set Initial States in beforeEnter, Not enter

```javascript
// ✅ Good - prevents flash of content
{
  beforeEnter({ next }) {
    gsap.set(next.container, { opacity: 0 });
  },
  enter({ next }) {
    return gsap.to(next.container, { opacity: 1 });
  }
}

// ❌ Risky - might flash visible
{
  enter({ next }) {
    return gsap.from(next.container, { opacity: 0 });
  }
}
```

### 6. Use Hook Contexts Appropriately

```javascript
// ✅ Correct usage
barba.init({
  // Global hooks - universal behavior
  hooks: {
    after: () => { /* ... */ }
  },

  // Transitions - animation logic
  transitions: [{
    leave() { /* ... */ },
    enter() { /* ... */ }
  }],

  // Views - page-specific logic
  views: [{
    namespace: 'home',
    afterEnter() { /* ... */ }
  }]
});
```

### 7. Handle Errors Gracefully

```javascript
barba.hooks.afterEnter(({ next }) => {
  try {
    initPageFeatures(next.container);
  } catch (error) {
    console.error('Failed to initialize page features:', error);
    // Fallback or report error
  }
});
```
