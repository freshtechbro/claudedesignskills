---
name: modern-web-design
description: Modern web design trends, principles, and implementation patterns for 2024-2025. Use this skill when designing websites, creating interactive experiences, implementing design systems, ensuring accessibility, or building performance-first interfaces. Triggers on tasks involving modern design trends, micro-interactions, scrollytelling, bold minimalism, cursor UX, glassmorphism, accessibility compliance, performance optimization, or design system architecture. References animation skills (GSAP, Framer Motion, React Spring), 3D skills (Three.js, R3F, Babylon.js), and component libraries for implementation guidance.
---

# Modern Web Design

## Overview

Modern web design in 2024-2025 emphasizes performance, accessibility, and meaningful interactions. This skill provides comprehensive guidance on current design trends, implementation patterns, and best practices for creating engaging, accessible, and performant web experiences.

This meta-skill synthesizes knowledge from all animation, interaction, and 3D skills in this repository to provide holistic design guidance.

## Core Design Principles (2024-2025)

### 1. Performance-First Design

**Philosophy**: Design decisions should prioritize Core Web Vitals and user experience on all devices.

**Key Metrics**:
- Largest Contentful Paint (LCP): < 2.5s
- First Input Delay (FID): < 100ms
- Cumulative Layout Shift (CLS): < 0.1
- Interaction to Next Paint (INP): < 200ms

**Implementation Guidelines**:
- Defer non-critical animations until after page load
- Use CSS transforms/opacity for animations (GPU-accelerated)
- Implement lazy loading for images, videos, and 3D content
- Progressive enhancement: core content without JavaScript

**Related Skills**: `gsap-scrolltrigger`, `motion-framer`, `lottie-animations` for optimized animations

### 2. Bold Minimalism

**Characteristics**:
- Large, impactful typography (clamp() for fluid sizing)
- Ample white space (negative space as design element)
- Limited color palettes (3-5 primary colors)
- Intentional use of bold accent colors
- Geometric shapes and clean lines

**Typography Scale** (Modern fluid system):
```css
/* Fluid typography using clamp() */
--font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
--font-size-lg: clamp(1.25rem, 1.1rem + 0.75vw, 1.75rem);
--font-size-xl: clamp(1.75rem, 1.5rem + 1.25vw, 2.5rem);
--font-size-2xl: clamp(2.5rem, 2rem + 2.5vw, 4rem);
--font-size-3xl: clamp(3.5rem, 2.5rem + 5vw, 6rem);
```

**Color System** (Accessibility-first):
```css
/* WCAG AAA compliant color system */
--color-primary: oklch(50% 0.2 250); /* Blue */
--color-accent: oklch(65% 0.25 30);  /* Coral */
--color-neutral-50: oklch(98% 0 0);
--color-neutral-900: oklch(20% 0 0);
/* Contrast ratio: minimum 7:1 for text */
```

**Related Skills**: `animated-component-libraries` for UI components

### 3. Micro-Interactions

**Definition**: Small, purposeful animations that provide feedback, guide users, and enhance perceived performance.

**Categories**:

**a) Hover States** (Desktop):
- Scale transformations (1.05-1.1x)
- Color transitions (200-300ms)
- Shadow depth changes
- Cursor transformations

**b) Loading States**:
- Skeleton screens (better than spinners)
- Progressive image loading (blur-up technique)
- Optimistic UI updates
- Staggered content reveals

**c) Interactive Feedback**:
- Button press states (scale down 0.95x)
- Toggle switches with spring physics
- Form field validation (immediate, kind feedback)
- Success/error states with motion

**Implementation Example** (Framer Motion):
```jsx
// Button with micro-interaction
<motion.button
  whileHover={{ scale: 1.05, y: -2 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>
```

**Related Skills**: `motion-framer`, `react-spring-physics`, `animejs` for micro-interactions

### 4. Scrollytelling

**Definition**: Narrative-driven experiences where content reveals and transforms as the user scrolls.

**Patterns**:

