# Magic UI Component Catalog

Complete reference for Magic UI components built on Tailwind CSS, Framer Motion, and shadcn/ui.

## Installation

```bash
# Via shadcn CLI (recommended)
npx shadcn@latest add https://magicui.design/r/[component-name]

# Manual installation
# 1. Copy component code to components/ui/
# 2. Install dependencies: npm install motion clsx tailwind-merge
# 3. Add required CSS animations to globals.css
# 4. Ensure cn() utility exists in lib/utils.ts
```

## Background Patterns

### Grid Pattern

Static SVG grid pattern for backgrounds.

**Props**:
- `width` (number): Grid cell width, default 40
- `height` (number): Grid cell height, default 40
- `x` (number): X offset, default -1
- `y` (number): Y offset, default -1
- `squares` (Array<[x, y]>): Highlighted squares
- `strokeDasharray` (string): Dash pattern, default "0"
- `className` (string): Additional CSS classes

**Usage**:
```typescript
<GridPattern
  squares={[[4, 4], [5, 1], [8, 2]]}
  className="[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]"
/>
```

### Animated Grid Pattern

Animated version with dynamic square animations.

**Props**:
- All GridPattern props
- `numSquares` (number): Number of animated squares, default 50
- `maxOpacity` (number): Maximum opacity, default 0.5
- `duration` (number): Animation duration in seconds, default 4
- `repeatDelay` (number): Delay between repeats, default 0.5

**Usage**:
```typescript
<AnimatedGridPattern
  numSquares={50}
  maxOpacity={0.5}
  duration={4}
  repeatDelay={0.5}
  className="inset-x-0 inset-y-[-30%] h-[200%] skew-y-12"
/>
```

### Interactive Grid Pattern

Grid pattern with interactive squares.

**Props**:
- `width` (number): Cell width, default 40
- `height` (number): Cell height, default 40
- `squares` ([horizontal, vertical]): Grid dimensions, default [24, 24]
- `squaresClassName` (string): Class for squares
- `className` (string): Container class

**Usage**:
```typescript
<InteractiveGridPattern
  squares={[24, 24]}
  className="[mask-image:radial-gradient(400px_circle_at_center,white,transparent)]"
/>
```

### Striped Pattern

Diagonal striped background pattern.

**Props**:
- `direction` ("left" | "right"): Stripe direction, default "left"
- `width` (number): Pattern width, default 10
- `height` (number): Pattern height, default 10
- `className` (string): Additional CSS classes

**Usage**:
```typescript
<StripedPattern
  direction="left"
  className="[mask-image:radial-gradient(300px_circle_at_center,white,transparent)]"
/>
```

## Buttons & Interactive Elements

### Shimmer Button

Button with animated shimmer effect.

**Props**:
- `shimmerColor` (string): Shimmer color, default "#ffffff"
- `shimmerSize` (string): Shimmer size, default "0.05em"
- `shimmerDuration` (string): Animation duration, default "3s"
- `borderRadius` (string): Border radius, default "100px"
- `background` (string): Background color, default "rgba(0, 0, 0, 1)"
- `className` (string): Additional CSS classes
- `children` (ReactNode): Button content
- All standard button props

**Usage**:
```typescript
<ShimmerButton
  shimmerColor="#ffffff"
  shimmerDuration="3s"
  background="rgba(0, 0, 0, 1)"
  className="px-8 py-3"
>
  Get Started
</ShimmerButton>
```

### Border Beam

Animated gradient border effect for containers.

**Props**:
- `duration` (number): Animation duration in seconds, default 15
- `size` (number): Beam width in pixels, default 200
- `className` (string): Additional CSS classes

**Usage**:
```typescript
<Card className="relative overflow-hidden">
  <CardContent>Your content</CardContent>
  <BorderBeam duration={8} size={100} />
</Card>
```

## Text & Typography

### Spinning Text

Text arranged in a circular path with rotation.

**Props**:
- `children` (string): Text content (use • for separators)
- `radius` (number): Circle radius, default 5
- `duration` (number): Rotation duration in seconds, default 10
- `reverse` (boolean): Reverse rotation direction, default false
- `className` (string): Additional CSS classes

**Usage**:
```typescript
<SpinningText
  reverse={false}
  className="text-4xl"
  duration={4}
  radius={6}
>
  learn more • earn more • grow more •
</SpinningText>
```

## Layout Components

### Marquee

Infinite scrolling content container.

**Props**:
- `className` (string): Additional CSS classes
- `reverse` (boolean): Reverse scroll direction, default false
- `pauseOnHover` (boolean): Pause on mouse hover, default false
- `vertical` (boolean): Vertical scrolling, default false
- `repeat` (number): Number of content repetitions, default 4
- `children` (ReactNode): Content to scroll

