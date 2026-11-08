# AOS Examples and Integration Patterns

Production-ready code examples for AOS (Animate On Scroll) integration across different frameworks and use cases.

## Table of Contents

- [Quick Start Templates](#quick-start-templates)
- [React Integration](#react-integration)
- [Next.js Integration](#nextjs-integration)
- [Vue.js Integration](#vuejs-integration)
- [Common Patterns](#common-patterns)
- [Performance Examples](#performance-examples)
- [Accessibility Patterns](#accessibility-patterns)

## Quick Start Templates

### Minimal CDN Setup

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Minimal Example</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
</head>
<body>
  <h1 data-aos="fade-down">Hello World</h1>
  <p data-aos="fade-up" data-aos-delay="200">
    This content fades in with a delay.
  </p>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({ duration: 800, once: true });
  </script>
</body>
</html>
```

### NPM Setup (ES6)

```bash
npm install aos@next
```

```javascript
// main.js
import AOS from 'aos';
import 'aos/dist/aos.css';

AOS.init({
  duration: 800,
  once: true,
  offset: 100
});
```

```html
<!-- index.html -->
<div data-aos="fade-up">Content here</div>
```

## React Integration

### Basic React Setup

```jsx
// App.jsx
import { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';

function App() {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
      offset: 100,
      easing: 'ease-out-cubic'
    });
  }, []);

  return (
    <div>
      <h1 data-aos="fade-down">Welcome</h1>
      <p data-aos="fade-up" data-aos-delay="200">
        Your content here
      </p>
    </div>
  );
}

export default App;
```

### React with React Router

```jsx
// App.jsx
import { useEffect } from 'react';
import { useLocation, Routes, Route } from 'react-router-dom';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Home from './pages/Home';
import About from './pages/About';

function App() {
  const location = useLocation();

  // Initialize AOS on mount
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
      offset: 100
    });
  }, []);

  // Refresh AOS on route change
  useEffect(() => {
    AOS.refresh();
  }, [location.pathname]);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
    </Routes>
  );
}

export default App;
```

### React Wrapper Component

```jsx
// components/AnimatedSection.jsx
import React from 'react';

const AnimatedSection = ({
  children,
  animation = 'fade-up',
  delay = 0,
  duration = 800,
  offset = 100,
  once = true,
  className = '',
  ...props
}) => {
  return (
    <div
      data-aos={animation}
      data-aos-delay={delay}
      data-aos-duration={duration}
      data-aos-offset={offset}
      data-aos-once={once}
      className={className}
      {...props}
    >
      {children}
    </div>
  );
};

export default AnimatedSection;
```

Usage:

```jsx
// pages/Home.jsx
import AnimatedSection from '../components/AnimatedSection';

function Home() {
  return (
    <main>
      <AnimatedSection animation="fade-down">
        <h1>Hero Title</h1>
      </AnimatedSection>

      <AnimatedSection animation="fade-up" delay={200}>
        <p>Hero subtext</p>
      </AnimatedSection>

      <AnimatedSection animation="zoom-in" delay={400}>
        <button>Get Started</button>
      </AnimatedSection>
    </main>
  );
}
```

### React with Dynamic Content

```jsx
// components/DynamicList.jsx
import { useState, useEffect } from 'react';
import AOS from 'aos';