**a) Scroll-Triggered Reveals**:
- Fade-in on scroll entry (with offset)
- Slide-in from sides with stagger
- Scale + opacity transitions
- Clip-path reveals

**b) Scroll-Linked Animations**:
- Parallax layers (different scroll speeds)
- Horizontal scrolling sections
- Pinned sections with scrubbing animations
- 3D object rotation tied to scroll

**c) Progress Indicators**:
- Reading progress bars
- Step-by-step visual guides
- Animated SVG paths following scroll

**Implementation Example** (GSAP ScrollTrigger):
```javascript
// Scroll-linked 3D rotation
gsap.to(".cube", {
  scrollTrigger: {
    trigger: ".section",
    start: "top top",
    end: "bottom top",
    scrub: 1, // Smooth scrubbing
  },
  rotationY: 360,
  ease: "none"
});
```

**Related Skills**: `gsap-scrolltrigger`, `locomotive-scroll`, `scroll-reveal-libraries`, `react-three-fiber` for 3D scrollytelling

### 5. Cursor UX

**Evolution**: Custom cursors that enhance interaction and provide contextual feedback.

**Patterns**:

**a) Custom Cursor Shapes**:
- Circle/dot followers (delayed with easing)
- Text-based cursors ("View", "Drag", "Click")
- Blend modes for visual interest
- Scale/morph on hover

**b) Contextual Transformations**:
- Expand on links/buttons
- Magnetic attraction to interactive elements
- Color inversion over images
- Custom icons for actions (play, zoom, expand)

**c) Performance Considerations**:
- Use CSS transforms only (no top/left)
- RequestAnimationFrame for JS cursors
- Disable on mobile/touch devices
- Respect `prefers-reduced-motion`

**Implementation Example**:
```javascript
// Simple smooth cursor follower
const cursor = document.querySelector('.cursor');
let mouseX = 0, mouseY = 0;
let cursorX = 0, cursorY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

function updateCursor() {
  // Smooth easing
  cursorX += (mouseX - cursorX) * 0.1;
  cursorY += (mouseY - cursorY) * 0.1;

  cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;
  requestAnimationFrame(updateCursor);
}
updateCursor();
```

**Related Skills**: `gsap-scrolltrigger` (for easing), `motion-framer` (for React cursor components)

### 6. Glassmorphism & Depth

**Characteristics**:
- Frosted glass effect (backdrop-filter)
- Layered UI with depth hierarchy
- Subtle shadows and borders
- Translucent backgrounds

**Modern Glassmorphism** (2024):
```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
}
```

**Depth System** (Layering):
```css
/* Elevation scale */
--elevation-1: 0 1px 3px rgba(0,0,0,0.12);
--elevation-2: 0 4px 8px rgba(0,0,0,0.15);
--elevation-3: 0 8px 16px rgba(0,0,0,0.18);
--elevation-4: 0 16px 32px rgba(0,0,0,0.2);
```

**Related Skills**: `animated-component-libraries` for glassmorphic components

### 7. AI-Enhanced Personalization

**Patterns**:

**a) Adaptive Content**:
- Dynamic layout based on user behavior
- Personalized content recommendations
- Adaptive color schemes (system preference + user history)
- Smart defaults based on context

**b) Intelligent Interactions**:
- Predictive search with instant results
- Smart form completion
- Context-aware suggestions
- Progressive disclosure based on usage

**c) Performance + Privacy**:
- Client-side personalization (localStorage, IndexedDB)
- Edge computing for fast personalization
- Privacy-preserving analytics
- Transparent data usage

**Implementation Considerations**:
- Fallback to default experience
- No layout shift from personalization
- Respect "Do Not Track"
- GDPR/CCPA compliance

## Common Design Patterns

### Pattern 1: Immersive Hero Section

**Use Case**: Landing pages, product launches, portfolio sites

**Characteristics**:
- Full viewport height
- Subtle 3D background or animated gradient
- Large headline with fluid typography
- Smooth scroll indicator
- Parallax on scroll exit

**Implementation** (Combined approach):