**Usage**:
```typescript
// Horizontal marquee
<Marquee pauseOnHover className="[--duration:40s]">
  {items.map((item) => (
    <div key={item.id} className="mx-4">
      {item.content}
    </div>
  ))}
</Marquee>

// Vertical marquee
<Marquee vertical reverse className="h-[400px]">
  {items.map((item) => (
    <div key={item.id}>{item.content}</div>
  ))}
</Marquee>
```

### Bento Grid

Responsive grid layout for product features.

**Props**:
- `children` (ReactNode): BentoCard components
- `className` (string): Grid customization classes

**BentoCard Props**:
- `name` (string): Card title
- `className` (string): Card size/position classes
- `background` (ReactNode): Background component/image
- `Icon` (React.ElementType): Icon component
- `description` (string): Card description
- `href` (string): Link URL
- `cta` (string): Call-to-action text

**Usage**:
```typescript
<BentoGrid className="grid-cols-3 gap-4">
  <BentoCard
    name="Feature Name"
    className="col-span-2"
    background={<div className="bg-gradient" />}
    Icon={FeatureIcon}
    description="Description text"
    href="/feature"
    cta="Learn More"
  />
</BentoGrid>
```

## 3D & Visual Effects

### Globe

Interactive 3D globe visualization.

**Props**:
- `className` (string): Additional CSS classes
- Additional THREE.js globe configuration props

**Usage**:
```typescript
<div className="relative flex size-full max-w-lg items-center justify-center">
  <span className="text-8xl font-semibold">Globe</span>
  <Globe className="top-28" />
</div>
```

## Required CSS Animations

Add these to `app/globals.css` for manual installations:

```css
@theme inline {
  --animate-ripple: ripple var(--duration, 2s) ease calc(var(--i, 0) * 0.2s) infinite;
  --animate-shimmer-slide: shimmer-slide var(--speed) ease-in-out infinite alternate;
  --animate-spin-around: spin-around calc(var(--speed) * 2) infinite linear;
  --animate-marquee: marquee var(--duration) linear infinite;
  --animate-marquee-vertical: marquee-vertical var(--duration) linear infinite;
  --animate-beam: beam 3s linear infinite;
}

@keyframes ripple {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    transform: translate(-50%, -50%) scale(0.9);
  }
}

@keyframes shimmer-slide {
  to {
    transform: translate(calc(100cqw - 100%), 0);
  }
}

@keyframes spin-around {
  0% {
    transform: translateZ(0) rotate(0);
  }
  15%, 35% {
    transform: translateZ(0) rotate(90deg);
  }
  65%, 85% {
    transform: translateZ(0) rotate(270deg);
  }
  100% {
    transform: translateZ(0) rotate(360deg);
  }
}

@keyframes marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(calc(-100% - var(--gap)));
  }
}

@keyframes marquee-vertical {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(calc(-100% - var(--gap)));
  }
}

@keyframes beam {
  0% {
    background-position: 0% 50%;
  }
  100% {
    background-position: 100% 50%;
  }
}
```

## Utility Function Required

All Magic UI components require the `cn()` utility function:

```typescript
// lib/utils.ts
import clsx, { ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Common Component Combinations

### Hero Section with Pattern
```typescript
<div className="relative flex h-screen items-center justify-center">
  <AnimatedGridPattern
    numSquares={50}
    className="[mask-image:radial-gradient(500px_circle_at_center,white,transparent)]"
  />
  <h1 className="relative z-10 text-7xl font-bold">Hero Title</h1>
</div>
```

### CTA Card with Border Beam
```typescript
<Card className="relative overflow-hidden">
  <CardHeader>
    <CardTitle>Premium Plan</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Get all features</p>
    <Button>Subscribe</Button>
  </CardContent>
  <BorderBeam duration={8} />
</Card>
```

### Testimonial Carousel
```typescript
<Marquee pauseOnHover className="py-4">
  {testimonials.map((t) => (
    <div key={t.id} className="mx-4 w-[350px] rounded-lg border p-6">
      <p className="mb-4">"{t.text}"</p>
      <div className="flex gap-3">
        <img src={t.avatar} className="w-10 h-10 rounded-full" />
        <p className="font-semibold">{t.name}</p>
      </div>
    </div>
  ))}
</Marquee>
```

## Tailwind Configuration

Ensure Tailwind can find Magic UI components:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Performance Tips

1. **Use CSS Masks**: More performant than clipping paths
2. **Limit Animated Elements**: Reduce `numSquares` on mobile devices
3. **Lazy Load Heavy Components**: Use React.lazy() for Globe and complex components
4. **Optimize Marquee**: Limit `repeat` prop and number of items
5. **Consider Reduced Motion**: Check `prefers-reduced-motion` media query

## TypeScript Support

All Magic UI components are fully typed. Extend props interface when customizing:

```typescript
interface CustomGridPatternProps extends React.ComponentPropsWithoutRef<"svg"> {
  customProp?: string
}
```

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Grid support required
- SVG support required
- Framer Motion browser requirements apply
