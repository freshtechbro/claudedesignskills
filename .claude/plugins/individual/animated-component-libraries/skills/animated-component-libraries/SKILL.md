---
name: animated-component-libraries
description: Pre-built animated React component collections combining Magic UI (150+ TypeScript/Tailwind/Motion components) and React Bits (90+ minimal-dependency animated components). Use this skill when building landing pages, marketing sites, dashboards, or interactive UIs requiring pre-made animated components instead of hand-crafting animations. Triggers on tasks involving animated UI components, Magic UI, React Bits, shadcn/ui integration, Tailwind CSS components, or component library selection. Alternative to manually implementing animations with Framer Motion or GSAP.
---

# Animated Component Libraries

## Overview

This skill provides expertise in pre-built animated React component libraries, specifically Magic UI and React Bits. These libraries offer production-ready, animated components that significantly accelerate development of modern, interactive web applications.

**Magic UI** provides 150+ TypeScript components built on Tailwind CSS and Framer Motion, designed for seamless integration with shadcn/ui. Components are copy-paste ready and highly customizable.

**React Bits** offers 90+ animated React components with minimal dependencies, focusing on visual effects, backgrounds, and micro-interactions. Components emphasize performance and ease of customization.

Both libraries follow modern React patterns, support TypeScript, and integrate with popular design systems.

## Core Concepts

### Magic UI Architecture

Magic UI components are built on three foundational technologies:

1. **Tailwind CSS**: Utility-first styling with full customization via `tailwind.config.js`
2. **Framer Motion**: Physics-based animations and gesture recognition
3. **shadcn/ui Integration**: Follows shadcn conventions for CLI installation and component structure

**Installation Methods**:

```bash
# Via shadcn CLI (recommended)
npx shadcn@latest add https://magicui.design/r/animated-beam

# Manual installation
# 1. Copy component code to components/ui/
# 2. Install motion: npm install motion
# 3. Add required CSS animations to globals.css
# 4. Ensure cn() utility exists in lib/utils.ts
```

**Component Structure**:

```typescript
// All Magic UI components follow this pattern:
import { cn } from "@/lib/utils"
import { motion } from "motion/react"

interface ComponentProps extends React.ComponentPropsWithoutRef<"div"> {
  customProp?: string
  className?: string
}

export function MagicComponent({ className, customProp, ...props }: ComponentProps) {
  return (
    <motion.div
      className={cn("base-styles", className)}
      {...props}
    >
      {/* Component content */}
    </motion.div>
  )
}
```

### React Bits Architecture

React Bits emphasizes lightweight, standalone components with minimal dependencies:

1. **Self-Contained**: Each component has minimal external dependencies
2. **CSS-in-JS Optional**: Many components use inline styles or CSS modules
3. **Performance-First**: Optimized for 60fps animations
4. **WebGL Support**: Some components (Particles, Plasma) use WebGL for advanced effects

**Installation**:

```bash
# Manual copy-paste (primary method)
# Copy component files from reactbits.dev to your project

# Key dependencies (install as needed):
npm install framer-motion  # For animation-heavy components
npm install ogl           # For WebGL components (Particles, Plasma)
```

**Component Categories**:

- **Text Animations**: BlurText, CircularText, CountUp, SpinningText
- **Interactive Elements**: MagicButton, Magnet, Dock, Stepper
- **Backgrounds**: Aurora, Plasma, Particles
- **Lists & Layouts**: AnimatedList, Bento Grid

## Common Patterns

### 1. Magic UI: Animated Background Patterns

Create dynamic background effects with SVG-based patterns:

```typescript
import { GridPattern } from "@/components/ui/grid-pattern"
import { AnimatedGridPattern } from "@/components/ui/animated-grid-pattern"
import { cn } from "@/lib/utils"

export default function HeroSection() {
  return (
    <div className="relative flex h-[500px] w-full items-center justify-center overflow-hidden rounded-lg border">
      {/* Static Grid Pattern */}
      <GridPattern
        squares={[
          [4, 4], [5, 1], [8, 2], [5, 3], [10, 10], [12, 15]
        ]}
        className={cn(
          "[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]",
          "fill-gray-400/30 stroke-gray-400/30"
        )}
      />

      {/* Animated Interactive Grid */}
      <AnimatedGridPattern
        numSquares={50}
        maxOpacity={0.5}
        duration={4}
        repeatDelay={0.5}
        className={cn(
          "[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]",
          "inset-x-0 inset-y-[-30%] h-[200%] skew-y-12"
        )}
      />

      <h1 className="relative z-10 text-6xl font-bold">
        Your Content Here
      </h1>
    </div>
  )
}
```

