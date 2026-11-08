# Barba.js API Reference

Complete reference for Barba.js core API, plugins, and configuration options.

## Table of Contents

- [Core API](#core-api)
  - [barba.init()](#barbainit)
  - [barba.go()](#barbago)
  - [barba.hooks](#barbahooks)
  - [barba.history](#barbahistory)
  - [barba.url](#barbaurl)
  - [barba.use()](#barbause)
- [Transitions](#transitions)
- [Views](#views)
- [Hooks](#hooks)
- [Data Object](#data-object)
- [Router Plugin](#router-plugin)
- [Prefetch Plugin](#prefetch-plugin)
- [CSS Plugin](#css-plugin)
- [Head Plugin](#head-plugin)

---

## Core API

### barba.init()

Initialize Barba with configuration options.

**Syntax**:
```javascript
barba.init({
  debug: false,
  logLevel: 'off',
  timeout: 2000,
  cacheIgnore: false,
  preventRunning: true,
  prevent: null,
  requestError: null,
  schema: {
    prefix: 'data-barba',
    wrapper: 'wrapper',
    container: 'container',
    namespace: 'namespace'
  },
  transitions: [],
  views: []
});
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `debug` | `boolean` | `false` | Enable debug mode (logs to console) |
| `logLevel` | `string` | `'off'` | Logging level: `'off'`, `'error'`, `'warning'`, `'info'`, `'debug'` |
| `timeout` | `number` | `2000` | Request timeout in milliseconds |
| `cacheIgnore` | `boolean\|string\|function` | `false` | Disable cache, specific query string, or custom function |
| `preventRunning` | `boolean` | `true` | Prevent transitions if one is already running |
| `prevent` | `function` | `null` | Custom function to prevent Barba on specific links |
| `requestError` | `function` | `null` | Custom request error handler |
| `schema` | `object` | See above | Custom data attribute names |
| `transitions` | `array` | `[]` | Array of transition objects |
| `views` | `array` | `[]` | Array of view objects |

**Examples**:

```javascript
// Minimal setup
barba.init();

// Custom configuration
barba.init({
  debug: true,
  timeout: 5000,
  prevent: ({ el, href }) => {
    // Prevent external links
    return href.indexOf('http') > -1 && href.indexOf(window.location.host) === -1;
  },
  requestError: (trigger, action, url, response) => {
    // Redirect to 404 page
    if (action === 'click' && response.status === 404) {
      barba.go('/404');
    }
  }
});

// Custom schema (use different data attributes)
barba.init({
  schema: {
    prefix: 'data-custom',
    wrapper: 'page-wrapper',
    container: 'page-container',
    namespace: 'page-type'
  }
});
```

### barba.go()

Programmatically navigate to a URL.

**Syntax**:
```javascript
barba.go(href, trigger, event);
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `href` | `string` | - | Target URL (relative or absolute) |
| `trigger` | `string` | `'barba'` | Trigger identifier (appears in `data.trigger`) |
| `event` | `object` | `null` | Event object (appears in `data.event`) |

**Examples**:

```javascript
// Navigate to URL
barba.go('/about');

// Navigate with custom trigger
barba.go('/contact', 'custom-button');

// Navigate with event data
barba.go('/products/123', 'product-link', { productId: 123 });

// Conditional navigation
if (userLoggedIn) {
  barba.go('/dashboard');
} else {
  barba.go('/login');
}
```

### barba.hooks

Global hooks object for registering lifecycle hooks.

**Available Hooks**:

All hooks receive a `data` object as parameter:

```javascript
barba.hooks.beforeOnce(data => { /* ... */ });
barba.hooks.once(data => { /* ... */ });
barba.hooks.afterOnce(data => { /* ... */ });
barba.hooks.before(data => { /* ... */ });
barba.hooks.beforeLeave(data => { /* ... */ });
barba.hooks.leave(data => { /* ... */ });
barba.hooks.afterLeave(data => { /* ... */ });
barba.hooks.beforeEnter(data => { /* ... */ });
barba.hooks.enter(data => { /* ... */ });
barba.hooks.afterEnter(data => { /* ... */ });
barba.hooks.after(data => { /* ... */ });
```

**Examples**:

```javascript
// Reset scroll on every transition
barba.hooks.beforeEnter(() => {
  window.scrollTo(0, 0);
});

// Track page views
barba.hooks.after(({ next }) => {
  gtag('config', 'GA_MEASUREMENT_ID', {
    page_path: next.url.path
  });
});

// Show/hide loading indicator
barba.hooks.before(() => {
  document.querySelector('.loader').classList.add('active');
});

barba.hooks.after(() => {
  document.querySelector('.loader').classList.remove('active');
});

// Re-initialize scripts
barba.hooks.afterEnter(() => {
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }
});
```

### barba.history

Access browser history and navigation state.

**Properties**:

| Property | Type | Description |
|----------|------|-------------|
| `previous` | `object` | Previous page data |
| `current` | `object` | Current page data |
| `size` | `number` | Number of items in history |
| `direction` | `string` | Navigation direction: `'forward'`, `'back'`, or `null` |

**Methods**:

| Method | Description |
|--------|-------------|
| `add(url, trigger)` | Add entry to history |
| `cancel()` | Cancel current transition |

**Examples**:

```javascript
// Check navigation direction
barba.hooks.before(({ current, next }) => {
  const direction = barba.history.direction;

  if (direction === 'back') {
    console.log('User went back');
  } else if (direction === 'forward') {
    console.log('User went forward');
  } else {
    console.log('Normal navigation');
  }
});

// Access previous page
const previousUrl = barba.history.previous.url.href;
const previousNamespace = barba.history.previous.namespace;

// Cancel transition programmatically
if (someCondition) {
  barba.history.cancel();
}
```

### barba.url

URL manipulation utilities.

**Methods**:

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `getAbsoluteHref(href)` | `string` | `string` | Convert relative URL to absolute |
| `getHref(url)` | `string` | `string` | Get clean href (without hash) |
| `getOrigin(url)` | `string` | `string` | Get origin from URL |
| `getPath(url)` | `string` | `string` | Get path from URL |
| `getPathname(url)` | `string` | `string` | Get pathname from URL |
| `getPort(url)` | `string` | `string` | Get port from URL |

**Examples**:

```javascript
// Get absolute URL
const absolute = barba.url.getAbsoluteHref('/about');
// Returns: "https://example.com/about"

// Get path without query/hash
const path = barba.url.getPath('/products?id=123#details');
// Returns: "/products"

// Get pathname
const pathname = barba.url.getPathname('https://example.com/blog/post-1');
// Returns: "/blog/post-1"
```

### barba.use()

Register Barba plugins.

**Syntax**:
```javascript
barba.use(plugin, options);
```

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `plugin` | `object` | Plugin object with `install()` method |
| `options` | `object` | Plugin-specific options |

**Examples**:

```javascript
import barba from '@barba/core';
import barbaRouter from '@barba/router';
import barbaPrefetch from '@barba/prefetch';
import barbaHead from '@barba/head';

// Register router
barba.use(barbaRouter, {
  routes: [
    { path: '/', name: 'home' },
    { path: '/about', name: 'about' }
  ]
});

// Register prefetch
barba.use(barbaPrefetch);

// Register head plugin
barba.use(barbaHead);

barba.init();
```

---

## Transitions

Transition objects define how pages animate during navigation.

**Transition Object Structure**:

```javascript
{
  name: 'transition-name',
  from: { /* rules */ },
  to: { /* rules */ },
  sync: false,
  once() { /* ... */ },
  leave() { /* ... */ },
  enter() { /* ... */ },
  // ... other hooks
}
```

**Properties**:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `name` | `string` | - | Unique transition identifier |
| `from` | `object` | - | Rules for leaving page |
| `to` | `object` | - | Rules for entering page |
| `sync` | `boolean` | `false` | Sync mode (play leave/enter simultaneously) |

**Rules**:

Rules determine when a transition applies:

```javascript
// Namespace rule
{ namespace: 'home' }
{ namespace: ['home', 'about'] }

// Route rule (requires @barba/router)
{ route: 'product' }

// Custom rule
{ custom: ({ current, next }) => current.namespace === next.namespace }
```

**Rule Priority** (highest to lowest):
1. `custom`
2. `route` (requires @barba/router)
3. `namespace`

**Transition Selection Examples**:

```javascript
barba.init({
  transitions: [
    // Only from home
    {
      name: 'from-home',
      from: { namespace: 'home' }
    },

    // Only to about
    {
      name: 'to-about',
      to: { namespace: 'about' }
    },

    // From home to about
    {
      name: 'home-to-about',
      from: { namespace: 'home' },
      to: { namespace: 'about' }
    },

    // Multiple namespaces
    {
      name: 'from-pages',
      from: { namespace: ['about', 'contact', 'services'] }
    },

    // Custom rule
    {
      name: 'same-namespace',
      custom: ({ current, next }) => current.namespace === next.namespace
    },

    // Always matches (fallback)
    {
      name: 'default'
    }
  ]
});
```

**Sync Mode**:

```javascript
// Async (default): leave → wait → swap → enter
{
  sync: false,
  async leave({ current }) {
    await gsap.to(current.container, { opacity: 0 });
  },
  async enter({ next }) {
    await gsap.from(next.container, { opacity: 0 });
  }
}

// Sync: wait → (leave + enter simultaneously) → swap
{
  sync: true,
  leave({ current }) {
    return gsap.to(current.container, { opacity: 0 });
  },
  enter({ next }) {
    return gsap.from(next.container, { opacity: 0 });
  }
}
```

---

## Views

View objects provide page-specific logic based on namespace.

**View Object Structure**:

```javascript
{
  namespace: 'page-namespace',
  beforeOnce() { /* ... */ },
  afterOnce() { /* ... */ },
  beforeLeave() { /* ... */ },
  afterLeave() { /* ... */ },
  beforeEnter() { /* ... */ },
  afterEnter() { /* ... */ }
}
```

**Properties**:

| Property | Type | Description |
|----------|------|-------------|
| `namespace` | `string` | Target namespace (matches `data-barba-namespace`) |

**Examples**:

```javascript
barba.init({
  views: [
    {
      namespace: 'home',
      beforeEnter() {
        console.log('About to enter home page');
      },
      afterEnter() {
        // Initialize home-specific features
        initHomeSlider();
        initParallax();
      },
      beforeLeave() {
        // Clean up
        destroyHomeSlider();
      }
    },
    {
      namespace: 'product',
      afterEnter({ next }) {
        // Get product ID from URL
        const productId = next.url.path.split('/').pop();
        loadProduct(productId);
      }
    },
    {
      namespace: 'gallery',
      afterEnter() {
        initMasonry();
        initLightbox();
      },
      beforeLeave() {
        destroyMasonry();
        destroyLightbox();
      }
    }
  ]
});
```

---

## Hooks

Complete reference for all 11 Barba.js hooks.

### Hook Execution Order

**Initial page load**:
```
beforeOnce → once → afterOnce
```

**Every navigation**:
```
before → beforeLeave → leave → afterLeave →
beforeEnter → enter → afterEnter → after
```

### Hook Contexts

Hooks can be defined in three places:

1. **Global hooks**: Run on every transition
   ```javascript
   barba.hooks.before(() => { /* ... */ });
   ```

2. **Transition hooks**: Run when that transition matches
   ```javascript
   barba.init({
     transitions: [{
       name: 'fade',
       leave() { /* ... */ }
     }]
   });
   ```

3. **View hooks**: Run for specific namespaces
   ```javascript
   barba.init({
     views: [{
       namespace: 'home',
       afterEnter() { /* ... */ }
     }]
   });
   ```

### Async Hooks

Hooks can be synchronous or asynchronous:

```javascript
// Synchronous
leave({ current }) {
  current.container.style.opacity = 0;
}

// Promise
leave({ current }) {
  return gsap.to(current.container, { opacity: 0 });
}

// Async/await
async leave({ current }) {
  await gsap.to(current.container, { opacity: 0 });
}

// Manual async with this.async()
leave({ current }) {
  const done = this.async();

  setTimeout(() => {
    gsap.to(current.container, { opacity: 0 });
    done();
  }, 500);
}
```

### Individual Hook Reference

#### beforeOnce

Runs once before initial page load (before `once` hook).

**Available in**: Transitions only
**When**: Before first page render
**Use for**: Initial setup, loading screens

```javascript
{
  beforeOnce() {
    console.log('Before initial page render');
    document.querySelector('.loader').classList.add('visible');
  }
}
```

#### once

Runs once on initial page load (animations for first view).

**Available in**: Transitions only
**When**: During first page render
**Use for**: Intro animations

```javascript
{
  async once({ next }) {
    await gsap.from(next.container, {
      opacity: 0,
      y: 50,
      duration: 1
    });
  }
}
```

#### afterOnce

Runs once after initial page load (after `once` hook).

**Available in**: Transitions only
**When**: After first page render completes
**Use for**: Post-intro initialization

```javascript
{
  afterOnce() {
    document.querySelector('.loader').classList.remove('visible');
    console.log('Initial page loaded');
  }
}
```

#### before

Runs before every transition starts.

**Available in**: Transitions only
**When**: Start of every navigation (except first load)
**Use for**: Pre-transition setup, loading indicators

```javascript
{
  before() {
    document.querySelector('.loader').classList.add('visible');
    console.log('Transition starting');
  }
}
```

#### beforeLeave

Runs before leaving current page.

**Available in**: Transitions and Views
**When**: Before leave animation
**Use for**: Preparing leave animation, resetting scroll

```javascript
{
  beforeLeave({ current }) {
    // Reset scroll
    window.scrollTo(0, 0);

    // Prepare elements
    gsap.set(current.container.querySelectorAll('.fade'), { opacity: 1 });
  }
}
```

#### leave

Main hook for animating current page out.

**Available in**: Transitions only
**When**: Current page exit animation
**Use for**: Exit animations

```javascript
{
  async leave({ current }) {
    await gsap.to(current.container, {
      opacity: 0,
      x: -100,
      duration: 0.5
    });
  }
}
```

#### afterLeave

Runs after leaving current page.

**Available in**: Transitions and Views
**When**: After leave animation completes
**Use for**: Cleanup, removing event listeners

```javascript
{
  afterLeave({ current }) {
    // Remove event listeners
    current.container.querySelectorAll('button').forEach(btn => {
      btn.removeEventListener('click', handleClick);
    });

    console.log('Left page:', current.namespace);
  }
}
```

#### beforeEnter

Runs before entering new page.

**Available in**: Transitions and Views
**When**: Before enter animation (after new container inserted)
**Use for**: Preparing enter animation, setting initial states

```javascript
{
  beforeEnter({ next }) {
    // Set initial state for enter animation
    gsap.set(next.container, { opacity: 0, x: 100 });

    // Prepare page-specific elements
    const images = next.container.querySelectorAll('img[data-src]');
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  }
}
```

#### enter

Main hook for animating new page in.

**Available in**: Transitions only
**When**: New page entrance animation
**Use for**: Entrance animations

```javascript
{
  async enter({ next }) {
    await gsap.to(next.container, {
      opacity: 1,
      x: 0,
      duration: 0.5
    });
  }
}
```

#### afterEnter

Runs after entering new page.

**Available in**: Transitions and Views
**When**: After enter animation completes
**Use for**: Initializing page features, analytics

```javascript
{
  afterEnter({ next }) {
    // Initialize page features
    initSlider(next.container);

    // Track page view
    gtag('config', 'GA_ID', {
      page_path: next.url.path
    });

    console.log('Entered page:', next.namespace);
  }
}
```

#### after

Runs after every transition completes.

**Available in**: Transitions only
**When**: End of every navigation (except first load)
**Use for**: Final cleanup, hiding loading indicators

```javascript
{
  after() {
    document.querySelector('.loader').classList.remove('visible');
    console.log('Transition complete');
  }
}
```

---

## Data Object

All hooks receive a `data` object with information about current and next pages.

**Data Object Structure**:

```javascript
{
  current: {
    container: HTMLElement,
    html: string,
    namespace: string,
    url: { href, path, port, query }
  },
  next: {
    container: HTMLElement,
    html: string,
    namespace: string,
    url: { href, path, port, query }
  },
  trigger: string | HTMLElement,
  event: Event
}
```

**Properties**:

### current

Information about the page being left.

| Property | Type | Description |
|----------|------|-------------|
| `container` | `HTMLElement` | Current page's `data-barba="container"` element |
| `html` | `string` | Full HTML of current page |
| `namespace` | `string` | Current page namespace |
| `url` | `object` | URL information |
| `url.href` | `string` | Full URL |
| `url.path` | `string` | Path without query/hash |
| `url.port` | `string` | Port number |
| `url.query` | `object` | Query parameters as key-value pairs |

### next

Information about the page being entered.

Same structure as `current`.

### trigger

Source of the navigation.

| Value | Type | Description |
|-------|------|-------------|
| Link element | `HTMLElement` | User clicked a link |
| `'barba'` | `string` | Programmatic navigation via `barba.go()` |
| `'back'` | `string` | Browser back button |
| `'forward'` | `string` | Browser forward button |

### event

The triggering event object (if navigation was from user interaction).

**Usage Examples**:

```javascript
barba.hooks.before(({ current, next, trigger, event }) => {
  console.log('Leaving:', current.namespace);
  console.log('Entering:', next.namespace);
  console.log('Current URL:', current.url.href);
  console.log('Next URL:', next.url.href);
  console.log('Trigger:', trigger);

  // Check trigger type
  if (trigger === 'back') {
    console.log('User went back');
  } else if (trigger instanceof HTMLElement) {
    console.log('User clicked:', trigger.href);
  }

  // Access query parameters
  if (next.url.query.id) {
    console.log('Product ID:', next.url.query.id);
  }
});
```

---

## Router Plugin

**Package**: `@barba/router`

Add route-based transition rules using path patterns.

**Installation**:
```bash
npm install --save-dev @barba/router
```

**API**:

```javascript
import barbaRouter from '@barba/router';

barbaRouter.init({
  routes: [
    { path: '/', name: 'home' },
    { path: '/about', name: 'about' },
    { path: '/products/:id', name: 'product' },
    { path: '/blog/:category/:slug', name: 'blog-post' },
    { path: '/:lang(en|fr)/:page', name: 'localized-page' }
  ]
});

barba.use(barbaRouter);
```

**Route Properties**:

| Property | Type | Description |
|----------|------|-------------|
| `path` | `string` | URL pattern (supports path-to-regexp syntax) |
| `name` | `string` | Route name (used in transition rules) |

**Path Patterns**:

```javascript
'/products/:id'              // Dynamic segment
'/blog/:category/:slug'      // Multiple segments
'/:lang(en|fr)/:page'        // Alternatives
'/files/:path*'              // Wildcard (0 or more)
'/files/:path+'              // Wildcard (1 or more)
'/products/:id?'             // Optional segment
```

**Usage in Transitions**:

```javascript
barba.init({
  transitions: [{
    name: 'product-transition',
    to: { route: 'product' },  // Matches route name
    enter({ next }) {
      // Get route params from URL
      const productId = next.url.path.split('/').pop();
      console.log('Loading product:', productId);
    }
  }]
});
```

---

## Prefetch Plugin

**Package**: `@barba/prefetch`

Prefetch pages on link hover for faster navigation.

**Installation**:
```bash
npm install --save-dev @barba/prefetch
```

**API**:

```javascript
import barbaPrefetch from '@barba/prefetch';

barba.use(barbaPrefetch);

barba.init({
  prefetch: {
    root: null,        // Element to observe (null = document)
    timeout: 3000      // Cache timeout in ms
  }
});
```

**How It Works**:

1. User hovers over a link
2. Plugin fetches the page via AJAX
3. Page is cached
4. On click, cached page loads instantly (if still in cache)

**Manual Prefetching**:

```javascript
// Prefetch specific URL
barba.prefetch('/about');

// Prefetch multiple URLs
['/about', '/contact', '/services'].forEach(url => {
  barba.prefetch(url);
});
```

---

## CSS Plugin

**Package**: `@barba/css`

CSS-based transitions without writing JavaScript.

**Installation**:
```bash
npm install --save-dev @barba/css
```

**Usage**:

```javascript
import barbaCSS from '@barba/css';

barba.use(barbaCSS);
barba.init();
```

**CSS Classes**:

Barba adds classes during transitions:

| Class | When | Description |
|-------|------|-------------|
| `.barba-once` | Initial load | Applied to wrapper during `once` hook |
| `.barba-leave` | Leave phase | Applied to current container |
| `.barba-leave-active` | Leave active | Added when animation starts |
| `.barba-leave-to` | Leave end | Added when animation should end |
| `.barba-enter` | Enter phase | Applied to next container |
| `.barba-enter-active` | Enter active | Added when animation starts |
| `.barba-enter-to` | Enter end | Added when animation should end |

**Example CSS**:

```css
/* Initial page load */
.barba-once [data-barba="container"] {
  opacity: 0;
  transform: translateY(50px);
  transition: opacity 0.5s, transform 0.5s;
}

.barba-once.barba-once-active [data-barba="container"] {
  opacity: 1;
  transform: translateY(0);
}

/* Leave transition */
.barba-leave-active [data-barba="container"] {
  opacity: 1;
  transition: opacity 0.5s;
}

.barba-leave-to [data-barba="container"] {
  opacity: 0;
}

/* Enter transition */
.barba-enter [data-barba="container"] {
  opacity: 0;
}

.barba-enter-active [data-barba="container"] {
  opacity: 1;
  transition: opacity 0.5s;
}
```

---

## Head Plugin

**Package**: `@barba/head`

Automatically update `<head>` tags (title, meta) on navigation.

**Installation**:
```bash
npm install --save-dev @barba/head
```

**Usage**:

```javascript
import barbaHead from '@barba/head';

barba.use(barbaHead);
barba.init();
```

**What It Updates**:

The plugin updates these `<head>` tags automatically:
- `<title>`
- `<meta>` (name, property, http-equiv)
- `<link>` (canonical, alternate)
- `<script>` (application/ld+json)

**Manual Head Updates**:

If not using the plugin, update manually:

```javascript
barba.hooks.after(({ next }) => {
  // Update title
  document.title = next.html.match(/<title>(.*?)<\/title>/i)[1];

  // Update meta description
  const metaDesc = next.html.match(/<meta name="description" content="(.*?)"/i);
  if (metaDesc) {
    document.querySelector('meta[name="description"]').content = metaDesc[1];
  }
});
```
