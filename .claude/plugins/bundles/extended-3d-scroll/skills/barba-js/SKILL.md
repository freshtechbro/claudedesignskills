---
name: barba-js
description: Page transitions library for creating fluid, smooth transitions between website pages. Use this skill when implementing page transitions, creating SPA-like experiences, adding animated route changes, or building websites with smooth navigation. Triggers on tasks involving Barba.js, page transitions, routing, view management, transition hooks, GSAP integration, or smooth page navigation. Works with gsap-scrolltrigger for transition animations.
---

# Barba.js

Modern page transition library for creating fluid, smooth transitions between website pages. Barba.js makes multi-page websites feel like Single Page Applications (SPAs) by hijacking navigation and managing transitions without full page reloads.

## Overview

Barba.js is a lightweight (7kb minified and compressed) JavaScript library that intercepts navigation between pages, fetches new content via AJAX, and smoothly transitions between old and new containers. It reduces page load delays and HTTP requests while maintaining the benefits of traditional multi-page architecture.

**Core Features**:
- Smooth page transitions without full reloads
- Lifecycle hooks for precise control over transition phases
- View-based logic for page-specific behaviors
- Built-in routing with @barba/router plugin
- Extensible plugin system
- Small footprint and high performance
- Framework-agnostic (works with vanilla JS, GSAP, anime.js, etc.)

## Core Concepts

### 1. Wrapper, Container, and Namespace

Barba.js uses a specific DOM structure to manage transitions:

**HTML Structure**:
```html
<body data-barba="wrapper">
  <!-- Static elements (header, nav) stay outside container -->
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
    </nav>
  </header>

  <!-- Dynamic content goes in container -->
  <main data-barba="container" data-barba-namespace="home">
    <!-- This content changes on navigation -->
    <h1>Home Page</h1>
    <p>Content that will transition out...</p>
  </main>

  <!-- Static footer outside container -->
  <footer>© 2025</footer>
</body>
```

**Three Key Elements**:

1. **Wrapper** (`data-barba="wrapper"`)
   - Outermost container
   - Everything inside wrapper but outside container stays persistent
   - Ideal for headers, navigation, footers that don't change

2. **Container** (`data-barba="container"`)
   - Dynamic content area that updates on navigation
   - Only this section gets replaced during transitions
   - Must exist on every page

3. **Namespace** (`data-barba-namespace="home"`)
   - Unique identifier for each page type
   - Used in transition rules and view logic
   - Examples: "home", "about", "product", "blog-post"

### 2. Transition Lifecycle

Barba.js follows a precise lifecycle for each navigation:

**Default Async Flow**:
1. User clicks link
2. Barba intercepts navigation
3. Prefetch next page (via AJAX)
4. Cache new content
5. **Leave hook** - Animate current page out
6. Wait for leave animation to complete
7. Remove old container, insert new container
8. **Enter hook** - Animate new page in
9. Wait for enter animation to complete
10. Update browser history

**Sync Flow** (with `sync: true`):
1. User clicks link
2. Barba intercepts navigation
3. Prefetch next page
4. Wait for new page to load
5. **Leave and Enter hooks run simultaneously** (crossfade effect)
6. Swap containers
7. Update browser history

### 3. Hooks

Barba provides 11 lifecycle hooks for controlling transitions:

**Hook Execution Order**:
```
Initial page load:
  beforeOnce → once → afterOnce

Every navigation:
  before → beforeLeave → leave → afterLeave →
  beforeEnter → enter → afterEnter → after
```

**Hook Types**:
- **Global hooks**: Run on every transition (`barba.hooks.before()`)
- **Transition hooks**: Defined within specific transition objects
- **View hooks**: Defined within view objects for page-specific logic

**Common Hook Use Cases**:
- `beforeLeave` - Reset scroll position, prepare animations
- `leave` - Animate current page out
- `afterLeave` - Clean up old page
- `beforeEnter` - Prepare new page (hide elements, set initial states)
- `enter` - Animate new page in
- `afterEnter` - Initialize page scripts, analytics tracking

### 4. Views

Views are page-specific logic containers that run based on namespace:

```javascript
barba.init({
  views: [{
    namespace: 'home',
    beforeEnter() {
      // Home-specific setup
      console.log('Entering home page');
    },
    afterEnter() {
      // Initialize home page features
      initHomeSlider();
    }
  }, {
    namespace: 'product',
    beforeEnter() {
      console.log('Entering product page');
    },
    afterEnter() {
      initProductGallery();
    }
  }]
});
```

## Common Patterns