### 2. React Bits: Text Reveal Animations

Implement scroll-triggered text reveals with BlurText:

```jsx
import BlurText from './components/BlurText'

export default function MarketingSection() {
  return (
    <section className="py-20">
      {/* Word-by-word reveal */}
      <BlurText
        text="Transform your ideas into reality"
        delay={100}
        animateBy="words"
        direction="top"
        className="text-5xl font-bold text-center mb-8"
      />

      {/* Character-by-character reveal with custom easing */}
      <BlurText
        text="Pixel-perfect animations at your fingertips"
        delay={50}
        animateBy="characters"
        direction="bottom"
        threshold={0.3}
        stepDuration={0.4}
        animationFrom={{ filter: 'blur(20px)', opacity: 0, y: 50 }}
        animationTo={{ filter: 'blur(0px)', opacity: 1, y: 0 }}
        className="text-2xl text-gray-600 text-center"
      />
    </section>
  )
}
```

### 3. Magic UI: Button Components with Effects

Create interactive buttons with shimmer and border beam effects:

```typescript
import { ShimmerButton } from "@/components/ui/shimmer-button"
import { BorderBeam } from "@/components/ui/border-beam"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

export default function CTASection() {
  return (
    <div className="flex gap-4 items-center">
      {/* Shimmer Button */}
      <ShimmerButton
        shimmerColor="#ffffff"
        shimmerSize="0.05em"
        shimmerDuration="3s"
        borderRadius="100px"
        background="rgba(0, 0, 0, 1)"
        className="px-8 py-3"
      >
        Get Started
      </ShimmerButton>

      {/* Card with Animated Border */}
      <Card className="relative w-[350px] overflow-hidden">
        <div className="p-6">
          <h3 className="text-2xl font-bold">Premium Plan</h3>
          <p className="text-gray-600">Unlock all features</p>
          <Button className="mt-4">Subscribe</Button>
        </div>
        <BorderBeam duration={8} size={100} />
      </Card>
    </div>
  )
}
```

### 4. React Bits: Interactive Dock Navigation

Implement macOS-style dock with magnification effects:

```jsx
import Dock from './components/Dock'
import { VscHome, VscArchive, VscAccount, VscSettingsGear } from 'react-icons/vsc'
import { useNavigate } from 'react-router-dom'

export default function AppNavigation() {
  const navigate = useNavigate()

  const dockItems = [
    {
      icon: <VscHome size={24} />,
      label: 'Dashboard',
      onClick: () => navigate('/dashboard')
    },
    {
      icon: <VscArchive size={24} />,
      label: 'Projects',
      onClick: () => navigate('/projects')
    },
    {
      icon: <VscAccount size={24} />,
      label: 'Profile',
      onClick: () => navigate('/profile')
    },
    {
      icon: <VscSettingsGear size={24} />,
      label: 'Settings',
      onClick: () => navigate('/settings')
    }
  ]

  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2">
      <Dock
        items={dockItems}
        spring={{ mass: 0.15, stiffness: 200, damping: 15 }}
        magnification={80}
        distance={250}
        panelHeight={70}
        baseItemSize={55}
      />
    </div>
  )
}
```

### 5. React Bits: Animated Statistics with CountUp

Display animated numbers for dashboards and landing pages:

```jsx
import CountUp from './components/CountUp'

export default function Statistics() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 py-16">
      {/* Revenue Counter */}
      <div className="stat-card text-center">
        <CountUp
          start={0}
          end={1000000}
          duration={3}
          separator=","
          prefix="$"
          className="text-6xl font-bold text-blue-600"
        />
        <p className="text-xl text-gray-600 mt-2">Revenue Generated</p>
      </div>

      {/* Uptime Percentage */}
      <div className="stat-card text-center">
        <CountUp
          end={99.9}
          duration={2.5}
          decimals={1}
          suffix="%"
          className="text-6xl font-bold text-green-600"
        />
        <p className="text-xl text-gray-600 mt-2">Uptime</p>
      </div>

      {/* Customer Count */}
      <div className="stat-card text-center">
        <CountUp
          end={10000}
          duration={2}
          separator=","
          className="text-6xl font-bold text-purple-600"
        />
        <p className="text-xl text-gray-600 mt-2">Happy Customers</p>
      </div>
    </div>
  )
}
```

### 6. Magic UI: Marquee Component for Infinite Scroll

Create infinite scrolling content displays:

```typescript
import { Marquee } from "@/components/ui/marquee"

const testimonials = [
  { name: "John Doe", text: "Amazing product!", avatar: "/avatar1.jpg" },
  { name: "Jane Smith", text: "Exceeded expectations", avatar: "/avatar2.jpg" },
  { name: "Bob Johnson", text: "Highly recommend", avatar: "/avatar3.jpg" }
]

export default function Testimonials() {
  return (
    <section className="py-20">
      <h2 className="text-4xl font-bold text-center mb-12">
        What Our Customers Say
      </h2>

      {/* Horizontal Marquee */}
      <Marquee pauseOnHover className="[--duration:40s]">
        {testimonials.map((item, idx) => (
          <div key={idx} className="mx-4 w-[350px] rounded-lg border p-6">
            <p className="text-lg mb-4">"{item.text}"</p>
            <div className="flex items-center gap-3">
              <img src={item.avatar} alt={item.name} className="w-10 h-10 rounded-full" />
              <p className="font-semibold">{item.name}</p>
            </div>
          </div>
        ))}
      </Marquee>

      {/* Vertical Marquee */}
      <Marquee vertical reverse className="h-[400px] mt-8">
        {testimonials.map((item, idx) => (
          <div key={idx} className="my-4 w-full max-w-md rounded-lg border p-6">
            <p>{item.text}</p>
          </div>
        ))}
      </Marquee>
    </section>
  )
}
```

### 7. React Bits: WebGL Background Effects

Add high-performance animated backgrounds:

```jsx
import Particles from './components/Particles'
import Plasma from './components/Plasma'
import Aurora from './components/Aurora'

// Particles Effect
export default function ParticlesHero() {
  return (
    <section style={{ position: 'relative', height: '100vh' }}>
      <Particles
        particleCount={200}
        particleColors={['#FF6B6B', '#4ECDC4', '#45B7D1']}
        particleSpread={10}
        speed={0.12}
        moveParticlesOnHover={true}
        particleHoverFactor={2}
        particleBaseSize={100}
        sizeRandomness={1.2}
        alphaParticles={true}
        cameraDistance={20}
        className="particles-bg"
      />
      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-7xl font-bold text-white">
          Welcome to the Future
        </h1>
      </div>
    </section>
  )
}

// Plasma Effect
export default function PlasmaBackground() {
  return (
    <div className="relative min-h-screen">
      <Plasma
        color1="#FF0080"
        color2="#7928CA"
        color3="#00DFD8"
        speed={0.8}
        blur={30}
        className="plasma-bg"
      />
      <div className="relative z-10 p-8">
        <h1>Content with Plasma Background</h1>
      </div>
    </div>
  )
}

// Aurora Effect
export default function AuroraHero() {
  return (
    <div className="relative min-h-screen">
      <Aurora
        colors={['#FF00FF', '#00FFFF', '#FFFF00']}
        speed={0.5}
        blur={80}
      />
      <main className="relative z-10">
        <h1>Cyberpunk Aurora Effect</h1>
      </main>
    </div>
  )
}
```

## Integration Patterns

### Integration with shadcn/ui

Magic UI components are designed to work seamlessly with shadcn/ui:

```bash
# Install shadcn/ui component
npx shadcn@latest add button card

# Install Magic UI component
npx shadcn@latest add https://magicui.design/r/shimmer-button

# Use together in components
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ShimmerButton } from "@/components/ui/shimmer-button"
import { BorderBeam } from "@/components/ui/border-beam"
```