**HTML Structure**:
```html
<section class="hero">
  <div id="bg-canvas"></div>
  <div class="hero__content">
    <h1 class="hero__title">Modern Design</h1>
    <p class="hero__subtitle">Performance meets beauty</p>
    <button class="hero__cta">Explore</button>
  </div>
  <div class="scroll-indicator">
    <span>Scroll</span>
  </div>
</section>
```

**Technologies**:
- Background: Vanta.js WAVES effect (`lightweight-3d-effects`)
- Text animation: GSAP SplitText with stagger (`gsap-scrolltrigger`)
- Button: Framer Motion hover states (`motion-framer`)
- Scroll indicator: CSS animation + GSAP fade out on scroll

**Related Skills**: `lightweight-3d-effects`, `gsap-scrolltrigger`, `motion-framer`

### Pattern 2: Horizontal Scroll Gallery

**Use Case**: Portfolio work, product showcases, case studies

**Implementation** (GSAP ScrollTrigger):
```javascript
gsap.to(".gallery__track", {
  x: () => -(document.querySelector(".gallery__track").scrollWidth - window.innerWidth),
  ease: "none",
  scrollTrigger: {
    trigger: ".gallery",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".gallery__track").scrollWidth
  }
});
```

**Enhancements**:
- Lazy load images as they scroll into view
- Parallax within cards
- Scale transformation on active card
- Smooth momentum scrolling with Locomotive

**Related Skills**: `gsap-scrolltrigger`, `locomotive-scroll`

### Pattern 3: 3D Product Viewer

**Use Case**: E-commerce, product marketing, showcases

**Implementation** (React Three Fiber):
```jsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'

function ProductViewer() {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} />
      <Product />
      <OrbitControls
        enableZoom={false}
        autoRotate
        autoRotateSpeed={2}
      />
    </Canvas>
  )
}
```

**Enhancements**:
- Material variants (color picker)
- Hotspots with annotations
- AR mode on mobile
- Screenshot/share functionality

**Related Skills**: `react-three-fiber`, `threejs-webgl`, `model-viewer-component`

### Pattern 4: Animated Data Visualization

**Use Case**: Dashboards, analytics, infographics

**Patterns**:
- Count-up animations on scroll into view
- Animated chart reveals (progress bars, pie charts)
- Staggered grid animations
- Particle backgrounds representing data

**Implementation** (Framer Motion + IntersectionObserver):
```jsx
function AnimatedStat({ end, label }) {
  const [count, setCount] = useState(0);
  const ref = useRef();
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (isInView) {
      // Count up animation
      const duration = 2000;
      const steps = 60;
      const increment = end / steps;
      let current = 0;

      const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
          setCount(end);
          clearInterval(timer);
        } else {
          setCount(Math.floor(current));
        }
      }, duration / steps);
    }
  }, [isInView, end]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6 }}
    >
      <h2>{count}+</h2>
      <p>{label}</p>
    </motion.div>
  );
}
```

**Related Skills**: `motion-framer`, `pixijs-2d` for canvas-based visualizations

### Pattern 5: Page Transitions

**Use Case**: Multi-page apps, portfolio sites, storytelling experiences

**Implementation** (Barba.js + GSAP):
```javascript
barba.init({
  transitions: [{
    name: 'slide',
    leave(data) {
      return gsap.to(data.current.container, {
        xPercent: -100,
        duration: 0.5
      });
    },
    enter(data) {
      return gsap.from(data.next.container, {
        xPercent: 100,
        duration: 0.5
      });
    }
  }]
});
```

**Modern Alternatives**:
- View Transitions API (Chrome 111+, progressive enhancement)
- Framer Motion's AnimatePresence for React SPAs
- Shared element transitions

**Related Skills**: `barba-js`, `gsap-scrolltrigger`, `motion-framer`

### Pattern 6: Interactive Cursor Effects

**Use Case**: Creative agencies, portfolios, interactive experiences

**Patterns**:
- Text cursor that follows with delay
- Magnetic buttons (cursor attracted to elements)
- Blend mode cursor (inverts colors)
- Cursor that reveals content

