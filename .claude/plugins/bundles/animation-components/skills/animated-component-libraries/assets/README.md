# Animated Component Libraries - Assets

This directory contains starter templates and example code for Magic UI and React Bits components.

## Quick Start Templates

### Magic UI + shadcn/ui Starter

Create a new Next.js project with Magic UI components:

```bash
# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest my-magic-ui-app --typescript --tailwind --app

cd my-magic-ui-app

# Install dependencies
npm install motion clsx tailwind-merge

# Install shadcn/ui
npx shadcn@latest init

# Add Magic UI components
npx shadcn@latest add https://magicui.design/r/grid-pattern
npx shadcn@latest add https://magicui.design/r/shimmer-button
npx shadcn@latest add https://magicui.design/r/marquee
```

**Required: lib/utils.ts**
```typescript
import clsx, { ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Required: app/globals.css (add animations)**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@theme inline {
  --animate-marquee: marquee var(--duration) linear infinite;
  --animate-shimmer-slide: shimmer-slide var(--speed) ease-in-out infinite alternate;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(calc(-100% - var(--gap))); }
}

@keyframes shimmer-slide {
  to { transform: translate(calc(100cqw - 100%), 0); }
}
```

### React Bits Starter

Create a Vite + React project with React Bits components:

```bash
# Create Vite app
npm create vite@latest my-react-bits-app -- --template react

cd my-react-bits-app

# Install dependencies
npm install
npm install framer-motion
npm install ogl  # For WebGL components (Particles, Plasma, Aurora)
```

**Copy components from reactbits.dev**:
- Visit https://reactbits.dev
- Browse component gallery
- Click "View Code" on desired component
- Copy to `src/components/`

## Example Implementations

### Landing Page with Magic UI

**app/page.tsx**
```typescript
import { GridPattern } from "@/components/ui/grid-pattern"
import { AnimatedGridPattern } from "@/components/ui/animated-grid-pattern"
import { ShimmerButton } from "@/components/ui/shimmer-button"
import { Marquee } from "@/components/ui/marquee"
import { cn } from "@/lib/utils"

const testimonials = [
  { id: 1, name: "John Doe", text: "Amazing product!", avatar: "/avatar1.jpg" },
  { id: 2, name: "Jane Smith", text: "Exceeded expectations", avatar: "/avatar2.jpg" }
]

export default function Home() {
  return (
    <main>
      {/* Hero Section */}
      <section className="relative flex h-screen items-center justify-center overflow-hidden">
        <AnimatedGridPattern
          numSquares={50}
          maxOpacity={0.5}
          duration={4}
          className={cn(
            "[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]",
            "inset-x-0 inset-y-[-30%] h-[200%] skew-y-12"
          )}
        />
        <div className="relative z-10 text-center">
          <h1 className="text-7xl font-bold mb-8">Welcome to the Future</h1>
          <ShimmerButton
            shimmerDuration="3s"
            className="px-8 py-3"
          >
            Get Started
          </ShimmerButton>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20">
        <h2 className="text-4xl font-bold text-center mb-12">Testimonials</h2>
        <Marquee pauseOnHover className="[--duration:40s]">
          {testimonials.map((item) => (
            <div key={item.id} className="mx-4 w-[350px] rounded-lg border p-6">
              <p className="text-lg mb-4">"{item.text}"</p>
              <div className="flex items-center gap-3">
                <img src={item.avatar} alt={item.name} className="w-10 h-10 rounded-full" />
                <p className="font-semibold">{item.name}</p>
              </div>
            </div>
          ))}
        </Marquee>
      </section>
    </main>
  )
}
```

### Interactive Dashboard with React Bits

**src/App.jsx**
```jsx
import { useState } from 'react'
import CountUp from './components/CountUp'
import BlurText from './components/BlurText'
import Particles from './components/Particles'
import './App.css'

function App() {
  return (
    <div className="app">
      {/* Background */}
      <Particles
        particleCount={150}
        particleColors={['#4ECDC4', '#45B7D1']}
        particleSpread={10}
        speed={0.1}
        className="fixed inset-0"
      />

      {/* Content */}
      <div className="relative z-10 min-h-screen p-8">
        <BlurText
          text="Analytics Dashboard"
          delay={100}
          animateBy="words"
          className="text-6xl font-bold text-center mb-16"
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Stats */}
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 text-center">
            <CountUp
              end={10000}
              duration={2}
              separator=","
              className="text-5xl font-bold text-blue-500"
            />
            <p className="text-xl mt-2">Active Users</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 text-center">
            <CountUp
              end={99.9}
              duration={2.5}
              decimals={1}
              suffix="%"
              className="text-5xl font-bold text-green-500"
            />
            <p className="text-xl mt-2">Uptime</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-xl p-8 text-center">
            <CountUp
              end={1000000}
              duration={3}
              prefix="$"
              separator=","
              className="text-5xl font-bold text-purple-500"
            />
            <p className="text-xl mt-2">Revenue</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
```