### 1. Basic Setup

**Installation**:
```bash
npm install --save-dev @barba/core
# or
yarn add @barba/core --dev
```

**Minimal Configuration**:
```javascript
import barba from '@barba/core';

barba.init({
  transitions: [{
    name: 'default',
    leave({ current }) {
      // Fade out current page
      return gsap.to(current.container, {
        opacity: 0,
        duration: 0.5
      });
    },
    enter({ next }) {
      // Fade in new page
      return gsap.from(next.container, {
        opacity: 0,
        duration: 0.5
      });
    }
  }]
});
```

### 2. Fade Transition (Async)

Classic fade-out, fade-in transition:

```javascript
import barba from '@barba/core';
import gsap from 'gsap';

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
      // Start invisible
      gsap.set(next.container, { opacity: 0 });

      // Fade in
      await gsap.to(next.container, {
        opacity: 1,
        duration: 0.5,
        ease: 'power2.inOut'
      });
    }
  }]
});
```

### 3. Crossfade Transition (Sync)

Simultaneous fade between pages:

```javascript
barba.init({
  transitions: [{
    name: 'crossfade',
    sync: true, // Enable sync mode
    leave({ current }) {
      return gsap.to(current.container, {
        opacity: 0,
        duration: 0.8,
        ease: 'power2.inOut'
      });
    },
    enter({ next }) {
      return gsap.from(next.container, {
        opacity: 0,
        duration: 0.8,
        ease: 'power2.inOut'
      });
    }
  }]
});
```

### 4. Slide Transition with Overlap

Slide old page out, new page in with overlap:

```javascript
barba.init({
  transitions: [{
    name: 'slide',
    sync: true,
    leave({ current }) {
      return gsap.to(current.container, {
        x: '-100%',
        duration: 0.7,
        ease: 'power3.inOut'
      });
    },
    enter({ next }) {
      // Start off-screen right
      gsap.set(next.container, { x: '100%' });

      // Slide in from right
      return gsap.to(next.container, {
        x: '0%',
        duration: 0.7,
        ease: 'power3.inOut'
      });
    }
  }]
});
```

### 5. Transition Rules (Conditional Transitions)

Define different transitions based on navigation context:

```javascript
barba.init({
  transitions: [
    // Home to any page: fade
    {
      name: 'from-home-fade',
      from: { namespace: 'home' },
      leave({ current }) {
        return gsap.to(current.container, {
          opacity: 0,
          duration: 0.5
        });
      },
      enter({ next }) {
        return gsap.from(next.container, {
          opacity: 0,
          duration: 0.5
        });
      }
    },
    // Product to product: slide left
    {
      name: 'product-to-product',
      from: { namespace: 'product' },
      to: { namespace: 'product' },
      leave({ current }) {
        return gsap.to(current.container, {
          x: '-100%',
          duration: 0.6
        });
      },
      enter({ next }) {
        gsap.set(next.container, { x: '100%' });
        return gsap.to(next.container, {
          x: '0%',
          duration: 0.6
        });
      }
    },
    // Default fallback
    {
      name: 'default',
      leave({ current }) {
        return gsap.to(current.container, {
          opacity: 0,
          duration: 0.3
        });
      },
      enter({ next }) {
        return gsap.from(next.container, {
          opacity: 0,
          duration: 0.3
        });
      }
    }
  ]
});
```

### 6. Router Plugin for Route-Based Transitions

Use `@barba/router` for route-specific transitions:

**Installation**:
```bash
npm install --save-dev @barba/router
```

**Usage**:
```javascript
import barba from '@barba/core';
import barbaPrefetch from '@barba/prefetch';
import barbaRouter from '@barba/router';

// Define routes
barbaRouter.init({
  routes: [
    { path: '/', name: 'home' },
    { path: '/about', name: 'about' },
    { path: '/products/:id', name: 'product' }, // Dynamic segment
    { path: '/blog/:category/:slug', name: 'blog-post' }
  ]
});

barba.use(barbaRouter);
barba.use(barbaPrefetch); // Optional: prefetch on hover

barba.init({
  transitions: [{
    name: 'product-transition',
    to: { route: 'product' }, // Trigger on route name
    leave({ current }) {
      return gsap.to(current.container, {
        scale: 0.95,
        opacity: 0,
        duration: 0.5
      });
    },
    enter({ next }) {
      return gsap.from(next.container, {
        scale: 1.05,
        opacity: 0,
        duration: 0.5
      });
    }
  }]
});
```

### 7. Loading Indicator

Show loading state during page fetch:

