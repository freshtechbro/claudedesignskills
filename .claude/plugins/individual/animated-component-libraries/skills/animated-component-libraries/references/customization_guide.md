# Component Customization Guide

Comprehensive guide for customizing Magic UI and React Bits components through props, styling, and composition.

## Customization Principles

Both libraries follow similar customization patterns:

1. **Prop-Based Customization**: Modify behavior through component props
2. **Class-Based Styling**: Use `className` prop with Tailwind CSS
3. **Composition**: Combine components for complex effects
4. **Theming**: Leverage CSS variables and Tailwind config

## Magic UI Customization

### Pattern Customization

#### Grid Pattern Masking

Create spotlight effects with CSS masks:

```typescript
// Radial gradient mask
<GridPattern
  className="[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]"
/>

// Linear gradient mask
<GridPattern
  className="[mask-image:linear-gradient(to_bottom,white,transparent)]"
/>

// Elliptical mask
<GridPattern
  className="[mask-image:radial-gradient(600px_ellipse_at_top,white,transparent)]"
/>

// Combined with positioning
<GridPattern
  squares={[[4,4], [8,2]]}
  className={cn(
    "[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]",
    "opacity-30",
    "fill-blue-400/20 stroke-blue-400/20"
  )}
/>
```

#### Animated Grid Pattern Timing

Control animation parameters for different effects:

```typescript
// Fast, subtle animation
<AnimatedGridPattern
  numSquares={30}
  maxOpacity={0.3}
  duration={2}
  repeatDelay={0.2}
/>

// Slow, dramatic animation
<AnimatedGridPattern
  numSquares={80}
  maxOpacity={0.8}
  duration={8}
  repeatDelay={1}
/>

// Responsive animation
const isMobile = typeof window !== 'undefined' && window.innerWidth < 768

<AnimatedGridPattern
  numSquares={isMobile ? 20 : 50}
  maxOpacity={isMobile ? 0.3 : 0.5}
  duration={isMobile ? 6 : 4}
/>
```

### Button Customization

#### Shimmer Button Variations

```typescript
// Minimal shimmer
<ShimmerButton
  shimmerColor="rgba(255,255,255,0.2)"
  shimmerSize="0.02em"
  shimmerDuration="4s"
  background="rgba(100,100,100,1)"
  className="px-6 py-2 text-sm"
>
  Subtle Effect
</ShimmerButton>

// Intense shimmer
<ShimmerButton
  shimmerColor="#FFD700"
  shimmerSize="0.1em"
  shimmerDuration="1.5s"
  background="rgba(0,0,0,1)"
  className="px-12 py-4 text-xl font-bold"
>
  Attention Grabber
</ShimmerButton>

// Branded shimmer
<ShimmerButton
  shimmerColor="var(--brand-primary)"
  borderRadius="8px"
  background="var(--brand-secondary)"
  className="px-8 py-3 font-semibold"
>
  Brand Button
</ShimmerButton>
```

#### Border Beam Customization

```typescript
// Slow, wide beam
<BorderBeam duration={20} size={300} />

// Fast, narrow beam
<BorderBeam duration={5} size={80} />

// Multiple beams
<div className="relative">
  <BorderBeam duration={8} size={100} />
  <BorderBeam duration={12} size={150} className="opacity-50" />
</div>
```

### Marquee Customization

#### Speed and Direction

```typescript
// Slow horizontal scroll
<Marquee className="[--duration:60s]">
  {items}
</Marquee>

// Fast horizontal scroll
<Marquee className="[--duration:20s]">
  {items}
</Marquee>

// Reverse direction
<Marquee reverse className="[--duration:40s]">
  {items}
</Marquee>

// Vertical with custom gap
<Marquee
  vertical
  className="h-[600px] [--gap:2rem]"
>
  {items}
</Marquee>
```

#### Content Repetition