**Implementation** (Vanilla JS + GSAP):
```javascript
const links = document.querySelectorAll('a');
const cursor = document.querySelector('.cursor');

links.forEach(link => {
  link.addEventListener('mouseenter', () => {
    gsap.to(cursor, {
      scale: 2,
      duration: 0.3,
      ease: "power2.out"
    });
  });

  link.addEventListener('mouseleave', () => {
    gsap.to(cursor, {
      scale: 1,
      duration: 0.3,
      ease: "power2.out"
    });
  });
});
```

**Related Skills**: `gsap-scrolltrigger`, `motion-framer`

### Pattern 7: Staggered Content Reveals

**Use Case**: Feature sections, testimonials, team grids

**Implementation** (Framer Motion variants):
```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

function FeatureGrid() {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.3 }}
      className="grid"
    >
      {features.map((feature, i) => (
        <motion.div key={i} variants={item}>
          {feature}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

**Related Skills**: `motion-framer`, `gsap-scrolltrigger`, `scroll-reveal-libraries`

## Integration with Other Skills

### Animation Skills Integration

**GSAP ScrollTrigger** (`gsap-scrolltrigger`):
- Use for scroll-driven storytelling
- Pin sections for multi-step reveals
- Scrub animations tied to scroll position
- Batch animations for performance

**Framer Motion** (`motion-framer`):
- React component animations
- Page transitions with AnimatePresence
- Gesture-based interactions (drag, hover, tap)
- Layout animations (shared element transitions)

**React Spring** (`react-spring-physics`):
- Physics-based animations (more natural feel)
- Interactive springs (drag, pull)
- Trail animations (sequential reveals)
- Use for UI feedback that feels "real"

**Anime.js** (`animejs`):
- SVG path animations (line drawing)
- SVG morphing transitions
- Stagger grid animations
- Timeline-based sequences

**Lottie** (`lottie-animations`):
- Complex designer-created animations
- Icon animations and micro-interactions
- Loading states
- Scroll-driven playback

### 3D Skills Integration

**Three.js** (`threejs-webgl`):
- Custom 3D scenes and experiences
- Shader effects and post-processing
- WebGL-based particle systems
- Advanced lighting and materials

**React Three Fiber** (`react-three-fiber`):
- 3D in React applications
- Product viewers and configurators
- Interactive 3D UI components
- Scroll-driven 3D animations

**Babylon.js** (`babylonjs-engine`):
- Physics-based 3D experiences
- VR/XR applications
- Game-like interactions
- PBR materials for realism

**Lightweight 3D** (`lightweight-3d-effects`):
- Background effects (Vanta.js)
- Subtle 3D illustrations (Zdog)
- Tilt effects (Vanilla-Tilt)
- Performance-friendly 3D accents

### Component Libraries

**Animated Components** (`animated-component-libraries`):
- Magic UI components (backgrounds, text effects)
- Pre-built interactive components
- Design system foundations
- Rapid prototyping

**Scroll Reveals** (`scroll-reveal-libraries`):
- Simple fade/slide on scroll
- AOS library integration
- Lightweight alternative to ScrollTrigger
- Quick implementation for basic reveals

## Accessibility Best Practices

### 1. Motion & Animation

**Respect User Preferences**:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**JavaScript Detection**:
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (prefersReducedMotion) {
  // Disable or simplify animations
  gsap.config({ nullTargetWarn: false });
  // Skip scroll animations, use instant reveals
}
```

### 2. Color Contrast

**WCAG AAA Standards**:
- Normal text: 7:1 contrast ratio
- Large text (18pt+): 4.5:1 contrast ratio
- Use OKLCH color space for perceptual uniformity

**Testing**:
```javascript
// Check contrast ratio
function getContrastRatio(color1, color2) {
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

### 3. Keyboard Navigation

**Requirements**:
- All interactive elements focusable
- Visible focus indicators (not outline: none)
- Logical tab order
- Skip links for long navigation
- Escape key closes modals/overlays

**Focus Styles** (Modern):
```css
:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Remove focus ring for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### 4. Screen Reader Support