```javascript
barba.init({
  transitions: [{
    async leave({ current }) {
      // Show loader
      const loader = document.querySelector('.loader');
      gsap.set(loader, { display: 'flex', opacity: 0 });
      gsap.to(loader, { opacity: 1, duration: 0.3 });

      // Fade out page
      await gsap.to(current.container, {
        opacity: 0,
        duration: 0.5
      });
    },
    async enter({ next }) {
      // Hide loader
      const loader = document.querySelector('.loader');
      await gsap.to(loader, { opacity: 0, duration: 0.3 });
      gsap.set(loader, { display: 'none' });

      // Fade in page
      await gsap.from(next.container, {
        opacity: 0,
        duration: 0.5
      });
    }
  }]
});
```

## Integration Patterns

### GSAP Integration

Barba.js works seamlessly with GSAP for animations:

**Timeline-Based Transitions**:
```javascript
import barba from '@barba/core';
import gsap from 'gsap';

barba.init({
  transitions: [{
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
      }, '-=0.2')
      .to(current.container, {
        opacity: 0,
        duration: 0.2
      });

      await tl.play();
    },
    async enter({ next }) {
      const tl = gsap.timeline();

      // Set initial states
      gsap.set(next.container, { opacity: 0 });
      gsap.set(next.container.querySelector('h1'), { y: 50, opacity: 0 });
      gsap.set(next.container.querySelector('.content'), { y: 30, opacity: 0 });

      tl.to(next.container, {
        opacity: 1,
        duration: 0.2
      })
      .to(next.container.querySelector('h1'), {
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
  }]
});
```

**Reference gsap-scrolltrigger skill** for advanced GSAP integration patterns.

### View-Specific Initialization

Initialize libraries or scripts per page:

```javascript
barba.init({
  views: [
    {
      namespace: 'home',
      afterEnter() {
        // Initialize home page features
        initHomepageSlider();
        initParallaxEffects();
      },
      beforeLeave() {
        // Clean up
        destroyHomepageSlider();
      }
    },
    {
      namespace: 'gallery',
      afterEnter() {
        initLightbox();
        initMasonry();
      },
      beforeLeave() {
        destroyLightbox();
      }
    }
  ]
});
```

### Analytics Tracking

Track page views on navigation:

```javascript
barba.hooks.after(() => {
  // Google Analytics
  if (typeof gtag !== 'undefined') {
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: window.location.pathname
    });
  }

  // Or use data layer
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'pageview',
    page: window.location.pathname
  });
});
```

### Third-Party Script Re-Initialization

Re-run scripts after page transitions:

```javascript
barba.hooks.after(() => {
  // Re-initialize third-party widgets
  if (typeof twttr !== 'undefined') {
    twttr.widgets.load(); // Twitter widgets
  }

  if (typeof FB !== 'undefined') {
    FB.XFBML.parse(); // Facebook widgets
  }

  // Re-run syntax highlighting
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }
});
```

## Performance Optimization

### 1. Prefetching

Use `@barba/prefetch` to load pages on hover:

```bash
npm install --save-dev @barba/prefetch
```

```javascript
import barba from '@barba/core';
import barbaPrefetch from '@barba/prefetch';

barba.use(barbaPrefetch);

barba.init({
  // Prefetch fires on link hover by default
  prefetch: {
    root: null, // Observe all links
    timeout: 3000 // Cache timeout in ms
  }
});
```

### 2. Prevent Layout Shift

Set container min-height to prevent content jump:

```css
[data-barba="container"] {
  min-height: 100vh;
  /* Or use viewport height minus header/footer */
  min-height: calc(100vh - 80px - 60px);
}
```

### 3. Optimize Animations

Use GPU-accelerated properties:

```javascript
// ✅ Good - GPU accelerated
gsap.to(element, {
  opacity: 0,
  x: -100,
  scale: 0.9,
  rotation: 45
});

// ❌ Avoid - causes reflow/repaint
gsap.to(element, {
  width: '50%',
  height: '300px',
  top: '100px'
});
```

### 4. Clean Up Event Listeners

Remove listeners in `beforeLeave` or view hooks:

```javascript
barba.init({
  views: [{
    namespace: 'home',
    afterEnter() {
      // Add listeners
      this.clickHandler = () => console.log('clicked');
      document.querySelector('.btn').addEventListener('click', this.clickHandler);
    },
    beforeLeave() {
      // Remove listeners
      document.querySelector('.btn').removeEventListener('click', this.clickHandler);
    }
  }]
});
```

### 5. Lazy Load Images

Defer image loading until after transition:

```javascript
barba.init({
  transitions: [{
    async enter({ next }) {
      // Complete transition first
      await gsap.from(next.container, {
        opacity: 0,
        duration: 0.5
      });

      // Then load images
      const images = next.container.querySelectorAll('img[data-src]');
      images.forEach(img => {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      });
    }
  }]
});
```

## Common Pitfalls

### 1. Forgetting to Return Promises

**Problem**: Transitions complete instantly without waiting for animations.

**Solution**: Always return promises or use `async/await`:

```javascript
// ❌ Wrong - animation starts but doesn't wait
leave({ current }) {
  gsap.to(current.container, { opacity: 0, duration: 0.5 });
}

// ✅ Correct - returns promise
leave({ current }) {
  return gsap.to(current.container, { opacity: 0, duration: 0.5 });
}

// ✅ Also correct - async/await
async leave({ current }) {
  await gsap.to(current.container, { opacity: 0, duration: 0.5 });
}
```

### 2. Not Preventing Default Link Behavior

**Problem**: Some links cause full page reloads.

**Solution**: Barba automatically prevents default on internal links, but you may need to exclude external links:

```javascript
barba.init({
  prevent: ({ href }) => {
    // Allow external links
    if (href.indexOf('http') > -1 && href.indexOf(window.location.host) === -1) {
      return true;
    }
    return false;
  }
});
```

### 3. CSS Conflicts Between Pages

**Problem**: Old page CSS affects new page layout during transition.

**Solution**: Use namespace-specific CSS or reset styles:

```css
/* Namespace-specific styles */
[data-barba-namespace="home"] .hero {
  background: blue;
}

[data-barba-namespace="about"] .hero {
  background: red;
}
```

Or reset in `beforeEnter`:

```javascript
beforeEnter({ next }) {
  // Reset scroll position
  window.scrollTo(0, 0);

  // Reset any global state
  document.body.classList.remove('menu-open');
}
```

### 4. Not Updating Document Title and Meta Tags

**Problem**: Page title and meta tags don't update on navigation.

**Solution**: Use `@barba/head` plugin or update manually:

```bash
npm install --save-dev @barba/head
```

```javascript
import barba from '@barba/core';
import barbaHead from '@barba/head';

barba.use(barbaHead);

barba.init({
  // Head plugin automatically updates <head> tags
});
```

Or manually:

```javascript
barba.hooks.after(({ next }) => {
  // Update title
  document.title = next.html.querySelector('title').textContent;

  // Update meta tags
  const newMeta = next.html.querySelectorAll('meta');
  newMeta.forEach(meta => {
    const name = meta.getAttribute('name') || meta.getAttribute('property');
    if (name) {
      const existing = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
      if (existing) {
        existing.setAttribute('content', meta.getAttribute('content'));
      }
    }
  });
});
```

### 5. Animation Flicker on Enter

**Problem**: New page flashes visible before enter animation starts.

**Solution**: Set initial invisible state in CSS or `beforeEnter`:

```css
/* CSS approach */
[data-barba="container"] {
  opacity: 0;
}

[data-barba="container"].is-visible {
  opacity: 1;
}
```

```javascript
// JavaScript approach
beforeEnter({ next }) {
  gsap.set(next.container, { opacity: 0 });
}
```

### 6. Sync Transitions Without Proper Positioning

**Problem**: Sync transitions cause layout shift as containers stack.

**Solution**: Position containers absolutely during transition:

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

Or manage in JavaScript:

```javascript
barba.init({
  transitions: [{
    sync: true,
    beforeLeave({ current }) {
      gsap.set(current.container, {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%'
      });
    }
  }]
});
```

## Resources

This skill includes:

### scripts/
Executable utilities for common Barba.js tasks:
- `transition_generator.py` - Generate transition boilerplate code
- `project_setup.py` - Initialize Barba.js project structure

### references/
Detailed documentation:
- `api_reference.md` - Complete Barba.js API (hooks, transitions, views, router)
- `hooks_guide.md` - All 11 hooks with execution order and use cases
- `gsap_integration.md` - GSAP animation patterns for Barba transitions
- `transition_patterns.md` - Common transition implementations

### assets/
Templates and starter projects:
- `starter_barba/` - Complete Barba.js + GSAP starter template
- `examples/` - Real-world transition implementations

## Related Skills

- **gsap-scrolltrigger** - For advanced GSAP animations in transitions
- **locomotive-scroll** - Can be combined with Barba for smooth scrolling between pages
- **motion-framer** - Alternative approach for React-based page transitions