```typescript
// Minimal repetition (better performance)
<Marquee repeat={2} className="[--duration:30s]">
  {largeItems}
</Marquee>

// Maximum repetition (smoother loop)
<Marquee repeat={6} className="[--duration:50s]">
  {smallItems}
</Marquee>
```

## React Bits Customization

### BlurText Customization

#### Animation Styles

```tsx
// Fade in from top
<BlurText
  text="Elegant entrance"
  direction="top"
  animationFrom={{ filter: 'blur(10px)', opacity: 0, y: -50 }}
  animationTo={{ filter: 'blur(0px)', opacity: 1, y: 0 }}
/>

// Zoom and blur
<BlurText
  text="Dynamic reveal"
  animationFrom={{ filter: 'blur(20px)', opacity: 0, scale: 0.5 }}
  animationTo={{ filter: 'blur(0px)', opacity: 1, scale: 1 }}
/>

// Slide from side with rotation
<BlurText
  text="Creative animation"
  direction="left"
  animationFrom={{ filter: 'blur(15px)', opacity: 0, x: -100, rotate: -15 }}
  animationTo={{ filter: 'blur(0px)', opacity: 1, x: 0, rotate: 0 }}
/>
```

#### Multi-Stage Animations

```tsx
<BlurText
  text="Complex reveal"
  animateBy="characters"
  animationFrom={{ filter: 'blur(20px)', opacity: 0, y: 100, scale: 0.8 }}
  animationTo={[
    { filter: 'blur(10px)', opacity: 0.3, y: 50, scale: 0.9 },
    { filter: 'blur(5px)', opacity: 0.7, y: 10, scale: 1 },
    { filter: 'blur(0px)', opacity: 1, y: 0, scale: 1 }
  ]}
  stepDuration={0.4}
  easing={(t) => t * t * (3 - 2 * t)} // Smoothstep easing
/>
```

#### Timing Control

```tsx
// Fast reveal
<BlurText
  text="Quick appearance"
  delay={30}
  stepDuration={0.03}
/>

// Slow, dramatic reveal
<BlurText
  text="Suspenseful entrance"
  delay={200}
  stepDuration={0.15}
/>

// Viewport-triggered with custom threshold
<BlurText
  text="Scroll-activated"
  threshold={0.5}
  rootMargin="-50px"
/>
```

### CountUp Customization

#### Formatting Options

```tsx
// Currency formatting
<CountUp
  end={1234567.89}
  duration={3}
  decimals={2}
  prefix="$"
  separator=","
/>
// Displays: $1,234,567.89

// Percentage
<CountUp
  end={75.5}
  decimals={1}
  suffix="%"
/>
// Displays: 75.5%

// Abbreviated large numbers
<CountUp
  end={1500000}
  separator=","
  suffix="+"
/>
// Displays: 1,500,000+

// Compact notation (custom implementation)
const formatCompact = (value) => {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return value.toString()
}
```

### Magnet Customization

#### Effect Strength Variations

```tsx
// Subtle magnetic effect
<Magnet
  magnitude={0.15}
  maxDistance={100}
  damping={30}
  stiffness={180}
>
  <button>Gentle Pull</button>
</Magnet>

// Strong magnetic effect
<Magnet
  magnitude={0.6}
  maxDistance={250}
  damping={15}
  stiffness={120}
>
  <div className="card">Strong Attraction</div>
</Magnet>

// Directional restriction (custom)
<Magnet
  magnitude={0.4}
  transformStyle={(x, y) => ({
    transform: `translate(${x}px, 0)` // Only horizontal movement
  })}
>
  <h1>Horizontal Only</h1>
</Magnet>
```

### Dock Customization

#### Physics and Sizing