## Component Showcase Examples

### Complete examples are available at:

**Magic UI**:
- Official examples: https://magicui.design
- GitHub repository: https://github.com/magicuidesign/magicui
- Component registry: Browse site for live demos

**React Bits**:
- Official examples: https://reactbits.dev
- Component demos: Each component page includes live preview
- GitHub: https://github.com/davidhdev/react-bits

## Integration Examples

### Combining Libraries

Both libraries can be used together in the same project:

```jsx
// Magic UI for structural patterns
import { GridPattern } from "@/components/ui/grid-pattern"
import { Marquee } from "@/components/ui/marquee"

// React Bits for interactive elements
import BlurText from './components/BlurText'
import CountUp from './components/CountUp'
import Particles from './components/Particles'

export default function HybridPage() {
  return (
    <div className="relative">
      {/* React Bits background */}
      <Particles particleCount={100} className="fixed inset-0" />

      {/* Magic UI pattern overlay */}
      <GridPattern
        squares={[[4,4], [8,2]]}
        className="absolute inset-0 opacity-30 -z-10"
      />

      {/* Content */}
      <div className="relative z-10 p-8">
        <BlurText
          text="Best of Both Worlds"
          className="text-6xl font-bold mb-8"
        />

        <Marquee>
          {items.map((item) => (
            <div key={item.id} className="mx-4">
              <CountUp end={item.value} />
            </div>
          ))}
        </Marquee>
      </div>
    </div>
  )
}
```

## Production-Ready Patterns

### Performance-Optimized Setup

```jsx
import { lazy, Suspense, useState, useEffect } from 'react'

// Lazy load heavy components
const Particles = lazy(() => import('./components/Particles'))
const AnimatedGridPattern = lazy(() => import('@/components/ui/animated-grid-pattern'))

export default function OptimizedPage() {
  const [enableHeavyEffects, setEnableHeavyEffects] = useState(false)

  useEffect(() => {
    // Enable on high-end devices only
    const isHighEnd = navigator.hardwareConcurrency > 4 &&
                     !navigator.userAgent.includes('Mobile')
    setEnableHeavyEffects(isHighEnd)
  }, [])

  return (
    <div className="relative">
      {enableHeavyEffects ? (
        <Suspense fallback={<div className="gradient-bg" />}>
          <Particles particleCount={200} />
        </Suspense>
      ) : (
        <div className="static-gradient-bg" />
      )}

      {/* Content */}
    </div>
  )
}
```

### Accessibility-First Implementation

```jsx
const prefersReducedMotion =
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

<BlurText
  text="Accessible text reveal"
  delay={prefersReducedMotion ? 0 : 100}
  animateBy={prefersReducedMotion ? "none" : "words"}
/>

<div role="presentation" aria-hidden="true">
  <GridPattern /> {/* Decorative only */}
</div>

<CountUp
  end={10000}
  aria-live="polite"
  aria-label="Total users: 10,000"
/>
```

## Additional Resources

- **Magic UI Documentation**: https://magicui.design/docs
- **React Bits Documentation**: https://reactbits.dev/docs
- **Framer Motion**: https://motion.dev
- **shadcn/ui**: https://ui.shadcn.com
- **Tailwind CSS**: https://tailwindcss.com

## Scripts

Use the provided scripts to assist with component implementation:

```bash
# Import component with instructions
../scripts/component_importer.py

# Generate component props
../scripts/props_generator.py
```

## Notes

1. **Magic UI** requires shadcn/ui setup and cn() utility
2. **React Bits** uses manual copy-paste installation
3. **WebGL components** (Particles, Plasma, Aurora) require `ogl` package
4. **Performance**: Test on target devices, especially for WebGL components
5. **Accessibility**: Always test with screen readers and keyboard navigation