**Semantic HTML**:
- Use proper heading hierarchy (h1-h6)
- Landmark regions (header, nav, main, footer)
- aria-labels for icon buttons
- aria-live regions for dynamic content

**Animation Announcements**:
```html
<!-- Announce when content loads -->
<div role="status" aria-live="polite" aria-atomic="true">
  Loading complete. 12 items displayed.
</div>
```

### 5. Touch Targets

**Minimum Size**: 44x44px (iOS), 48x48px (Android)

**Spacing**: Minimum 8px between touch targets

**Implementation**:
```css
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
  /* Tap target includes padding */
}
```

## Performance Optimization

### 1. Animation Performance

**60 FPS Checklist**:
- Use CSS transforms (translateX/Y/Z, scale, rotate) - GPU accelerated
- Use opacity for fades - GPU accelerated
- Avoid: top/left, width/height, margin, padding animations
- Use `will-change` sparingly (memory cost)
- RequestAnimationFrame for JS animations

**GSAP Performance**:
```javascript
// Force GPU acceleration
gsap.set(element, { force3D: true });

// Use will-change during animation only
gsap.to(element, {
  x: 100,
  onStart: () => element.style.willChange = 'transform',
  onComplete: () => element.style.willChange = 'auto'
});
```

### 2. Loading Strategies

**Critical Path**:
- Inline critical CSS (above-the-fold)
- Defer non-critical CSS
- Async JavaScript loading
- Preload fonts and hero images

**Progressive Enhancement**:
```html
<!-- Load essential styles first -->
<style>
  /* Critical CSS inlined */
</style>

<!-- Defer non-critical styles -->
<link rel="preload" href="animations.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="animations.css"></noscript>
```

### 3. Image Optimization

**Modern Formats**:
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

**Responsive Images**:
```html
<img
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  src="image-800.jpg"
  alt="Description"
  loading="lazy"
>
```

### 4. 3D Content Optimization

**Loading Strategy**:
- Show placeholder while loading
- Load low-poly model first
- Progressive enhancement with high-poly
- Lazy load 3D scenes below fold

**Runtime Performance**:
- Use object pooling
- Implement LOD (Level of Detail)
- Frustum culling
- Texture compression (Basis Universal)

**Related Skills**: `threejs-webgl`, `react-three-fiber`, `babylonjs-engine`

### 5. JavaScript Bundle Size

**Code Splitting**:
```javascript
// Dynamic imports
const AnimationModule = lazy(() => import('./animations'));

// Route-based splitting
const Gallery = lazy(() => import('./pages/Gallery'));
```

**Tree Shaking**:
- Use ES6 imports
- Import only what you need
- Use modern build tools (Vite, esbuild)

## Common Pitfalls

### Pitfall 1: Over-Animation

**Problem**: Too many animations distract from content and hurt performance.

**Solution**:
- Limit animations to meaningful interactions
- Use animation to guide attention, not demand it
- Follow the principle: "Animation with purpose"
- Measure performance impact (Chrome DevTools Performance tab)

**Rule of Thumb**: If you can't explain why an animation exists, remove it.

### Pitfall 2: Ignoring Mobile Performance

**Problem**: Animations work on desktop but lag on mobile devices.

**Solution**:
- Test on real devices (not just simulators)
- Reduce animation complexity on mobile
- Disable expensive effects (parallax, 3D) on low-end devices
- Use `matchMedia` for device-specific experiences

```javascript
const isLowEndDevice = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) &&
         navigator.hardwareConcurrency < 4;
};

if (isLowEndDevice()) {
  // Simplify or disable animations
}
```

### Pitfall 3: Missing Fallbacks

**Problem**: Experience breaks without JavaScript or on older browsers.

**Solution**:
- Progressive enhancement mindset
- Core content accessible without JS
- Feature detection before using modern APIs
- Polyfills for critical features

```javascript
// Feature detection
if ('IntersectionObserver' in window) {
  // Use scroll-triggered animations
} else {
  // Show content immediately
}
```

### Pitfall 4: Accessibility Oversight

**Problem**: Forgetting keyboard users, screen readers, or motion-sensitive users.