**Utility Function Required** (`lib/utils.ts`):

```typescript
import clsx, { ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Integration with Framer Motion

Both libraries leverage Framer Motion for animations:

```jsx
import { motion } from "framer-motion"
import { Magnet } from './components/Magnet'

// Combine React Bits Magnet with Framer Motion gestures
export default function InteractiveCard() {
  return (
    <Magnet magnitude={0.4} maxDistance={180}>
      <motion.div
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="card p-6 rounded-xl shadow-lg"
      >
        <h3>Interactive Card</h3>
        <p>Combines magnetic pull with scale animation</p>
      </motion.div>
    </Magnet>
  )
}
```

### Integration with React Router

Combine animated components with routing:

```jsx
import { AnimatePresence, motion } from "framer-motion"
import { useLocation, Routes, Route } from "react-router-dom"
import { Dock } from './components/Dock'

export default function App() {
  const location = useLocation()

  return (
    <>
      {/* Animated Page Transitions */}
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <HomePage />
            </motion.div>
          } />
        </Routes>
      </AnimatePresence>

      {/* Persistent Dock Navigation */}
      <Dock items={navItems} />
    </>
  )
}
```

### Combining Magic UI and React Bits

Leverage strengths of both libraries in a single project:

```jsx
// Magic UI: Patterns and structural components
import { GridPattern } from "@/components/ui/grid-pattern"
import { BorderBeam } from "@/components/ui/border-beam"
import { Marquee } from "@/components/ui/marquee"

// React Bits: Interactive elements and effects
import BlurText from './components/BlurText'
import CountUp from './components/CountUp'
import Particles from './components/Particles'

export default function LandingPage() {
  return (
    <main>
      {/* Hero with React Bits background + Magic UI pattern */}
      <section className="relative h-screen">
        <Particles particleCount={150} />
        <GridPattern
          squares={[[4,4], [8,2], [12,6]]}
          className="opacity-30"
        />
        <BlurText
          text="Next-Generation Platform"
          className="text-7xl font-bold"
        />
      </section>

      {/* Stats with React Bits CountUp */}
      <section>
        <CountUp end={10000} suffix="+" />
      </section>

      {/* Testimonials with Magic UI Marquee */}
      <section>
        <Marquee>
          {/* Testimonial cards */}
        </Marquee>
      </section>
    </main>
  )
}
```

## Performance Optimization

### Magic UI Performance Tips

1. **Use CSS Masks Instead of Clipping**: More performant for large patterns

```typescript
<GridPattern
  className="[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]"
/>
```

2. **Reduce Animation Complexity**: Lower `numSquares` for AnimatedGridPattern on mobile

```typescript
const isMobile = window.innerWidth < 768
<AnimatedGridPattern
  numSquares={isMobile ? 20 : 50}
  duration={isMobile ? 6 : 4}
/>
```

3. **Lazy Load Components**: Use React.lazy for heavy components

```typescript
const AnimatedGridPattern = React.lazy(() =>
  import("@/components/ui/animated-grid-pattern")
)
```

### React Bits Performance Tips

1. **WebGL Components**: Reduce particle count on low-end devices

```jsx
const particleCount = navigator.hardwareConcurrency > 4 ? 300 : 150

<Particles
  particleCount={particleCount}
  speed={0.1}
/>
```

2. **Disable Animations on Reduced Motion**:

```jsx
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

<BlurText
  text="Accessible text"
  delay={prefersReducedMotion ? 0 : 100}
  animateBy={prefersReducedMotion ? "none" : "words"}
/>
```

3. **Optimize Marquee Content**: Limit items for better performance

```typescript
<Marquee repeat={2}> {/* Instead of default 4 */}
  {items.slice(0, 10)} {/* Limit items */}
</Marquee>
```

4. **Use RequestIdleCallback for Non-Critical Animations**:

```jsx
useEffect(() => {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      // Initialize expensive animations
    })
  }
}, [])
```

## Common Pitfalls

### 1. Missing Dependencies

**Problem**: Component breaks due to missing `motion` or utility functions.

**Solution**: Always install required dependencies and utilities:

```bash
# Magic UI requirements
npm install motion clsx tailwind-merge