```tsx
// Bouncy, playful dock
<Dock
  items={items}
  spring={{ mass: 0.2, stiffness: 250, damping: 10 }}
  magnification={100}
  distance={300}
  panelHeight={80}
  baseItemSize={60}
/>

// Smooth, minimal dock
<Dock
  items={items}
  spring={{ mass: 0.08, stiffness: 180, damping: 18 }}
  magnification={50}
  distance={120}
  panelHeight={50}
  baseItemSize={40}
/>

// Professional dock
<Dock
  items={items}
  spring={{ mass: 0.1, stiffness: 200, damping: 15 }}
  magnification={70}
  distance={200}
  panelHeight={64}
  baseItemSize={48}
  className="shadow-xl bg-gray-900/90 backdrop-blur-md rounded-2xl p-2"
/>
```

### Particles Customization

#### Visual Styles

```tsx
// Minimal particles
<Particles
  particleCount={50}
  particleColors={['#ffffff']}
  particleSpread={20}
  speed={0.03}
  particleBaseSize={60}
  sizeRandomness={0.3}
  alphaParticles={true}
  disableRotation={true}
/>

// Dense, colorful particles
<Particles
  particleCount={500}
  particleColors={['#FF0080', '#00FFFF', '#FFFF00', '#00FF00']}
  particleSpread={8}
  speed={0.2}
  particleBaseSize={80}
  sizeRandomness={2}
  alphaParticles={false}
/>

// Interactive particles
<Particles
  particleCount={200}
  particleColors={['#4ECDC4', '#45B7D1']}
  moveParticlesOnHover={true}
  particleHoverFactor={3}
  speed={0.08}
/>
```

## Cross-Library Combinations

### Magic UI Patterns + React Bits Text

```tsx
<div className="relative h-screen">
  {/* Magic UI background */}
  <AnimatedGridPattern
    numSquares={50}
    className="[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]"
  />

  {/* React Bits text animation */}
  <div className="relative z-10 flex items-center justify-center h-full">
    <BlurText
      text="Powerful Combination"
      animateBy="words"
      className="text-7xl font-bold"
    />
  </div>
</div>
```

### Shimmer Button + Magnet Effect

```tsx
import { ShimmerButton } from "@/components/ui/shimmer-button"
import Magnet from "./components/Magnet"

<Magnet magnitude={0.3}>
  <ShimmerButton
    shimmerDuration="3s"
    className="px-8 py-3"
  >
    Interactive CTA
  </ShimmerButton>
</Magnet>
```

### Marquee + CountUp Statistics

```tsx
import { Marquee } from "@/components/ui/marquee"
import CountUp from "./components/CountUp"

<Marquee pauseOnHover>
  {stats.map((stat) => (
    <div key={stat.id} className="mx-8 text-center">
      <CountUp
        end={stat.value}
        separator=","
        className="text-4xl font-bold"
      />
      <p className="text-sm text-gray-600">{stat.label}</p>
    </div>
  ))}
</Marquee>
```

## Theming with CSS Variables

### Creating Theme Variables

```css
/* app/globals.css */
:root {
  --component-duration: 3s;
  --component-primary: #4F46E5;
  --component-secondary: #06B6D4;
  --component-radius: 8px;
  --component-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.dark {
  --component-primary: #818CF8;
  --component-secondary: #22D3EE;
  --component-shadow: 0 10px 40px rgba(255,255,255,0.05);
}
```

### Using Theme Variables

```tsx
// Magic UI with theme
<ShimmerButton
  shimmerColor="var(--component-primary)"
  shimmerDuration="var(--component-duration)"
  borderRadius="var(--component-radius)"
  className="shadow-[var(--component-shadow)]"
>
  Themed Button
</ShimmerButton>

// React Bits with theme
<Particles
  particleColors={[
    'var(--component-primary)',
    'var(--component-secondary)'
  ]}
  speed={0.1}
/>
```

## Responsive Customization

### Breakpoint-Based Props