**Solution**:
- Test with keyboard only
- Test with screen reader (NVDA, VoiceOver)
- Always check `prefers-reduced-motion`
- Use semantic HTML
- Maintain proper focus management

**Checklist**:
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AAA
- [ ] Motion can be disabled
- [ ] Screen reader announcements make sense

### Pitfall 5: Ignoring Loading States

**Problem**: Blank screen or layout shifts during content load.

**Solution**:
- Skeleton screens for predictable layouts
- Smooth loading transitions
- Reserve space for dynamic content
- Show meaningful loading indicators

```jsx
// Skeleton screen pattern
function ProductCard({ loading, data }) {
  if (loading) {
    return (
      <div className="skeleton">
        <div className="skeleton__image" />
        <div className="skeleton__title" />
        <div className="skeleton__price" />
      </div>
    );
  }

  return <ProductCardContent data={data} />;
}
```

### Pitfall 6: Scroll Hijacking

**Problem**: Overriding native scroll behavior frustrates users.

**Solution**:
- Preserve browser's native scroll (momentum, keyboard)
- Use ScrollTrigger/Locomotive without changing scroll physics
- Allow users to scroll at their own pace
- Never disable scroll entirely
- Avoid scroll-jacking for full-page sections

**Good Practice**: Enhance scroll, don't replace it.

## Design System Architecture

### Token Structure

**Modern Design Tokens** (CSS Custom Properties):
```css
:root {
  /* Colors - OKLCH for perceptual uniformity */
  --color-primary: oklch(50% 0.2 250);
  --color-accent: oklch(65% 0.25 30);

  /* Spacing - Consistent scale */
  --space-2xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.375rem);
  --space-xs: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-sm: clamp(0.75rem, 0.6rem + 0.75vw, 1.125rem);
  --space-md: clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);
  --space-xl: clamp(2rem, 1.6rem + 2vw, 3rem);
  --space-2xl: clamp(3rem, 2.4rem + 3vw, 4.5rem);

  /* Typography - Fluid scale */
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);

  /* Animation - Consistent timing */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;

  /* Easing - Natural motion */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Component Architecture

**Atomic Design** (Brad Frost):
1. **Atoms**: Buttons, inputs, labels
2. **Molecules**: Form fields, cards
3. **Organisms**: Navigation, hero sections
4. **Templates**: Page layouts
5. **Pages**: Specific instances

**Related Skills**: `animated-component-libraries` for component patterns

## Resources

This skill references the following skills for implementation:

### Animation & Interaction
- `gsap-scrolltrigger` - Scroll-driven animations, pinning, scrubbing
- `motion-framer` - React animations, gestures, layout animations
- `react-spring-physics` - Physics-based animations
- `animejs` - SVG animations, stagger effects
- `lottie-animations` - Designer-created animations
- `scroll-reveal-libraries` - Simple scroll reveals (AOS)

### 3D & WebGL
- `threejs-webgl` - Custom 3D scenes and effects
- `react-three-fiber` - 3D in React applications
- `babylonjs-engine` - Physics-based 3D, VR/XR
- `lightweight-3d-effects` - Vanta.js backgrounds, Zdog illustrations

### Page Transitions & Scroll
- `barba-js` - Page transitions
- `locomotive-scroll` - Smooth scrolling

### Component Libraries
- `animated-component-libraries` - Magic UI, React Bits
- `pixijs-2d` - Canvas-based 2D graphics

### Detailed References

See the `references/` directory for in-depth documentation:
- `design_trends_2024.md` - Current web design trends and forecasts
- `interaction_patterns.md` - Comprehensive micro-interaction catalog
- `accessibility_guide.md` - WCAG compliance patterns and testing
- `performance_checklist.md` - Optimization strategies and metrics

### Scripts

The `scripts/` directory includes tools for implementing design patterns:
- `pattern_generator.py` - Generate design pattern boilerplate
- `design_audit.py` - Audit existing designs for compliance

### Assets

The `assets/` directory contains design system templates and starter files. See `assets/README.md` for details.