# React Bits WebGL components
npm install ogl

# Ensure cn() utility exists
```

```typescript
// lib/utils.ts
import clsx, { ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 2. CSS Animations Not Applied

**Problem**: Magic UI animations don't work after manual installation.

**Solution**: Add required CSS animations to `globals.css`:

```css
/* app/globals.css */
@theme inline {
  --animate-ripple: ripple var(--duration, 2s) ease calc(var(--i, 0) * 0.2s) infinite;
  --animate-shimmer-slide: shimmer-slide var(--speed) ease-in-out infinite alternate;
  --animate-marquee: marquee var(--duration) linear infinite;
  --animate-marquee-vertical: marquee-vertical var(--duration) linear infinite;
}

@keyframes ripple {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(0.9); }
}

@keyframes shimmer-slide {
  to { transform: translate(calc(100cqw - 100%), 0); }
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(calc(-100% - var(--gap))); }
}

@keyframes marquee-vertical {
  from { transform: translateY(0); }
  to { transform: translateY(calc(-100% - var(--gap))); }
}
```

### 3. Z-Index Conflicts

**Problem**: Background patterns or effects cover foreground content.

**Solution**: Use proper z-index layering:

```jsx
<div className="relative">
  {/* Background (z-0 or negative) */}
  <GridPattern className="absolute inset-0 -z-10" />

  {/* Content (higher z-index) */}
  <div className="relative z-10">
    <h1>Content appears above pattern</h1>
  </div>
</div>
```

### 4. Performance Issues with Multiple Animated Components

**Problem**: Page lags when multiple heavy animations run simultaneously.

**Solution**: Implement progressive enhancement and conditional rendering:

```jsx
import { useState, useEffect } from 'react'

export default function OptimizedPage() {
  const [enableHeavyEffects, setEnableHeavyEffects] = useState(false)

  useEffect(() => {
    // Check device capability
    const isHighEnd = navigator.hardwareConcurrency > 4 &&
                     !navigator.userAgent.includes('Mobile')
    setEnableHeavyEffects(isHighEnd)
  }, [])

  return (
    <section className="relative">
      {enableHeavyEffects ? (
        <Particles particleCount={300} />
      ) : (
        <GridPattern /> {/* Lighter alternative */}
      )}

      <div className="content">
        {/* Page content */}
      </div>
    </section>
  )
}
```

### 5. TypeScript Type Errors

**Problem**: TypeScript complains about component props.

**Solution**: Extend proper base types:

```typescript
// Magic UI pattern
interface CustomComponentProps extends React.ComponentPropsWithoutRef<"div"> {
  customProp?: string
  className?: string
}

// React Bits pattern
interface CustomProps extends React.HTMLAttributes<HTMLDivElement> {
  customProp?: string
}
```

### 6. Tailwind Classes Not Applied

**Problem**: Custom Tailwind classes in Magic UI components don't work.

**Solution**: Ensure content paths include component directory:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}", // Include components directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Resources

### Official Documentation
- **Magic UI**: https://magicui.design
- **React Bits**: https://reactbits.dev
- **shadcn/ui**: https://ui.shadcn.com
- **Framer Motion**: https://motion.dev

### Key Scripts
- `scripts/component_importer.py` - Import and customize components from both libraries
- `scripts/props_generator.py` - Generate component prop configurations

### References
- `references/magic_ui_components.md` - Complete Magic UI component catalog with usage examples
- `references/react_bits_components.md` - React Bits component library reference
- `references/customization_guide.md` - Prop-based customization patterns for both libraries

### Starter Assets
- `assets/component_showcase/` - Interactive demo of all components
- `assets/examples/` - Landing page sections, dashboard widgets, micro-interactions

## Related Skills

- **motion-framer**: For understanding underlying animation concepts used by both libraries
- **gsap-scrolltrigger**: Alternative approach for scroll-driven animations
- **react-spring-physics**: Alternative physics-based animation library
- **threejs-webgl**: For 3D background effects as alternative to Particles/Plasma