```tsx
import { useState, useEffect } from 'react'

function useBreakpoint() {
  const [breakpoint, setBreakpoint] = useState('desktop')

  useEffect(() => {
    const updateBreakpoint = () => {
      if (window.innerWidth < 640) setBreakpoint('mobile')
      else if (window.innerWidth < 1024) setBreakpoint('tablet')
      else setBreakpoint('desktop')
    }

    updateBreakpoint()
    window.addEventListener('resize', updateBreakpoint)
    return () => window.removeEventListener('resize', updateBreakpoint)
  }, [])

  return breakpoint
}

export default function ResponsiveComponent() {
  const breakpoint = useBreakpoint()

  const particleConfig = {
    mobile: { count: 50, spread: 15, size: 60 },
    tablet: { count: 150, spread: 12, size: 80 },
    desktop: { count: 300, spread: 10, size: 100 }
  }

  const config = particleConfig[breakpoint]

  return (
    <Particles
      particleCount={config.count}
      particleSpread={config.spread}
      particleBaseSize={config.size}
    />
  )
}
```

### Tailwind Responsive Classes

```tsx
<BlurText
  text="Responsive Text"
  className="text-2xl md:text-4xl lg:text-6xl"
  delay={50}
/>

<AnimatedGridPattern
  numSquares={50}
  className="hidden md:block"
/>

<Marquee className="[--duration:60s] md:[--duration:40s] lg:[--duration:30s]">
  {items}
</Marquee>
```

## Accessibility Customization

### Respect User Preferences

```tsx
const prefersReducedMotion =
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

// Disable animations for reduced motion
<BlurText
  text="Accessible text"
  delay={prefersReducedMotion ? 0 : 100}
  animateBy="none" // Skip animation entirely
/>

<Particles
  particleCount={prefersReducedMotion ? 0 : 200}
  speed={prefersReducedMotion ? 0 : 0.1}
/>

// Or provide alternative visual effect
{prefersReducedMotion ? (
  <div className="gradient-bg static" />
) : (
  <AnimatedGridPattern numSquares={50} />
)}
```

### ARIA Labels and Semantic HTML

```tsx
<div role="presentation" aria-hidden="true">
  <GridPattern /> {/* Decorative only */}
</div>

<Dock
  items={navItems}
  role="navigation"
  aria-label="Main navigation"
/>

<CountUp
  end={10000}
  aria-live="polite"
  aria-label="Total users: 10,000"
/>
```

## Performance Customization

### Conditional Rendering

```tsx
const [isLowPowerMode, setIsLowPowerMode] = useState(false)

useEffect(() => {
  // Detect low power mode or battery status
  if ('getBattery' in navigator) {
    navigator.getBattery().then((battery) => {
      setIsLowPowerMode(battery.level < 0.2)
    })
  }
}, [])

return isLowPowerMode ? (
  <StaticBackground />
) : (
  <Particles particleCount={300} />
)
```

### Lazy Loading Heavy Components

```tsx
import { lazy, Suspense } from 'react'

const Particles = lazy(() => import('./components/Particles'))
const Plasma = lazy(() => import('./components/Plasma'))

export default function OptimizedPage() {
  return (
    <Suspense fallback={<div className="gradient-bg" />}>
      <Particles particleCount={200} />
    </Suspense>
  )
}
```

## Advanced Customization Patterns

### Component Composition

```tsx
// Layered effects
<div className="relative">
  <Particles particleCount={100} className="absolute inset-0" />
  <AnimatedGridPattern
    numSquares={30}
    className="absolute inset-0 opacity-50"
  />
  <div className="relative z-10">
    <BlurText text="Layered Effects" />
  </div>
</div>
```

### Custom Animation Sequences

```tsx
import { motion, AnimatePresence } from "framer-motion"

<AnimatePresence>
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.5 }}
  >
    <BlurText text="Delayed text" />

    <motion.div
      initial={{ y: 50 }}
      animate={{ y: 0 }}
      transition={{ delay: 1.5 }}
    >
      <CountUp end={10000} />
    </motion.div>
  </motion.div>
</AnimatePresence>
```

This guide covers the most common customization patterns. For advanced customizations, consult the component source code and extend as needed.