function DynamicList() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    AOS.init({ duration: 600 });
  }, []);

  const addItem = () => {
    const newItem = {
      id: Date.now(),
      text: `Item ${items.length + 1}`
    };

    setItems([...items, newItem]);

    // Refresh AOS after adding to DOM
    setTimeout(() => AOS.refresh(), 50);
  };

  const removeItem = (id) => {
    setItems(items.filter(item => item.id !== id));
    setTimeout(() => AOS.refresh(), 50);
  };

  return (
    <div>
      <button onClick={addItem}>Add Item</button>

      <div className="list">
        {items.map((item, index) => (
          <div
            key={item.id}
            data-aos="fade-in"
            data-aos-delay={index * 50}
          >
            {item.text}
            <button onClick={() => removeItem(item.id)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DynamicList;
```

## Next.js Integration

### Next.js App Router (_app.js)

```jsx
// pages/_app.js
import { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true,
      offset: 100,
      easing: 'ease-out-cubic'
    });
  }, []);

  return <Component {...pageProps} />;
}

export default MyApp;
```

### Next.js Page Example

```jsx
// pages/index.js
export default function Home() {
  return (
    <main>
      <section className="hero">
        <h1 data-aos="fade-down">Next.js + AOS</h1>
        <p data-aos="fade-up" data-aos-delay="200">
          Server-side rendered content with scroll animations
        </p>
      </section>

      <section className="features">
        {features.map((feature, index) => (
          <div
            key={feature.id}
            data-aos="fade-up"
            data-aos-delay={index * 100}
            className="feature-card"
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </section>
    </main>
  );
}

const features = [
  { id: 1, title: 'Fast', description: 'Lightning fast performance' },
  { id: 2, title: 'Secure', description: 'Enterprise-grade security' },
  { id: 3, title: 'Scalable', description: 'Grows with your needs' }
];
```

### Next.js with TypeScript

```tsx
// pages/_app.tsx
import { useEffect } from 'react';
import type { AppProps } from 'next/app';
import AOS from 'aos';
import 'aos/dist/aos.css';

function MyApp({ Component, pageProps }: AppProps) {
  useEffect(() => {
    AOS.init({
      duration: 800,
      once: true
    });
  }, []);

  return <Component {...pageProps} />;
}

export default MyApp;
```

```tsx
// components/AnimatedCard.tsx
interface AnimatedCardProps {
  title: string;
  description: string;
  delay?: number;
}

const AnimatedCard = ({ title, description, delay = 0 }: AnimatedCardProps) => {
  return (
    <div
      data-aos="fade-up"
      data-aos-delay={delay}
      className="card"
    >
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
};

export default AnimatedCard;
```

## Vue.js Integration

### Vue 3 Composition API

```vue
<!-- App.vue -->
<template>
  <div>
    <h1 data-aos="fade-down">Vue 3 + AOS</h1>

    <div
      v-for="(item, index) in items"
      :key="item.id"
      data-aos="fade-up"
      :data-aos-delay="index * 100"
    >
      {{ item.text }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import AOS from 'aos';
import 'aos/dist/aos.css';

const items = ref([
  { id: 1, text: 'Item 1' },
  { id: 2, text: 'Item 2' },
  { id: 3, text: 'Item 3' }
]);

onMounted(() => {
  AOS.init({
    duration: 800,
    once: true
  });
});
</script>
```

### Vue 3 with Dynamic Updates

```vue
<!-- DynamicList.vue -->
<template>
  <div>
    <button @click="addItem">Add Item</button>

    <div
      v-for="(item, index) in items"
      :key="item.id"
      data-aos="fade-in"
      :data-aos-delay="index * 50"
      class="list-item"
    >
      {{ item.text }}
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue';
import AOS from 'aos';
import 'aos/dist/aos.css';

const items = ref([]);

onMounted(() => {
  AOS.init({ duration: 600 });
});

const addItem = async () => {
  items.value.push({
    id: Date.now(),
    text: `Item ${items.value.length + 1}`
  });

  // Wait for DOM update, then refresh AOS
  await nextTick();
  AOS.refresh();
};
</script>
```

### Vue 2 Options API

```vue
<!-- App.vue -->
<template>
  <div>
    <h1 data-aos="fade-down">Vue 2 + AOS</h1>
    <p data-aos="fade-up">Content here</p>
  </div>
</template>

<script>
import AOS from 'aos';
import 'aos/dist/aos.css';

export default {
  name: 'App',
  mounted() {
    AOS.init({
      duration: 800,
      once: true
    });
  },
  updated() {
    // Refresh when component updates
    this.$nextTick(() => {
      AOS.refresh();
    });
  }
};
</script>
```

## Common Patterns

### Landing Page Pattern

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AOS Landing Page</title>
  <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

    /* Hero */
    .hero {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 2rem;
    }

    .hero h1 { font-size: 3rem; margin-bottom: 1rem; }
    .hero p { font-size: 1.25rem; margin-bottom: 2rem; }
    .hero button {
      padding: 1rem 2.5rem;
      font-size: 1.1rem;
      background: white;
      color: #667eea;
      border: none;
      border-radius: 50px;
      cursor: pointer;
    }

    /* Features */
    .features {
      padding: 5rem 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .features h2 {
      text-align: center;
      font-size: 2.5rem;
      margin-bottom: 3rem;
    }

    .feature-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 2rem;
    }

    .feature-card {
      background: white;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    .feature-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
    }
  </style>
</head>
<body>
  <!-- Hero Section -->
  <section class="hero">
    <div>
      <h1 data-aos="fade-down" data-aos-duration="800">
        Build Something Amazing
      </h1>
      <p data-aos="fade-up" data-aos-delay="200" data-aos-duration="600">
        The most powerful platform for creating extraordinary experiences
      </p>
      <button data-aos="zoom-in" data-aos-delay="400" data-aos-duration="500">
        Get Started
      </button>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <h2 data-aos="fade-down">Why Choose Us</h2>

    <div class="feature-grid">
      <div class="feature-card" data-aos="fade-up" data-aos-delay="0">
        <div class="feature-icon">🚀</div>
        <h3>Lightning Fast</h3>
        <p>Optimized for speed and performance</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
        <div class="feature-icon">🎨</div>
        <h3>Beautiful UI</h3>
        <p>Stunning designs that users love</p>
      </div>

      <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
        <div class="feature-icon">🔒</div>
        <h3>Secure</h3>
        <p>Enterprise-grade security built-in</p>
      </div>
    </div>
  </section>

  <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
  <script>
    AOS.init({
      duration: 800,
      once: true,
      offset: 100
    });
  </script>
</body>
</html>
```

### Staggered Grid Pattern

```jsx
// React example
function ProductGrid({ products }) {
  useEffect(() => {
    AOS.init({ duration: 600, once: true });
  }, []);

  return (
    <div className="product-grid">
      {products.map((product, index) => (
        <div
          key={product.id}
          data-aos="zoom-in-up"
          data-aos-delay={index * 50}
          className="product-card"
        >
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>
          <p>{product.price}</p>
        </div>
      ))}
    </div>
  );
}
```

### Alternating Content Pattern

```html
<!-- Alternating image-text sections -->
<div class="content-sections">
  <!-- Section 1: Image on right -->
  <section class="content-row">
    <div class="text-col" data-aos="slide-right" data-aos-duration="800">
      <h2>Feature One</h2>
      <p>Description of the feature...</p>
    </div>
    <div class="image-col" data-aos="fade-left" data-aos-delay="200">
      <img src="feature1.jpg" alt="Feature 1">
    </div>
  </section>

  <!-- Section 2: Image on left -->
  <section class="content-row reverse">
    <div class="image-col" data-aos="fade-right">
      <img src="feature2.jpg" alt="Feature 2">
    </div>
    <div class="text-col" data-aos="slide-left" data-aos-duration="800" data-aos-delay="200">
      <h2>Feature Two</h2>
      <p>Description of the feature...</p>
    </div>
  </section>
</div>
```

## Performance Examples

### Optimized Configuration

```javascript
// Best performance configuration
AOS.init({
  // Animation settings
  duration: 400,  // Shorter = smoother
  easing: 'ease',  // Simple easing

  // Behavior
  once: true,  // Animate only once (better performance)
  mirror: false,  // Don't animate out

  // Device settings
  disable: function() {
    // Disable on mobile or reduced motion preference
    return window.innerWidth < 768 ||
           window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },

  // Performance tuning
  throttleDelay: 120,  // Increase for slower devices
  debounceDelay: 80,
  disableMutationObserver: true  // For fully static content
});
```

### Selective Animation

```jsx
// Don't animate everything - be selective
function BlogPost({ post }) {
  return (
    <article>
      {/* Animate hero elements */}
      <h1 data-aos="fade-down">{post.title}</h1>
      <p className="meta" data-aos="fade-up" data-aos-delay="100">
        {post.author} • {post.date}
      </p>

      {/* Don't animate body text - better for readability */}
      <div className="content">
        {post.content}
      </div>

      {/* Animate CTA */}
      <button data-aos="fade-up" className="cta">
        Share This Post
      </button>
    </article>
  );
}
```

## Accessibility Patterns

### Reduced Motion Support

```javascript
// Respect user's motion preferences
AOS.init({
  disable: function() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
});
```

### Conditional Animation

```jsx
// React: Disable animations based on user preference
import { useEffect, useState } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';

function App() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handleChange = () => setPrefersReducedMotion(mediaQuery.matches);
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  useEffect(() => {
    if (!prefersReducedMotion) {
      AOS.init({ duration: 800, once: true });
    }
  }, [prefersReducedMotion]);

  return (
    <div>
      <h1 data-aos={prefersReducedMotion ? undefined : "fade-down"}>
        Accessible Heading
      </h1>
    </div>
  );
}
```

### ARIA-friendly Animations

```html
<!-- Use aria-live for important content -->
<div
  data-aos="fade-up"
  aria-live="polite"
  aria-atomic="true"
>
  <h2>Important Update</h2>
  <p>This content will be announced to screen readers</p>
</div>

<!-- Mark decorative animations -->
<div
  data-aos="zoom-in"
  aria-hidden="true"
  role="presentation"
>
  Decorative element
</div>
```

## Best Practices Summary

### Do's

✅ Initialize AOS once on app mount
✅ Use `AOS.refresh()` after dynamic content changes
✅ Prefer simpler animations (fade, slide) over complex (flip)
✅ Use `once: true` for better performance
✅ Disable on mobile if not needed
✅ Respect `prefers-reduced-motion` preference
✅ Be selective - don't animate everything
✅ Use consistent animation types per page (2-3 max)

### Don'ts

❌ Don't initialize AOS multiple times
❌ Don't forget to call `AOS.refresh()` after adding elements
❌ Don't animate too many elements at once
❌ Don't use very long durations (>1500ms)
❌ Don't ignore accessibility
❌ Don't animate critical content (nav, forms, body text)
❌ Don't mix too many animation types

## Troubleshooting Checklist

- [ ] AOS initialized? (`AOS.init()` called)
- [ ] CSS imported? (`import 'aos/dist/aos.css'`)
- [ ] Valid `data-aos` attribute?
- [ ] Called `AOS.refresh()` after dynamic changes?
- [ ] Check browser console for errors
- [ ] Try simplified config (duration, once, offset only)
- [ ] Verify element is in viewport when scrolling
- [ ] Check for CSS conflicts (`opacity`, `transform`)

## Additional Resources

- **Scripts**: Use `scripts/aos_generator.py` to generate HTML templates
- **Scripts**: Use `scripts/config_builder.py` to build custom configurations
- **References**: See `references/aos_api.md` for complete API documentation
- **References**: See `references/animation_catalog.md` for all 28 built-in animations
- **Official Docs**: https://michalsnik.github.io/aos/
